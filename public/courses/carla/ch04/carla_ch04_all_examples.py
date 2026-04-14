# %% [markdown]
# 第三章 RGB 与语义分割双通道采集对齐
# 建议在 Jupyter / IPython Notebook 中按顺序逐段执行。
# 这一章的主线非常明确：
# 1. 开启同步模式
# 2. 生成主车
# 3. 挂 RGB 和语义分割双相机
# 4. 等待同一帧的两路图像
# 5. 按帧号配对保存
# 6. 输出参数记录和对齐报告

# %% Cell 1: 导入依赖并定义实验常量
import json
import queue
import random
import time
from pathlib import Path

import carla

OUTPUT_ROOT = Path("output/exp02")
RGB_DIR = OUTPUT_ROOT / "rgb"
SEG_DIR = OUTPUT_ROOT / "seg"

TARGET_PAIRS = 30
AUTOPILOT_WARMUP_TICKS = 20
CAPTURE_INTERVAL_TICKS = 8
SYNC_DELTA = 0.05
TRAFFIC_MANAGER_PORT = 8000
IGNORE_LIGHTS_PERCENTAGE = 100.0
IMAGE_SIZE_X = "800"
IMAGE_SIZE_Y = "600"
CAMERA_FOV = "90"

CAMERA_TRANSFORM = carla.Transform(
    carla.Location(x=1.5, y=0.0, z=2.4),
    carla.Rotation(pitch=0.0, yaw=0.0, roll=0.0),
)


# %% Cell 2: 连接 CARLA，准备输出目录和共享变量
client = carla.Client("localhost", 2000)
client.set_timeout(10.0)
world = client.get_world()
bp_lib = world.get_blueprint_library()

RGB_DIR.mkdir(parents=True, exist_ok=True)
SEG_DIR.mkdir(parents=True, exist_ok=True)

actor_list = []
original_settings = world.get_settings()
rgb_queue = queue.Queue(maxsize=1)
seg_queue = queue.Queue(maxsize=1)
traffic_manager = None
ego_vehicle = None

print("当前地图：", world.get_map().name)
print("输出目录：", OUTPUT_ROOT.resolve())


# %% Cell 3: 准备小工具函数
def safe_destroy(actor):
    if actor is None:
        return
    try:
        actor.destroy()
    except RuntimeError:
        pass


def push_latest(channel_queue, image):
    """只保留最新帧，避免旧帧在队列中堆积。"""
    while not channel_queue.empty():
        try:
            channel_queue.get_nowait()
        except queue.Empty:
            break

    try:
        channel_queue.put_nowait(image)
    except queue.Full:
        pass


def wait_for_image(channel_queue, target_frame, timeout=2.0):
    """等待某一路图像追上目标帧号。"""
    deadline = time.time() + timeout

    while time.time() < deadline:
        remaining = max(0.0, deadline - time.time())
        try:
            image = channel_queue.get(timeout=remaining)
        except queue.Empty as exc:
            raise TimeoutError(f"未在 {timeout:.1f} 秒内收到目标图像") from exc

        if image.frame >= target_frame:
            return image

    raise TimeoutError(f"等待目标帧 {target_frame} 超时")


def wait_for_aligned_pair(target_frame, timeout=3.0):
    """等待同一帧的 RGB 与语义分割图像。"""
    deadline = time.time() + timeout
    rgb_image = wait_for_image(rgb_queue, target_frame, timeout=timeout)
    seg_image = wait_for_image(seg_queue, target_frame, timeout=timeout)

    while time.time() < deadline:
        if rgb_image.frame == seg_image.frame:
            return rgb_image, seg_image

        remaining = max(0.1, deadline - time.time())
        if rgb_image.frame < seg_image.frame:
            rgb_image = wait_for_image(rgb_queue, seg_image.frame, timeout=remaining)
        else:
            seg_image = wait_for_image(seg_queue, rgb_image.frame, timeout=remaining)

    raise TimeoutError("两路图像未能在规定时间内对齐到同一帧")


def cleanup():
    if traffic_manager is not None and ego_vehicle is not None:
        try:
            ego_vehicle.set_autopilot(False, traffic_manager.get_port())
        except RuntimeError:
            pass
        try:
            traffic_manager.set_synchronous_mode(False)
        except RuntimeError:
            pass

    for actor in reversed(actor_list):
        if isinstance(actor, carla.Sensor):
            actor.stop()
        safe_destroy(actor)

    actor_list.clear()
    world.apply_settings(original_settings)


# %% Cell 4: 开启同步模式并生成主车
settings = world.get_settings()
settings.synchronous_mode = True
settings.fixed_delta_seconds = SYNC_DELTA
world.apply_settings(settings)

vehicle_bp = bp_lib.find("vehicle.tesla.model3")
vehicle_bp.set_attribute("role_name", "hero")

spawn_points = world.get_map().get_spawn_points()
random.shuffle(spawn_points)

ego_vehicle = None
for spawn_point in spawn_points:
    ego_vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
    if ego_vehicle is not None:
        break

if ego_vehicle is None:
    raise RuntimeError("主车生成失败，请更换地图或重新运行")

actor_list.append(ego_vehicle)
print("主车已生成：", ego_vehicle.type_id)
print("主车位姿：", ego_vehicle.get_transform())


# %% Cell 5: 准备双通道相机蓝图并挂载到主车
rgb_bp = bp_lib.find("sensor.camera.rgb")
seg_bp = bp_lib.find("sensor.camera.semantic_segmentation")

for bp in (rgb_bp, seg_bp):
    bp.set_attribute("image_size_x", IMAGE_SIZE_X)
    bp.set_attribute("image_size_y", IMAGE_SIZE_Y)
    bp.set_attribute("fov", CAMERA_FOV)
    bp.set_attribute("sensor_tick", "0.0")

rgb_camera = world.spawn_actor(
    rgb_bp,
    CAMERA_TRANSFORM,
    attach_to=ego_vehicle,
    attachment_type=carla.AttachmentType.Rigid,
)
seg_camera = world.spawn_actor(
    seg_bp,
    CAMERA_TRANSFORM,
    attach_to=ego_vehicle,
    attachment_type=carla.AttachmentType.Rigid,
)

actor_list.extend([rgb_camera, seg_camera])
print("RGB 相机：", rgb_camera.type_id)
print("语义分割相机：", seg_camera.type_id)


# %% Cell 6: 注册双监听，并让主车进入自动驾驶
rgb_camera.listen(lambda image: push_latest(rgb_queue, image))
seg_camera.listen(lambda image: push_latest(seg_queue, image))

traffic_manager = client.get_trafficmanager(TRAFFIC_MANAGER_PORT)
traffic_manager.set_synchronous_mode(True)
ego_vehicle.set_autopilot(True, traffic_manager.get_port())
traffic_manager.ignore_lights_percentage(ego_vehicle, IGNORE_LIGHTS_PERCENTAGE)

print("Traffic Manager 端口：", traffic_manager.get_port())
print("主车已切入自动驾驶，并设置为无视红绿灯")
print("ignore_lights_percentage =", IGNORE_LIGHTS_PERCENTAGE)
print("准备先热身再间隔采样")


# %% Cell 7: 先让车辆跑起来，再每隔几帧保存一对图像
for warmup_index in range(AUTOPILOT_WARMUP_TICKS):
    frame_id = world.tick()
    rgb_image, seg_image = wait_for_aligned_pair(frame_id)
    if (warmup_index + 1) % 5 == 0:
        print(
            f"warmup {warmup_index + 1}/{AUTOPILOT_WARMUP_TICKS}: "
            f"rgb={rgb_image.frame}, seg={seg_image.frame}"
        )

captured_frames = []
drive_ticks = 0

while len(captured_frames) < TARGET_PAIRS:
    frame_id = world.tick()
    drive_ticks += 1
    rgb_image, seg_image = wait_for_aligned_pair(frame_id)

    if drive_ticks % CAPTURE_INTERVAL_TICKS != 0:
        continue

    frame_name = f"{rgb_image.frame:06d}.png"
    rgb_path = RGB_DIR / frame_name
    seg_path = SEG_DIR / frame_name

    rgb_image.save_to_disk(str(rgb_path))
    seg_image.save_to_disk(str(seg_path))
    captured_frames.append(rgb_image.frame)

    print(
        f"pair {len(captured_frames):02d}/{TARGET_PAIRS}: "
        f"tick={drive_ticks}, frame={rgb_image.frame}, "
        f"rgb={rgb_path.name}, seg={seg_path.name}"
    )


# %% Cell 8: 统计结果并输出参数记录
rgb_frames = {path.stem for path in RGB_DIR.glob("*.png")}
seg_frames = {path.stem for path in SEG_DIR.glob("*.png")}
matched_frames = sorted(rgb_frames & seg_frames)

params = {
    "map": world.get_map().name,
    "vehicle_blueprint": vehicle_bp.id,
    "rgb_blueprint": rgb_bp.id,
    "seg_blueprint": seg_bp.id,
    "image_size_x": int(IMAGE_SIZE_X),
    "image_size_y": int(IMAGE_SIZE_Y),
    "fov": int(CAMERA_FOV),
    "fixed_delta_seconds": SYNC_DELTA,
    "traffic_manager_port": traffic_manager.get_port() if traffic_manager else None,
    "ignore_lights_percentage": IGNORE_LIGHTS_PERCENTAGE,
    "autopilot_warmup_ticks": AUTOPILOT_WARMUP_TICKS,
    "capture_interval_ticks": CAPTURE_INTERVAL_TICKS,
    "capture_interval_seconds": CAPTURE_INTERVAL_TICKS * SYNC_DELTA,
    "target_pairs": TARGET_PAIRS,
    "captured_pairs": len(captured_frames),
    "camera_transform": {
        "x": CAMERA_TRANSFORM.location.x,
        "y": CAMERA_TRANSFORM.location.y,
        "z": CAMERA_TRANSFORM.location.z,
        "pitch": CAMERA_TRANSFORM.rotation.pitch,
        "yaw": CAMERA_TRANSFORM.rotation.yaw,
        "roll": CAMERA_TRANSFORM.rotation.roll,
    },
}

report = {
    "rgb_count": len(rgb_frames),
    "seg_count": len(seg_frames),
    "matched_count": len(matched_frames),
    "missing_in_seg": sorted(rgb_frames - seg_frames),
    "missing_in_rgb": sorted(seg_frames - rgb_frames),
    "captured_frame_min": min(captured_frames) if captured_frames else None,
    "captured_frame_max": max(captured_frames) if captured_frames else None,
    "total_drive_ticks_after_warmup": drive_ticks,
    "is_aligned": len(rgb_frames) == len(seg_frames) == len(matched_frames),
}

(OUTPUT_ROOT / "params.json").write_text(
    json.dumps(params, indent=2, ensure_ascii=False),
    encoding="utf-8",
)
(OUTPUT_ROOT / "alignment_report.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("参数记录已输出：", OUTPUT_ROOT / "params.json")
print("对齐报告已输出：", OUTPUT_ROOT / "alignment_report.json")
print(report)


# %% Cell 9: 清理资源
cleanup()
print("第三章示例代码已清理完成")
