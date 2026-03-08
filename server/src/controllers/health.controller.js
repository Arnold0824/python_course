export function createHealthController({ config, db, deployService }) {
  return async function healthController(req, res, next) {
    try {
      const database = await db.ping();
      const statusCode = database.ok ? 200 : 503;

      res.status(statusCode).json({
        ok: database.ok,
        service: config.app.name,
        env: config.app.env,
        uptimeSeconds: Math.round(process.uptime()),
        deploying: deployService.isDeploying(),
        database,
      });
    } catch (error) {
      next(error);
    }
  };
}
