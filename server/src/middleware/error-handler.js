export function notFoundHandler(req, res) {
  res.status(404).json({
    ok: false,
    message: 'Not Found',
  });
}

export function createErrorHandler({ logger }) {
  return function errorHandler(error, req, res, next) {
    logger.error('request failed', {
      message: error.message,
      method: req.method,
      path: req.originalUrl,
    });

    if (res.headersSent) {
      return next(error);
    }

    res.status(error.statusCode ?? 500).json({
      ok: false,
      message: error.expose ? error.message : 'Internal Server Error',
    });
  };
}
