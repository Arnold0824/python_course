const ADMIN_ANALYTICS_BASE = "/api/admin/analytics";

function buildHeaders(token) {
  const trimmedToken = String(token || "").trim();
  if (!trimmedToken) {
    throw new Error("请先输入管理员令牌");
  }

  return {
    Authorization: `Bearer ${trimmedToken}`,
  };
}

async function requestJson(url, token) {
  const response = await fetch(url, {
    headers: buildHeaders(token),
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok || !payload?.ok) {
    throw new Error(payload?.message || `请求失败：${response.status}`);
  }

  return payload.data;
}

export async function fetchAnalyticsDashboard({ token, days = 14, limit = 50 }) {
  const query = new URLSearchParams({
    days: String(days),
    limit: String(limit),
  });

  return requestJson(`${ADMIN_ANALYTICS_BASE}/dashboard?${query.toString()}`, token);
}
