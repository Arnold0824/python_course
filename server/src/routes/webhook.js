import express from 'express';
import { createWebhookController } from '../controllers/webhook.controller.js';

export function registerWebhookRoutes(app, deps) {
  const controller = createWebhookController(deps);

  app.post(
    deps.config.webhook.path,
    express.raw({
      type: ['application/json', 'application/*+json'],
      limit: deps.config.webhook.maxBodySize,
    }),
    controller.handleGithubWebhook,
  );
}
