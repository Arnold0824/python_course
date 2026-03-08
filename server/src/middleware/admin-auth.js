export function createAdminAuth({ config }) {
  return function requireAdminToken(req, res, next) {
    if (!config.admin.token && config.app.env !== 'production') {
      return next();
    }

    if (!config.admin.token) {
      return res.status(503).json({
        ok: false,
        message: 'ADMIN_TOKEN is not configured',
      });
    }

    const authHeader = req.get('authorization') || '';
    const bearerToken = authHeader.startsWith('Bearer ')
      ? authHeader.slice('Bearer '.length).trim()
      : '';
    const headerToken = (req.get('x-admin-token') || '').trim();
    const token = bearerToken || headerToken;

    if (token !== config.admin.token) {
      return res.status(401).json({
        ok: false,
        message: 'Unauthorized',
      });
    }

    next();
  };
}
