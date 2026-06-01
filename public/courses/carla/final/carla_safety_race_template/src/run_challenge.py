"""CARLA fixed-scene safety race starter template.

This script provides the teacher-controlled baseline environment:

- fixed map
- fixed random seed
- fixed vehicle and walker counts
- synchronous mode
- outer-loop route generation
- basic event logging and scoring

Students should primarily edit student_policy.py.
"""

from __future__ import annotations

import argparse
import copy
import csv
import datetime as dt
import heapq
import hashlib
import importlib
import json
import math
import os
import random
import sys
import urllib.error
import urllib.request
from pathlib import Path
from types import SimpleNamespace


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_ROOT = SCRIPT_DIR.parent


def add_carla_paths():
    api_root = os.environ.get("CARLA_PYTHONAPI")
    if api_root:
        sys.path.insert(0, api_root)
        sys.path.insert(0, str(Path(api_root).parent))

    # Common CARLA source tree layout.
    candidates = [
        Path.cwd() / "PythonAPI" / "carla",
        Path.cwd().parent / "PythonAPI" / "carla",
    ]
    for candidate in candidates:
        if candidate.exists():
            sys.path.insert(0, str(candidate))
            sys.path.insert(0, str(candidate.parent))


add_carla_paths()

try:
    import carla  # type: ignore
except ImportError as exc:
    raise SystemExit(
        "Could not import carla. Start from a CARLA Python environment or "
        "set CARLA_PYTHONAPI to the PythonAPI/carla directory."
    ) from exc

from student_policy import StudentPolicy


def speed_kmh(actor):
    velocity = actor.get_velocity()
    return 3.6 * math.sqrt(
        velocity.x * velocity.x
        + velocity.y * velocity.y
        + velocity.z * velocity.z
    )


def distance(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def location_dict(location):
    return {
        "x": round(location.x, 3),
        "y": round(location.y, 3),
        "z": round(location.z, 3),
    }


def copy_location(location):
    return SimpleNamespace(
        x=float(location.x),
        y=float(location.y),
        z=float(location.z),
    )


def actor_kind(actor):
    type_id = getattr(actor, "type_id", "")
    if type_id.startswith("walker.pedestrian"):
        return "pedestrian"
    if type_id.startswith("vehicle."):
        return "vehicle"
    return "static"


def light_state_label(state):
    if state == carla.TrafficLightState.Red:
        return "Red"
    if state == carla.TrafficLightState.Yellow:
        return "Yellow"
    if state == carla.TrafficLightState.Green:
        return "Green"
    if state == carla.TrafficLightState.Off:
        return "Off"
    return "Unknown"


def resolve_template_path(path):
    candidate = Path(path)
    if candidate.is_absolute() or candidate.exists():
        return candidate
    return TEMPLATE_ROOT / candidate


def load_config(path):
    config_path = resolve_template_path(path)
    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def apply_student_identity(config, student_id, student_name):
    normalized_id = str(student_id or "").strip()
    normalized_name = str(student_name or "").strip()
    if not normalized_id or not normalized_name:
        return False
    student = config.setdefault("student", {})
    student["student_id"] = normalized_id
    student["student_name"] = normalized_name
    return True


def has_student_identity(config):
    student = config.get("student", {})
    return bool(
        str(student.get("student_id", "")).strip()
        and str(student.get("student_name", "")).strip()
    )


def prompt_student_identity_console(config, reason=None):
    if reason:
        print(f"无法打开身份信息弹窗: {reason}")
    if not getattr(sys.stdin, "isatty", lambda: False)():
        if not has_student_identity(config):
            print("未检测到可交互终端，且学号/姓名为空；排行榜提交会跳过。")
        return has_student_identity(config)

    student = config.get("student", {})
    current_id = str(student.get("student_id", "")).strip()
    current_name = str(student.get("student_name", "")).strip()
    print("\n请输入本次期末作业身份信息。直接回车可保留已有配置。")
    try:
        student_id = input(f"学号 [{current_id}]: ").strip() or current_id
        student_name = input(f"姓名 [{current_name}]: ").strip() or current_name
    except (EOFError, KeyboardInterrupt):
        print("\n身份信息输入已取消。")
        return has_student_identity(config)

    if apply_student_identity(config, student_id, student_name):
        print(f"本次成绩身份: {student_id} {student_name}")
        return True

    print("学号或姓名为空，本次排行榜提交会跳过。")
    return False


def prompt_student_identity(config):
    student = config.get("student", {})
    current_id = str(student.get("student_id", "")).strip()
    current_name = str(student.get("student_name", "")).strip()

    try:
        import tkinter as tk
        from tkinter import messagebox
    except Exception as exc:
        return prompt_student_identity_console(config, exc)

    submitted = {"value": False}

    try:
        root = tk.Tk()
        root.title("CARLA 期末作业身份信息")
        root.resizable(False, False)
        try:
            root.attributes("-topmost", True)
        except tk.TclError:
            pass

        student_id_var = tk.StringVar(value=current_id)
        student_name_var = tk.StringVar(value=current_name)

        frame = tk.Frame(root, padx=18, pady=16)
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(
            frame,
            text="请先输入学号和姓名，成绩报告和排行榜都会使用该信息。",
            anchor="w",
            justify="left",
            wraplength=360,
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        tk.Label(frame, text="学号").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=6)
        id_entry = tk.Entry(frame, textvariable=student_id_var, width=30)
        id_entry.grid(row=1, column=1, sticky="ew", pady=6)
        tk.Label(frame, text="姓名").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=6)
        name_entry = tk.Entry(frame, textvariable=student_name_var, width=30)
        name_entry.grid(row=2, column=1, sticky="ew", pady=6)

        button_frame = tk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="e", pady=(14, 0))

        def submit():
            if apply_student_identity(
                config,
                student_id_var.get(),
                student_name_var.get(),
            ):
                submitted["value"] = True
                root.destroy()
                return
            messagebox.showwarning(
                "信息不完整",
                "请填写学号和姓名。",
                parent=root,
            )

        def cancel():
            root.destroy()

        tk.Button(button_frame, text="开始测试", command=submit, width=12).grid(
            row=0,
            column=0,
            padx=(0, 8),
        )
        tk.Button(button_frame, text="取消", command=cancel, width=8).grid(row=0, column=1)
        root.bind("<Return>", lambda _event: submit())
        root.bind("<Escape>", lambda _event: cancel())
        root.protocol("WM_DELETE_WINDOW", cancel)

        frame.columnconfigure(1, weight=1)
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() - width) // 2
        y = (root.winfo_screenheight() - height) // 3
        root.geometry(f"+{x}+{y}")
        id_entry.focus_set()
        root.mainloop()
    except Exception as exc:
        return prompt_student_identity_console(config, exc)

    if submitted["value"]:
        student = config.get("student", {})
        print(
            "本次成绩身份: "
            f"{student.get('student_id', '')} {student.get('student_name', '')}"
        )
        return True

    if not has_student_identity(config):
        print("未填写学号/姓名，本次排行榜提交会跳过。")
    return has_student_identity(config)


def sanitize_config_for_output(config):
    sanitized = copy.deepcopy(config)
    leaderboard = sanitized.get("leaderboard")
    if isinstance(leaderboard, dict) and leaderboard.get("submit_token"):
        leaderboard["submit_token"] = "***redacted***"
    return sanitized


def build_leaderboard_payload(config, summary):
    student = config.get("student", {})
    student_id = str(student.get("student_id", "")).strip()
    student_name = str(student.get("student_name", "")).strip()
    if not student_id or not student_name:
        return None
    return {
        "studentId": student_id,
        "studentName": student_name,
        "summary": summary,
    }


def submit_leaderboard_score(config, summary, urlopen_func=None):
    leaderboard_config = config.get("leaderboard", {})
    if not leaderboard_config.get("enabled", False):
        return {
            "status": "disabled",
            "message": "排行榜提交未启用",
        }

    payload = build_leaderboard_payload(config, summary)
    if payload is None:
        return {
            "status": "skipped",
            "message": "缺少学号或姓名，未提交排行榜",
        }

    submit_url = str(leaderboard_config.get("submit_url", "")).strip()
    submit_token = str(leaderboard_config.get("submit_token", "")).strip()
    if not submit_url or not submit_token:
        return {
            "status": "skipped",
            "message": "缺少排行榜提交地址或令牌，未提交",
        }

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        submit_url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Carla-Submit-Token": submit_token,
        },
        method="POST",
    )
    timeout = float(leaderboard_config.get("timeout_seconds", 5.0))
    opener = urlopen_func or urllib.request.urlopen

    try:
        with opener(request, timeout=timeout) as response:
            status_code = getattr(response, "status", None) or response.getcode()
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        try:
            response_body = exc.read().decode("utf-8")
        except Exception:
            response_body = str(exc)
        return {
            "status": "failed",
            "message": f"排行榜提交失败: HTTP {exc.code} {response_body}",
        }
    except Exception as exc:
        return {
            "status": "failed",
            "message": f"排行榜提交失败: {exc}",
        }

    if status_code < 200 or status_code >= 300:
        return {
            "status": "failed",
            "message": f"排行榜提交失败: HTTP {status_code} {response_body}",
        }

    try:
        payload = json.loads(response_body) if response_body else {}
    except json.JSONDecodeError:
        return {
            "status": "failed",
            "message": "排行榜提交失败: 后端返回不是 JSON",
        }

    if not payload.get("ok"):
        return {
            "status": "failed",
            "message": f"排行榜提交失败: {payload.get('message', '未知错误')}",
        }

    data = payload.get("data", {})
    rank = data.get("rank")
    return {
        "status": "success",
        "message": f"排行榜提交成功，第 {rank} 名" if rank else "排行榜提交成功",
        "submission_id": data.get("submissionId"),
        "rank": rank,
        "best_for_student": data.get("bestForStudent"),
    }


def protected_settings(config):
    """Return the teacher-controlled settings that should not be changed."""
    return {
        "map_name": config.get("map_name"),
        "random_seed": config.get("random_seed"),
        "fixed_delta_seconds": config.get("fixed_delta_seconds"),
        "traffic_manager_port": config.get("traffic_manager_port"),
        "background_vehicle_count": config.get("background_vehicle_count"),
        "walker_count": config.get("walker_count"),
        "route": config.get("route", {}),
        "rules": {
            "speed_limit_tolerance_ratio": config.get("rules", {}).get(
                "speed_limit_tolerance_ratio"
            ),
            "speeding_min_seconds": config.get("rules", {}).get(
                "speeding_min_seconds"
            ),
            "max_lane_invasion_penalty": config.get("rules", {}).get(
                "max_lane_invasion_penalty"
            ),
            "max_speeding_penalty": config.get("rules", {}).get(
                "max_speeding_penalty"
            ),
        },
        "scoring": config.get("scoring", {}),
    }


def protected_settings_checksum(config):
    payload = json.dumps(
        protected_settings(config),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def scoring_duration_seconds(config):
    scoring = config.get("scoring", {})
    if "duration_seconds" in scoring:
        return float(scoring["duration_seconds"])
    return float(config.get("max_ticks", 0)) * float(config.get("fixed_delta_seconds", 0.05))


def distance_points_for(config, distance_m):
    scoring = config.get("scoring", {})
    rate = float(scoring.get("distance_points_per_meter", 1.0))
    return round(float(distance_m) * rate, 2)


def print_challenge_settings(config):
    penalties = config["scoring"]["penalties"]
    print("\n=== CARLA Safety Race Fixed Settings ===")
    print(f"Map: {config['map_name']}")
    print("Route: fixed road-follow route")
    print(f"Random seed: {config['random_seed']}")
    print(f"Fixed delta seconds: {config['fixed_delta_seconds']}")
    print(
        "Score rule: "
        f"{scoring_duration_seconds(config):.1f}s distance challenge, "
        "1 meter = 1 point before penalties"
    )
    print(f"Background vehicles: {config['background_vehicle_count']}")
    print(f"Walkers: {config['walker_count']}")
    print("Penalty rules:")
    print(f"  pedestrian collision: {penalties['collision_pedestrian']} each")
    print(f"  vehicle collision: {penalties['collision_vehicle']} each")
    print(f"  static collision: {penalties['collision_static']} each")
    print(f"  red light: {penalties['red_light']} each")
    print(f"  off route: {penalties['off_route']} each")
    print(
        "  lane invasion: "
        f"{penalties['lane_invasion']} each, "
        f"max {config['rules']['max_lane_invasion_penalty']}"
    )
    print(
        "  speeding: "
        f"{penalties['speeding']} each, "
        f"max {config['rules']['max_speeding_penalty']}"
    )
    print(f"Protected settings checksum: {protected_settings_checksum(config)}")
    print("Students should not modify fixed settings, scoring, or rule detection.\n")


DEFAULT_RENDER_CONFIG = {
    "enabled": True,
    "width": 1280,
    "height": 720,
    "score_pages_wait_for_input": True,
    "camera_fov": 90.0,
    "camera_x": -7.0,
    "camera_z": 3.0,
    "camera_pitch": -12.0,
    "spectator_distance": 8.0,
    "spectator_height": 4.0,
    "spectator_pitch": -18.0,
    "max_fps": 30,
}


def normalize_render_config(config):
    render_config = dict(DEFAULT_RENDER_CONFIG)
    raw_render_config = config.get("render", {})
    render_config.update(raw_render_config)
    if (
        "score_pages_wait_for_input" not in raw_render_config
        and "score_screen_wait_for_click" in raw_render_config
    ):
        render_config["score_pages_wait_for_input"] = raw_render_config[
            "score_screen_wait_for_click"
        ]
    render_config["enabled"] = bool(render_config["enabled"])
    render_config["width"] = int(render_config["width"])
    render_config["height"] = int(render_config["height"])
    render_config["score_pages_wait_for_input"] = bool(
        render_config["score_pages_wait_for_input"]
    )
    render_config["camera_fov"] = float(render_config["camera_fov"])
    render_config["camera_x"] = float(render_config["camera_x"])
    render_config["camera_z"] = float(render_config["camera_z"])
    render_config["camera_pitch"] = float(render_config["camera_pitch"])
    render_config["spectator_distance"] = float(render_config["spectator_distance"])
    render_config["spectator_height"] = float(render_config["spectator_height"])
    render_config["spectator_pitch"] = float(render_config["spectator_pitch"])
    render_config["max_fps"] = int(render_config["max_fps"])
    return render_config


def _format_optional_distance(value):
    if value is None or value == "":
        return "无"
    return f"{float(value):.1f} m"


def _format_optional_age(value):
    if value is None or value == "":
        return "无"
    return f"{float(value):.1f}s 前"


def _traffic_light_cn(value):
    labels = {
        "Red": "红灯",
        "Yellow": "黄灯",
        "Green": "绿灯",
        "Off": "关闭",
        "Unknown": "未知",
    }
    return labels.get(value, str(value or "未知"))


def _collision_cn(value):
    labels = {
        "collision_pedestrian": "行人",
        "collision_vehicle": "车辆",
        "collision_static": "静态物体",
    }
    if not value:
        return "无"
    return labels.get(value, str(value))


def _event_type_cn(value):
    labels = {
        "collision_pedestrian": "行人碰撞",
        "collision_vehicle": "车辆碰撞",
        "collision_static": "静态物体碰撞",
        "red_light": "闯红灯",
        "off_route": "偏离路线",
        "lane_invasion": "车道入侵/压线",
        "speeding": "超速",
        "stuck": "长时间停滞",
    }
    return labels.get(value, str(value or "未知事件"))


def _policy_mode_cn(value):
    labels = {
        "init": "初始化",
        "no_target": "无目标停车",
        "normal": "正常巡线",
        "off_route_rejoin": "偏航回正",
        "stopped_red_light": "红灯停车",
        "stopped_obstacle": "障碍停车",
        "recovery_reverse": "脱困倒车",
        "recovery_forward": "脱困前进",
    }
    return labels.get(value, str(value or "未知"))


def _waiting_reason_cn(value):
    labels = {
        "none": "无",
        "red_light": "红灯",
        "obstacle": "近距离障碍",
    }
    return labels.get(value, str(value or "无"))


def _format_target(target):
    if target is None:
        return "无"
    try:
        return f"x={target.x:.1f}, y={target.y:.1f}"
    except AttributeError:
        return str(target)


def build_hud_lines(snapshot):
    obstacle = snapshot.get("nearest_obstacle_distance_m")
    policy_debug = snapshot.get("policy_debug") or {}
    target_speed = float(policy_debug.get("target_speed_kmh", 0.0))
    heading_error = float(policy_debug.get("heading_error_deg", 0.0))
    waiting_reason = _waiting_reason_cn(policy_debug.get("waiting_reason", "none"))
    last_collision = _collision_cn(snapshot.get("last_collision_type"))
    last_collision_age = _format_optional_age(snapshot.get("last_collision_age_s"))
    distance_traveled = float(snapshot.get("distance_traveled_m", 0.0))
    distance_points = snapshot.get("distance_points", distance_traveled)

    return [
        "CARLA 安全竞速调试面板",
        (
            f"帧/时间: {snapshot.get('frame', '-')} / "
            f"{float(snapshot.get('sim_time_s', 0.0)):.1f} s"
        ),
        (
            "速度/限速: "
            f"{float(snapshot.get('speed_kmh', 0.0)):.1f} / "
            f"{float(snapshot.get('speed_limit_kmh', 0.0)):.1f} km/h"
        ),
        f"行驶距离: {distance_traveled:.1f} m",
        f"当前距离分: {_format_score_value(distance_points)}",
        (
            f"检查点: {snapshot.get('checkpoint_index', '-')}/"
            f"{snapshot.get('checkpoint_count', '-')}"
        ),
        f"路线进度: {float(snapshot.get('route_progress', 0.0)) * 100.0:.1f}%",
        (
            f"路线索引: 最近 {snapshot.get('route_index', '-')} / "
            f"目标 {snapshot.get('route_target_index', '-')}"
        ),
        f"路线偏移: {float(snapshot.get('distance_to_route_m', 0.0)):.1f} m",
        f"目标点索引: {snapshot.get('route_target_index', '-')}",
        f"目标坐标: {_format_target(snapshot.get('route_target'))}",
        f"红绿灯: {_traffic_light_cn(snapshot.get('traffic_light_state'))}",
        f"最近障碍: {_format_optional_distance(obstacle)}",
        f"最近碰撞: {last_collision} {last_collision_age}",
        f"策略模式: {_policy_mode_cn(policy_debug.get('mode'))}",
        f"等待原因: {waiting_reason}",
        f"目标速度: {target_speed:.1f} km/h",
        f"航向误差: {heading_error:.1f} deg",
        (
            "控制: "
            f"油门 {float(snapshot.get('control_throttle', 0.0)):.2f} "
            f"刹车 {float(snapshot.get('control_brake', 0.0)):.2f} "
            f"转向 {float(snapshot.get('control_steer', 0.0)):.2f} "
            f"倒车 {'是' if snapshot.get('control_reverse') else '否'}"
        ),
        f"累计扣分: {snapshot.get('penalty_points', 0)}",
        f"事件数量: {snapshot.get('event_count', 0)}",
        f"输出目录: {snapshot.get('output_dir', '-')}",
    ]


def _format_score_value(value):
    if value is None or value == "":
        return "-"
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return f"{number:.2f}"


def _format_lap_time(value):
    if value is None or value == "":
        return "未完成"
    return f"{float(value):.3f} s"


def _format_meters(value):
    if value is None or value == "":
        return "-"
    return f"{float(value):.3f} m"


def _format_seconds(value):
    return f"{float(value):.3f} s"


def _format_leaderboard_submission(value):
    if not value:
        return "无"
    status = value.get("status")
    message = value.get("message", "")
    labels = {
        "success": "成功",
        "failed": "失败",
        "skipped": "跳过",
        "disabled": "未启用",
    }
    label = labels.get(status, str(status or "未知"))
    return f"{label}: {message}" if message else label


def build_scoring_standard_lines(config):
    scoring = config["scoring"]
    penalties = scoring["penalties"]
    rules = config.get("rules", {})
    duration_s = scoring_duration_seconds(config)
    points_per_meter = float(scoring.get("distance_points_per_meter", 1.0))
    if points_per_meter == 1.0:
        distance_rule = "1 m = 1 分"
    else:
        distance_rule = f"1 m = {_format_score_value(points_per_meter)} 分"
    lines = [
        "CARLA 期末距离挑战评分标准",
        f"计时窗口: {_format_seconds(duration_s)}",
        f"距离分: {distance_rule}",
        "总分构成: 距离分 - 扣分合计",
        f"目标: {_format_seconds(duration_s)} 内安全行驶得越远，成绩越高",
        "有效距离按固定路线向前推进计算，倒车或绕圈不会额外加分",
        "扣分规则:",
    ]

    penalty_order = [
        "collision_pedestrian",
        "collision_vehicle",
        "collision_static",
        "red_light",
        "off_route",
        "lane_invasion",
        "speeding",
        "stuck",
    ]
    for event_type in penalty_order:
        if event_type not in penalties:
            continue
        line = (
            f"- {_event_type_cn(event_type)}: "
            f"每次扣 {_format_score_value(penalties[event_type])} 分"
        )
        if event_type == "lane_invasion":
            cap = rules.get("max_lane_invasion_penalty")
            if cap is not None:
                line += f"，最多扣 {_format_score_value(cap)} 分"
        elif event_type == "speeding":
            cap = rules.get("max_speeding_penalty")
            if cap is not None:
                line += f"，最多扣 {_format_score_value(cap)} 分"
        lines.append(line)

    pedestrian_cap = rules.get("pedestrian_collision_score_cap")
    if pedestrian_cap is not None:
        lines.append(f"行人碰撞后最高分: {_format_score_value(pedestrian_cap)}")
    lines.extend(
        [
            "最终成绩: max(0, 距离分 - 扣分合计)",
            "按 Enter 或 Space 开始；按 Esc 或关闭窗口退出",
        ]
    )
    return lines


def build_score_screen_lines(summary, output_dir):
    completed = bool(summary.get("completed"))
    penalty_breakdown = summary.get("penalty_breakdown") or {}
    student = summary.get("student") or {}
    student_id = str(student.get("student_id", "")).strip()
    student_name = str(student.get("student_name", "")).strip()
    identity = f"{student_id} {student_name}".strip() or "未填写"
    lines = [
        "CARLA 期末距离挑战成绩报告",
        f"学生信息: {identity}",
        f"是否跑完全程: {'是' if completed else '否'}",
        f"计时窗口: {_format_seconds(summary.get('duration_s', 0.0))}",
        f"行驶距离: {_format_meters(summary.get('distance_traveled_m'))}",
        f"距离分: {_format_score_value(summary.get('distance_points'))}",
        f"最终成绩: {_format_score_value(summary.get('final_score'))}",
        f"扣分合计: {_format_score_value(summary.get('penalty_points'))}",
        f"原始分: {_format_score_value(summary.get('raw_score'))}",
        "评分公式: 距离分 - 扣分合计 = 最终成绩",
        f"跑完全程用时: {_format_lap_time(summary.get('lap_time_s'))}",
        (
            "固定设置校验: "
            f"{summary.get('protected_settings_checksum', '-')}"
        ),
        f"排行榜提交: {_format_leaderboard_submission(summary.get('leaderboard_submission'))}",
        "扣分明细:",
    ]
    if penalty_breakdown:
        for event_type, points in sorted(penalty_breakdown.items()):
            lines.append(f"- {_event_type_cn(event_type)}: {_format_score_value(points)}")
    else:
        lines.append("- 无")
    lines.extend(
        [
            f"输出目录: {output_dir}",
            "报告文件: lap_summary.json / events.csv / trajectory.csv / score_report.md",
            "按 Esc 键或关闭窗口结束截图页",
        ]
    )
    return lines


def is_score_report_close_event(pygame, event):
    if event.type == pygame.QUIT:
        return True
    return event.type == pygame.KEYDOWN and getattr(event, "key", None) == pygame.K_ESCAPE


def apply_render_overrides(config, args):
    render = config.setdefault("render", {})
    if args.render:
        render["enabled"] = True
    if args.no_render:
        render["enabled"] = False
    if getattr(args, "no_score_screen", False):
        render["score_pages_wait_for_input"] = False
        render["score_screen_wait_for_click"] = False
    if args.render_width is not None:
        render["width"] = int(args.render_width)
    if args.render_height is not None:
        render["height"] = int(args.render_height)


def resolve_output_root(root):
    output_root = Path(root)
    if output_root.is_absolute():
        return output_root
    return TEMPLATE_ROOT / output_root


def make_output_dir(root):
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = resolve_output_root(root) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_json(path, data):
    with Path(path).open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def write_csv(path, rows, fieldnames):
    with Path(path).open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def choose_vehicle_blueprint(bp_lib, rng):
    blueprints = []
    for bp in bp_lib.filter("vehicle.*"):
        if bp.has_attribute("number_of_wheels"):
            wheels = int(bp.get_attribute("number_of_wheels"))
            if wheels != 4:
                continue
        blueprints.append(bp)
    if not blueprints:
        blueprints = list(bp_lib.filter("vehicle.*"))
    bp = rng.choice(blueprints)
    if bp.has_attribute("role_name"):
        bp.set_attribute("role_name", "autopilot")
    return bp


def choose_ego_blueprint(bp_lib):
    preferred = ["vehicle.tesla.model3", "vehicle.lincoln.mkz_2020"]
    for type_id in preferred:
        try:
            bp = bp_lib.find(type_id)
            bp.set_attribute("role_name", "hero")
            return bp
        except (IndexError, RuntimeError):
            pass
    bp = bp_lib.filter("vehicle.*")[0]
    if bp.has_attribute("role_name"):
        bp.set_attribute("role_name", "hero")
    return bp


def build_outer_checkpoints(world, checkpoint_count):
    spawn_points = list(world.get_map().get_spawn_points())
    if len(spawn_points) < checkpoint_count:
        raise RuntimeError("Not enough spawn points to build route checkpoints")

    xs = [sp.location.x for sp in spawn_points]
    ys = [sp.location.y for sp in spawn_points]
    center_x = sum(xs) / len(xs)
    center_y = sum(ys) / len(ys)

    def radius(spawn_point):
        loc = spawn_point.location
        return math.hypot(loc.x - center_x, loc.y - center_y)

    outer = sorted(spawn_points, key=radius, reverse=True)
    outer = outer[: max(checkpoint_count * 3, checkpoint_count)]

    def angle(spawn_point):
        loc = spawn_point.location
        return math.atan2(loc.y - center_y, loc.x - center_x)

    outer = sorted(outer, key=angle)
    step = max(1, len(outer) // checkpoint_count)
    selected = outer[::step][:checkpoint_count]
    return [sp.location for sp in selected]


def waypoint_key(waypoint, sampling_resolution):
    step = max(float(sampling_resolution), 0.5)
    return (
        int(getattr(waypoint, "road_id", 0)),
        int(getattr(waypoint, "section_id", 0)),
        int(getattr(waypoint, "lane_id", 0)),
        int(round(float(getattr(waypoint, "s", 0.0)) / step)),
    )


def driving_waypoint(world_map, location):
    try:
        return world_map.get_waypoint(
            location,
            project_to_road=True,
            lane_type=carla.LaneType.Driving,
        )
    except TypeError:
        return world_map.get_waypoint(location)
    except RuntimeError:
        return None


def waypoint_is_driving(waypoint):
    lane_type = getattr(waypoint, "lane_type", carla.LaneType.Driving)
    return lane_type == carla.LaneType.Driving


def trace_route_with_waypoints(world_map, start_location, end_location, sampling_resolution):
    start_waypoint = driving_waypoint(world_map, start_location)
    end_waypoint = driving_waypoint(world_map, end_location)
    if start_waypoint is None or end_waypoint is None:
        return []

    step = max(float(sampling_resolution), 1.0)
    end_loc = end_waypoint.transform.location
    goal_radius = max(step * 1.5, 5.0)
    max_nodes = 20000

    start_key = waypoint_key(start_waypoint, step)
    frontier = []
    counter = 0
    heapq.heappush(
        frontier,
        (distance(start_waypoint.transform.location, end_loc), counter, start_key),
    )
    came_from = {start_key: None}
    costs = {start_key: 0.0}
    waypoints = {start_key: start_waypoint}
    best_key = start_key
    best_distance = distance(start_waypoint.transform.location, end_loc)
    visited = 0

    while frontier and visited < max_nodes:
        _priority, _counter, current_key = heapq.heappop(frontier)
        current = waypoints[current_key]
        current_loc = current.transform.location
        current_distance = distance(current_loc, end_loc)
        visited += 1

        if current_distance < best_distance:
            best_distance = current_distance
            best_key = current_key
        if current_distance <= goal_radius:
            best_key = current_key
            break

        for next_waypoint in current.next(step):
            if not waypoint_is_driving(next_waypoint):
                continue
            next_key = waypoint_key(next_waypoint, step)
            next_loc = next_waypoint.transform.location
            edge_cost = max(distance(current_loc, next_loc), step)
            new_cost = costs[current_key] + edge_cost
            if new_cost >= costs.get(next_key, float("inf")):
                continue
            costs[next_key] = new_cost
            waypoints[next_key] = next_waypoint
            came_from[next_key] = current_key
            counter += 1
            priority = new_cost + distance(next_loc, end_loc)
            heapq.heappush(frontier, (priority, counter, next_key))

    if best_distance > max(30.0, step * 8.0):
        return []

    route = []
    key = best_key
    while key is not None:
        waypoint = waypoints[key]
        route.append(waypoint.transform.location)
        key = came_from[key]
    route.reverse()
    if route and distance(route[-1], end_loc) > 0.5:
        route.append(end_loc)
    return route


def append_route_segment(dense, segment):
    for loc in segment:
        if not dense or distance(dense[-1], loc) > 0.5:
            dense.append(loc)


def waypoint_yaw(waypoint, previous_location=None):
    rotation = getattr(waypoint.transform, "rotation", None)
    if rotation is not None and hasattr(rotation, "yaw"):
        return float(rotation.yaw)
    if previous_location is None:
        return 0.0
    loc = waypoint.transform.location
    return math.degrees(math.atan2(loc.y - previous_location.y, loc.x - previous_location.x))


def choose_lane_follow_next(current_waypoint, next_options, previous_location):
    if not next_options:
        return None
    if len(next_options) == 1:
        return next_options[0]

    current_yaw = waypoint_yaw(current_waypoint, previous_location)

    def turn_cost(next_waypoint):
        yaw_delta = _normalize_degrees(waypoint_yaw(next_waypoint) - current_yaw)
        # Prefer staying on the current lane unless the road forces a turn.
        return abs(yaw_delta)

    return min(next_options, key=turn_cost)


def _normalize_degrees(angle):
    while angle > 180.0:
        angle -= 360.0
    while angle < -180.0:
        angle += 360.0
    return angle


def sample_checkpoints_from_route(route_points, checkpoint_count):
    if len(route_points) < checkpoint_count:
        return list(route_points)
    last_index = len(route_points) - 1
    checkpoints = []
    for index in range(checkpoint_count):
        route_index = round(index * last_index / max(1, checkpoint_count - 1))
        checkpoints.append(route_points[route_index])
    return checkpoints


def build_lane_follow_route(world, checkpoint_count, sampling_resolution, route_length_m):
    world_map = world.get_map()
    spawn_points = list(world_map.get_spawn_points())
    if not spawn_points:
        raise RuntimeError("No spawn points in the map")

    waypoint = driving_waypoint(world_map, spawn_points[0].location)
    if waypoint is None:
        raise RuntimeError("Could not project first spawn point to a driving lane")

    step = max(float(sampling_resolution), 1.0)
    target_length = max(float(route_length_m), step * checkpoint_count)
    max_steps = int(target_length / step) + checkpoint_count * 10
    route_points = []
    traveled = 0.0
    previous_location = None

    for _ in range(max_steps):
        loc = waypoint.transform.location
        append_route_segment(route_points, [loc])
        if traveled >= target_length:
            break

        next_options = [
            next_waypoint
            for next_waypoint in waypoint.next(step)
            if waypoint_is_driving(next_waypoint)
        ]
        next_waypoint = choose_lane_follow_next(
            waypoint,
            next_options,
            previous_location,
        )
        if next_waypoint is None:
            break

        next_loc = next_waypoint.transform.location
        traveled += distance(loc, next_loc)
        previous_location = loc
        waypoint = next_waypoint

    if len(route_points) < checkpoint_count:
        raise RuntimeError("Lane-follow route is too short")

    return sample_checkpoints_from_route(route_points, checkpoint_count), route_points


def try_build_dense_route(world, checkpoints, sampling_resolution):
    dense = []
    try:
        import agents.navigation.global_route_planner as grp_module
    except ImportError:
        grp_module = None

    grp = None
    if grp_module is not None:
        try:
            grp = grp_module.GlobalRoutePlanner(
                world.get_map(),
                sampling_resolution,
            )
        except TypeError:
            # Older CARLA versions use a slightly different constructor.
            grp = grp_module.GlobalRoutePlanner(world.get_map(), sampling_resolution)
        except Exception:
            grp = None

    pairs = list(zip(checkpoints, checkpoints[1:] + checkpoints[:1]))
    if grp is not None:
        for start, end in pairs:
            try:
                segment = grp.trace_route(start, end)
            except Exception:
                segment = []
            append_route_segment(
                dense,
                [waypoint.transform.location for waypoint, _road_option in segment],
            )
        if len(dense) > len(checkpoints):
            return dense

    dense = []
    world_map = world.get_map()
    for start, end in pairs:
        segment = trace_route_with_waypoints(
            world_map,
            start,
            end,
            sampling_resolution,
        )
        append_route_segment(dense, segment)
    return dense if len(dense) > len(checkpoints) else checkpoints


def nearest_route_index(location, route_points, start_index=0, search_window=80):
    if not route_points:
        return 0, float("inf")
    best_index = start_index % len(route_points)
    best_distance = float("inf")
    total = len(route_points)
    for offset in range(search_window):
        idx = (start_index + offset) % total
        dist = distance(location, route_points[idx])
        if dist < best_distance:
            best_distance = dist
            best_index = idx
    return best_index, best_distance


def select_route_target(location, route_points, nearest_index, lookahead_m):
    if not route_points:
        return None, nearest_index

    total = len(route_points)
    target_index = nearest_index
    walked = 0.0
    prev = route_points[nearest_index]
    for step in range(1, total):
        idx = (nearest_index + step) % total
        current = route_points[idx]
        walked += distance(prev, current)
        prev = current
        target_index = idx
        if walked >= lookahead_m:
            break
    return route_points[target_index], target_index


def cumulative_route_distances(route_points):
    if not route_points:
        return []
    distances = [0.0]
    for previous, current in zip(route_points, route_points[1:]):
        distances.append(distances[-1] + distance(previous, current))
    return distances


class EventRecorder:
    def __init__(self, config):
        self.config = config
        self.rows = []
        self.penalty_totals = {}
        self.last_event_time = {}
        self.has_pedestrian_collision = False

    def add(self, event_type, sim_time, frame, ego_vehicle, route_progress, penalty, detail):
        loc = ego_vehicle.get_location()
        row = {
            "frame": frame,
            "sim_time_s": round(sim_time, 3),
            "x": round(loc.x, 3),
            "y": round(loc.y, 3),
            "z": round(loc.z, 3),
            "speed_kmh": round(speed_kmh(ego_vehicle), 3),
            "route_progress": round(route_progress, 4),
            "event_type": event_type,
            "penalty": penalty,
            "detail": detail,
        }
        self.rows.append(row)
        self.penalty_totals[event_type] = self.penalty_totals.get(event_type, 0) + penalty
        if event_type == "collision_pedestrian":
            self.has_pedestrian_collision = True

    def add_with_cooldown(
        self,
        event_type,
        sim_time,
        frame,
        ego_vehicle,
        route_progress,
        penalty,
        detail,
    ):
        cooldown = float(self.config["rules"].get("event_cooldown_seconds", 2.0))
        last_time = self.last_event_time.get(event_type, -1e9)
        if sim_time - last_time < cooldown:
            return False
        self.last_event_time[event_type] = sim_time
        self.add(event_type, sim_time, frame, ego_vehicle, route_progress, penalty, detail)
        return True

    def add_collision(
        self,
        event_type,
        sim_time,
        frame,
        ego_vehicle,
        route_progress,
        penalty,
        detail,
    ):
        return self.add_with_cooldown(
            event_type,
            sim_time,
            frame,
            ego_vehicle,
            route_progress,
            penalty,
            detail,
        )

    def penalty_sum(self):
        return sum(row["penalty"] for row in self.rows)


def follow_spectator_transform(carla_module, ego_transform, distance_m, height_m, pitch_deg):
    yaw_rad = math.radians(ego_transform.rotation.yaw)
    location = carla_module.Location(
        x=ego_transform.location.x - math.cos(yaw_rad) * distance_m,
        y=ego_transform.location.y - math.sin(yaw_rad) * distance_m,
        z=ego_transform.location.z + height_m,
    )
    rotation = carla_module.Rotation(
        pitch=pitch_deg,
        yaw=ego_transform.rotation.yaw,
        roll=0.0,
    )
    return carla_module.Transform(location, rotation)


class PygameViewer:
    def __init__(self, carla_module, world, ego_vehicle, bp_lib, render_config):
        self.carla = carla_module
        self.world = world
        self.ego_vehicle = ego_vehicle
        self.bp_lib = bp_lib
        self.config = render_config
        self.width = int(render_config["width"])
        self.height = int(render_config["height"])
        self.latest_image = None
        self.camera = None
        self.enabled = False
        self.closed_by_user = False

        try:
            os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
            import pygame  # type: ignore
        except ImportError as exc:
            print(f"Pygame viewer disabled: pygame is not installed ({exc})")
            return

        self.pygame = pygame
        try:
            pygame.init()
            pygame.font.init()
            self.display = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("CARLA Safety Race")
            self.clock = pygame.time.Clock()
            self.font = self._make_font(18)
            self.title_font = self._make_font(22, bold=True)
            self._spawn_camera()
            self.enabled = True
        except Exception as exc:
            print(f"Pygame viewer disabled: {exc}")
            self.cleanup()

    def _make_font(self, size, bold=False):
        # Prefer common CJK fonts on Windows so the Chinese HUD renders correctly.
        names = [
            "microsoftyahei",
            "simhei",
            "simsun",
            "noto sans cjk sc",
            "arial unicode ms",
            "consolas",
        ]
        for name in names:
            font_path = self.pygame.font.match_font(name, bold=bold)
            if font_path:
                return self.pygame.font.Font(font_path, size)
        return self.pygame.font.Font(None, size)

    def _spawn_camera(self):
        camera_bp = self.bp_lib.find("sensor.camera.rgb")
        camera_bp.set_attribute("image_size_x", str(self.width))
        camera_bp.set_attribute("image_size_y", str(self.height))
        camera_bp.set_attribute("fov", f"{float(self.config['camera_fov']):.1f}")
        transform = self.carla.Transform(
            self.carla.Location(
                x=float(self.config["camera_x"]),
                z=float(self.config["camera_z"]),
            ),
            self.carla.Rotation(pitch=float(self.config["camera_pitch"])),
        )
        self.camera = self.world.spawn_actor(
            camera_bp,
            transform,
            attach_to=self.ego_vehicle,
        )
        self.camera.listen(self._on_image)

    def _on_image(self, image):
        self.latest_image = image

    def actors(self):
        if self.camera is None:
            return []
        return [self.camera]

    def tick(self, snapshot):
        if not self.enabled:
            return True

        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.closed_by_user = True
                return False
            if event.type == self.pygame.KEYDOWN and event.key in (
                self.pygame.K_ESCAPE,
                self.pygame.K_q,
            ):
                return False

        self._update_spectator()
        self._draw(snapshot)
        self.pygame.display.flip()
        self.clock.tick(int(self.config["max_fps"]))
        return True

    def _update_spectator(self):
        spectator = self.world.get_spectator()
        spectator.set_transform(
            follow_spectator_transform(
                self.carla,
                self.ego_vehicle.get_transform(),
                float(self.config["spectator_distance"]),
                float(self.config["spectator_height"]),
                float(self.config["spectator_pitch"]),
            )
        )

    def _draw(self, snapshot):
        if self.latest_image is None:
            self.display.fill((16, 18, 24))
        else:
            image = self.latest_image
            surface = self.pygame.image.frombuffer(
                bytes(image.raw_data),
                (image.width, image.height),
                "BGRA",
            )
            self.display.blit(surface, (0, 0))
        self._draw_hud(snapshot)

    def _draw_hud(self, snapshot):
        lines = build_hud_lines(snapshot)
        line_height = 24
        columns = 2 if 18 + line_height * len(lines) > self.height - 24 and self.width >= 520 else 1
        rows_per_column = math.ceil(len(lines) / columns)
        panel_width = min(900 if columns == 2 else 620, self.width - 24)
        panel_height = 18 + line_height * rows_per_column
        panel = self.pygame.Surface((panel_width, panel_height), self.pygame.SRCALPHA)
        panel.fill((0, 0, 0, 150))
        self.display.blit(panel, (12, 12))

        for index, line in enumerate(lines):
            column = index // rows_per_column
            row = index % rows_per_column
            column_width = panel_width // columns
            x = 24 + column * column_width
            y = 20 + row * line_height
            font = self.title_font if index == 0 else self.font
            color = (255, 255, 255) if index != 0 else (120, 220, 255)
            text = font.render(self._fit_text(font, line, column_width - 20), True, color)
            self.display.blit(text, (x, y))

    def show_score_screen(self, summary, output_dir):
        if not self.enabled or self.closed_by_user:
            return
        if not self._score_pages_wait_enabled():
            return

        self._draw_score_screen(summary, output_dir)
        self.pygame.display.flip()
        while True:
            for event in self.pygame.event.get():
                if is_score_report_close_event(self.pygame, event):
                    if event.type == self.pygame.QUIT:
                        self.closed_by_user = True
                    return
            self.clock.tick(30)

    def show_scoring_standard_screen(self, config):
        if not self.enabled or self.closed_by_user:
            return True
        if not self._score_pages_wait_enabled():
            return True

        self._draw_scoring_standard_screen(config)
        self.pygame.display.flip()
        while True:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.closed_by_user = True
                    return False
                if (
                    event.type == self.pygame.KEYDOWN
                    and event.key == self.pygame.K_ESCAPE
                ):
                    self.closed_by_user = True
                    return False
                if (
                    event.type == self.pygame.KEYDOWN
                    and event.key
                    in (
                        self.pygame.K_RETURN,
                        self.pygame.K_KP_ENTER,
                        self.pygame.K_SPACE,
                    )
                ):
                    return True
            self.clock.tick(30)

    def _draw_score_screen(self, summary, output_dir):
        self._draw_text_screen(build_score_screen_lines(summary, output_dir))

    def _draw_scoring_standard_screen(self, config):
        self._draw_text_screen(build_scoring_standard_lines(config))

    def _draw_text_screen(self, lines):
        self.display.fill((12, 16, 22))

        margin = 24
        panel_width = max(280, self.width - margin * 2)
        panel_height = max(220, self.height - margin * 2)
        panel = self.pygame.Surface((panel_width, panel_height), self.pygame.SRCALPHA)
        panel.fill((0, 0, 0, 185))
        self.display.blit(panel, (margin, margin))

        x0 = margin + 22
        y0 = margin + 18
        max_width = panel_width - 44
        title = self.title_font.render(
            self._fit_text(self.title_font, lines[0], max_width),
            True,
            (120, 220, 255),
        )
        self.display.blit(title, (x0, y0))

        body = lines[1:]
        line_height = 26
        body_top = y0 + 38
        columns = (
            2
            if body_top + line_height * len(body) > margin + panel_height - 36
            and self.width >= 520
            else 1
        )
        rows_per_column = math.ceil(len(body) / columns)
        column_width = max_width // columns

        for index, line in enumerate(body):
            column = index // rows_per_column
            row = index % rows_per_column
            x = x0 + column * column_width
            y = body_top + row * line_height
            font = self.title_font if line.startswith("最终成绩") else self.font
            if line.startswith("最终成绩"):
                color = (255, 230, 120)
            elif line.startswith("按 "):
                color = (150, 255, 180)
            elif line.endswith(":"):
                color = (120, 220, 255)
            else:
                color = (245, 245, 245)
            text = font.render(
                self._fit_text(font, line, column_width - 24),
                True,
                color,
            )
            self.display.blit(text, (x, y))

    def _score_pages_wait_enabled(self):
        return bool(
            self.config.get(
                "score_pages_wait_for_input",
                self.config.get("score_screen_wait_for_click", True),
            )
        )

    def _fit_text(self, font, text, max_width):
        if font.size(text)[0] <= max_width:
            return text
        ellipsis = "..."
        while text and font.size(text + ellipsis)[0] > max_width:
            text = text[:-1]
        return text + ellipsis

    def cleanup(self):
        if not self.enabled and self.camera is not None:
            try:
                if getattr(self.camera, "is_listening", False):
                    self.camera.stop()
            except RuntimeError:
                pass
            try:
                if self.camera.is_alive:
                    self.camera.destroy()
            except RuntimeError:
                pass
        try:
            if hasattr(self, "pygame"):
                self.pygame.quit()
        except Exception:
            pass


class ChallengeRunner:
    def __init__(self, config, max_ticks_override=None):
        self.config = config
        self.max_ticks_override = max_ticks_override
        if max_ticks_override is not None:
            self.config["max_ticks"] = int(max_ticks_override)
        self.rng = random.Random(config["random_seed"])
        self.output_dir = make_output_dir(config["output"]["root"])
        self.actors = []
        self.walker_controllers = []
        self.collision_queue = []
        self.lane_queue = []
        self.obstacle_distance = None
        self.event_recorder = EventRecorder(config)
        self.trajectory_rows = []
        self.completed = False
        self.lap_time = None
        self.elapsed_time_s = 0.0
        self.distance_traveled_m = 0.0
        self._last_distance_location = None
        self.render_config = normalize_render_config(config)
        self.viewer = None
        self.last_collision_type = None
        self.last_collision_time = None

    def connect(self):
        self.client = carla.Client(self.config["host"], int(self.config["port"]))
        self.client.set_timeout(float(self.config["timeout_seconds"]))
        if self.client.get_world().get_map().name.split("/")[-1] != self.config["map_name"]:
            self.world = self.client.load_world(self.config["map_name"])
        else:
            self.world = self.client.get_world()
        self.bp_lib = self.world.get_blueprint_library()
        self.traffic_manager = self.client.get_trafficmanager(
            int(self.config["traffic_manager_port"])
        )

    def enable_sync(self):
        self.original_settings = self.world.get_settings()
        settings = self.world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = float(self.config["fixed_delta_seconds"])
        self.world.apply_settings(settings)
        self.traffic_manager.set_synchronous_mode(True)
        self.traffic_manager.set_random_device_seed(int(self.config["random_seed"]))
        random.seed(int(self.config["random_seed"]))

    def spawn_ego(self):
        spawn_points = list(self.world.get_map().get_spawn_points())
        if not spawn_points:
            raise RuntimeError("No spawn points in the map")
        ego_bp = choose_ego_blueprint(self.bp_lib)

        transform = spawn_points[0]
        if hasattr(self, "checkpoints") and self.checkpoints:
            try:
                waypoint = self.world.get_map().get_waypoint(
                    self.checkpoints[0],
                    project_to_road=True,
                    lane_type=carla.LaneType.Driving,
                )
                transform = waypoint.transform
                transform.location.z += 0.5
            except RuntimeError:
                pass

        ego = self.world.try_spawn_actor(ego_bp, transform)
        if ego is None:
            for transform in spawn_points:
                ego = self.world.try_spawn_actor(ego_bp, transform)
                if ego is not None:
                    break
        if ego is None:
            raise RuntimeError("Could not spawn ego vehicle")
        self.ego = ego
        self.actors.append(ego)

    def spawn_background_vehicles(self):
        spawn_points = list(self.world.get_map().get_spawn_points())
        self.rng.shuffle(spawn_points)
        count = int(self.config["background_vehicle_count"])
        spawned = 0
        for transform in spawn_points:
            if spawned >= count:
                break
            if distance(transform.location, self.ego.get_location()) < 20.0:
                continue
            bp = choose_vehicle_blueprint(self.bp_lib, self.rng)
            vehicle = self.world.try_spawn_actor(bp, transform)
            if vehicle is None:
                continue
            vehicle.set_autopilot(True, self.traffic_manager.get_port())
            self.actors.append(vehicle)
            spawned += 1
        print(f"Spawned background vehicles: {spawned}/{count}")

    def spawn_walkers(self):
        walker_bps = list(self.bp_lib.filter("walker.pedestrian.*"))
        controller_bp = self.bp_lib.find("controller.ai.walker")
        count = int(self.config["walker_count"])
        spawned = 0
        for _ in range(count * 4):
            if spawned >= count:
                break
            location = self.world.get_random_location_from_navigation()
            if location is None:
                continue
            transform = carla.Transform(location)
            walker_bp = self.rng.choice(walker_bps)
            if walker_bp.has_attribute("is_invincible"):
                walker_bp.set_attribute("is_invincible", "false")
            walker = self.world.try_spawn_actor(walker_bp, transform)
            if walker is None:
                continue
            controller = self.world.try_spawn_actor(controller_bp, carla.Transform(), walker)
            if controller is None:
                walker.destroy()
                continue
            self.actors.append(walker)
            self.walker_controllers.append(controller)
            self.actors.append(controller)
            spawned += 1

        self.world.tick()
        for controller in self.walker_controllers:
            controller.start()
            destination = self.world.get_random_location_from_navigation()
            if destination is not None:
                controller.go_to_location(destination)
            controller.set_max_speed(self.rng.uniform(0.8, 1.6))
        print(f"Spawned walkers: {spawned}/{count}")

    def attach_sensors(self):
        collision_bp = self.bp_lib.find("sensor.other.collision")
        collision = self.world.spawn_actor(
            collision_bp,
            carla.Transform(),
            attach_to=self.ego,
        )
        collision.listen(lambda event: self.collision_queue.append(event))
        self.actors.append(collision)

        lane_bp = self.bp_lib.find("sensor.other.lane_invasion")
        lane = self.world.spawn_actor(lane_bp, carla.Transform(), attach_to=self.ego)
        lane.listen(lambda event: self.lane_queue.append(event))
        self.actors.append(lane)

        try:
            obstacle_bp = self.bp_lib.find("sensor.other.obstacle")
            obstacle_bp.set_attribute("distance", "30")
            obstacle_bp.set_attribute("hit_radius", "1.5")
            obstacle_bp.set_attribute("only_dynamics", "true")
            obstacle = self.world.spawn_actor(
                obstacle_bp,
                carla.Transform(carla.Location(x=2.5, z=1.0)),
                attach_to=self.ego,
            )
            obstacle.listen(self._on_obstacle)
            self.actors.append(obstacle)
        except Exception as exc:
            print(f"Obstacle sensor unavailable: {exc}")

    def setup_viewer(self):
        if not self.render_config["enabled"]:
            return
        viewer = PygameViewer(
            carla,
            self.world,
            self.ego,
            self.bp_lib,
            self.render_config,
        )
        if viewer.enabled:
            self.viewer = viewer
            self.actors.extend(viewer.actors())
            print(
                "Pygame viewer enabled: "
                f"{self.render_config['width']}x{self.render_config['height']}"
            )

    def _on_obstacle(self, event):
        self.obstacle_distance = float(event.distance)

    def prepare_route(self):
        route_cfg = self.config["route"]
        checkpoint_count = int(route_cfg["checkpoint_count"])
        sampling_resolution = float(route_cfg["sampling_resolution_m"])
        generation = route_cfg.get("generation", "lane_follow")
        if generation == "outer_checkpoints":
            checkpoints = build_outer_checkpoints(self.world, checkpoint_count)
            dense = try_build_dense_route(
                self.world,
                checkpoints,
                sampling_resolution,
            )
        else:
            checkpoints, dense = build_lane_follow_route(
                self.world,
                checkpoint_count,
                sampling_resolution,
                float(route_cfg.get("route_length_m", 900.0)),
            )
        self.checkpoints = checkpoints
        self.route_points = dense
        self.route_cumulative_distances = cumulative_route_distances(dense)
        write_json(
            self.output_dir / "route_checkpoints.json",
            [location_dict(loc) for loc in checkpoints],
        )
        write_json(
            self.output_dir / "route_points.json",
            [location_dict(loc) for loc in dense],
        )
        print(f"Route checkpoints: {len(checkpoints)}, route points: {len(dense)}")

    def setup_policy(self):
        self.policy = StudentPolicy(carla, self.config)
        self.policy.setup(self.world, self.ego, self.route_points)

    def process_sensor_events(self, sim_time, frame, route_progress):
        penalties = self.config["scoring"]["penalties"]
        while self.collision_queue:
            event = self.collision_queue.pop(0)
            kind = actor_kind(event.other_actor)
            if kind == "pedestrian":
                event_type = "collision_pedestrian"
            elif kind == "vehicle":
                event_type = "collision_vehicle"
            else:
                event_type = "collision_static"
            self.last_collision_type = event_type
            self.last_collision_time = sim_time
            self.event_recorder.add_collision(
                event_type,
                sim_time,
                frame,
                self.ego,
                route_progress,
                int(penalties[event_type]),
                f"other_actor={event.other_actor.type_id}",
            )

        lane_penalty_total = self.event_recorder.penalty_totals.get("lane_invasion", 0)
        max_lane_penalty = int(self.config["rules"]["max_lane_invasion_penalty"])
        while self.lane_queue:
            event = self.lane_queue.pop(0)
            if lane_penalty_total >= max_lane_penalty:
                continue
            penalty = min(int(penalties["lane_invasion"]), max_lane_penalty - lane_penalty_total)
            markings = ",".join(str(marking.type) for marking in event.crossed_lane_markings)
            self.event_recorder.add_with_cooldown(
                "lane_invasion",
                sim_time,
                frame,
                self.ego,
                route_progress,
                penalty,
                f"markings={markings}",
            )
            lane_penalty_total += penalty

    def process_rule_events(self, sim_time, frame, route_progress, off_route_distance):
        penalties = self.config["scoring"]["penalties"]
        rules = self.config["rules"]

        speed = speed_kmh(self.ego)
        speed_limit = float(self.ego.get_speed_limit() or 30.0)
        tolerance = float(rules["speed_limit_tolerance_ratio"])
        speeding = speed > speed_limit * (1.0 + tolerance)
        if speeding:
            if not hasattr(self, "_speeding_start"):
                self._speeding_start = sim_time
            min_seconds = float(rules["speeding_min_seconds"])
            max_penalty = int(rules["max_speeding_penalty"])
            current_penalty = self.event_recorder.penalty_totals.get("speeding", 0)
            if sim_time - self._speeding_start >= min_seconds and current_penalty < max_penalty:
                penalty = min(int(penalties["speeding"]), max_penalty - current_penalty)
                self.event_recorder.add_with_cooldown(
                    "speeding",
                    sim_time,
                    frame,
                    self.ego,
                    route_progress,
                    penalty,
                    f"speed={speed:.1f}, limit={speed_limit:.1f}",
                )
        elif hasattr(self, "_speeding_start"):
            delattr(self, "_speeding_start")

        off_threshold = float(self.config["route"]["off_route_threshold_m"])
        if off_route_distance > off_threshold:
            self.event_recorder.add_with_cooldown(
                "off_route",
                sim_time,
                frame,
                self.ego,
                route_progress,
                int(penalties["off_route"]),
                f"distance_to_route={off_route_distance:.1f}",
            )

        at_light = self.ego.is_at_traffic_light()
        if at_light and self.ego.get_traffic_light_state() == carla.TrafficLightState.Red:
            if speed > 5.0:
                self.event_recorder.add_with_cooldown(
                    "red_light",
                    sim_time,
                    frame,
                    self.ego,
                    route_progress,
                    int(penalties["red_light"]),
                    f"speed={speed:.1f}",
                )

        stuck_speed = float(rules["stuck_speed_kmh"])
        if speed < stuck_speed and not (
            at_light and self.ego.get_traffic_light_state() == carla.TrafficLightState.Red
        ):
            if not hasattr(self, "_stuck_start"):
                self._stuck_start = sim_time
            if sim_time - self._stuck_start >= float(rules["stuck_min_seconds"]):
                self.event_recorder.add_with_cooldown(
                    "stuck",
                    sim_time,
                    frame,
                    self.ego,
                    route_progress,
                    int(penalties["stuck"]),
                    f"speed={speed:.1f}",
                )
        elif hasattr(self, "_stuck_start"):
            delattr(self, "_stuck_start")

    def update_distance_traveled(self, location, route_index=None):
        route_distances = getattr(self, "route_cumulative_distances", [])
        if route_index is not None and route_distances:
            safe_index = max(0, min(int(route_index), len(route_distances) - 1))
            self.distance_traveled_m = max(
                self.distance_traveled_m,
                route_distances[safe_index],
            )
            self._last_distance_location = copy_location(location)
            return

        if self._last_distance_location is None:
            self._last_distance_location = copy_location(location)
            return

        step_distance = distance(location, self._last_distance_location)
        if 0.0 <= step_distance < 50.0:
            self.distance_traveled_m += step_distance
        self._last_distance_location = copy_location(location)

    def append_trajectory(self, frame, sim_time, route_progress, target_index):
        transform = self.ego.get_transform()
        loc = transform.location
        light_state = light_state_label(self.ego.get_traffic_light_state())
        self.trajectory_rows.append(
            {
                "frame": frame,
                "sim_time_s": round(sim_time, 3),
                "x": round(loc.x, 3),
                "y": round(loc.y, 3),
                "z": round(loc.z, 3),
                "yaw": round(transform.rotation.yaw, 3),
                "speed_kmh": round(speed_kmh(self.ego), 3),
                "speed_limit_kmh": round(float(self.ego.get_speed_limit() or 0.0), 3),
                "distance_traveled_m": round(self.distance_traveled_m, 3),
                "route_progress": round(route_progress, 4),
                "route_target_index": target_index,
                "traffic_light_state": light_state,
                "nearest_obstacle_distance_m": (
                    round(self.obstacle_distance, 3)
                    if self.obstacle_distance is not None
                    else ""
                ),
            }
        )

    def compute_score(self, elapsed):
        duration_s = float(elapsed) if elapsed is not None else scoring_duration_seconds(self.config)
        distance_m = round(float(getattr(self, "distance_traveled_m", 0.0)), 3)
        distance_points = distance_points_for(self.config, distance_m)
        completion_points = 0
        time_points = 0
        penalty = self.event_recorder.penalty_sum()
        raw_score = round(distance_points - penalty, 2)
        final_score = max(0.0, raw_score)
        cap = self.config["rules"].get("pedestrian_collision_score_cap")
        if self.event_recorder.has_pedestrian_collision and cap is not None:
            final_score = min(final_score, float(cap))
        student = self.config.get("student", {})
        return {
            "completed": self.completed,
            "duration_s": round(duration_s, 3),
            "lap_time_s": round(self.lap_time, 3) if self.lap_time is not None else None,
            "distance_traveled_m": distance_m,
            "distance_points": distance_points,
            "protected_settings_checksum": protected_settings_checksum(self.config),
            "fixed_settings": protected_settings(self.config),
            "student": {
                "student_id": str(student.get("student_id", "")).strip(),
                "student_name": str(student.get("student_name", "")).strip(),
            },
            "completion_points": completion_points,
            "time_points": time_points,
            "penalty_points": penalty,
            "raw_score": raw_score,
            "final_score": round(final_score, 2),
            "penalty_breakdown": self.event_recorder.penalty_totals,
        }

    def write_outputs(self, summary):
        write_json(self.output_dir / "config_used.json", sanitize_config_for_output(self.config))
        write_csv(
            self.output_dir / "trajectory.csv",
            self.trajectory_rows,
            [
                "frame",
                "sim_time_s",
                "x",
                "y",
                "z",
                "yaw",
                "speed_kmh",
                "speed_limit_kmh",
                "distance_traveled_m",
                "route_progress",
                "route_target_index",
                "traffic_light_state",
                "nearest_obstacle_distance_m",
            ],
        )
        write_csv(
            self.output_dir / "events.csv",
            self.event_recorder.rows,
            [
                "frame",
                "sim_time_s",
                "x",
                "y",
                "z",
                "speed_kmh",
                "route_progress",
                "event_type",
                "penalty",
                "detail",
            ],
        )
        write_json(self.output_dir / "lap_summary.json", summary)
        report = [
            "# CARLA 期末距离挑战成绩报告",
            "",
            f"- 学号: {summary.get('student', {}).get('student_id', '')}",
            f"- 姓名: {summary.get('student', {}).get('student_name', '')}",
            f"- 计时窗口: {summary['duration_s']} s",
            f"- 行驶距离: {summary['distance_traveled_m']} m",
            f"- 距离分: {summary['distance_points']}",
            f"- 扣分合计: {summary['penalty_points']}",
            f"- 最终成绩: {summary['final_score']}",
            f"- 是否跑完全程: {summary['completed']}",
            f"- 跑完全程用时: {summary['lap_time_s']}",
            f"- 排行榜提交: {_format_leaderboard_submission(summary.get('leaderboard_submission'))}",
            "",
            "## 扣分明细",
        ]
        for key, value in sorted(summary["penalty_breakdown"].items()):
            report.append(f"- {key}: {value}")
        (self.output_dir / "score_report.md").write_text(
            "\n".join(report) + "\n",
            encoding="utf-8",
        )

    def cleanup(self):
        try:
            for controller in self.walker_controllers:
                try:
                    controller.stop()
                except RuntimeError:
                    pass

            for actor in self.actors:
                try:
                    if hasattr(actor, "is_listening") and actor.is_listening:
                        actor.stop()
                except RuntimeError:
                    pass

            if hasattr(self, "traffic_manager"):
                self.traffic_manager.set_synchronous_mode(False)
            if hasattr(self, "world") and hasattr(self, "original_settings"):
                self.world.apply_settings(self.original_settings)

            if hasattr(self, "client") and self.actors:
                commands = []
                for actor in reversed(self.actors):
                    try:
                        if actor.is_alive:
                            commands.append(carla.command.DestroyActor(actor))
                    except RuntimeError:
                        pass
                if commands:
                    self.client.apply_batch(commands)
            else:
                for actor in reversed(self.actors):
                    try:
                        if actor.is_alive:
                            actor.destroy()
                    except RuntimeError:
                        pass
        finally:
            if self.viewer is not None:
                self.viewer.cleanup()
            self.actors = []
            self.walker_controllers = []

    def run(self):
        self.connect()
        self.enable_sync()
        try:
            self.prepare_route()
            self.spawn_ego()
            self.spawn_background_vehicles()
            self.spawn_walkers()
            self.attach_sensors()
            self.setup_viewer()
            if self.viewer is not None and not self.viewer.show_scoring_standard_screen(
                self.config
            ):
                print("Pygame window closed before start; ending run.")
                return
            self.setup_policy()

            # Let actors and sensors settle.
            for _ in range(20):
                self.world.tick()

            route_cfg = self.config["route"]
            lookahead = float(route_cfg["target_lookahead_m"])
            checkpoint_radius = float(route_cfg["checkpoint_radius_m"])
            max_ticks = int(self.config["max_ticks"])
            fixed_delta = float(self.config["fixed_delta_seconds"])
            duration_s = scoring_duration_seconds(self.config)
            if self.max_ticks_override is None and duration_s > 0:
                max_ticks = min(max_ticks, max(1, math.ceil(duration_s / fixed_delta)))

            route_index = 0
            checkpoint_index = 0
            start_time = 0.0
            last_sim_time = 0.0

            for tick_index in range(max_ticks):
                frame = self.world.tick()
                sim_time = (tick_index + 1) * fixed_delta
                last_sim_time = sim_time
                self.elapsed_time_s = sim_time
                ego_loc = self.ego.get_location()

                route_index, off_route_distance = nearest_route_index(
                    ego_loc,
                    self.route_points,
                    route_index,
                )
                self.update_distance_traveled(ego_loc, route_index)
                target, target_index = select_route_target(
                    ego_loc,
                    self.route_points,
                    route_index,
                    lookahead,
                )

                if checkpoint_index < len(self.checkpoints):
                    checkpoint = self.checkpoints[checkpoint_index]
                    if distance(ego_loc, checkpoint) <= checkpoint_radius:
                        checkpoint_index += 1
                        print(f"Checkpoint {checkpoint_index}/{len(self.checkpoints)}")

                route_progress = checkpoint_index / max(1, len(self.checkpoints))

                traffic_light_state = light_state_label(self.ego.get_traffic_light_state())
                last_collision_age = None
                if self.last_collision_time is not None:
                    last_collision_age = sim_time - self.last_collision_time
                state = {
                    "frame": frame,
                    "sim_time_s": sim_time,
                    "ego_transform": self.ego.get_transform(),
                    "speed_kmh": speed_kmh(self.ego),
                    "speed_limit_kmh": float(self.ego.get_speed_limit() or 30.0),
                    "route_target": target,
                    "route_target_index": target_index,
                    "route_index": route_index,
                    "route_progress": route_progress,
                    "distance_to_route_m": off_route_distance,
                    "last_collision_type": self.last_collision_type,
                    "last_collision_age_s": last_collision_age,
                    "at_traffic_light": self.ego.is_at_traffic_light(),
                    "traffic_light_state": traffic_light_state,
                    "nearest_obstacle_distance_m": self.obstacle_distance,
                    "distance_traveled_m": self.distance_traveled_m,
                    "distance_points": distance_points_for(
                        self.config,
                        self.distance_traveled_m,
                    ),
                }

                control = self.policy.run_step(state)
                if control is not None:
                    self.ego.apply_control(control)

                self.process_sensor_events(sim_time, frame, route_progress)
                self.process_rule_events(
                    sim_time,
                    frame,
                    route_progress,
                    off_route_distance,
                )

                if tick_index % int(self.config["output"]["trajectory_every_ticks"]) == 0:
                    self.append_trajectory(frame, sim_time, route_progress, target_index)

                if self.viewer is not None:
                    hud_state = dict(state)
                    hud_state.update(
                        {
                            "penalty_points": self.event_recorder.penalty_sum(),
                            "event_count": len(self.event_recorder.rows),
                            "output_dir": str(self.output_dir),
                            "checkpoint_index": checkpoint_index,
                            "checkpoint_count": len(self.checkpoints),
                            "policy_debug": getattr(self.policy, "debug_info", {}),
                            "control_throttle": getattr(control, "throttle", 0.0),
                            "control_brake": getattr(control, "brake", 0.0),
                            "control_steer": getattr(control, "steer", 0.0),
                            "control_reverse": getattr(control, "reverse", False),
                        }
                    )
                    if not self.viewer.tick(hud_state):
                        print("Pygame window closed; ending run and writing outputs.")
                        break

                if checkpoint_index >= len(self.checkpoints):
                    if not self.completed:
                        self.completed = True
                        self.lap_time = sim_time - start_time
                        print(f"Route completed at {self.lap_time:.2f}s")

                self.obstacle_distance = None

            summary = self.compute_score(last_sim_time)
            leaderboard_submission = submit_leaderboard_score(self.config, summary)
            summary["leaderboard_submission"] = leaderboard_submission
            self.write_outputs(summary)
            print(f"Output directory: {self.output_dir.resolve()}")
            print(f"Leaderboard submission: {leaderboard_submission['message']}")
            print(json.dumps(summary, indent=2, ensure_ascii=False))
            if self.viewer is not None:
                self.viewer.show_score_screen(summary, self.output_dir)
        finally:
            self.cleanup()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/default_config.json")
    parser.add_argument("--max-ticks", type=int, default=None)
    parser.add_argument("--render", action="store_true", help="Force-enable the pygame viewer")
    parser.add_argument("--no-render", action="store_true", help="Run without the pygame viewer")
    parser.add_argument(
        "--no-score-screen",
        action="store_true",
        help="Do not pause on the final pygame score report screen",
    )
    parser.add_argument(
        "--no-student-dialog",
        action="store_true",
        help="Skip the startup student id/name dialog",
    )
    parser.add_argument("--render-width", type=int, default=None)
    parser.add_argument("--render-height", type=int, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    apply_render_overrides(config, args)
    if not args.no_student_dialog:
        prompt_student_identity(config)
    print_challenge_settings(config)
    runner = ChallengeRunner(config, max_ticks_override=args.max_ticks)
    runner.run()


if __name__ == "__main__":
    main()
    # libcarla can abort during Python interpreter shutdown after a completed run.
    # Cleanup above has already destroyed actors and restored world settings.
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
