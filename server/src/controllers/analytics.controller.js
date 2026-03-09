function normalizeString(value, fallback = '') {
  if (typeof value !== 'string') {
    return fallback;
  }

  return value.trim();
}

function normalizeIpAddress(value) {
  const ip = normalizeString(value, null);
  if (!ip) {
    return null;
  }

  if (ip === '::1') {
    return '127.0.0.1';
  }

  if (ip.startsWith('::ffff:')) {
    return ip.slice(7);
  }

  return ip;
}

export function createAnalyticsController({ analyticsService }) {
  return {
    getOverview: async (req, res, next) => {
      try {
        const data = await analyticsService.getOverview();
        res.json({
          ok: true,
          data,
        });
      } catch (error) {
        next(error);
      }
    },

    trackPageView: async (req, res, next) => {
      try {
        const path = normalizeString(req.body?.path);
        const sessionId = normalizeString(req.body?.sessionId);

        if (!path || !sessionId) {
          return res.status(400).json({
            ok: false,
            message: 'path and sessionId are required',
          });
        }

        const result = await analyticsService.trackPageView({
          chapterId: normalizeString(req.body?.chapterId, null),
          ipAddress: normalizeIpAddress(req.ip),
          path,
          referrer:
            normalizeString(req.body?.referrer) || normalizeString(req.get('referer'), null),
          sessionId,
          userAgent:
            normalizeString(req.body?.userAgent) || normalizeString(req.get('user-agent'), null),
        });

        res.status(201).json({
          ok: true,
          id: result.id,
        });
      } catch (error) {
        next(error);
      }
    },
  };
}
