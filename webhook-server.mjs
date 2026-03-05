import { spawn } from 'node:child_process';
import crypto from 'node:crypto';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = Number.parseInt(process.env.WEBHOOK_PORT ?? '9001', 10);
const WEBHOOK_PATH = process.env.WEBHOOK_PATH ?? '/webhook/github';
const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET ?? '';
const TARGET_BRANCH_REF = process.env.WEBHOOK_BRANCH_REF ?? 'refs/heads/main';
const DEPLOY_SCRIPT = process.env.DEPLOY_SCRIPT ?? path.join(__dirname, 'deploy.sh');
const DEPLOY_SHELL = process.env.DEPLOY_SHELL ?? '/bin/bash';
const MAX_BODY_SIZE = Number.parseInt(process.env.WEBHOOK_MAX_BODY_SIZE ?? '1048576', 10);

let deploying = false;
let rerunRequested = false;

function replyJson(res, statusCode, payload) {
  res.writeHead(statusCode, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload));
}

function getHeaderValue(value) {
  if (!value) {
    return '';
  }
  return Array.isArray(value) ? value[0] : value;
}

function verifySignature(rawBody, signatureHeader) {
  if (!signatureHeader || !signatureHeader.startsWith('sha256=')) {
    return false;
  }

  const expected = `sha256=${crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(rawBody)
    .digest('hex')}`;

  const receivedBuffer = Buffer.from(signatureHeader);
  const expectedBuffer = Buffer.from(expected);

  if (receivedBuffer.length !== expectedBuffer.length) {
    return false;
  }

  return crypto.timingSafeEqual(receivedBuffer, expectedBuffer);
}

function runDeploy(reason) {
  deploying = true;
  console.log(`[webhook] deploy started: ${reason}`);

  const child = spawn(DEPLOY_SHELL, [DEPLOY_SCRIPT], {
    cwd: __dirname,
    env: process.env,
    stdio: 'inherit',
  });

  child.on('exit', (code, signal) => {
    deploying = false;
    if (code === 0) {
      console.log('[webhook] deploy completed');
    } else {
      console.error(`[webhook] deploy failed, code=${code ?? 'null'}, signal=${signal ?? 'null'}`);
    }

    if (rerunRequested) {
      rerunRequested = false;
      runDeploy('queued push');
    }
  });
}

function triggerDeploy(reason) {
  if (deploying) {
    rerunRequested = true;
    console.log('[webhook] deploy is running, queued one rerun');
    return;
  }
  runDeploy(reason);
}

const server = http.createServer((req, res) => {
  const reqUrl = new URL(req.url ?? '/', `http://${req.headers.host ?? 'localhost'}`);

  if (req.method === 'GET' && reqUrl.pathname === '/healthz') {
    return replyJson(res, 200, { ok: true, deploying });
  }

  if (req.method !== 'POST' || reqUrl.pathname !== WEBHOOK_PATH) {
    return replyJson(res, 404, { ok: false, message: 'Not Found' });
  }

  if (!WEBHOOK_SECRET) {
    return replyJson(res, 500, { ok: false, message: 'WEBHOOK_SECRET is required' });
  }

  const event = getHeaderValue(req.headers['x-github-event']);
  if (event !== 'push') {
    return replyJson(res, 202, { ok: true, ignored: `event:${event || 'unknown'}` });
  }

  const signature = getHeaderValue(req.headers['x-hub-signature-256']);
  const chunks = [];
  let bodySize = 0;
  let tooLarge = false;

  req.on('data', (chunk) => {
    if (tooLarge) {
      return;
    }

    bodySize += chunk.length;
    if (bodySize > MAX_BODY_SIZE) {
      tooLarge = true;
      return;
    }
    chunks.push(chunk);
  });

  req.on('end', () => {
    if (tooLarge) {
      return replyJson(res, 413, { ok: false, message: 'Payload too large' });
    }

    const rawBody = Buffer.concat(chunks);
    if (!verifySignature(rawBody, signature)) {
      return replyJson(res, 401, { ok: false, message: 'Invalid signature' });
    }

    let payload;
    try {
      payload = JSON.parse(rawBody.toString('utf8'));
    } catch {
      return replyJson(res, 400, { ok: false, message: 'Invalid JSON payload' });
    }

    if (payload.ref !== TARGET_BRANCH_REF) {
      return replyJson(res, 202, { ok: true, ignored: `ref:${payload.ref || 'unknown'}` });
    }

    const shortSha = (payload.after || '').slice(0, 7);
    triggerDeploy(`ref=${payload.ref}, sha=${shortSha}`);
    return replyJson(res, 202, { ok: true, message: 'Deploy triggered' });
  });

  req.on('error', (err) => {
    console.error('[webhook] request error:', err);
    return replyJson(res, 400, { ok: false, message: 'Request stream error' });
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`[webhook] listening on 0.0.0.0:${PORT}${WEBHOOK_PATH}`);
  console.log(`[webhook] branch filter: ${TARGET_BRANCH_REF}`);
  console.log(`[webhook] deploy script: ${DEPLOY_SCRIPT}`);
});
