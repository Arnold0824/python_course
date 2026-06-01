const IDEA_ENDPOINT = '/api/ideas/messages'
const SESSION_STORAGE_KEY = 'python-course-session-id'

function createSessionId() {
  if (globalThis.crypto?.randomUUID) {
    return globalThis.crypto.randomUUID()
  }

  return `session-${Date.now()}-${Math.random().toString(16).slice(2)}`
}

export function getIdeaSessionId() {
  const existing = sessionStorage.getItem(SESSION_STORAGE_KEY)
  if (existing) {
    return existing
  }

  const sessionId = createSessionId()
  sessionStorage.setItem(SESSION_STORAGE_KEY, sessionId)
  return sessionId
}

async function readJsonResponse(response) {
  let payload = null
  try {
    payload = await response.json()
  } catch {
    payload = null
  }

  if (!response.ok || !payload?.ok) {
    throw new Error(payload?.message || `请求失败：${response.status}`)
  }

  return payload.data
}

export async function fetchIdeaMessages({ limit = 50 } = {}) {
  const query = new URLSearchParams({
    limit: String(limit),
  })
  const response = await fetch(`${IDEA_ENDPOINT}?${query.toString()}`)
  const data = await readJsonResponse(response)
  return data.messages || []
}

export async function submitIdeaMessage({
  chapterId = null,
  content,
  courseId = 'python',
  displayName = '',
  pagePath = '',
}) {
  const response = await fetch(IDEA_ENDPOINT, {
    body: JSON.stringify({
      chapterId,
      content,
      courseId,
      displayName,
      pagePath,
      sessionId: getIdeaSessionId(),
      userAgent: navigator.userAgent || null,
    }),
    headers: {
      'Content-Type': 'application/json',
    },
    method: 'POST',
  })

  const data = await readJsonResponse(response)
  return data.message
}
