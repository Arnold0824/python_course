import csv
import json
import math
from pathlib import Path

import carla


OUTPUT_ROOT = Path("output/exp03")

FIXED_DELTA_SECONDS = 0.05
RUN_SECONDS = 30
WARMUP_TICKS = 30
SAMPLE_EVERY_TICKS = 5
RUN_TICKS = int(RUN_SECONDS / FIXED_DELTA_SECONDS)

TRAFFIC_MANAGER_PORT = 8000
BACKGROUND_VEHICLE_COUNT = 12

# 任务 1：补全至少两套参数方案。可以参考“保守慢行”和“普通通勤”的写法继续扩展。
SCENARIOS = [
    {
        "name": "保守慢行",
        "speed_difference": 35.0,
        "distance_to_leading_vehicle": 6.0,
        "auto_lane_change": False,
        "ignore_lights_percentage": 0.0,
        "note": "车距更大、速度更慢，观察是否更稳但效率较低。",
    },
    {
        "name": "普通通勤",
        "speed_difference": 0.0,
        "distance_to_leading_vehicle": 3.0,
        "auto_lane_change": True,
        "ignore_lights_percentage": 0.0,
        "note": "作为基准方案，用来和其他方案比较。",
    },
]

SUMMARY_FIELDS = [
    "方案",
    "速度差%",
    "跟车距离m",
    "允许自动变道",
    "忽略红灯%",
    "样本数",
    "平均速度kmh",
    "最高速度kmh",
    "最低速度kmh",
    "行驶距离m",
    "低速样本占比",
    "趣味标签",
    "说明",
]

SAMPLE_FIELDS = [
    "scenario",
    "tick",
    "sim_time_s",
    "frame",
    "speed_kmh",
    "x",
    "y",
    "z",
]


def speed_kmh(actor):
    velocity = actor.get_velocity()
    speed_mps = math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2)
    return speed_mps * 3.6


def point_from_actor(actor):
    location = actor.get_location()
    return (location.x, location.y, location.z)


def walked_distance(points):
    total = 0.0
    for current, following in zip(points, points[1:]):
        dx = following[0] - current[0]
        dy = following[1] - current[1]
        dz = following[2] - current[2]
        total += math.sqrt(dx * dx + dy * dy + dz * dz)
    return total


def fun_label(avg_speed, distance_m, low_speed_ratio):
    # 任务 2：可以按照自己的理解调整标签规则，但不要让标签代替统计数据。
    if low_speed_ratio > 0.4:
        return "等待型"
    if avg_speed >= 32 and distance_m >= 250:
        return "冲刺型"
    if avg_speed <= 12:
        return "慢热型"
    return "均衡型"


def enable_sync_mode(world):
    original_settings = world.get_settings()

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = FIXED_DELTA_SECONDS
    world.apply_settings(settings)

    return original_settings


def restore_world(world, traffic_manager, original_settings):
    if traffic_manager is not None:
        traffic_manager.set_synchronous_mode(False)
    world.apply_settings(original_settings)


def safe_destroy(actor):
    if actor is None:
        return
    try:
        actor.destroy()
    except RuntimeError:
        pass


def tick_world(world, timeout=10.0):
    return world.tick(timeout)


def spawn_ego_vehicle(world, bp_lib, spawn_points):
    ego_bp = bp_lib.find("vehicle.tesla.model3")
    ego_bp.set_attribute("role_name", "hero")

    for spawn_point in spawn_points:
        ego_vehicle = world.try_spawn_actor(ego_bp, spawn_point)
        if ego_vehicle is not None:
            return ego_vehicle

    raise RuntimeError("主车生成失败，请重新运行或更换地图")


def spawn_background_vehicles(world, bp_lib, spawn_points, traffic_manager):
    vehicle_bps = bp_lib.filter("vehicle.*")
    background_vehicles = []

    for spawn_point in spawn_points:
        if len(background_vehicles) >= BACKGROUND_VEHICLE_COUNT:
            break

        vehicle_bp = vehicle_bps[len(background_vehicles) % len(vehicle_bps)]
        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        if vehicle is None:
            continue

        vehicle.set_autopilot(True, traffic_manager.get_port())
        traffic_manager.vehicle_percentage_speed_difference(vehicle, 10.0)
        background_vehicles.append(vehicle)

    return background_vehicles


def apply_scenario(traffic_manager, ego_vehicle, scenario):
    ego_vehicle.set_autopilot(True, traffic_manager.get_port())

    # 任务 3：把 scenario 中的四个参数真正设置到 Traffic Manager。
    traffic_manager.vehicle_percentage_speed_difference(
        ego_vehicle,
        scenario["speed_difference"],
    )
    traffic_manager.distance_to_leading_vehicle(
        ego_vehicle,
        scenario["distance_to_leading_vehicle"],
    )
    traffic_manager.auto_lane_change(
        ego_vehicle,
        scenario["auto_lane_change"],
    )
    traffic_manager.ignore_lights_percentage(
        ego_vehicle,
        scenario["ignore_lights_percentage"],
    )


def collect_samples(world, ego_vehicle, scenario, run_ticks=RUN_TICKS):
    samples = []
    positions = []

    for _ in range(WARMUP_TICKS):
        tick_world(world)

    progress_step = max(1, run_ticks // 5)

    for tick_index in range(run_ticks):
        frame_id = tick_world(world)

        if (tick_index + 1) % progress_step == 0 or tick_index == run_ticks - 1:
            percent = (tick_index + 1) / run_ticks * 100
            print(f"  {scenario['name']} 进度 {percent:5.1f}%")

        if tick_index % SAMPLE_EVERY_TICKS != 0:
            continue

        speed = speed_kmh(ego_vehicle)
        point = point_from_actor(ego_vehicle)
        positions.append(point)

        samples.append(
            {
                "scenario": scenario["name"],
                "tick": tick_index,
                "sim_time_s": round(tick_index * FIXED_DELTA_SECONDS, 2),
                "frame": frame_id,
                "speed_kmh": round(speed, 2),
                "x": round(point[0], 2),
                "y": round(point[1], 2),
                "z": round(point[2], 2),
            }
        )

    return samples, positions


def summarize_scenario(scenario, samples, positions):
    speeds = [row["speed_kmh"] for row in samples]
    low_speed_count = sum(1 for speed in speeds if speed < 1.0)
    low_speed_ratio = low_speed_count / len(speeds)
    avg_speed = sum(speeds) / len(speeds)
    distance_m = walked_distance(positions)

    # 任务 4：理解每个统计字段的意义，并在实验报告中引用至少两个指标。
    return {
        "方案": scenario["name"],
        "速度差%": scenario["speed_difference"],
        "跟车距离m": scenario["distance_to_leading_vehicle"],
        "允许自动变道": scenario["auto_lane_change"],
        "忽略红灯%": scenario["ignore_lights_percentage"],
        "样本数": len(samples),
        "平均速度kmh": round(avg_speed, 2),
        "最高速度kmh": round(max(speeds), 2),
        "最低速度kmh": round(min(speeds), 2),
        "行驶距离m": round(distance_m, 2),
        "低速样本占比": round(low_speed_ratio, 3),
        "趣味标签": fun_label(avg_speed, distance_m, low_speed_ratio),
        "说明": scenario["note"],
    }


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_outputs(summary_rows, sample_rows):
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUT_ROOT / "summary.csv", summary_rows, SUMMARY_FIELDS)
    write_csv(OUTPUT_ROOT / "samples.csv", sample_rows, SAMPLE_FIELDS)

    (OUTPUT_ROOT / "summary.json").write_text(
        json.dumps(summary_rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def run_one_scenario(client, scenario, run_ticks=RUN_TICKS):
    world = client.get_world()
    bp_lib = world.get_blueprint_library()
    traffic_manager = client.get_trafficmanager(TRAFFIC_MANAGER_PORT)
    original_settings = enable_sync_mode(world)
    traffic_manager.set_synchronous_mode(True)

    actors = []
    try:
        spawn_points = list(world.get_map().get_spawn_points())
        if len(spawn_points) < 2:
            raise RuntimeError("地图出生点不足，无法完成实验")

        ego_vehicle = spawn_ego_vehicle(world, bp_lib, spawn_points)
        actors.append(ego_vehicle)

        background_vehicles = spawn_background_vehicles(
            world,
            bp_lib,
            spawn_points[1:],
            traffic_manager,
        )
        actors.extend(background_vehicles)

        tick_world(world)
        apply_scenario(traffic_manager, ego_vehicle, scenario)
        samples, positions = collect_samples(world, ego_vehicle, scenario, run_ticks)
        summary = summarize_scenario(scenario, samples, positions)
        return summary, samples

    finally:
        for actor in actors:
            if isinstance(actor, carla.Vehicle):
                try:
                    actor.set_autopilot(False, traffic_manager.get_port())
                except RuntimeError:
                    pass

        for actor in reversed(actors):
            safe_destroy(actor)

        restore_world(world, traffic_manager, original_settings)


def print_leaderboard(summary_rows):
    ranked = sorted(summary_rows, key=lambda row: row["行驶距离m"], reverse=True)

    print("\n=== 参数方案行驶距离排行榜 ===")
    for index, row in enumerate(ranked, start=1):
        print(
            f"{index}. {row['方案']} | "
            f"距离 {row['行驶距离m']} m | "
            f"均速 {row['平均速度kmh']} km/h | "
            f"标签 {row['趣味标签']}"
        )


def main(run_seconds=RUN_SECONDS, scenario_limit=None):
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    summary_rows = []
    sample_rows = []
    run_ticks = int(run_seconds / FIXED_DELTA_SECONDS)
    scenarios = SCENARIOS if scenario_limit is None else SCENARIOS[:scenario_limit]

    print(f"本次运行 {len(scenarios)} 组方案，每组 {run_seconds} 秒，约 {run_ticks} ticks")

    for index, scenario in enumerate(scenarios, start=1):
        print(f"\n开始运行方案 {index}/{len(scenarios)}：{scenario['name']}")
        summary, samples = run_one_scenario(client, scenario, run_ticks)
        summary_rows.append(summary)
        sample_rows.extend(samples)

    save_outputs(summary_rows, sample_rows)
    print_leaderboard(summary_rows)
    print(f"\n结果已保存到：{OUTPUT_ROOT.resolve()}")


if __name__ == "__main__":
    main()
