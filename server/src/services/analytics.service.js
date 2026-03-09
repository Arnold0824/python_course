export function createAnalyticsService({ config, db }) {
  const tableName = config.analytics.pageViewTable;

  function toSafeInt(value, fallback, min, max) {
    const parsed = Number.parseInt(value, 10);
    if (Number.isNaN(parsed)) {
      return fallback;
    }

    return Math.max(min, Math.min(parsed, max));
  }

  function tableRef() {
    return `\`${tableName}\``;
  }

  function formatDateKey(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  function formatDateLabel(dateKey) {
    return dateKey.slice(5).replace('-', '/');
  }

  function formatHourKey(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    return `${year}-${month}-${day} ${hour}:00`;
  }

  function formatHourLabel(hourKey) {
    return hourKey.slice(5);
  }

  function buildRecentDateKeys(days) {
    const keys = [];
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    for (let offset = days - 1; offset >= 0; offset -= 1) {
      const current = new Date(today);
      current.setDate(today.getDate() - offset);
      keys.push(formatDateKey(current));
    }

    return keys;
  }

  function buildRecentHourKeys(hours) {
    const keys = [];
    const now = new Date();
    now.setMinutes(0, 0, 0);

    for (let offset = hours - 1; offset >= 0; offset -= 1) {
      const current = new Date(now);
      current.setHours(now.getHours() - offset);
      keys.push(formatHourKey(current));
    }

    return keys;
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
          COUNT(DISTINCT NULLIF(ip_address, '')) AS uniqueUsers,
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
      uniqueUsers: Number(totalsRows[0]?.uniqueUsers ?? 0),
      uniqueSessions: Number(totalsRows[0]?.uniqueSessions ?? 0),
    };
  }

  async function getRecentPageViews(limit = 50) {
    const safeLimit = Math.max(1, Math.min(Number(limit) || 50, 200));
    const [rows] = await db.getPool().query(
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
        LIMIT ${safeLimit}
      `,
    );

    return rows;
  }

  async function getDailyMetrics(days = 7) {
    const safeDays = toSafeInt(days, 7, 1, 90);
    const [rows] = await db.getPool().query(
      `
        SELECT
          DATE(created_at) AS viewDate,
          COUNT(*) AS views,
          COUNT(DISTINCT NULLIF(ip_address, '')) AS uniqueUsers
        FROM ${tableRef()}
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL ${safeDays} DAY)
        GROUP BY DATE(created_at)
        ORDER BY viewDate DESC
      `,
    );

    const rowMap = new Map(
      rows.map((row) => [
        String(row.viewDate),
        {
          uniqueUsers: Number(row.uniqueUsers ?? 0),
          views: Number(row.views ?? 0),
        },
      ]),
    );

    return buildRecentDateKeys(safeDays).map((dateKey) => {
      const hit = rowMap.get(dateKey) ?? { views: 0, uniqueUsers: 0 };
      return {
        label: formatDateLabel(dateKey),
        uniqueUsers: hit.uniqueUsers,
        viewDate: dateKey,
        views: hit.views,
      };
    });
  }

  async function getHourlyMetrics(hours = 24) {
    const safeHours = toSafeInt(hours, 24, 6, 72);
    const [rows] = await db.getPool().query(
      `
        SELECT
          DATE_FORMAT(created_at, '%Y-%m-%d %H:00') AS hourKey,
          COUNT(*) AS views,
          COUNT(DISTINCT NULLIF(ip_address, '')) AS uniqueUsers
        FROM ${tableRef()}
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL ${safeHours} HOUR)
        GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d %H:00')
        ORDER BY hourKey ASC
      `,
    );

    const rowMap = new Map(
      rows.map((row) => [
        String(row.hourKey),
        {
          uniqueUsers: Number(row.uniqueUsers ?? 0),
          views: Number(row.views ?? 0),
        },
      ]),
    );

    return buildRecentHourKeys(safeHours).map((hourKey) => {
      const hit = rowMap.get(hourKey) ?? { views: 0, uniqueUsers: 0 };
      return {
        hourKey,
        label: formatHourLabel(hourKey),
        uniqueUsers: hit.uniqueUsers,
        views: hit.views,
      };
    });
  }

  async function getChapterTrend(days = 7, topN = 4) {
    const safeDays = toSafeInt(days, 7, 1, 90);
    const safeTopN = toSafeInt(topN, 4, 1, 6);
    const [rows] = await db.getPool().query(
      `
        SELECT
          DATE(created_at) AS viewDate,
          chapter_id AS chapterId,
          COUNT(*) AS views
        FROM ${tableRef()}
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL ${safeDays} DAY)
          AND chapter_id IS NOT NULL
          AND chapter_id <> ''
        GROUP BY DATE(created_at), chapter_id
        ORDER BY viewDate ASC
      `,
    );

    const totals = new Map();
    const valueMap = new Map();

    for (const row of rows) {
      const chapterId = String(row.chapterId);
      const viewDate = String(row.viewDate);
      const views = Number(row.views ?? 0);

      totals.set(chapterId, (totals.get(chapterId) ?? 0) + views);
      valueMap.set(`${chapterId}|${viewDate}`, views);
    }

    const topChapterIds = [...totals.entries()]
      .sort((left, right) => right[1] - left[1])
      .slice(0, safeTopN)
      .map(([chapterId]) => chapterId);

    const dateKeys = buildRecentDateKeys(safeDays);

    return {
      labels: dateKeys.map((dateKey) => formatDateLabel(dateKey)),
      series: topChapterIds.map((chapterId) => ({
        chapterId,
        totalViews: totals.get(chapterId) ?? 0,
        values: dateKeys.map((dateKey) => Number(valueMap.get(`${chapterId}|${dateKey}`) ?? 0)),
      })),
    };
  }

  async function getAdminDashboard({ days = 7, limit = 50 } = {}) {
    const [overview, recentViews, dailyMetrics, hourlyMetrics, chapterTrend] = await Promise.all([
      getOverview(),
      getRecentPageViews(limit),
      getDailyMetrics(days),
      getHourlyMetrics(),
      getChapterTrend(days),
    ]);

    return {
      chapterTrend,
      dailyMetrics,
      hourlyMetrics,
      overview,
      recentViews,
    };
  }

  return {
    getAdminDashboard,
    getChapterTrend,
    getDailyMetrics,
    getHourlyMetrics,
    getOverview,
    getRecentPageViews,
    initSchema,
    trackPageView,
  };
}
