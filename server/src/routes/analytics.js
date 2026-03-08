import { Router } from 'express';
import { createAnalyticsController } from '../controllers/analytics.controller.js';

export function createAnalyticsRouter(deps) {
  const router = Router();
  const controller = createAnalyticsController(deps);

  router.post('/page-views', controller.trackPageView);

  return router;
}
