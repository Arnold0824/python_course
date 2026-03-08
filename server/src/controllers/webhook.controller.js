import { getHeaderValue, verifyGitHubSignature } from '../utils/github-signature.js';

export function createWebhookController({ config, deployService, logger }) {
  return {
    handleGithubWebhook(req, res, next) {
      try {
        if (!config.webhook.secret) {
          return res.status(500).json({
            ok: false,
            message: 'WEBHOOK_SECRET is required',
          });
        }

        const event = getHeaderValue(req.get('x-github-event'));
        const deliveryId = getHeaderValue(req.get('x-github-delivery'));
        if (event !== 'push') {
          logger.info('ignored non-push event', {
            deliveryId,
            event: event || 'unknown',
          });
          return res.status(202).json({
            ok: true,
            ignored: `event:${event || 'unknown'}`,
          });
        }

        const rawBody = Buffer.isBuffer(req.body) ? req.body : Buffer.from([]);
        const signature = getHeaderValue(req.get('x-hub-signature-256'));
        if (!verifyGitHubSignature(rawBody, signature, config.webhook.secret)) {
          logger.warn('invalid webhook signature', { deliveryId });
          return res.status(401).json({
            ok: false,
            message: 'Invalid signature',
          });
        }

        let payload;
        try {
          payload = JSON.parse(rawBody.toString('utf8'));
        } catch {
          logger.warn('invalid webhook payload json', { deliveryId });
          return res.status(400).json({
            ok: false,
            message: 'Invalid JSON payload',
          });
        }

        if (payload.ref !== config.webhook.branchRef) {
          logger.info('ignored webhook ref', {
            deliveryId,
            ref: payload.ref || 'unknown',
          });
          return res.status(202).json({
            ok: true,
            ignored: `ref:${payload.ref || 'unknown'}`,
          });
        }

        const shortSha = String(payload.after || '').slice(0, 7);
        const reason = `ref=${payload.ref}, sha=${shortSha}`;

        if (config.webhook.testOnly) {
          logger.info('webhook validated in test mode', {
            deliveryId,
            ref: payload.ref,
            sha: shortSha,
          });
          return res.status(202).json({
            ok: true,
            message: 'Webhook validated (test only)',
          });
        }

        if (deployService.isDeploying()) {
          logger.info('deploy skipped: already running', {
            deliveryId,
            ref: payload.ref,
            sha: shortSha,
          });
          return res.status(202).json({
            ok: true,
            message: 'Deploy already running',
          });
        }

        deployService.start(reason);

        logger.info('webhook accepted', {
          deliveryId,
          ref: payload.ref,
          sha: shortSha,
        });

        return res.status(202).json({
          ok: true,
          message: 'Deploy triggered',
        });
      } catch (error) {
        next(error);
      }
    },
  };
}
