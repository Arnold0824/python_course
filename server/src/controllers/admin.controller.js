function readPositiveInt(value, fallback, max) {
  const parsed = Number.parseInt(value, 10);
  if (Number.isNaN(parsed) || parsed <= 0) {
    return fallback;
  }

  return Math.min(parsed, max);
}

export function createAdminController({ analyticsService, ideaService }) {
  return {
    getDashboard: async (req, res, next) => {
      try {
        const days = readPositiveInt(req.query.days, 7, 90);
        const limit = readPositiveInt(req.query.limit, 50, 200);
        const data = await analyticsService.getAdminDashboard({ days, limit });

        res.json({
          ok: true,
          data,
        });
      } catch (error) {
        next(error);
      }
    },

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

    getRecentViews: async (req, res, next) => {
      try {
        const limit = readPositiveInt(req.query.limit, 50, 200);
        const data = await analyticsService.getRecentPageViews(limit);
        res.json({
          ok: true,
          data,
        });
      } catch (error) {
        next(error);
      }
    },

    hideIdeaMessage: async (req, res, next) => {
      try {
        const id = readPositiveInt(req.params.id, 0, Number.MAX_SAFE_INTEGER);
        if (!id) {
          return res.status(400).json({
            ok: false,
            message: 'valid message id is required',
          });
        }

        const result = await ideaService.hideMessage({
          id,
          reason: typeof req.body?.reason === 'string' ? req.body.reason.trim().slice(0, 255) : '',
        });

        if (!result.hidden) {
          return res.status(404).json({
            ok: false,
            message: 'message not found',
          });
        }

        return res.json({
          ok: true,
          data: result,
        });
      } catch (error) {
        return next(error);
      }
    },
  };
}
