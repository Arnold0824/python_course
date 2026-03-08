export function createAnalyticsService({ config, db }) {
  const tableName = config.analytics.pageViewTable;

  function tableRef() {
    return `\`${tableName}\``;
  }

  async function initSchema() {
    await db.getPool().query(`
      CREATE TABLE IF NOT EXISTS ${tableRef()} (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        path VARCHAR(255) NOT NULL,
        chapter_id VARCHAR(64) NULL,
        session_id VARCHAR(128) NOT NULL,
        referrer VARCHAR(500) NULL,
        user_agent VARCHAR(500) NULL,
        ip_address VARCHAR(64) NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY idx_page_views_path (path),
        KEY idx_page_views_chapter_id (chapter_id),
        KEY idx_page_views_created_at (created_at)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    `);
  }

  async function trackPageView(payload) {
    const [result] = await db.getPool().execute(
      `
        INSERT INTO ${tableRef()} (
          path,
          chapter_id,
          session_id,
          referrer,
          user_agent,
          ip_address
        )
        VALUES (?, ?, ?, ?, ?, ?)
      `,
      [
        payload.path,
        payload.chapterId,
        payload.sessionId,
        payload.referrer,
        payload.userAgent,
        payload.ipAddress,
      ],
    );

    return {
      id: result.insertId,
    };
  }

  async function getOverview() {
    const [totalsRows] = await db.getPool().query(
      `
        SELECT
          COUNT(*) AS totalViews,
          COUNT(DISTINCT session_id) AS uniqueSessions
        FROM ${tableRef()}
      `,
    );

    const [chapterRows] = await db.getPool().query(
      `
        SELECT
          chapter_id AS chapterId,
          COUNT(*) AS views
        FROM ${tableRef()}
        GROUP BY chapter_id
        ORDER BY views DESC
        LIMIT 20
      `,
    );

    const [pathRows] = await db.getPool().query(
      `
        SELECT
          path,
          COUNT(*) AS views
        FROM ${tableRef()}
        GROUP BY path
        ORDER BY views DESC
        LIMIT 20
      `,
    );

    return {
      chapters: chapterRows,
      paths: pathRows,
      totalViews: Number(totalsRows[0]?.totalViews ?? 0),
      uniqueSessions: Number(totalsRows[0]?.uniqueSessions ?? 0),
    };
  }

  async function getRecentPageViews(limit = 50) {
    const safeLimit = Math.max(1, Math.min(Number(limit) || 50, 200));
    const [rows] = await db.getPool().execute(
      `
        SELECT
          id,
          path,
          chapter_id AS chapterId,
          session_id AS sessionId,
          referrer,
          user_agent AS userAgent,
          ip_address AS ipAddress,
          created_at AS createdAt
        FROM ${tableRef()}
        ORDER BY created_at DESC, id DESC
        LIMIT ?
      `,
      [safeLimit],
    );

    return rows;
  }

  async function getDailyViews(days = 7) {
    const safeDays = Math.max(1, Math.min(Number(days) || 7, 90));
    const [rows] = await db.getPool().execute(
      `
        SELECT
          DATE(created_at) AS viewDate,
          COUNT(*) AS views
        FROM ${tableRef()}
        WHERE created_at >= DATE_SUB(UTC_TIMESTAMP(), INTERVAL ? DAY)
        GROUP BY DATE(created_at)
        ORDER BY viewDate DESC
      `,
      [safeDays],
    );

    return rows;
  }

  async function getAdminDashboard({ days = 7, limit = 50 } = {}) {
    const [overview, recentViews, dailyViews] = await Promise.all([
      getOverview(),
      getRecentPageViews(limit),
      getDailyViews(days),
    ]);

    return {
      dailyViews,
      overview,
      recentViews,
    };
  }

  return {
    getAdminDashboard,
    getDailyViews,
    getOverview,
    getRecentPageViews,
    initSchema,
    trackPageView,
  };
}
