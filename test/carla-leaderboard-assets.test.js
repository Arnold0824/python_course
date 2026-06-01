import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import path from 'node:path';

const rootDir = path.resolve(import.meta.dirname, '..');
const leaderboardViewPath = path.join(
  rootDir,
  'src/courses/carla/views/CarlaLeaderboardView.vue',
);
const carlaTemplateConfigPath = path.join(
  rootDir,
  'public/courses/carla/final/carla_safety_race_template/config/default_config.json',
);
const serverEnvPath = path.join(rootDir, 'server/systemd/python-course-server.env');
const courseSubmitToken = 'carla-final-2026-submit-token';
const courseSubmitUrl = 'https://niuniulab.com/api/carla/scores';

test('CARLA leaderboard exposes final report template and code package downloads', () => {
  const viewSource = fs.readFileSync(leaderboardViewPath, 'utf8');
  const expectedAssets = [
    {
      href: '/courses/carla/final/2%20%E5%AE%9E%E8%AE%AD%E8%AF%BE%E7%A8%8B%E6%8A%A5%E5%91%8A-%E5%AD%A6%E5%8F%B7%E5%A7%93%E5%90%8D-%E8%AF%BE%E7%A8%8B%E8%AE%BE%E8%AE%A1%E9%A1%B9%E7%9B%AE%E5%90%8D%E7%A7%B0-%E4%B8%AA%E4%BA%BA.docx',
      localPath: 'public/courses/carla/final/2 实训课程报告-学号姓名-课程设计项目名称-个人.docx',
      label: '实训报告模板',
    },
    {
      href: '/courses/carla/final/carla_safety_race_template.zip',
      localPath: 'public/courses/carla/final/carla_safety_race_template.zip',
      label: '代码包',
    },
    {
      href: 'https://f.wps.cn/g/zjfA9ogS/',
      label: 'WPS 提交',
    },
  ];

  for (const asset of expectedAssets) {
    assert.match(viewSource, new RegExp(asset.href.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
    assert.match(viewSource, new RegExp(asset.label));
    if (asset.localPath) {
      assert.equal(fs.existsSync(path.join(rootDir, asset.localPath)), true);
    }
  }
});

test('CARLA template submits scores by default with the configured course token', () => {
  const config = JSON.parse(fs.readFileSync(carlaTemplateConfigPath, 'utf8'));
  const serverEnv = fs.readFileSync(serverEnvPath, 'utf8');

  assert.equal(config.leaderboard.enabled, true);
  assert.equal(config.leaderboard.submit_token, courseSubmitToken);
  assert.equal(config.leaderboard.submit_url, courseSubmitUrl);
  assert.match(serverEnv, new RegExp(`^CARLA_SCORE_SUBMIT_TOKEN=${courseSubmitToken}$`, 'm'));
});

test('CARLA leaderboard page explains the final project task and rubric', () => {
  const viewSource = fs.readFileSync(leaderboardViewPath, 'utf8');
  const expectedText = [
    '基于 CARLA 的自动驾驶安全竞速挑战',
    '主要修改 `src/student_policy.py`',
    '60 秒',
    '1 m = 1 分',
    '至少两次有效运行',
    '不得修改固定地图、路线、车辆和行人数量',
    '系统功能设计与实现',
    '40 分',
    '工程规范与模板扩展',
    '30 分',
    '报告与数据分析质量',
    '20 分',
    '展示答辩与个人说明',
    '10 分',
    'timeZone: "Asia/Shanghai"',
  ];

  for (const text of expectedText) {
    assert.match(viewSource, new RegExp(text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  }
});
