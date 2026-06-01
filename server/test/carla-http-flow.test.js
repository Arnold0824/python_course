import assert from 'node:assert/strict';
import test from 'node:test';
import { createApp } from '../src/app.js';
import { createCarlaScoreService } from '../src/services/carla-score.service.js';

function createMemoryDb() {
  const rows = [];
  let nextId = 1;

  return {
    getPool() {
      return {
        async execute(_sql, params) {
          const id = nextId;
          nextId += 1;
          rows.push({
            id,
            student_id: params[0],
            student_name: params[1],
            final_score: params[2],
            completed: params[3],
            lap_time_s: params[4],
            completion_points: params[5],
            time_points: params[6],
            penalty_points: params[7],
            raw_score: params[8],
            protected_settings_checksum: params[9],
            penalty_breakdown_json: params[10],
            summary_json: params[11],
            ip_address: params[12],
            created_at: new Date(Date.UTC(2026, 5, 1, 10, 0, id)).toISOString(),
          });
          return [{ insertId: id }];
        },
        async query() {
          return [[...rows].sort((left, right) => right.id - left.id)];
        },
      };
    },
    async ping() {
      return { ok: true };
    },
  };
}

function createTestRuntime() {
  const config = {
    app: {
      jsonLimit: '1mb',
      name: 'python-course-server-test',
    },
    admin: {
      token: '',
    },
    carlaScore: {
      submitToken: 'test-token',
      tableName: 'carla_score_submissions',
    },
    webhook: {
      maxBodySize: '1mb',
      path: '/api/webhooks/github',
      secret: '',
    },
  };
  const logger = {
    error() {},
    info() {},
    warn() {},
  };
  const db = createMemoryDb();
  const carlaScoreService = createCarlaScoreService({ config, db });
  const app = createApp({
    analyticsService: {
      trackPageView: async () => ({ id: 1 }),
    },
    carlaScoreService,
    config,
    db,
    deployService: {
      isDeploying: () => false,
    },
    logger,
  });

  return { app };
}

async function withServer(app, callback) {
  const server = await new Promise((resolve) => {
    const instance = app.listen(0, '127.0.0.1', () => resolve(instance));
  });
  try {
    const { port } = server.address();
    return await callback(`http://127.0.0.1:${port}`);
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
}

test('CARLA HTTP score submission appears on public leaderboard', async () => {
  const { app } = createTestRuntime();

  await withServer(app, async (baseUrl) => {
    const submitResponse = await fetch(`${baseUrl}/api/carla/scores`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Carla-Submit-Token': 'test-token',
      },
      body: JSON.stringify({
        studentId: '20230001',
        studentName: '张三',
        summary: {
          completed: false,
          completion_points: 0,
          distance_points: 137.5,
          distance_traveled_m: 137.5,
          duration_s: 60,
          final_score: 132.5,
          lap_time_s: null,
          penalty_breakdown: { lane_invasion: 5 },
          penalty_points: 5,
          protected_settings_checksum: 'abc123',
          raw_score: 132.5,
          time_points: 0,
        },
      }),
    });

    assert.equal(submitResponse.status, 201);
    const submitPayload = await submitResponse.json();
    assert.equal(submitPayload.ok, true);
    assert.equal(submitPayload.data.rank, 1);

    const leaderboardResponse = await fetch(`${baseUrl}/api/carla/leaderboard?limit=50`);
    assert.equal(leaderboardResponse.status, 200);
    const leaderboardPayload = await leaderboardResponse.json();
    assert.equal(leaderboardPayload.ok, true);
    assert.deepEqual(leaderboardPayload.data.entries[0], {
      bestSubmittedAt: '2026-06-01T10:00:01.000Z',
      completed: false,
      distancePoints: 137.5,
      distanceTraveledM: 137.5,
      durationS: 60,
      finalScore: 132.5,
      lapTimeS: null,
      penaltyPoints: 5,
      rank: 1,
      studentId: '20230001',
      studentName: '张三',
      submissionCount: 1,
      submissionId: 1,
    });
  });
});
