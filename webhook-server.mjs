import { spawn } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs/promises';
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
const STATUS_FILE = process.env.WEBHOOK_STATUS_FILE ?? path.join(__dirname, 'webhook-last-event.json');
const TEST_ONLY = process.env.WEBHOOK_TEST_ONLY === '1';

let deploying = false;
let rerunRequested = false;
let lastDelivery = {
  updatedAt: null,
  state: 'init',
  detail: 'server started',
  deploying: false,
};

function cleanObject(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([, value]) => value !== undefined));
}

function updateLastDelivery(patch) {
  lastDelivery = cleanObject({
    ...lastDelivery,
    ...patch,
    updatedAt: new Date().toISOString(),
    deploying,
  });

  void fs
    .writeFile(STATUS_FILE, `${JSON.stringify(lastDelivery, null, 2)}\n`, 'utf8')
    .catch((err) => console.error('[webhook] write status file failed:', err));
}

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
  updateLastDelivery({ state: 'deploying', detail: reason });
  console.log(`[webhook] deploy started: ${reason}`);

  const child = spawn(DEPLOY_SHELL, [DEPLOY_SCRIPT], {
    cwd: __dirname,
    env: process.env,
    stdio: 'inherit',
  });

  child.on('exit', (code, signal) => {
    deploying = false;
    if (code === 0) {
      updateLastDelivery({ state: 'deploy_success', detail: reason, exitCode: 0 });
      console.log('[webhook] deploy completed');
    } else {
      updateLastDelivery({ state: 'deploy_failed', detail: reason, exitCode: code ?? null, signal: signal ?? null });
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
    updateLastDelivery({ state: 'queued', detail: `${reason} (deploy running)` });
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

  if (req.method === 'GET' && reqUrl.pathname === '/webhook/last') {
    return replyJson(res, 200, { ok: true, lastDelivery });
  }

  if (req.method !== 'POST' || reqUrl.pathname !== WEBHOOK_PATH) {
    return replyJson(res, 404, { ok: false, message: 'Not Found' });
  }

  if (!WEBHOOK_SECRET) {
    return replyJson(res, 500, { ok: false, message: 'WEBHOOK_SECRET is required' });
  }

  const event = getHeaderValue(req.headers['x-github-event']);
  const deliveryId = getHeaderValue(req.headers['x-github-delivery']);
  if (event !== 'push') {
    updateLastDelivery({ state: 'ignored_event', detail: `event:${event || 'unknown'}`, deliveryId });
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
      updateLastDelivery({ state: 'payload_too_large', detail: `size>${MAX_BODY_SIZE}`, deliveryId });
      return replyJson(res, 413, { ok: false, message: 'Payload too large' });
    }

    const rawBody = Buffer.concat(chunks);
    if (!verifySignature(rawBody, signature)) {
      updateLastDelivery({ state: 'invalid_signature', detail: 'signature mismatch', deliveryId });
      return replyJson(res, 401, { ok: false, message: 'Invalid signature' });
    }

    let payload;
    try {
      payload = JSON.parse(rawBody.toString('utf8'));
    } catch {
      updateLastDelivery({ state: 'invalid_json', detail: 'payload parse failed', deliveryId });
      return replyJson(res, 400, { ok: false, message: 'Invalid JSON payload' });
    }

    if (payload.ref !== TARGET_BRANCH_REF) {
      updateLastDelivery({
        state: 'ignored_ref',
        detail: `ref:${payload.ref || 'unknown'}`,
        deliveryId,
        ref: payload.ref || null,
      });
      return replyJson(res, 202, { ok: true, ignored: `ref:${payload.ref || 'unknown'}` });
    }

    const shortSha = (payload.after || '').slice(0, 7);
    updateLastDelivery({
      state: TEST_ONLY ? 'test_ok' : 'accepted',
      detail: `ref=${payload.ref}, sha=${shortSha}`,
      deliveryId,
      ref: payload.ref || null,
      sha: shortSha || null,
    });

    if (TEST_ONLY) {
      return replyJson(res, 202, { ok: true, message: 'Webhook validated (test only)' });
    }

    triggerDeploy(`ref=${payload.ref}, sha=${shortSha}`);
    return replyJson(res, 202, { ok: true, message: 'Deploy triggered' });
  });

  req.on('error', (err) => {
    updateLastDelivery({ state: 'request_error', detail: err.message });
    console.error('[webhook] request error:', err);
    return replyJson(res, 400, { ok: false, message: 'Request stream error' });
  });
});

server.listen(PORT, '0.0.0.0', () => {
  updateLastDelivery({ state: 'listening', detail: 'webhook server is ready' });
  console.log(`[webhook] listening on 0.0.0.0:${PORT}${WEBHOOK_PATH}`);
  console.log(`[webhook] branch filter: ${TARGET_BRANCH_REF}`);
  console.log(`[webhook] deploy script: ${DEPLOY_SCRIPT}`);
  console.log(`[webhook] status file: ${STATUS_FILE}`);
  if (TEST_ONLY) {
    console.log('[webhook] running in TEST_ONLY mode, deploy script will not be executed');
  }
});
