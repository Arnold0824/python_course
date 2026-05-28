export function createIdeaService({ config, db }) {
  const tableName = config.ideas.messageTable

  function tableRef() {
    return `\`${tableName}\``
  }

  function toSafeLimit(value, fallback = 50, max = 100) {
    const parsed = Number.parseInt(value, 10)
    if (Number.isNaN(parsed) || parsed <= 0) {
      return fallback
    }

    return Math.min(parsed, max)
  }

  function mapMessageRow(row) {
    return {
      content: row.content,
      createdAt:
        row.createdAt instanceof Date ? row.createdAt.toISOString() : String(row.createdAt ?? ''),
      displayName: row.displayName,
      id: Number(row.id),
    }
  }

  async function initSchema() {
    await db.getPool().query(`
      CREATE TABLE IF NOT EXISTS ${tableRef()} (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        content VARCHAR(500) NOT NULL,
        display_name VARCHAR(64) NOT NULL DEFAULT '匿名同学',
        course_id VARCHAR(64) NOT NULL DEFAULT 'python',
        chapter_id VARCHAR(64) NULL,
        page_path VARCHAR(255) NULL,
        session_id VARCHAR(128) NULL,
        ip_hash CHAR(64) NULL,
        user_agent VARCHAR(500) NULL,
        status ENUM('visible', 'hidden', 'pending') NOT NULL DEFAULT 'visible',
        hidden_reason VARCHAR(255) NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        hidden_at DATETIME NULL,
        PRIMARY KEY (id),
        KEY idx_idea_messages_status_created (status, created_at),
        KEY idx_idea_messages_course_chapter (course_id, chapter_id),
        KEY idx_idea_messages_session (session_id),
        KEY idx_idea_messages_ip_hash_created (ip_hash, created_at)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    `)
  }

  async function getMessageById(id) {
    const [rows] = await db.getPool().execute(
      `
        SELECT
          id,
          content,
          display_name AS displayName,
          created_at AS createdAt
        FROM ${tableRef()}
        WHERE id = ?
        LIMIT 1
      `,
      [id],
    )

    return rows[0] ? mapMessageRow(rows[0]) : null
  }

  async function createMessage(payload) {
    const [result] = await db.getPool().execute(
      `
        INSERT INTO ${tableRef()} (
          content,
          display_name,
          course_id,
          chapter_id,
          page_path,
          session_id,
          ip_hash,
          user_agent,
          status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'visible')
      `,
      [
        payload.content,
        payload.displayName,
        payload.courseId,
        payload.chapterId,
        payload.pagePath,
        payload.sessionId,
        payload.ipHash,
        payload.userAgent,
      ],
    )

    const savedMessage = await getMessageById(result.insertId)
    return (
      savedMessage ?? {
        content: payload.content,
        createdAt: new Date().toISOString(),
        displayName: payload.displayName,
        id: result.insertId,
      }
    )
  }

  async function listVisibleMessages({ limit = 50 } = {}) {
    const safeLimit = toSafeLimit(limit)
    const [rows] = await db.getPool().query(
      `
        SELECT
          id,
          content,
          display_name AS displayName,
          created_at AS createdAt
        FROM ${tableRef()}
        WHERE status = 'visible'
        ORDER BY created_at DESC, id DESC
        LIMIT ${safeLimit}
      `,
    )

    return rows.map(mapMessageRow)
  }

  async function hideMessage({ id, reason = '' }) {
    const [result] = await db.getPool().execute(
      `
        UPDATE ${tableRef()}
        SET
          status = 'hidden',
          hidden_reason = ?,
          hidden_at = NOW()
        WHERE id = ?
      `,
      [reason || null, id],
    )

    return {
      hidden: result.affectedRows > 0,
    }
  }

  return {
    createMessage,
    hideMessage,
    initSchema,
    listVisibleMessages,
  }
}
