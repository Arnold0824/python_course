import { Router } from 'express';
import { createHealthController } from '../controllers/health.controller.js';

export function createHealthRouter(deps) {
  const router = Router();
  const healthController = createHealthController(deps);

  router.get('/', healthController);

  return router;
}
