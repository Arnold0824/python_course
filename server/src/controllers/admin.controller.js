function readPositiveInt(value, fallback, max) {
  const parsed = Number.parseInt(value, 10);
  if (Number.isNaN(parsed) || parsed <= 0) {
    return fallback;
  }

  return Math.min(parsed, max);
}

export function createAdminController({ analyticsService }) {
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
  };
}
