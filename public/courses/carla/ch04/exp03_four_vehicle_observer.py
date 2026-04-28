"""实验三趣味扩展：四宫格观察四种自动驾驶风格。

运行方式：
    python exp03_four_vehicle_observer.py --risk-level high
    python exp03_four_vehicle_observer.py --risk-level extreme

观察窗口默认使用异步模式，让 Traffic Manager 按真实时间驱动车辆。
按 ESC 或关闭窗口结束实验。脚本会自动清理车辆、行人和传感器。
"""

import argparse
import math
import os
import random
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple

import carla
import numpy as np
import pygame


FIXED_DELTA_SECONDS = 0.05
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 360
TRAFFIC_MANAGER_PORT = 8000


@dataclass
class DrivingStyle:
    name: str
    color: str
    vehicle_blueprint_id: str
    speed_difference: float
    desired_speed_kmh: Optional[float]
    distance_to_leading_vehicle: float
    auto_lane_change: bool
    ignore_lights_percentage: float
    ignore_signs_percentage: float
    ignore_vehicles_percentage: float
    ignore_walkers_percentage: float
    random_lanechange_percentage: float
    note: str


@dataclass
class VehiclePanel:
    style: DrivingStyle
    vehicle: carla.Vehicle
    camera: Optional[carla.Sensor] = None
    collision_sensor: Optional[carla.Sensor] = None
    lane_sensor: Optional[carla.Sensor] = None
    surface: Optional[pygame.Surface] = None
    collisions: int = 0
    lane_events: int = 0
    last_event: str = "暂无事件"
    distance_m: float = 0.0
    current_speed: float = 0.0
    max_speed: float = 0.0
    speed_sum: float = 0.0
    samples: int = 0
    low_speed_samples: int = 0
    stuck_ticks: int = 0
    nudge_ticks: int = 0
    last_location: Optional[carla.Location] = None

    @property
    def avg_speed(self):
        if self.samples == 0:
            return 0.0
        return self.speed_sum / self.samples

    @property
    def low_speed_ratio(self):
        if self.samples == 0:
            return 0.0
        return self.low_speed_samples / self.samples


DRIVING_STYLES = [
    DrivingStyle(
        name="保守慢行",
        color="76,175,80",
        vehicle_blueprint_id="vehicle.tesla.model3",
        speed_difference=35.0,
        desired_speed_kmh=None,
        distance_to_leading_vehicle=6.0,
        auto_lane_change=False,
        ignore_lights_percentage=0.0,
        ignore_signs_percentage=0.0,
        ignore_vehicles_percentage=0.0,
        ignore_walkers_percentage=0.0,
        random_lanechange_percentage=0.0,
        note="大车距 慢速度 不主动变道",
    ),
    DrivingStyle(
        name="普通通勤",
        color="33,150,243",
        vehicle_blueprint_id="vehicle.tesla.model3",
        speed_difference=0.0,
        desired_speed_kmh=None,
        distance_to_leading_vehicle=3.0,
        auto_lane_change=True,
        ignore_lights_percentage=0.0,
        ignore_signs_percentage=0.0,
        ignore_vehicles_percentage=0.0,
        ignore_walkers_percentage=0.0,
        random_lanechange_percentage=8.0,
        note="标准速度 标准车距",
    ),
    DrivingStyle(
        name="赶时间",
        color="255,152,0",
        vehicle_blueprint_id="vehicle.ford.mustang",
        speed_difference=-100.0,
        desired_speed_kmh=128.7,
        distance_to_leading_vehicle=0.4,
        auto_lane_change=True,
        ignore_lights_percentage=65.0,
        ignore_signs_percentage=75.0,
        ignore_vehicles_percentage=55.0,
        ignore_walkers_percentage=45.0,
        random_lanechange_percentage=75.0,
        note="Mustang 目标80mph 短车距猛开",
    ),
    DrivingStyle(
        name="路口冒险",
        color="244,67,54",
        vehicle_blueprint_id="vehicle.dodge.charger_2020",
        speed_difference=-45.0,
        desired_speed_kmh=128.7,
        distance_to_leading_vehicle=0.6,
        auto_lane_change=True,
        ignore_lights_percentage=100.0,
        ignore_signs_percentage=100.0,
        ignore_vehicles_percentage=80.0,
        ignore_walkers_percentage=80.0,
        random_lanechange_percentage=65.0,
        note="忽略信号 更少避让 观察风险",
    ),
]

RISK_DEFAULTS = {
    "normal": {
        "background_vehicles": 20,
        "walkers": 12,
        "pedestrian_cross_factor": 0.35,
        "traffic_distance": 2.5,
    },
    "high": {
        "background_vehicles": 35,
        "walkers": 35,
        "pedestrian_cross_factor": 0.85,
        "traffic_distance": 1.2,
    },
    "extreme": {
        "background_vehicles": 10,
        "walkers": 200,
        "pedestrian_cross_factor": 1.0,
        "traffic_distance": 0.6,
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description="四宫格观察四种自动驾驶风格")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=2000)
    parser.add_argument("--tm-port", type=int, default=TRAFFIC_MANAGER_PORT)
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument(
        "--risk-level",
        choices=["normal", "high", "extreme"],
        default="high",
        help="观察风险等级；等级越高，交通越密集，激进车辆越容易触发碰撞观察。",
    )
    parser.add_argument("--background-vehicles", type=int, default=None)
    parser.add_argument("--walkers", type=int, default=None)
    parser.add_argument("--pedestrian-cross-factor", type=float, default=None)
    parser.add_argument("--traffic-distance", type=float, default=None)
    parser.add_argument("--duration", type=float, default=0.0, help="运行秒数；0 表示一直运行到手动关闭")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--sync", action="store_true", help="可选：使用同步模式。观察窗口默认使用异步模式，车辆更容易正常运动。")
    parser.add_argument("--headless", action="store_true", help="测试用：使用隐藏窗口运行")
    args = parser.parse_args()

    defaults = RISK_DEFAULTS[args.risk_level]
    if args.background_vehicles is None:
        args.background_vehicles = defaults["background_vehicles"]
    if args.walkers is None:
        args.walkers = defaults["walkers"]
    if args.pedestrian_cross_factor is None:
        args.pedestrian_cross_factor = defaults["pedestrian_cross_factor"]
    if args.traffic_distance is None:
        args.traffic_distance = defaults["traffic_distance"]

    return args


def speed_kmh(actor):
    velocity = actor.get_velocity()
    speed_mps = math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2)
    return speed_mps * 3.6


def image_to_surface(image):
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    array = np.ascontiguousarray(array.swapaxes(0, 1))
    return pygame.surfarray.make_surface(array)


def safe_destroy(actor):
    if actor is None:
        return
    try:
        actor.destroy()
    except RuntimeError:
        pass


def safe_stop(sensor):
    if sensor is None:
        return
    try:
        sensor.stop()
    except RuntimeError:
        pass


def tm_try(method, *args):
    try:
        method(*args)
    except RuntimeError:
        pass


def set_vehicle_color(vehicle_bp, color):
    if vehicle_bp.has_attribute("color"):
        vehicle_bp.set_attribute("color", color)


def choose_font(size, bold=False):
    font_names = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial"]
    return pygame.font.SysFont(font_names, size, bold=bold)


def configure_world_for_observation(world, traffic_manager, sync_mode=False):
    original_settings = world.get_settings()
    settings = world.get_settings()
    settings.synchronous_mode = sync_mode
    settings.fixed_delta_seconds = FIXED_DELTA_SECONDS if sync_mode else None
    world.apply_settings(settings)

    if traffic_manager is not None:
        traffic_manager.set_synchronous_mode(sync_mode)

    return original_settings


def restore_world(world, traffic_manager, original_settings):
    if traffic_manager is not None:
        traffic_manager.set_synchronous_mode(False)
    world.apply_settings(original_settings)


def advance_world(world, sync_mode):
    if sync_mode:
        return world.tick(10.0)
    snapshot = world.wait_for_tick(10.0)
    return snapshot.frame


def make_camera_callback(panel):
    def callback(image):
        panel.surface = image_to_surface(image)

    return callback


def make_collision_callback(panel):
    def callback(event):
        impulse = event.normal_impulse
        intensity = math.sqrt(impulse.x ** 2 + impulse.y ** 2 + impulse.z ** 2)
        other_actor = event.other_actor.type_id if event.other_actor else "unknown"
        panel.collisions += 1
        panel.last_event = f"碰撞 {other_actor} 强度 {intensity:.0f}"

    return callback


def make_lane_callback(panel):
    def callback(event):
        markings = [str(marking.type).split(".")[-1] for marking in event.crossed_lane_markings]
        panel.lane_events += 1
        panel.last_event = "压线 " + ",".join(markings[:2])

    return callback


def find_vehicle_blueprint(bp_lib, blueprint_id):
    try:
        return bp_lib.find(blueprint_id)
    except IndexError:
        return bp_lib.find("vehicle.tesla.model3")


def spawn_vehicle(world, bp_lib, spawn_points, blueprint_id, color=None, role_name=None):
    vehicle_bp = find_vehicle_blueprint(bp_lib, blueprint_id)
    if color:
        set_vehicle_color(vehicle_bp, color)
    if role_name and vehicle_bp.has_attribute("role_name"):
        vehicle_bp.set_attribute("role_name", role_name)

    while spawn_points:
        spawn_point = spawn_points.pop(0)
        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        if vehicle is not None:
            return vehicle

    raise RuntimeError("车辆生成失败：可用出生点不足")


def spawn_main_vehicles(world, bp_lib, spawn_points):
    panels = []
    for index, style in enumerate(DRIVING_STYLES):
        vehicle = spawn_vehicle(
            world,
            bp_lib,
            spawn_points,
            blueprint_id=style.vehicle_blueprint_id,
            color=style.color,
            role_name=f"style_{index}",
        )
        panels.append(VehiclePanel(style=style, vehicle=vehicle))
    return panels


def spawn_background_vehicles(world, bp_lib, spawn_points, traffic_manager, count, risk_level):
    vehicles = []
    vehicle_bps = bp_lib.filter("vehicle.*")

    if risk_level == "extreme":
        speed_range = (-45.0, 18.0)
        distance_range = (0.6, 2.8)
        ignore_light_range = (0.0, 55.0)
        ignore_vehicle_range = (0.0, 45.0)
        ignore_walker_range = (0.0, 35.0)
        lanechange_range = (20.0, 80.0)
    elif risk_level == "high":
        speed_range = (-25.0, 25.0)
        distance_range = (1.0, 4.0)
        ignore_light_range = (0.0, 25.0)
        ignore_vehicle_range = (0.0, 20.0)
        ignore_walker_range = (0.0, 12.0)
        lanechange_range = (5.0, 45.0)
    else:
        speed_range = (-10.0, 30.0)
        distance_range = (2.0, 6.0)
        ignore_light_range = (0.0, 5.0)
        ignore_vehicle_range = (0.0, 5.0)
        ignore_walker_range = (0.0, 2.0)
        lanechange_range = (0.0, 20.0)

    while spawn_points and len(vehicles) < count:
        vehicle_bp = random.choice(vehicle_bps)
        if vehicle_bp.has_attribute("color"):
            colors = vehicle_bp.get_attribute("color").recommended_values
            if colors:
                vehicle_bp.set_attribute("color", random.choice(colors))
        if vehicle_bp.has_attribute("role_name"):
            vehicle_bp.set_attribute("role_name", "observer_background")

        spawn_point = spawn_points.pop(0)
        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        if vehicle is None:
            continue

        tm_try(vehicle.set_autopilot, True, traffic_manager.get_port())
        tm_try(traffic_manager.vehicle_percentage_speed_difference, vehicle, random.uniform(*speed_range))
        tm_try(traffic_manager.distance_to_leading_vehicle, vehicle, random.uniform(*distance_range))
        tm_try(traffic_manager.auto_lane_change, vehicle, random.choice([True, False]))
        tm_try(traffic_manager.ignore_lights_percentage, vehicle, random.uniform(*ignore_light_range))
        tm_try(traffic_manager.ignore_signs_percentage, vehicle, random.uniform(*ignore_light_range))
        tm_try(traffic_manager.ignore_vehicles_percentage, vehicle, random.uniform(*ignore_vehicle_range))
        tm_try(traffic_manager.ignore_walkers_percentage, vehicle, random.uniform(*ignore_walker_range))
        tm_try(traffic_manager.random_left_lanechange_percentage, vehicle, random.uniform(*lanechange_range))
        tm_try(traffic_manager.random_right_lanechange_percentage, vehicle, random.uniform(*lanechange_range))
        vehicles.append(vehicle)

    return vehicles


def spawn_walkers(world, bp_lib, count, risk_level, sync_mode):
    walkers = []
    controllers = []
    walker_bps = bp_lib.filter("walker.pedestrian.*")
    controller_bp = bp_lib.find("controller.ai.walker")

    for _ in range(count):
        location = world.get_random_location_from_navigation()
        if location is None:
            continue

        walker_bp = random.choice(walker_bps)
        if walker_bp.has_attribute("is_invincible"):
            walker_bp.set_attribute("is_invincible", "false")

        walker = world.try_spawn_actor(walker_bp, carla.Transform(location))
        if walker is None:
            continue

        controller = world.try_spawn_actor(controller_bp, carla.Transform(), attach_to=walker)
        if controller is None:
            safe_destroy(walker)
            continue

        walkers.append(walker)
        controllers.append(controller)

    advance_world(world, sync_mode)

    for controller in controllers:
        controller.start()
        destination = world.get_random_location_from_navigation()
        if destination is not None:
            controller.go_to_location(destination)
        if risk_level == "extreme":
            controller.set_max_speed(random.uniform(1.5, 3.2))
        elif risk_level == "high":
            controller.set_max_speed(random.uniform(1.2, 2.6))
        else:
            controller.set_max_speed(random.uniform(1.0, 2.2))

    return walkers, controllers


def attach_observation_sensors(world, bp_lib, panels, camera_width, camera_height):
    camera_bp = bp_lib.find("sensor.camera.rgb")
    camera_bp.set_attribute("image_size_x", str(camera_width))
    camera_bp.set_attribute("image_size_y", str(camera_height))
    camera_bp.set_attribute("fov", "105")
    camera_bp.set_attribute("sensor_tick", "0.0")

    collision_bp = bp_lib.find("sensor.other.collision")
    lane_bp = bp_lib.find("sensor.other.lane_invasion")
    camera_transform = carla.Transform(
        carla.Location(x=-8.0, y=0.0, z=3.6),
        carla.Rotation(pitch=-6.0, yaw=0.0, roll=0.0),
    )
    attachment_type = getattr(
        carla.AttachmentType,
        "SpringArmGhost",
        carla.AttachmentType.Rigid,
    )

    for panel in panels:
        panel.camera = world.spawn_actor(
            camera_bp,
            camera_transform,
            attach_to=panel.vehicle,
            attachment_type=attachment_type,
        )
        panel.collision_sensor = world.spawn_actor(
            collision_bp,
            carla.Transform(),
            attach_to=panel.vehicle,
        )
        panel.lane_sensor = world.spawn_actor(
            lane_bp,
            carla.Transform(),
            attach_to=panel.vehicle,
        )

        panel.camera.listen(make_camera_callback(panel))
        panel.collision_sensor.listen(make_collision_callback(panel))
        panel.lane_sensor.listen(make_lane_callback(panel))


def apply_driving_style(traffic_manager, panel):
    style = panel.style
    vehicle = panel.vehicle
    tm_try(vehicle.set_autopilot, True, traffic_manager.get_port())
    tm_try(traffic_manager.vehicle_percentage_speed_difference, vehicle, style.speed_difference)
    if style.desired_speed_kmh is not None:
        tm_try(traffic_manager.set_desired_speed, vehicle, style.desired_speed_kmh)
    tm_try(traffic_manager.distance_to_leading_vehicle, vehicle, style.distance_to_leading_vehicle)
    tm_try(traffic_manager.auto_lane_change, vehicle, style.auto_lane_change)
    tm_try(traffic_manager.ignore_lights_percentage, vehicle, style.ignore_lights_percentage)
    tm_try(traffic_manager.ignore_signs_percentage, vehicle, style.ignore_signs_percentage)
    tm_try(traffic_manager.ignore_vehicles_percentage, vehicle, style.ignore_vehicles_percentage)
    tm_try(traffic_manager.ignore_walkers_percentage, vehicle, style.ignore_walkers_percentage)
    tm_try(traffic_manager.random_left_lanechange_percentage, vehicle, style.random_lanechange_percentage)
    tm_try(traffic_manager.random_right_lanechange_percentage, vehicle, style.random_lanechange_percentage)


def update_panel_metrics(panel):
    location = panel.vehicle.get_location()
    if panel.last_location is not None:
        step = location.distance(panel.last_location)
        if step < 20.0:
            panel.distance_m += step
    panel.last_location = location

    panel.current_speed = speed_kmh(panel.vehicle)
    panel.max_speed = max(panel.max_speed, panel.current_speed)
    panel.speed_sum += panel.current_speed
    panel.samples += 1
    if panel.current_speed < 1.0:
        panel.low_speed_samples += 1
        panel.stuck_ticks += 1
    else:
        panel.stuck_ticks = 0


def keep_vehicle_active(traffic_manager, panel):
    if panel.nudge_ticks > 0:
        steer = 0.0
        if panel.style.name in {"赶时间", "路口冒险"}:
            steer = random.uniform(-0.18, 0.18)

        panel.vehicle.apply_control(
            carla.VehicleControl(throttle=0.88, steer=steer, brake=0.0)
        )
        panel.nudge_ticks -= 1

        if panel.nudge_ticks == 0:
            apply_driving_style(traffic_manager, panel)
            panel.last_event = "脱困后交回自动驾驶"
        return

    if panel.stuck_ticks >= 80:
        tm_try(panel.vehicle.set_autopilot, False, traffic_manager.get_port())
        panel.nudge_ticks = 28
        panel.stuck_ticks = 0
        panel.last_event = "低速脱困：短暂人工给油"


def traffic_light_text(vehicle):
    if not vehicle.is_at_traffic_light():
        return "无"
    traffic_light = vehicle.get_traffic_light()
    if traffic_light is None:
        return "未知"
    return str(traffic_light.get_state()).split(".")[-1]


def draw_text(surface, font, text, position, color=(255, 255, 255)):
    rendered = font.render(text, True, color)
    surface.blit(rendered, position)


def draw_panel(screen, panel, rect, fonts):
    title_font, info_font, small_font = fonts
    x, y, width, height = rect

    if panel.surface is not None:
        scaled = pygame.transform.smoothscale(panel.surface, (width, height))
        screen.blit(scaled, (x, y))
    else:
        pygame.draw.rect(screen, (16, 24, 39), rect)
        draw_text(screen, title_font, "等待相机图像...", (x + 18, y + 18))

    overlay_height = 118
    overlay_y = y + height - overlay_height
    overlay = pygame.Surface((width, overlay_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (x, overlay_y))

    border_color = (244, 67, 54) if panel.collisions else (56, 189, 248)
    pygame.draw.rect(screen, border_color, rect, width=4)

    draw_text(screen, title_font, panel.style.name, (x + 14, overlay_y + 8), border_color)
    draw_text(screen, small_font, panel.style.note, (x + 124, overlay_y + 13), (235, 245, 255))

    line_1 = (
        f"速度 {panel.current_speed:5.1f} km/h  "
        f"均速 {panel.avg_speed:5.1f}  "
        f"最高 {panel.max_speed:5.1f}"
    )
    line_2 = (
        f"距离 {panel.distance_m:6.1f} m  "
        f"碰撞 {panel.collisions}  "
        f"压线 {panel.lane_events}  "
        f"红灯 {traffic_light_text(panel.vehicle)}"
    )
    line_3 = f"低速占比 {panel.low_speed_ratio:4.0%}  最近事件：{panel.last_event}"

    draw_text(screen, info_font, line_1, (x + 14, overlay_y + 40), (255, 255, 255))
    draw_text(screen, info_font, line_2, (x + 14, overlay_y + 67), (255, 255, 255))
    draw_text(screen, small_font, line_3, (x + 14, overlay_y + 94), (235, 245, 255))


def draw_dashboard(screen, panels, fonts):
    width, height = screen.get_size()
    cell_w = width // 2
    cell_h = height // 2
    rects = [
        (0, 0, cell_w, cell_h),
        (cell_w, 0, width - cell_w, cell_h),
        (0, cell_h, cell_w, height - cell_h),
        (cell_w, cell_h, width - cell_w, height - cell_h),
    ]

    for panel, rect in zip(panels, rects):
        draw_panel(screen, panel, rect, fonts)

    pygame.display.flip()


def cleanup(world, traffic_manager, original_settings, panels, background_vehicles, walkers, controllers):
    for panel in panels:
        for sensor in (panel.camera, panel.collision_sensor, panel.lane_sensor):
            safe_stop(sensor)

    for panel in panels:
        try:
            panel.vehicle.set_autopilot(False, traffic_manager.get_port())
        except RuntimeError:
            pass

    for vehicle in background_vehicles:
        try:
            vehicle.set_autopilot(False, traffic_manager.get_port())
        except RuntimeError:
            pass

    for controller in controllers:
        try:
            controller.stop()
        except RuntimeError:
            pass

    sensor_actors = []
    for panel in panels:
        sensor_actors.extend([panel.camera, panel.collision_sensor, panel.lane_sensor])

    for actor in reversed(sensor_actors):
        safe_destroy(actor)
    for actor in reversed([panel.vehicle for panel in panels] + background_vehicles):
        safe_destroy(actor)
    for actor in reversed(controllers):
        safe_destroy(actor)
    for actor in reversed(walkers):
        safe_destroy(actor)

    restore_world(world, traffic_manager, original_settings)
    pygame.quit()


def main():
    args = parse_args()
    random.seed(args.seed)

    if args.headless:
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((args.width, args.height))
    pygame.display.set_caption(f"CARLA 四车驾驶风格观察实验 | {args.risk_level}")
    fonts = (
        choose_font(24, bold=True),
        choose_font(20),
        choose_font(17),
    )

    client = carla.Client(args.host, args.port)
    client.set_timeout(10.0)
    world = client.get_world()
    bp_lib = world.get_blueprint_library()
    traffic_manager = client.get_trafficmanager(args.tm_port)

    original_settings = configure_world_for_observation(world, traffic_manager, sync_mode=args.sync)
    world.set_pedestrians_seed(args.seed)
    world.set_pedestrians_cross_factor(args.pedestrian_cross_factor)
    traffic_manager.set_random_device_seed(args.seed)
    traffic_manager.set_global_distance_to_leading_vehicle(args.traffic_distance)
    print(
        "观察模式:",
        args.risk_level,
        "| 同步模式:",
        args.sync,
        "| 背景车:",
        args.background_vehicles,
        "| 行人:",
        args.walkers,
        "| 行人过街系数:",
        args.pedestrian_cross_factor,
    )

    panels = []
    background_vehicles = []
    walkers = []
    controllers = []

    try:
        spawn_points = list(world.get_map().get_spawn_points())
        random.shuffle(spawn_points)

        panels = spawn_main_vehicles(world, bp_lib, spawn_points)
        background_vehicles = spawn_background_vehicles(
            world,
            bp_lib,
            spawn_points,
            traffic_manager,
            args.background_vehicles,
            args.risk_level,
        )
        walkers, controllers = spawn_walkers(world, bp_lib, args.walkers, args.risk_level, args.sync)
        attach_observation_sensors(world, bp_lib, panels, CAMERA_WIDTH, CAMERA_HEIGHT)

        for panel in panels:
            apply_driving_style(traffic_manager, panel)

        for _ in range(20):
            advance_world(world, args.sync)

        clock = pygame.time.Clock()
        start_time = time.time()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            advance_world(world, args.sync)
            for panel in panels:
                update_panel_metrics(panel)
                keep_vehicle_active(traffic_manager, panel)

            draw_dashboard(screen, panels, fonts)
            clock.tick(30)

            if args.duration > 0 and time.time() - start_time >= args.duration:
                running = False

    finally:
        cleanup(world, traffic_manager, original_settings, panels, background_vehicles, walkers, controllers)


if __name__ == "__main__":
    main()
