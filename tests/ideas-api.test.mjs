import assert from 'node:assert/strict'
import { once } from 'node:events'

import { createApp } from '../server/src/app.js'

const calls = []

const ideaService = {
  async createMessage(payload) {
    calls.push(payload)
    return {
      content: payload.content,
      createdAt: '2026-05-28T12:00:00.000Z',
      displayName: payload.displayName,
      id: 12,
    }
  },
  async listVisibleMessages() {
    return [
      {
        content: '我想做一个文字冒险游戏',
        createdAt: '2026-05-28T11:00:00.000Z',
        displayName: '匿名同学 1024',
        id: 9,
      },
    ]
  },
}

const deps = {
  analyticsService: {
    async getAdminDashboard() {
      return {}
    },
    async getOverview() {
      return {}
    },
    async getRecentPageViews() {
      return []
    },
    async trackPageView() {
      return { id: 1 }
    },
  },
  config: {
    admin: { token: '' },
    app: { env: 'test', jsonLimit: '1mb' },
    ideas: {
      ipHashSalt: 'test-salt',
      maxContentLength: 500,
      messageTable: 'idea_messages',
    },
    webhook: {
      branchRef: 'refs/heads/main',
      maxBodySize: '1mb',
      path: '/api/webhooks/github-test',
      secret: '',
      testOnly: true,
    },
  },
  deployService: {
    isDeploying() {
      return false
    },
    start() {},
  },
  ideaService,
  logger: {
    error() {},
    info() {},
    warn() {},
  },
}

const app = createApp(deps)
const server = app.listen(0)
await once(server, 'listening')

const baseUrl = `http://127.0.0.1:${server.address().port}`

try {
  const listResponse = await fetch(`${baseUrl}/api/ideas/messages`)
  const listPayload = await listResponse.json()

  assert.equal(listResponse.status, 200)
  assert.equal(listPayload.ok, true)
  assert.equal(listPayload.data.messages.length, 1)
  assert.equal(listPayload.data.messages[0].content, '我想做一个文字冒险游戏')

  const createResponse = await fetch(`${baseUrl}/api/ideas/messages`, {
    body: JSON.stringify({
      chapterId: '10',
      content: '  我想做一个躲避小球小游戏  ',
      displayName: '  学生A  ',
      pagePath: '/python/chapter/10',
      sessionId: 'session-abc',
    }),
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'idea-test-agent',
    },
    method: 'POST',
  })
  const createPayload = await createResponse.json()

  assert.equal(createResponse.status, 201)
  assert.equal(createPayload.ok, true)
  assert.equal(createPayload.data.message.id, 12)
  assert.equal(calls[0].content, '我想做一个躲避小球小游戏')
  assert.equal(calls[0].displayName, '学生A')
  assert.equal(calls[0].courseId, 'python')
  assert.equal(calls[0].chapterId, '10')
  assert.equal(calls[0].pagePath, '/python/chapter/10')
  assert.equal(calls[0].sessionId, 'session-abc')
  assert.ok(calls[0].ipHash)
} finally {
  await new Promise((resolve) => server.close(resolve))
}
