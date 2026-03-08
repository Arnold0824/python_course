import { Router } from 'express';
import { createAdminController } from '../controllers/admin.controller.js';
import { createAdminAuth } from '../middleware/admin-auth.js';

export function createAdminRouter(deps) {
  const router = Router();
  const controller = createAdminController(deps);
  const requireAdminToken = createAdminAuth(deps);

  router.use(requireAdminToken);
  router.get('/analytics/dashboard', controller.getDashboard);
  router.get('/analytics/overview', controller.getOverview);
  router.get('/analytics/recent', controller.getRecentViews);

  return router;
}
