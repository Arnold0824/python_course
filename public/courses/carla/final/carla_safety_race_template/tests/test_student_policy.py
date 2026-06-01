from __future__ import annotations

import importlib.util
import types
import unittest
from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = TEMPLATE_ROOT / "src"


class FakeVehicleControl:
    def __init__(
        self,
        throttle=0.0,
        steer=0.0,
        brake=0.0,
        hand_brake=False,
        reverse=False,
        manual_gear_shift=False,
    ):
        self.throttle = throttle
        self.steer = steer
        self.brake = brake
        self.hand_brake = hand_brake
        self.reverse = reverse
        self.manual_gear_shift = manual_gear_shift


class Location:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z


class Rotation:
    def __init__(self, yaw=0.0):
        self.yaw = yaw


class Transform:
    def __init__(self, location=None, rotation=None):
        self.location = location or Location()
        self.rotation = rotation or Rotation()


def load_student_policy_module():
    spec = importlib.util.spec_from_file_location(
        "student_policy_under_test",
        SRC_DIR / "student_policy.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_policy(config=None):
    module = load_student_policy_module()
    carla = types.SimpleNamespace(VehicleControl=FakeVehicleControl)
    policy = module.StudentPolicy(carla, config or {"policy": {}})
    policy.setup(None, None, [])
    return policy


def make_state(
    sim_time,
    location=None,
    target=None,
    speed_kmh=0.0,
    route_progress=0.0,
    route_target_index=1,
    traffic_light_state="Green",
    obstacle_distance=None,
    distance_to_route_m=0.0,
):
    return {
        "frame": int(sim_time / 0.05),
        "sim_time_s": sim_time,
        "ego_transform": Transform(location or Location(), Rotation(yaw=0.0)),
        "speed_kmh": speed_kmh,
        "speed_limit_kmh": 50.0,
        "route_target": target or Location(30.0, 8.0, 0.0),
        "route_target_index": route_target_index,
        "route_progress": route_progress,
        "distance_to_route_m": distance_to_route_m,
        "at_traffic_light": traffic_light_state == "Red",
        "traffic_light_state": traffic_light_state,
        "nearest_obstacle_distance_m": obstacle_distance,
    }


class StudentPolicyRecoveryTests(unittest.TestCase):
    def test_normal_step_exposes_debug_info_for_hud(self):
        policy = make_policy({"policy": {"target_speed_kmh": 35.0}})

        control = policy.run_step(
            make_state(
                0.0,
                location=Location(0.0, 0.0),
                target=Location(30.0, 0.0, 0.0),
                speed_kmh=10.0,
                distance_to_route_m=0.5,
            )
        )

        self.assertFalse(control.reverse)
        self.assertEqual(policy.debug_info["mode"], "normal")
        self.assertGreater(policy.debug_info["target_speed_kmh"], 0.0)
        self.assertAlmostEqual(policy.debug_info["heading_error_deg"], 0.0)
        self.assertIn("waiting_reason", policy.debug_info)

    def test_reverses_with_steering_after_being_stuck_without_wait_reason(self):
        policy = make_policy(
            {
                "policy": {
                    "stuck_recovery_seconds": 1.0,
                    "stuck_recovery_reverse_seconds": 1.2,
                    "stuck_displacement_m": 0.15,
                }
            }
        )

        for sim_time in (0.0, 0.4, 0.8, 1.2):
            control = policy.run_step(make_state(sim_time, location=Location(0.0, 0.0)))

        self.assertTrue(control.reverse)
        self.assertGreater(control.throttle, 0.0)
        self.assertEqual(control.brake, 0.0)
        self.assertNotEqual(control.steer, 0.0)

    def test_red_light_stop_does_not_trigger_reverse_recovery(self):
        policy = make_policy({"policy": {"stuck_recovery_seconds": 1.0}})

        for sim_time in (0.0, 0.4, 0.8, 1.2, 1.6):
            control = policy.run_step(
                make_state(
                    sim_time,
                    location=Location(0.0, 0.0),
                    traffic_light_state="Red",
                )
            )

        self.assertFalse(control.reverse)
        self.assertEqual(control.throttle, 0.0)
        self.assertGreater(control.brake, 0.0)

    def test_far_off_route_uses_low_rejoin_speed(self):
        policy = make_policy({"policy": {"off_route_speed_kmh": 10.0}})

        control = policy.run_step(
            make_state(
                0.0,
                location=Location(0.0, 0.0),
                target=Location(30.0, 30.0, 0.0),
                speed_kmh=32.0,
                distance_to_route_m=25.0,
            )
        )

        self.assertEqual(control.throttle, 0.0)
        self.assertGreater(control.brake, 0.7)
        self.assertNotEqual(control.steer, 0.0)

    def test_recent_collision_triggers_immediate_reverse_recovery(self):
        policy = make_policy(
            {
                "policy": {
                    "collision_recovery_window_seconds": 0.6,
                    "stuck_recovery_reverse_seconds": 1.2,
                }
            }
        )

        control = policy.run_step(
            make_state(
                3.0,
                location=Location(-262.5, -25.6),
                target=Location(-260.0, -35.0, 0.0),
                speed_kmh=0.2,
            )
            | {
                "last_collision_type": "collision_static",
                "last_collision_age_s": 0.1,
            }
        )

        self.assertTrue(control.reverse)
        self.assertGreater(control.throttle, 0.0)
        self.assertEqual(control.brake, 0.0)


if __name__ == "__main__":
    unittest.main()
