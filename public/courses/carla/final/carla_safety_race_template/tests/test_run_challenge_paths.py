from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
import tempfile
import types
import unittest
from urllib.error import URLError
from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = TEMPLATE_ROOT / "src"


def load_run_challenge_module():
    carla_stub = types.ModuleType("carla")
    carla_stub.TrafficLightState = types.SimpleNamespace(
        Red=object(),
        Yellow=object(),
        Green=object(),
        Off=object(),
    )
    carla_stub.LaneType = types.SimpleNamespace(Driving=object())

    policy_stub = types.ModuleType("student_policy")

    class StudentPolicy:
        pass

    policy_stub.StudentPolicy = StudentPolicy

    previous_carla = sys.modules.get("carla")
    previous_policy = sys.modules.get("student_policy")
    sys.modules["carla"] = carla_stub
    sys.modules["student_policy"] = policy_stub

    try:
        spec = importlib.util.spec_from_file_location(
            "run_challenge_under_test",
            SRC_DIR / "run_challenge.py",
        )
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module
    finally:
        if previous_carla is None:
            sys.modules.pop("carla", None)
        else:
            sys.modules["carla"] = previous_carla

        if previous_policy is None:
            sys.modules.pop("student_policy", None)
        else:
            sys.modules["student_policy"] = previous_policy


class RunChallengePathTests(unittest.TestCase):
    def test_default_config_resolves_from_template_root_when_cwd_is_elsewhere(self):
        module = load_run_challenge_module()
        previous_cwd = Path.cwd()

        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            try:
                config = module.load_config("config/default_config.json")
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(config["map_name"], "Town05")
        self.assertEqual(config["output"]["root"], "output")

    def test_relative_output_root_resolves_from_template_root_when_cwd_is_elsewhere(self):
        module = load_run_challenge_module()
        previous_cwd = Path.cwd()
        output_parent = TEMPLATE_ROOT / "output"

        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            try:
                output_dir = module.make_output_dir("output")
            finally:
                os.chdir(previous_cwd)

        try:
            self.assertEqual(output_dir.parent, output_parent)
            self.assertTrue(output_dir.exists())
        finally:
            shutil.rmtree(output_dir, ignore_errors=True)
            try:
                output_parent.rmdir()
            except OSError:
                pass

    def test_student_identity_helper_trims_and_writes_config(self):
        module = load_run_challenge_module()
        config = {}

        updated = module.apply_student_identity(config, " 20230001 ", " 张三 ")

        self.assertTrue(updated)
        self.assertEqual(config["student"]["student_id"], "20230001")
        self.assertEqual(config["student"]["student_name"], "张三")

    def test_student_identity_helper_rejects_incomplete_identity(self):
        module = load_run_challenge_module()
        config = {"student": {"student_id": "old", "student_name": "旧姓名"}}

        updated = module.apply_student_identity(config, "20230001", " ")

        self.assertFalse(updated)
        self.assertEqual(config["student"]["student_id"], "old")
        self.assertEqual(config["student"]["student_name"], "旧姓名")


class RunChallengeScoringTests(unittest.TestCase):
    def test_distance_score_uses_one_point_per_meter_and_penalties(self):
        module = load_run_challenge_module()
        runner = module.ChallengeRunner.__new__(module.ChallengeRunner)
        runner.config = {
            "scoring": {
                "duration_seconds": 60.0,
                "distance_points_per_meter": 1.0,
            },
            "rules": {"pedestrian_collision_score_cap": None},
        }
        runner.completed = False
        runner.lap_time = None
        runner.distance_traveled_m = 123.456
        runner.event_recorder = types.SimpleNamespace(
            penalty_sum=lambda: 7,
            penalty_totals={"speeding": 3, "off_route": 4},
            has_pedestrian_collision=False,
        )

        summary = runner.compute_score(elapsed=60.0)

        self.assertFalse(summary["completed"])
        self.assertEqual(summary["duration_s"], 60.0)
        self.assertEqual(summary["lap_time_s"], None)
        self.assertEqual(summary["distance_traveled_m"], 123.456)
        self.assertEqual(summary["distance_points"], 123.46)
        self.assertEqual(summary["completion_points"], 0)
        self.assertEqual(summary["time_points"], 0)
        self.assertEqual(summary["penalty_points"], 7)
        self.assertEqual(summary["raw_score"], 116.46)
        self.assertEqual(summary["final_score"], 116.46)

    def test_distance_progress_uses_route_forward_distance(self):
        module = load_run_challenge_module()
        runner = module.ChallengeRunner.__new__(module.ChallengeRunner)
        runner.distance_traveled_m = 0.0
        runner._last_distance_location = None
        runner.route_cumulative_distances = [0.0, 10.0, 25.5]
        location = types.SimpleNamespace(x=0.0, y=0.0, z=0.0)

        runner.update_distance_traveled(location, route_index=1)
        runner.update_distance_traveled(location, route_index=0)
        runner.update_distance_traveled(location, route_index=2)

        self.assertEqual(runner.distance_traveled_m, 25.5)


class RunChallengeRenderTests(unittest.TestCase):
    def test_render_config_defaults_to_enabled_window(self):
        module = load_run_challenge_module()

        render_config = module.normalize_render_config({})

        self.assertTrue(render_config["enabled"])
        self.assertEqual(render_config["width"], 1280)
        self.assertEqual(render_config["height"], 720)
        self.assertEqual(render_config["camera_fov"], 90.0)
        self.assertEqual(render_config["camera_x"], -7.0)
        self.assertEqual(render_config["camera_z"], 3.0)

    def test_hud_lines_include_runtime_safety_data(self):
        module = load_run_challenge_module()

        lines = module.build_hud_lines(
            {
                "frame": 123,
                "sim_time_s": 4.5,
                "speed_kmh": 32.1,
                "speed_limit_kmh": 50.0,
                "checkpoint_index": 4,
                "checkpoint_count": 16,
                "route_index": 80,
                "route_progress": 0.625,
                "distance_to_route_m": 1.75,
                "route_target_index": 8,
                "traffic_light_state": "Red",
                "nearest_obstacle_distance_m": 8.25,
                "distance_traveled_m": 42.75,
                "distance_points": 42.75,
                "last_collision_type": "collision_static",
                "last_collision_age_s": 0.3,
                "control_throttle": 0.42,
                "control_brake": 0.0,
                "control_steer": -0.25,
                "control_reverse": True,
                "policy_debug": {
                    "mode": "recovery_reverse",
                    "target_speed_kmh": 10.0,
                    "heading_error_deg": -18.5,
                    "waiting_reason": "none",
                },
                "penalty_points": 7,
                "event_count": 2,
                "output_dir": "output/run",
            }
        )
        joined = "\n".join(lines)

        self.assertIn("CARLA 安全竞速调试面板", joined)
        self.assertIn("速度/限速: 32.1 / 50.0 km/h", joined)
        self.assertIn("检查点: 4/16", joined)
        self.assertIn("路线进度: 62.5%", joined)
        self.assertIn("路线偏移: 1.8 m", joined)
        self.assertIn("行驶距离: 42.8 m", joined)
        self.assertIn("当前距离分: 42.75", joined)
        self.assertIn("目标点索引: 8", joined)
        self.assertIn("红绿灯: 红灯", joined)
        self.assertIn("最近障碍: 8.2 m", joined)
        self.assertIn("最近碰撞: 静态物体 0.3s 前", joined)
        self.assertIn("策略模式: 脱困倒车", joined)
        self.assertIn("目标速度: 10.0 km/h", joined)
        self.assertIn("航向误差: -18.5 deg", joined)
        self.assertIn("控制: 油门 0.42 刹车 0.00 转向 -0.25 倒车 是", joined)
        self.assertIn("累计扣分: 7", joined)
        self.assertIn("事件数量: 2", joined)

    def test_score_screen_lines_include_report_ready_breakdown(self):
        module = load_run_challenge_module()

        lines = module.build_score_screen_lines(
            {
                "completed": False,
                "duration_s": 60.0,
                "lap_time_s": None,
                "distance_traveled_m": 123.456,
                "distance_points": 123.46,
                "protected_settings_checksum": "abc123def456",
                "completion_points": 0,
                "time_points": 0,
                "penalty_points": 12,
                "raw_score": 111.46,
                "final_score": 111.46,
                "penalty_breakdown": {
                    "collision_static": 5,
                    "red_light": 5,
                    "lane_invasion": 2,
                },
            },
            TEMPLATE_ROOT / "output" / "run",
        )
        joined = "\n".join(lines)

        self.assertIn("CARLA 期末距离挑战成绩报告", joined)
        self.assertIn("计时窗口: 60.000 s", joined)
        self.assertIn("行驶距离: 123.456 m", joined)
        self.assertIn("距离分: 123.46", joined)
        self.assertIn("最终成绩: 111.46", joined)
        self.assertIn("扣分合计: 12", joined)
        self.assertIn("原始分: 111.46", joined)
        self.assertIn("评分公式: 距离分 - 扣分合计 = 最终成绩", joined)
        self.assertIn("固定设置校验: abc123def456", joined)
        self.assertIn("静态物体碰撞: 5", joined)
        self.assertIn("闯红灯: 5", joined)
        self.assertIn("车道入侵/压线: 2", joined)
        self.assertIn("lap_summary.json / events.csv / trajectory.csv / score_report.md", joined)
        self.assertIn("按 Esc 键或关闭窗口结束截图页", joined)

    def test_scoring_standard_lines_include_startup_rules(self):
        module = load_run_challenge_module()

        lines = module.build_scoring_standard_lines(
            {
                "scoring": {
                    "duration_seconds": 60.0,
                    "distance_points_per_meter": 1.0,
                    "penalties": {
                        "collision_pedestrian": 15,
                        "collision_vehicle": 10,
                        "collision_static": 5,
                        "red_light": 5,
                        "off_route": 5,
                        "lane_invasion": 2,
                        "speeding": 3,
                        "stuck": 5,
                    },
                },
                "rules": {
                    "max_lane_invasion_penalty": 10,
                    "max_speeding_penalty": 15,
                    "pedestrian_collision_score_cap": 60,
                },
            }
        )
        joined = "\n".join(lines)

        self.assertIn("CARLA 期末距离挑战评分标准", joined)
        self.assertIn("计时窗口: 60.000 s", joined)
        self.assertIn("距离分: 1 m = 1 分", joined)
        self.assertIn("总分构成: 距离分 - 扣分合计", joined)
        self.assertIn("行人碰撞: 每次扣 15 分", joined)
        self.assertIn("车道入侵/压线: 每次扣 2 分，最多扣 10 分", joined)
        self.assertIn("超速: 每次扣 3 分，最多扣 15 分", joined)
        self.assertIn("行人碰撞后最高分: 60", joined)
        self.assertIn("按 Enter 或 Space 开始", joined)

    def test_final_score_screen_only_closes_on_escape_or_window_close(self):
        module = load_run_challenge_module()
        pygame = types.SimpleNamespace(
            QUIT=1,
            KEYDOWN=2,
            MOUSEBUTTONDOWN=3,
            K_ESCAPE=27,
            K_q=113,
        )

        self.assertTrue(
            module.is_score_report_close_event(
                pygame,
                types.SimpleNamespace(type=pygame.QUIT),
            )
        )
        self.assertTrue(
            module.is_score_report_close_event(
                pygame,
                types.SimpleNamespace(type=pygame.KEYDOWN, key=pygame.K_ESCAPE),
            )
        )
        self.assertFalse(
            module.is_score_report_close_event(
                pygame,
                types.SimpleNamespace(type=pygame.KEYDOWN, key=pygame.K_q),
            )
        )
        self.assertFalse(
            module.is_score_report_close_event(
                pygame,
                types.SimpleNamespace(type=pygame.MOUSEBUTTONDOWN),
            )
        )


class LeaderboardSubmissionTests(unittest.TestCase):
    def test_leaderboard_payload_uses_student_config_and_summary(self):
        module = load_run_challenge_module()
        summary = {
            "completed": True,
            "final_score": 88.5,
            "lap_time_s": 191.2,
        }

        payload = module.build_leaderboard_payload(
            {
                "student": {
                    "student_id": " 20230001 ",
                    "student_name": " 张三 ",
                }
            },
            summary,
        )

        self.assertEqual(payload["studentId"], "20230001")
        self.assertEqual(payload["studentName"], "张三")
        self.assertIs(payload["summary"], summary)

    def test_leaderboard_payload_skips_missing_student_identity(self):
        module = load_run_challenge_module()

        payload = module.build_leaderboard_payload(
            {"student": {"student_id": "", "student_name": "张三"}},
            {"final_score": 80},
        )

        self.assertIsNone(payload)

    def test_config_output_redacts_leaderboard_token(self):
        module = load_run_challenge_module()

        sanitized = module.sanitize_config_for_output(
            {
                "leaderboard": {
                    "enabled": True,
                    "submit_url": "http://example.test/api/carla/scores",
                    "submit_token": "secret-token",
                }
            }
        )

        self.assertEqual(sanitized["leaderboard"]["submit_token"], "***redacted***")

    def test_leaderboard_submit_failure_returns_status_without_raising(self):
        module = load_run_challenge_module()

        def failing_urlopen(_request, timeout=None):
            raise URLError("connection refused")

        result = module.submit_leaderboard_score(
            {
                "student": {
                    "student_id": "20230001",
                    "student_name": "张三",
                },
                "leaderboard": {
                    "enabled": True,
                    "submit_url": "http://example.test/api/carla/scores",
                    "submit_token": "secret-token",
                    "timeout_seconds": 0.1,
                },
            },
            {"final_score": 80},
            urlopen_func=failing_urlopen,
        )

        self.assertEqual(result["status"], "failed")
        self.assertIn("connection refused", result["message"])

    def test_leaderboard_submit_success_returns_rank(self):
        module = load_run_challenge_module()
        captured = {}

        class FakeResponse:
            status = 201

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                return False

            def getcode(self):
                return self.status

            def read(self):
                return (
                    b'{"ok":true,"data":{"submissionId":12,'
                    b'"rank":3,"bestForStudent":true}}'
                )

        def fake_urlopen(request, timeout=None):
            captured["timeout"] = timeout
            captured["url"] = request.full_url
            captured["method"] = request.get_method()
            captured["token"] = request.get_header("X-carla-submit-token")
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse()

        result = module.submit_leaderboard_score(
            {
                "student": {
                    "student_id": "20230001",
                    "student_name": "张三",
                },
                "leaderboard": {
                    "enabled": True,
                    "submit_url": "http://example.test/api/carla/scores",
                    "submit_token": "secret-token",
                    "timeout_seconds": 0.1,
                },
            },
            {
                "completed": False,
                "duration_s": 60,
                "lap_time_s": None,
                "distance_traveled_m": 137.5,
                "distance_points": 137.5,
                "completion_points": 0,
                "time_points": 0,
                "penalty_points": 5,
                "raw_score": 132.5,
                "final_score": 132.5,
                "protected_settings_checksum": "abc123",
                "penalty_breakdown": {"lane_invasion": 5},
            },
            urlopen_func=fake_urlopen,
        )

        self.assertEqual(captured["method"], "POST")
        self.assertEqual(captured["token"], "secret-token")
        self.assertEqual(captured["body"]["studentId"], "20230001")
        self.assertEqual(captured["body"]["summary"]["final_score"], 132.5)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["rank"], 3)
        self.assertEqual(result["submission_id"], 12)


class EventRecorderTests(unittest.TestCase):
    def test_collision_events_use_cooldown(self):
        module = load_run_challenge_module()
        recorder = module.EventRecorder(
            {
                "rules": {"event_cooldown_seconds": 2.0},
                "scoring": {"penalties": {}},
            }
        )

        actor = types.SimpleNamespace(
            get_location=lambda: types.SimpleNamespace(x=1.0, y=2.0, z=3.0),
            get_velocity=lambda: types.SimpleNamespace(x=0.0, y=0.0, z=0.0),
        )

        first = recorder.add_collision(
            "collision_static",
            10.0,
            100,
            actor,
            0.25,
            5,
            "other_actor=static.fence",
        )
        second = recorder.add_collision(
            "collision_static",
            10.1,
            101,
            actor,
            0.25,
            5,
            "other_actor=static.fence",
        )

        self.assertTrue(first)
        self.assertFalse(second)
        self.assertEqual(len(recorder.rows), 1)


class RoutePlannerFallbackTests(unittest.TestCase):
    def test_waypoint_fallback_traces_connected_next_waypoints(self):
        module = load_run_challenge_module()

        class Location:
            def __init__(self, x, y=0.0, z=0.0):
                self.x = x
                self.y = y
                self.z = z

        class Transform:
            def __init__(self, location):
                self.location = location

        class Waypoint:
            def __init__(self, name, x):
                self.name = name
                self.transform = Transform(Location(x))
                self.road_id = 1
                self.section_id = 0
                self.lane_id = 1
                self.s = float(x)
                self.lane_type = module.carla.LaneType.Driving
                self._next = []

            def next(self, _distance):
                return self._next

        start = Waypoint("start", 0.0)
        middle = Waypoint("middle", 10.0)
        end = Waypoint("end", 20.0)
        start._next = [middle]
        middle._next = [end]

        class FakeMap:
            def get_waypoint(self, location, **_kwargs):
                return start if location.x < 10.0 else end

        route = module.trace_route_with_waypoints(
            FakeMap(),
            Location(0.0),
            Location(20.0),
            10.0,
        )

        self.assertEqual([round(point.x) for point in route], [0, 10, 20])


if __name__ == "__main__":
    unittest.main()
