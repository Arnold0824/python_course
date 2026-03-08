import mysql from 'mysql2/promise';

export function createDatabase({ config, logger }) {
  let pool;

  function getPool() {
    if (!pool) {
      pool = mysql.createPool({
        host: config.mysql.host,
        port: config.mysql.port,
        user: config.mysql.user,
        password: config.mysql.password,
        database: config.mysql.database,
        connectionLimit: config.mysql.connectionLimit,
        connectTimeout: config.mysql.connectTimeout,
        charset: 'utf8mb4',
        namedPlaceholders: false,
        timezone: 'Z',
      });
    }

    return pool;
  }

  async function ping() {
    try {
      const connection = await getPool().getConnection();
      try {
        await connection.ping();
        return { ok: true };
      } finally {
        connection.release();
      }
    } catch (error) {
      logger.warn('database ping failed', {
        message: error.message,
      });
      return { ok: false, message: error.message };
    }
  }

  async function close() {
    if (!pool) {
      return;
    }

    await pool.end();
    pool = undefined;
  }

  return {
    close,
    getPool,
    ping,
  };
}
