import { Router } from 'express';
import { createCarlaController } from '../controllers/carla.controller.js';

export function createCarlaRouter(deps) {
  const router = Router();
  const controller = createCarlaController(deps);

  router.get('/leaderboard', controller.getLeaderboard);
  router.post('/scores', controller.submitScore);

  return router;
}
