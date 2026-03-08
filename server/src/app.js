import express from 'express';
import { createAnalyticsRouter } from './routes/analytics.js';
import { createHealthRouter } from './routes/health.js';
import { createAdminRouter } from './routes/admin.js';
import { registerWebhookRoutes } from './routes/webhook.js';
import { createErrorHandler, notFoundHandler } from './middleware/error-handler.js';

export function createApp(deps) {
  const app = express();

  app.disable('x-powered-by');
  app.set('trust proxy', true);

  app.use((req, res, next) => {
    const startedAt = Date.now();

    res.on('finish', () => {
      deps.logger.info('request completed', {
        durationMs: Date.now() - startedAt,
        method: req.method,
        path: req.originalUrl,
        statusCode: res.statusCode,
      });
    });

    next();
  });

  registerWebhookRoutes(app, deps);

  app.use(express.json({ limit: deps.config.app.jsonLimit }));
  app.use(express.urlencoded({ extended: false }));

  app.use('/healthz', createHealthRouter(deps));
  app.use('/api/analytics', createAnalyticsRouter(deps));
  app.use('/api/admin', createAdminRouter(deps));

  app.use(notFoundHandler);
  app.use(createErrorHandler({ logger: deps.logger }));

  return app;
}
