import { Router } from 'express'
import { createIdeasController } from '../controllers/ideas.controller.js'

export function createIdeasRouter(deps) {
  const router = Router()
  const controller = createIdeasController(deps)

  router.get('/messages', controller.listMessages)
  router.post('/messages', controller.createMessage)

  return router
}
