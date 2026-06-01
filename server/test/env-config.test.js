import assert from 'node:assert/strict';
import test from 'node:test';
import { loadConfig } from '../src/config/env.js';

test('CARLA score submit token has a course default when env is not configured', () => {
  const originalToken = process.env.CARLA_SCORE_SUBMIT_TOKEN;
  delete process.env.CARLA_SCORE_SUBMIT_TOKEN;

  try {
    const config = loadConfig();
    assert.equal(config.carlaScore.submitToken, 'carla-final-2026-submit-token');
  } finally {
    if (originalToken === undefined) {
      delete process.env.CARLA_SCORE_SUBMIT_TOKEN;
    } else {
      process.env.CARLA_SCORE_SUBMIT_TOKEN = originalToken;
    }
  }
});

test('CARLA score submit token env value overrides the course default', () => {
  const originalToken = process.env.CARLA_SCORE_SUBMIT_TOKEN;
  process.env.CARLA_SCORE_SUBMIT_TOKEN = 'custom-token';

  try {
    const config = loadConfig();
    assert.equal(config.carlaScore.submitToken, 'custom-token');
  } finally {
    if (originalToken === undefined) {
      delete process.env.CARLA_SCORE_SUBMIT_TOKEN;
    } else {
      process.env.CARLA_SCORE_SUBMIT_TOKEN = originalToken;
    }
  }
});
