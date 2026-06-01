"""Student policy entry point.

Students are expected to improve this file.

The template calls StudentPolicy.run_step(state) every simulation tick.
Return a carla.VehicleControl object to control the ego vehicle.

Do not change fixed scenario settings such as map, route, seed, vehicle
count, walker count, or scoring entry points.
"""

import math


def _clamp(value, low, high):
    return max(low, min(high, value))


def _normalize_angle(angle):
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle


def _distance_xy(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return math.sqrt(dx * dx + dy * dy)


def _sign_or_alternate(value, fallback_index):
    if value > 0.05:
        return 1.0
    if value < -0.05:
        return -1.0
    return 1.0 if fallback_index % 2 == 0 else -1.0


class StudentPolicy:
    """A safer baseline controller.

    It follows the next route target with pure-pursuit style steering,
    slows down for red lights, obstacles, sharp turns and route recovery,
    and uses a small stuck-recovery state machine.

    This is still intentionally understandable starter code. Students can
    improve the controller without touching the fixed scoring logic.
    """

    def __init__(self, carla_module, config):
        self.carla = carla_module
        self.config = config
        self.policy_cfg = config.get("policy", {})
        self._reset_runtime_state()

    def setup(self, world, ego_vehicle, route_points):
        """Called once after the ego vehicle and route are created."""
        self.world = world
        self.ego_vehicle = ego_vehicle
        self.route_points = route_points
        self._reset_runtime_state()

    def _reset_runtime_state(self):
        self._last_motion_location = None
        self._last_motion_progress = 0.0
        self._last_motion_time = None
        self._recovery_reverse_until = 0.0
        self._recovery_forward_until = 0.0
        self._recovery_steer = 0.65
        self._recovery_count = 0
        self.debug_info = {
            "mode": "init",
            "target_speed_kmh": 0.0,
            "heading_error_deg": 0.0,
            "waiting_reason": "none",
        }

    def _control(self, throttle, steer, brake, reverse=False):
        return self.carla.VehicleControl(
            throttle=float(_clamp(throttle, 0.0, 1.0)),
            steer=float(_clamp(steer, -1.0, 1.0)),
            brake=float(_clamp(brake, 0.0, 1.0)),
            hand_brake=False,
            reverse=bool(reverse),
            manual_gear_shift=False,
        )

    def _is_waiting_for_rule(self, state, obstacle_distance):
        if state.get("at_traffic_light") and state.get("traffic_light_state") == "Red":
            return True
        if obstacle_distance is None:
            return False
        stop_distance = float(self.policy_cfg.get("obstacle_stop_distance_m", 7.0))
        return float(obstacle_distance) <= stop_distance

    def _waiting_reason(self, state, obstacle_distance):
        if state.get("at_traffic_light") and state.get("traffic_light_state") == "Red":
            return "red_light"
        if obstacle_distance is not None:
            stop_distance = float(self.policy_cfg.get("obstacle_stop_distance_m", 7.0))
            if float(obstacle_distance) <= stop_distance:
                return "obstacle"
        return "none"

    def _start_recovery(self, sim_time, heading_error):
        reverse_seconds = float(
            self.policy_cfg.get("stuck_recovery_reverse_seconds", 1.6)
        )
        forward_seconds = float(
            self.policy_cfg.get("stuck_recovery_forward_seconds", 1.2)
        )
        steer_strength = float(self.policy_cfg.get("stuck_recovery_steer", 0.75))
        turn_sign = _sign_or_alternate(heading_error, self._recovery_count)
        self._recovery_steer = _clamp(turn_sign * steer_strength, -1.0, 1.0)
        self._recovery_reverse_until = sim_time + reverse_seconds
        self._recovery_forward_until = self._recovery_reverse_until + forward_seconds
        self._recovery_count += 1

    def _recovery_control(self, sim_time):
        if sim_time < self._recovery_reverse_until:
            throttle = float(self.policy_cfg.get("stuck_reverse_throttle", 0.42))
            return self._control(
                throttle=throttle,
                steer=-self._recovery_steer,
                brake=0.0,
                reverse=True,
            )
        if sim_time < self._recovery_forward_until:
            throttle = float(self.policy_cfg.get("stuck_forward_throttle", 0.38))
            return self._control(
                throttle=throttle,
                steer=self._recovery_steer,
                brake=0.0,
                reverse=False,
            )
        return None

    def _set_debug_info(
        self,
        mode,
        target_speed,
        heading_error,
        steer,
        waiting_reason,
        distance_to_route,
        obstacle_distance,
    ):
        self.debug_info = {
            "mode": mode,
            "target_speed_kmh": round(float(target_speed), 3),
            "heading_error_deg": round(math.degrees(float(heading_error)), 3),
            "steer_command": round(float(steer), 3),
            "waiting_reason": waiting_reason,
            "distance_to_route_m": round(float(distance_to_route), 3),
            "obstacle_distance_m": (
                round(float(obstacle_distance), 3)
                if obstacle_distance is not None
                else None
            ),
            "recovery_reverse_remaining_s": round(
                max(0.0, self._recovery_reverse_until), 3
            ),
            "recovery_forward_until_s": round(
                max(0.0, self._recovery_forward_until), 3
            ),
            "recovery_count": self._recovery_count,
        }

    def _has_recent_collision(self, state):
        if not state.get("last_collision_type"):
            return False
        age = state.get("last_collision_age_s")
        if age is None:
            return False
        window = float(self.policy_cfg.get("collision_recovery_window_seconds", 0.6))
        return 0.0 <= float(age) <= window

    def _update_stuck_detector(
        self,
        state,
        ego_location,
        target_speed,
        heading_error,
        waiting_for_rule,
    ):
        sim_time = float(state.get("sim_time_s", 0.0))
        speed = float(state.get("speed_kmh", 0.0))
        route_progress = float(state.get("route_progress", 0.0))

        if self._last_motion_location is None:
            self._last_motion_location = ego_location
            self._last_motion_progress = route_progress
            self._last_motion_time = sim_time
            return

        displacement = _distance_xy(ego_location, self._last_motion_location)
        progress_gain = route_progress - self._last_motion_progress
        displacement_threshold = float(self.policy_cfg.get("stuck_displacement_m", 0.25))
        progress_threshold = float(self.policy_cfg.get("stuck_progress_delta", 0.002))
        moving_speed = float(self.policy_cfg.get("stuck_speed_kmh", 1.0))

        has_moved = (
            speed > moving_speed
            or displacement > displacement_threshold
            or progress_gain > progress_threshold
        )

        if waiting_for_rule or target_speed <= 0.1 or has_moved:
            self._last_motion_location = ego_location
            self._last_motion_progress = route_progress
            self._last_motion_time = sim_time
            return

        stuck_seconds = float(self.policy_cfg.get("stuck_recovery_seconds", 2.5))
        if self._last_motion_time is not None and sim_time - self._last_motion_time >= stuck_seconds:
            self._start_recovery(sim_time, heading_error)
            self._last_motion_time = sim_time

    def run_step(self, state):
        """Return carla.VehicleControl for the current tick."""
        target = state.get("route_target")
        if target is None:
            self._set_debug_info(
                "no_target",
                0.0,
                0.0,
                0.0,
                "none",
                float(state.get("distance_to_route_m", 0.0) or 0.0),
                state.get("nearest_obstacle_distance_m"),
            )
            return self._control(throttle=0.0, brake=1.0, steer=0.0)

        ego_transform = state["ego_transform"]
        ego_location = ego_transform.location
        yaw = math.radians(ego_transform.rotation.yaw)
        sim_time = float(state.get("sim_time_s", 0.0))

        dx = target.x - ego_location.x
        dy = target.y - ego_location.y
        target_angle = math.atan2(dy, dx)
        heading_error = _normalize_angle(target_angle - yaw)

        distance_to_route = float(state.get("distance_to_route_m", 0.0) or 0.0)
        off_route_threshold = float(
            self.policy_cfg.get("off_route_rejoin_distance_m", 12.0)
        )
        steer_divisor = 0.62 if distance_to_route > off_route_threshold else 0.75
        steer = _clamp(heading_error / steer_divisor, -1.0, 1.0)

        target_speed = float(self.policy_cfg.get("target_speed_kmh", 35.0))
        speed_limit = float(state.get("speed_limit_kmh") or 30.0)
        speed_limit_ratio = float(self.policy_cfg.get("speed_limit_ratio", 0.92))
        target_speed = min(target_speed, max(8.0, speed_limit * speed_limit_ratio))

        abs_heading = abs(heading_error)
        if abs_heading > 1.25:
            target_speed = min(
                target_speed,
                float(self.policy_cfg.get("hard_turn_speed_kmh", 10.0)),
            )
        elif abs_heading > 0.75:
            target_speed = min(
                target_speed,
                float(self.policy_cfg.get("sharp_turn_speed_kmh", 15.0)),
            )
        elif abs_heading > 0.45:
            target_speed = min(
                target_speed,
                float(self.policy_cfg.get("curve_speed_kmh", 22.0)),
            )

        if distance_to_route > off_route_threshold:
            target_speed = min(
                target_speed,
                float(self.policy_cfg.get("off_route_speed_kmh", 12.0)),
            )

        if state.get("at_traffic_light") and state.get("traffic_light_state") == "Red":
            target_speed = min(target_speed, 0.0)

        obstacle_distance = state.get("nearest_obstacle_distance_m")
        if obstacle_distance is not None:
            slow_distance = float(
                self.policy_cfg.get("obstacle_slow_distance_m", 14.0)
            )
            stop_distance = float(
                self.policy_cfg.get("obstacle_stop_distance_m", 7.0)
            )
            if obstacle_distance <= stop_distance:
                target_speed = 0.0
            elif obstacle_distance <= slow_distance:
                target_speed = min(
                    target_speed,
                    float(self.policy_cfg.get("obstacle_slow_speed_kmh", 10.0)),
                )

        waiting_reason = self._waiting_reason(state, obstacle_distance)
        waiting_for_rule = waiting_reason != "none"
        if waiting_for_rule:
            self._recovery_reverse_until = 0.0
            self._recovery_forward_until = 0.0
        else:
            if (
                self._has_recent_collision(state)
                and sim_time >= self._recovery_forward_until
            ):
                self._start_recovery(sim_time, heading_error)
            recovery = self._recovery_control(sim_time)
            if recovery is not None:
                mode = "recovery_reverse" if recovery.reverse else "recovery_forward"
                self._set_debug_info(
                    mode,
                    target_speed,
                    heading_error,
                    recovery.steer,
                    waiting_reason,
                    distance_to_route,
                    obstacle_distance,
                )
                return recovery

        self._update_stuck_detector(
            state,
            ego_location,
            target_speed,
            heading_error,
            waiting_for_rule,
        )
        recovery = self._recovery_control(sim_time)
        if recovery is not None:
            mode = "recovery_reverse" if recovery.reverse else "recovery_forward"
            self._set_debug_info(
                mode,
                target_speed,
                heading_error,
                recovery.steer,
                waiting_reason,
                distance_to_route,
                obstacle_distance,
            )
            return recovery

        speed = state["speed_kmh"]
        error = target_speed - speed

        if target_speed <= 0.1:
            throttle = 0.0
            brake = 1.0 if speed > 0.5 else 0.5
        elif error > 1.0:
            max_throttle = float(self.policy_cfg.get("max_throttle", 0.62))
            throttle = _clamp(0.22 + error / 48.0, 0.0, max_throttle)
            brake = 0.0
        elif error < -1.5:
            throttle = 0.0
            brake = _clamp((-error) / 25.0, 0.08, 0.9)
        else:
            throttle = 0.14
            brake = 0.0

        if waiting_reason == "red_light":
            mode = "stopped_red_light"
        elif waiting_reason == "obstacle":
            mode = "stopped_obstacle"
        elif distance_to_route > off_route_threshold:
            mode = "off_route_rejoin"
        else:
            mode = "normal"

        control = self._control(
            throttle=throttle,
            steer=steer,
            brake=brake,
            reverse=False,
        )
        self._set_debug_info(
            mode,
            target_speed,
            heading_error,
            steer,
            waiting_reason,
            distance_to_route,
            obstacle_distance,
        )
        return control
