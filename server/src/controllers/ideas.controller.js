import { createHash } from 'node:crypto'

function normalizeString(value, fallback = '') {
  if (typeof value !== 'string') {
    return fallback
  }

  return value.trim()
}

function normalizeIpAddress(value) {
  const ip = normalizeString(value, null)
  if (!ip) {
    return null
  }

  if (ip === '::1') {
    return '127.0.0.1'
  }

  if (ip.startsWith('::ffff:')) {
    return ip.slice(7)
  }

  return ip
}

function hashIpAddress(ipAddress, salt = '') {
  if (!ipAddress) {
    return null
  }

  return createHash('sha256').update(`${salt}:${ipAddress}`).digest('hex')
}

function clampString(value, maxLength) {
  const normalized = normalizeString(value)
  if (!normalized) {
    return ''
  }

  return normalized.slice(0, maxLength)
}

function createAnonymousName(sessionId, ipHash) {
  const seed = normalizeString(sessionId) || normalizeString(ipHash) || String(Date.now())
  const hash = createHash('sha256').update(seed).digest('hex')
  const suffix = String(Number.parseInt(hash.slice(0, 6), 16) % 9000).padStart(4, '0')
  return `匿名同学 ${suffix}`
}

function readPositiveInt(value, fallback, max) {
  const parsed = Number.parseInt(value, 10)
  if (Number.isNaN(parsed) || parsed <= 0) {
    return fallback
  }

  return Math.min(parsed, max)
}

export function createIdeasController({ config, ideaService }) {
  return {
    createMessage: async (req, res, next) => {
      try {
        const content = clampString(req.body?.content, config.ideas.maxContentLength)
        const sessionId = clampString(req.body?.sessionId, 128) || null
        const ipAddress = normalizeIpAddress(req.ip)
        const ipHash = hashIpAddress(ipAddress, config.ideas.ipHashSalt)
        const displayName =
          clampString(req.body?.displayName, 64) || createAnonymousName(sessionId, ipHash)

        if (!content) {
          return res.status(400).json({
            ok: false,
            message: 'content is required',
          })
        }

        const message = await ideaService.createMessage({
          chapterId: clampString(req.body?.chapterId, 64) || null,
          content,
          courseId: clampString(req.body?.courseId, 64) || 'python',
          displayName,
          ipHash,
          pagePath: clampString(req.body?.pagePath, 255) || null,
          sessionId,
          userAgent:
            clampString(req.body?.userAgent, 500) || clampString(req.get('user-agent'), 500) || null,
        })

        return res.status(201).json({
          ok: true,
          data: {
            message,
          },
        })
      } catch (error) {
        return next(error)
      }
    },

    hideMessage: async (req, res, next) => {
      try {
        const id = readPositiveInt(req.params.id, 0, Number.MAX_SAFE_INTEGER)
        if (!id) {
          return res.status(400).json({
            ok: false,
            message: 'valid message id is required',
          })
        }

        const result = await ideaService.hideMessage({
          id,
          reason: clampString(req.body?.reason, 255),
        })

        if (!result.hidden) {
          return res.status(404).json({
            ok: false,
            message: 'message not found',
          })
        }

        return res.json({
          ok: true,
          data: result,
        })
      } catch (error) {
        return next(error)
      }
    },

    listMessages: async (req, res, next) => {
      try {
        const messages = await ideaService.listVisibleMessages({
          limit: readPositiveInt(req.query.limit, 50, 100),
        })

        return res.json({
          ok: true,
          data: {
            messages,
          },
        })
      } catch (error) {
        return next(error)
      }
    },
  }
}
