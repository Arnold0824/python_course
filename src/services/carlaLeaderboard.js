const CARLA_LEADERBOARD_ENDPOINT = "/api/carla/leaderboard";

async function requestJson(url) {
  const response = await fetch(url);
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

export async function fetchCarlaLeaderboard({ limit = 50 } = {}) {
  const query = new URLSearchParams({
    limit: String(limit),
  });

  return requestJson(`${CARLA_LEADERBOARD_ENDPOINT}?${query.toString()}`);
}
