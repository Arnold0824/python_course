import csv
import json
import math
from pathlib import Path

import carla


OUTPUT_ROOT = Path("output/exp04")

FIXED_DELTA_SECONDS = 0.05
RUN_SECONDS = 60
WARMUP_TICKS = 30
RUN_TICKS = int(RUN_SECONDS / FIXED_DELTA_SECONDS)

TRAFFIC_MANAGER_PORT = 8000

TRIGGER_DISTANCE_M = 25.0
EVENT_COOLDOWN_TICKS = 20

EVENT_FIELDS = [
    "frame",
    "tick",
    "sim_time_s",
    "speed_kmh",
    "light_state",
    "distance_m",
    "light_id",
    "ego_x",
    "ego_y",
]

LIGHT_STATE_LABELS = {
    carla.TrafficLightState.Red: "Red",
    carla.TrafficLightState.Yellow: "Yellow",
    carla.TrafficLightState.Green: "Green",
    carla.TrafficLightState.Off: "Off",
    carla.TrafficLightState.Unknown: "Unknown",
}


def speed_kmh(actor):
    velocity = actor.get_velocity()
    speed_mps = math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2)
    return speed_mps * 3.6


def distance_between(actor_a, actor_b):
    loc_a = actor_a.get_location()
    loc_b = actor_b.get_location()
    dx = loc_a.x - loc_b.x
    dy = loc_a.y - loc_b.y
    dz = loc_a.z - loc_b.z
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def light_state_label(state):
    return LIGHT_STATE_LABELS.get(state, "Unknown")


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


def get_traffic_lights(world):
    lights = list(world.get_actors().filter("traffic.traffic_light*"))
    if not lights:
        raise RuntimeError("当前地图没有交通灯，请切换到 Town03 / Town05 等城市地图")
    return lights


def find_nearest_traffic_light(ego_vehicle, traffic_lights):
    nearest_light = None
    nearest_distance = float("inf")

    for light in traffic_lights:
        distance = distance_between(ego_vehicle, light)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_light = light

    return nearest_light, nearest_distance


def collect_events(world, ego_vehicle, traffic_lights, run_ticks=RUN_TICKS):
    events = []
    last_event_tick = -EVENT_COOLDOWN_TICKS
    last_light_id = None

    for _ in range(WARMUP_TICKS):
        tick_world(world)

    progress_step = max(1, run_ticks // 5)

    for tick_index in range(run_ticks):
        frame_id = tick_world(world)

        if (tick_index + 1) % progress_step == 0 or tick_index == run_ticks - 1:
            percent = (tick_index + 1) / run_ticks * 100
            print(
                f"  红灯监测进度 {percent:5.1f}%  |  已记录事件 {len(events)} 条"
            )

        nearest_light, nearest_distance = find_nearest_traffic_light(
            ego_vehicle, traffic_lights
        )
        if nearest_light is None:
            continue
        if nearest_distance >= TRIGGER_DISTANCE_M:
            continue

        is_new_light = nearest_light.id != last_light_id
        is_cooled_down = tick_index - last_event_tick >= EVENT_COOLDOWN_TICKS
        if not (is_new_light or is_cooled_down):
            continue

        location = ego_vehicle.get_location()
        events.append(
            {
                "frame": frame_id,
                "tick": tick_index,
                "sim_time_s": round(tick_index * FIXED_DELTA_SECONDS, 2),
                "speed_kmh": round(speed_kmh(ego_vehicle), 2),
                "light_state": light_state_label(nearest_light.get_state()),
                "distance_m": round(nearest_distance, 2),
                "light_id": nearest_light.id,
                "ego_x": round(location.x, 2),
                "ego_y": round(location.y, 2),
            }
        )
        last_event_tick = tick_index
        last_light_id = nearest_light.id

    return events


def write_events_csv(path, events):
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=EVENT_FIELDS)
        writer.writeheader()
        writer.writerows(events)


def summarize_events(events, run_seconds):
    total = len(events)
    state_counts = {"Red": 0, "Yellow": 0, "Green": 0, "Off": 0, "Unknown": 0}
    for event in events:
        state_counts[event["light_state"]] = state_counts.get(event["light_state"], 0) + 1

    red_count = state_counts["Red"]
    red_ratio = round(red_count / total, 3) if total else 0.0

    speed_when_red = [event["speed_kmh"] for event in events if event["light_state"] == "Red"]
    avg_red_speed = round(sum(speed_when_red) / len(speed_when_red), 2) if speed_when_red else 0.0

    return {
        "run_seconds": run_seconds,
        "trigger_distance_m": TRIGGER_DISTANCE_M,
        "event_cooldown_ticks": EVENT_COOLDOWN_TICKS,
        "total_events": total,
        "red_events": red_count,
        "yellow_events": state_counts["Yellow"],
        "green_events": state_counts["Green"],
        "red_ratio": red_ratio,
        "avg_speed_when_red_kmh": avg_red_speed,
    }


def save_outputs(events, summary):
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    write_events_csv(OUTPUT_ROOT / "events.csv", events)

    (OUTPUT_ROOT / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "实验四 红灯状态监测与事件日志分析 汇总",
        f"运行时长（秒）: {summary['run_seconds']}",
        f"触发阈值（米）: {summary['trigger_distance_m']}",
        f"事件冷却（ticks）: {summary['event_cooldown_ticks']}",
        f"总事件数: {summary['total_events']}",
        f"红灯事件: {summary['red_events']}",
        f"黄灯事件: {summary['yellow_events']}",
        f"绿灯事件: {summary['green_events']}",
        f"红灯占比: {summary['red_ratio']}",
        f"红灯时平均车速 (km/h): {summary['avg_speed_when_red_kmh']}",
    ]
    (OUTPUT_ROOT / "summary.txt").write_text("\n".join(lines), encoding="utf-8")


def main(run_seconds=RUN_SECONDS):
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

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
        ego_vehicle.set_autopilot(True, traffic_manager.get_port())

        traffic_lights = get_traffic_lights(world)
        print(f"地图中共发现 {len(traffic_lights)} 个交通灯对象")

        run_ticks = int(run_seconds / FIXED_DELTA_SECONDS)
        print(f"本次运行 {run_seconds} 秒，约 {run_ticks} ticks")

        events = collect_events(world, ego_vehicle, traffic_lights, run_ticks)
        summary = summarize_events(events, run_seconds)
        save_outputs(events, summary)

        print("\n=== 实验四 汇总 ===")
        for key, value in summary.items():
            print(f"{key}: {value}")
        print(f"\n结果已保存到：{OUTPUT_ROOT.resolve()}")

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


if __name__ == "__main__":
    main()
