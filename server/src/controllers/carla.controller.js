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

function readPositiveInt(value, fallback, max) {
  const parsed = Number.parseInt(value, 10);
  if (Number.isNaN(parsed) || parsed <= 0) {
    return fallback;
  }

  return Math.min(parsed, max);
}

export function createCarlaController({ carlaScoreService, config }) {
  return {
    getLeaderboard: async (req, res, next) => {
      try {
        const limit = readPositiveInt(req.query.limit, 50, 200);
        const data = await carlaScoreService.getLeaderboard({ limit });

        res.json({
          ok: true,
          data,
        });
      } catch (error) {
        next(error);
      }
    },

    submitScore: async (req, res, next) => {
      try {
        const expectedToken = normalizeString(config.carlaScore.submitToken);
        if (!expectedToken) {
          return res.status(503).json({
            ok: false,
            message: 'CARLA_SCORE_SUBMIT_TOKEN is not configured',
          });
        }

        const providedToken = normalizeString(req.get('x-carla-submit-token'));
        if (providedToken !== expectedToken) {
          return res.status(401).json({
            ok: false,
            message: 'Unauthorized',
          });
        }

        const data = await carlaScoreService.submitScore({
          ipAddress: normalizeIpAddress(req.ip),
          studentId: req.body?.studentId,
          studentName: req.body?.studentName,
          summary: req.body?.summary,
        });

        res.status(201).json({
          ok: true,
          data,
        });
      } catch (error) {
        next(error);
      }
    },
  };
}
