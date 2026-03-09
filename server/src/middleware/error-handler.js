export function notFoundHandler(req, res) {
  res.status(404).json({
    ok: false,
    message: 'Not Found',
  });
}

export function createErrorHandler({ logger }) {
  return function errorHandler(error, req, res, next) {
    const requestBody =
      req.body && typeof req.body === 'object' && !Buffer.isBuffer(req.body)
        ? req.body
        : undefined;

    logger.error('request failed', {
      body: requestBody,
      message: error.message,
      method: req.method,
      path: req.originalUrl,
      query: req.query,
      stack: error.stack,
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
