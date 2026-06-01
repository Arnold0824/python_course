import assert from 'node:assert/strict';
import test from 'node:test';
import { createCarlaController } from '../src/controllers/carla.controller.js';
import {
  buildLeaderboardEntries,
  createCarlaScoreService,
} from '../src/services/carla-score.service.js';

function row(overrides) {
  return {
    id: overrides.id,
    student_id: overrides.studentId,
    student_name: overrides.studentName,
    final_score: overrides.finalScore,
    completed: overrides.completed ? 1 : 0,
    lap_time_s: overrides.lapTimeS ?? null,
    completion_points: overrides.completionPoints ?? 0,
    time_points: overrides.timePoints ?? 0,
    penalty_points: overrides.penaltyPoints ?? 0,
    raw_score: overrides.rawScore ?? overrides.finalScore,
    protected_settings_checksum: overrides.checksum ?? 'checksum',
    penalty_breakdown_json: '{}',
    summary_json: JSON.stringify(overrides.summary ?? {}),
    created_at: overrides.createdAt,
  };
}

test('leaderboard keeps each student best submission and applies tie breakers', () => {
  const entries = buildLeaderboardEntries(
    [
      row({
        id: 1,
        studentId: '20230001',
        studentName: '张三',
        finalScore: 80,
        completed: true,
        lapTimeS: 200,
        penaltyPoints: 2,
        createdAt: '2026-06-01T10:00:00.000Z',
      }),
      row({
        id: 2,
        studentId: '20230001',
        studentName: '张三',
        finalScore: 90,
        completed: false,
        lapTimeS: null,
        penaltyPoints: 0,
        createdAt: '2026-06-01T11:00:00.000Z',
      }),
      row({
        id: 3,
        studentId: '20230002',
        studentName: '李四',
        finalScore: 90,
        completed: true,
        lapTimeS: 230,
        penaltyPoints: 0,
        createdAt: '2026-06-01T12:00:00.000Z',
      }),
      row({
        id: 4,
        studentId: '20230003',
        studentName: '王五',
        finalScore: 90,
        completed: true,
        lapTimeS: 210,
        penaltyPoints: 4,
        createdAt: '2026-06-01T09:00:00.000Z',
      }),
    ],
    50,
  );

  assert.deepEqual(
    entries.map((entry) => [entry.rank, entry.studentId, entry.finalScore, entry.submissionCount]),
    [
      [1, '20230003', 90, 1],
      [2, '20230002', 90, 1],
      [3, '20230001', 90, 2],
    ],
  );
});

test('leaderboard exposes distance challenge fields from summary json', () => {
  const entries = buildLeaderboardEntries(
    [
      row({
        id: 5,
        studentId: '20230004',
        studentName: '赵六',
        finalScore: 132.5,
        completed: false,
        lapTimeS: null,
        penaltyPoints: 5,
        createdAt: '2026-06-01T13:00:00.000Z',
        summary: {
          duration_s: 60,
          distance_traveled_m: 137.5,
          distance_points: 137.5,
        },
      }),
    ],
    50,
  );

  assert.equal(entries[0].durationS, 60);
  assert.equal(entries[0].distanceTraveledM, 137.5);
  assert.equal(entries[0].distancePoints, 137.5);
});

test('service inserts a score and reports rank plus best-for-student flag', async () => {
  const executed = [];
  const db = {
    getPool() {
      return {
        async execute(sql, params) {
          executed.push({ params, sql });
          return [{ insertId: 10 }];
        },
        async query() {
          return [
            [
              row({
                id: 10,
                studentId: '20230001',
                studentName: '张三',
                finalScore: 95,
                completed: true,
                lapTimeS: 180,
                penaltyPoints: 1,
                createdAt: '2026-06-01T10:00:00.000Z',
              }),
              row({
                id: 11,
                studentId: '20230002',
                studentName: '李四',
                finalScore: 90,
                completed: true,
                lapTimeS: 190,
                penaltyPoints: 0,
                createdAt: '2026-06-01T11:00:00.000Z',
              }),
            ],
          ];
        },
      };
    },
  };
  const service = createCarlaScoreService({
    config: { carlaScore: { tableName: 'carla_score_submissions' } },
    db,
  });

  const result = await service.submitScore({
    ipAddress: '127.0.0.1',
    studentId: '20230001',
    studentName: '张三',
    summary: {
      completed: true,
      completion_points: 30,
      final_score: 95,
      lap_time_s: 180,
      penalty_breakdown: { speeding: 1 },
      penalty_points: 1,
      protected_settings_checksum: 'abc123',
      raw_score: 95,
      time_points: 40,
    },
  });

  assert.equal(result.submissionId, 10);
  assert.equal(result.rank, 1);
  assert.equal(result.bestForStudent, true);
  assert.equal(executed.length, 1);
  assert.equal(executed[0].params[0], '20230001');
  assert.equal(executed[0].params[1], '张三');
});

test('controller rejects score submissions without the course token', async () => {
  const controller = createCarlaController({
    carlaScoreService: { submitScore: async () => assert.fail('should not submit') },
    config: { carlaScore: { submitToken: 'secret' } },
  });
  const response = {
    body: null,
    statusCode: 200,
    json(payload) {
      this.body = payload;
      return this;
    },
    status(code) {
      this.statusCode = code;
      return this;
    },
  };

  await controller.submitScore(
    {
      body: {},
      get() {
        return '';
      },
      ip: '127.0.0.1',
    },
    response,
    (error) => {
      throw error;
    },
  );

  assert.equal(response.statusCode, 401);
  assert.equal(response.body.ok, false);
});
