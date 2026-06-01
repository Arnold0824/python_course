function createPublicError(message, statusCode = 400) {
  const error = new Error(message);
  error.statusCode = statusCode;
  error.expose = true;
  return error;
}

function toNumber(value, fieldName, { nullable = false } = {}) {
  if ((value === null || value === undefined || value === '') && nullable) {
    return null;
  }

  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    throw createPublicError(`${fieldName} must be a number`);
  }

  return parsed;
}

function toSafeLimit(value, fallback = 50) {
  const parsed = Number.parseInt(value, 10);
  if (Number.isNaN(parsed) || parsed <= 0) {
    return fallback;
  }

  return Math.min(parsed, 200);
}

function tableRef(tableName) {
  return `\`${tableName}\``;
}

function parseJsonField(value, fallback) {
  if (value === null || value === undefined || value === '') {
    return fallback;
  }
  if (typeof value === 'object') {
    return value;
  }
  try {
    return JSON.parse(String(value));
  } catch {
    return fallback;
  }
}

function toIsoString(value) {
  if (!value) {
    return null;
  }
  if (value instanceof Date) {
    return value.toISOString();
  }
  const parsed = new Date(value);
  if (!Number.isNaN(parsed.getTime())) {
    return parsed.toISOString();
  }
  return String(value);
}

function optionalSummaryNumber(summary, snakeName, camelName) {
  const value = summary?.[snakeName] ?? summary?.[camelName];
  if (value === null || value === undefined || value === '') {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function normalizeLeaderboardRow(row) {
  return {
    completed: Boolean(row.completed),
    completionPoints: Number(row.completion_points ?? 0),
    createdAt: toIsoString(row.created_at),
    finalScore: Number(row.final_score ?? 0),
    lapTimeS: row.lap_time_s === null || row.lap_time_s === undefined ? null : Number(row.lap_time_s),
    penaltyBreakdown: parseJsonField(row.penalty_breakdown_json, {}),
    penaltyPoints: Number(row.penalty_points ?? 0),
    protectedSettingsChecksum: row.protected_settings_checksum || '',
    rawScore: Number(row.raw_score ?? 0),
    studentId: String(row.student_id || ''),
    studentName: String(row.student_name || ''),
    submissionId: Number(row.id),
    summary: parseJsonField(row.summary_json, {}),
    timePoints: Number(row.time_points ?? 0),
  };
}

function compareLeaderboardRecords(left, right) {
  if (right.finalScore !== left.finalScore) {
    return right.finalScore - left.finalScore;
  }
  if (Number(right.completed) !== Number(left.completed)) {
    return Number(right.completed) - Number(left.completed);
  }
  const leftLap = left.lapTimeS === null ? Number.POSITIVE_INFINITY : left.lapTimeS;
  const rightLap = right.lapTimeS === null ? Number.POSITIVE_INFINITY : right.lapTimeS;
  if (leftLap !== rightLap) {
    return leftLap - rightLap;
  }
  if (left.penaltyPoints !== right.penaltyPoints) {
    return left.penaltyPoints - right.penaltyPoints;
  }
  const leftCreated = Date.parse(left.createdAt || '');
  const rightCreated = Date.parse(right.createdAt || '');
  if (leftCreated !== rightCreated) {
    return leftCreated - rightCreated;
  }
  return left.submissionId - right.submissionId;
}

export function buildLeaderboardEntries(rows, limit = 50) {
  const submissions = rows.map(normalizeLeaderboardRow).filter((row) => row.studentId);
  const byStudent = new Map();

  for (const submission of submissions) {
    const current = byStudent.get(submission.studentId);
    if (!current) {
      byStudent.set(submission.studentId, {
        best: submission,
        count: 1,
      });
      continue;
    }

    current.count += 1;
    if (compareLeaderboardRecords(submission, current.best) < 0) {
      current.best = submission;
    }
  }

  return [...byStudent.values()]
    .map(({ best, count }) => ({
      ...best,
      submissionCount: count,
    }))
    .sort(compareLeaderboardRecords)
    .slice(0, toSafeLimit(limit))
    .map((best, index) => ({
      bestSubmittedAt: best.createdAt,
      completed: best.completed,
      distancePoints: optionalSummaryNumber(best.summary, 'distance_points', 'distancePoints'),
      distanceTraveledM: optionalSummaryNumber(
        best.summary,
        'distance_traveled_m',
        'distanceTraveledM',
      ),
      durationS: optionalSummaryNumber(best.summary, 'duration_s', 'durationS'),
      finalScore: best.finalScore,
      lapTimeS: best.lapTimeS,
      penaltyPoints: best.penaltyPoints,
      rank: index + 1,
      studentId: best.studentId,
      studentName: best.studentName,
      submissionCount: best.submissionCount,
      submissionId: best.submissionId,
    }));
}

function normalizeSubmission({ ipAddress, studentId, studentName, summary }) {
  const normalizedStudentId = String(studentId || '').trim();
  const normalizedStudentName = String(studentName || '').trim();

  if (!normalizedStudentId || !normalizedStudentName) {
    throw createPublicError('studentId and studentName are required');
  }
  if (normalizedStudentId.length > 64 || normalizedStudentName.length > 100) {
    throw createPublicError('studentId or studentName is too long');
  }
  if (!summary || typeof summary !== 'object' || Array.isArray(summary)) {
    throw createPublicError('summary is required');
  }

  return {
    completed: Boolean(summary.completed),
    completionPoints: toNumber(summary.completion_points ?? summary.completionPoints, 'completion_points'),
    finalScore: toNumber(summary.final_score ?? summary.finalScore, 'final_score'),
    ipAddress: ipAddress || null,
    lapTimeS: toNumber(summary.lap_time_s ?? summary.lapTimeS, 'lap_time_s', { nullable: true }),
    penaltyBreakdown: summary.penalty_breakdown ?? summary.penaltyBreakdown ?? {},
    penaltyPoints: toNumber(summary.penalty_points ?? summary.penaltyPoints, 'penalty_points'),
    protectedSettingsChecksum: String(
      summary.protected_settings_checksum ?? summary.protectedSettingsChecksum ?? '',
    ).trim(),
    rawScore: toNumber(summary.raw_score ?? summary.rawScore, 'raw_score'),
    studentId: normalizedStudentId,
    studentName: normalizedStudentName,
    summary,
    timePoints: toNumber(summary.time_points ?? summary.timePoints, 'time_points'),
  };
}

export function createCarlaScoreService({ config, db }) {
  const tableName = config.carlaScore.tableName;

  async function initSchema() {
    await db.getPool().query(`
      CREATE TABLE IF NOT EXISTS ${tableRef(tableName)} (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        student_id VARCHAR(64) NOT NULL,
        student_name VARCHAR(100) NOT NULL,
        final_score DECIMAL(6,2) NOT NULL,
        completed TINYINT(1) NOT NULL DEFAULT 0,
        lap_time_s DECIMAL(10,3) NULL,
        completion_points DECIMAL(6,2) NOT NULL DEFAULT 0,
        time_points DECIMAL(6,2) NOT NULL DEFAULT 0,
        penalty_points DECIMAL(6,2) NOT NULL DEFAULT 0,
        raw_score DECIMAL(6,2) NOT NULL DEFAULT 0,
        protected_settings_checksum VARCHAR(64) NULL,
        penalty_breakdown_json JSON NULL,
        summary_json JSON NOT NULL,
        ip_address VARCHAR(64) NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY idx_carla_scores_student_id (student_id),
        KEY idx_carla_scores_final_score (final_score),
        KEY idx_carla_scores_created_at (created_at)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    `);
  }

  async function listSubmissions() {
    const [rows] = await db.getPool().query(`
      SELECT
        id,
        student_id,
        student_name,
        final_score,
        completed,
        lap_time_s,
        completion_points,
        time_points,
        penalty_points,
        raw_score,
        protected_settings_checksum,
        penalty_breakdown_json,
        summary_json,
        created_at
      FROM ${tableRef(tableName)}
      ORDER BY created_at DESC, id DESC
    `);

    return rows;
  }

  async function getLeaderboard({ limit = 50 } = {}) {
    const rows = await listSubmissions();
    return {
      entries: buildLeaderboardEntries(rows, limit),
    };
  }

  async function submitScore(payload) {
    const submission = normalizeSubmission(payload);
    const [result] = await db.getPool().execute(
      `
        INSERT INTO ${tableRef(tableName)} (
          student_id,
          student_name,
          final_score,
          completed,
          lap_time_s,
          completion_points,
          time_points,
          penalty_points,
          raw_score,
          protected_settings_checksum,
          penalty_breakdown_json,
          summary_json,
          ip_address
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `,
      [
        submission.studentId,
        submission.studentName,
        submission.finalScore,
        submission.completed ? 1 : 0,
        submission.lapTimeS,
        submission.completionPoints,
        submission.timePoints,
        submission.penaltyPoints,
        submission.rawScore,
        submission.protectedSettingsChecksum || null,
        JSON.stringify(submission.penaltyBreakdown),
        JSON.stringify(submission.summary),
        submission.ipAddress,
      ],
    );

    const submissionId = Number(result.insertId);
    const leaderboard = await getLeaderboard({ limit: 10000 });
    const entry = leaderboard.entries.find((item) => item.studentId === submission.studentId);

    return {
      bestForStudent: entry?.submissionId === submissionId,
      rank: entry?.rank ?? null,
      submissionId,
    };
  }

  return {
    getLeaderboard,
    initSchema,
    submitScore,
  };
}
