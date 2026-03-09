import { createApp } from './app.js';
import { loadConfig } from './config/env.js';
import { createDatabase } from './db/index.js';
import { createLogger } from './lib/logger.js';
import { createAnalyticsService } from './services/analytics.service.js';
import { createDeployService } from './services/deploy.service.js';

async function buildRuntime() {
  const config = loadConfig();
  const logger = createLogger({
    level: config.app.logLevel,
    logFile: config.app.logFile,
  });
  const db = createDatabase({ config, logger });
  const deployService = createDeployService({ config, logger });
  const analyticsService = createAnalyticsService({ config, db, logger });

  try {
    await analyticsService.initSchema();
    logger.info('analytics schema ready', {
      table: config.analytics.pageViewTable,
    });
  } catch (error) {
    logger.warn('analytics schema init failed', {
      message: error.message,
    });
  }

  const app = createApp({
    analyticsService,
    config,
    db,
    deployService,
    logger,
  });

  return {
    app,
    analyticsService,
    config,
    db,
    deployService,
    logger,
  };
}

function installSignalHandlers({ logger, server, db }) {
  let shuttingDown = false;

  const shutdown = async (signal) => {
    if (shuttingDown) {
      return;
    }

    shuttingDown = true;
    logger.info('shutdown requested', { signal });

    await new Promise((resolve) => {
      server.close(() => resolve());
    });

    await db.close();
    logger.info('shutdown complete', { signal });
  };

  for (const signal of ['SIGINT', 'SIGTERM']) {
    process.on(signal, () => {
      void shutdown(signal).finally(() => {
        process.exit(0);
      });
    });
  }
}

export async function startServer() {
  const runtime = await buildRuntime();

  return new Promise((resolve, reject) => {
    const server = runtime.app.listen(runtime.config.app.port, runtime.config.app.host, () => {
      runtime.logger.info('server ready', {
        host: runtime.config.app.host,
        port: runtime.config.app.port,
        webhookPath: runtime.config.webhook.path,
      });

      installSignalHandlers({
        db: runtime.db,
        logger: runtime.logger,
        server,
      });

      resolve({
        server,
        ...runtime,
      });
    });

    server.on('error', (error) => {
      runtime.logger.error('server listen failed', {
        message: error.message,
      });
      reject(error);
    });
  });
}
