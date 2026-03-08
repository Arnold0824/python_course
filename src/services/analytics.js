const SESSION_STORAGE_KEY = "python-course-session-id";
const PAGE_VIEW_ENDPOINT = "/api/analytics/page-views";

let lastTrackedKey = "";

function createSessionId() {
  if (globalThis.crypto?.randomUUID) {
    return globalThis.crypto.randomUUID();
  }

  return `session-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function getSessionId() {
  const existing = sessionStorage.getItem(SESSION_STORAGE_KEY);
  if (existing) {
    return existing;
  }

  const sessionId = createSessionId();
  sessionStorage.setItem(SESSION_STORAGE_KEY, sessionId);
  return sessionId;
}

function buildPayload(route, referrer) {
  return {
    chapterId: route?.meta?.chapterId ? String(route.meta.chapterId) : null,
    path: route?.fullPath || "/",
    referrer,
    sessionId: getSessionId(),
    userAgent: navigator.userAgent || null,
  };
}

async function sendPageView(payload) {
  const body = JSON.stringify(payload);

  if (navigator.sendBeacon) {
    const blob = new Blob([body], { type: "application/json" });
    if (navigator.sendBeacon(PAGE_VIEW_ENDPOINT, blob)) {
      return;
    }
  }

  await fetch(PAGE_VIEW_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body,
    keepalive: true,
  });
}

function trackRoute(route, previousRoute) {
  const routeKey = `${route?.fullPath || "/"}|${route?.meta?.chapterId || ""}`;
  if (routeKey === lastTrackedKey) {
    return;
  }

  lastTrackedKey = routeKey;
  const referrer = previousRoute?.fullPath || document.referrer || null;

  void sendPageView(buildPayload(route, referrer)).catch((error) => {
    console.warn("[analytics] page view tracking failed", error);
  });
}

export function installPageViewTracking(router) {
  router.afterEach((to, from) => {
    trackRoute(to, from);
  });

  router.isReady().then(() => {
    trackRoute(router.currentRoute.value, null);
  });
}
