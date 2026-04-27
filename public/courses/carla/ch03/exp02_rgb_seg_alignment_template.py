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


def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    bp_lib = world.get_blueprint_library()

    RGB_DIR.mkdir(parents=True, exist_ok=True)
    SEG_DIR.mkdir(parents=True, exist_ok=True)

    original_settings = world.get_settings()
    actor_list = []
    rgb_queue = queue.Queue(maxsize=1)
    seg_queue = queue.Queue(maxsize=1)
    traffic_manager = None
    ego_vehicle = None

    try:
        # 第 0 步：先准备 4 个小工具
        # 1. safe_destroy(actor): 销毁 actor 时更稳
        # 2. push_latest(channel_queue, image): 只保留最新帧
        # 3. wait_for_image(channel_queue, target_frame): 等某一路追上目标帧
        # 4. wait_for_aligned_pair(rgb_queue, seg_queue, target_frame): 等两路图像对齐到同一帧

        # 第 1 步：开启同步模式和固定步长
        # settings = world.get_settings()
        # settings.synchronous_mode = __________
        # settings.fixed_delta_seconds = _______
        # world.apply_settings(settings)

        # 第 2 步：生成主车 ego_vehicle
        # vehicle_bp = __________________________________
        # vehicle_bp.set_attribute("role_name", "hero")
        # spawn_points = _________________________________
        # random.shuffle(spawn_points)
        # ego_vehicle = None
        # for spawn_point in spawn_points:
        #     ego_vehicle = _____________________________
        #     if ego_vehicle is not None:
        #         break
        #
        # if ego_vehicle is None:
        #     raise RuntimeError("主车生成失败")
        # actor_list.append(ego_vehicle)

        # 第 3 步：准备 RGB 与语义分割蓝图
        # rgb_bp = ______________________________________
        # seg_bp = ______________________________________
        # for bp in (rgb_bp, seg_bp):
        #     bp.set_attribute("image_size_x", IMAGE_SIZE_X)
        #     bp.set_attribute("image_size_y", IMAGE_SIZE_Y)
        #     bp.set_attribute("fov", CAMERA_FOV)
        #     bp.set_attribute("sensor_tick", "0.0")

        # 第 4 步：定义公共 camera_transform 并挂载双相机
        # camera_transform = carla.Transform(
        #     carla.Location(x=____, y=____, z=____),
        #     carla.Rotation(pitch=____, yaw=____, roll=____),
        # )
        # rgb_camera = world.spawn_actor(..., attach_to=ego_vehicle, ...)
        # seg_camera = world.spawn_actor(..., attach_to=ego_vehicle, ...)
        # actor_list.extend([rgb_camera, seg_camera])

        # 第 5 步：分别为 rgb_queue 和 seg_queue 注册监听
        # rgb_camera.listen(lambda image: ______________________________)
        # seg_camera.listen(lambda image: ______________________________)

        # 第 6 步：启动 Traffic Manager，并让主车进入自动驾驶
        # traffic_manager = client.get_trafficmanager(TRAFFIC_MANAGER_PORT)
        # traffic_manager.set_synchronous_mode(True)
        # ego_vehicle.set_autopilot(True, traffic_manager.get_port())
        # traffic_manager.ignore_lights_percentage(ego_vehicle, IGNORE_LIGHTS_PERCENTAGE)

        # 第 7 步：先做热身，让自动驾驶和双通道都进入稳定状态
        # for _ in range(AUTOPILOT_WARMUP_TICKS):
        #     frame_id = world.tick()
        #     wait_for_aligned_pair(rgb_queue, seg_queue, frame_id)

        # 第 8 步：正式采集不少于 30 对图像
        # 提示：不要每 tick 都保存，可以每隔 CAPTURE_INTERVAL_TICKS 帧保存一对
        # captured_frames = []
        # drive_ticks = 0
        # while len(captured_frames) < TARGET_PAIRS:
        #     frame_id = world.tick()
        #     drive_ticks += 1
        #     rgb_image, seg_image = wait_for_aligned_pair(
        #         rgb_queue, seg_queue, frame_id
        #     )
        #     if drive_ticks % CAPTURE_INTERVAL_TICKS != 0:
        #         continue
        #     frame_name = f"{rgb_image.frame:06d}.png"
        #     rgb_image.save_to_disk(str(RGB_DIR / frame_name))
        #     seg_image.save_to_disk(str(SEG_DIR / frame_name))
        #     captured_frames.append(rgb_image.frame)

        # 第 9 步：统计结果并输出 params.json 与 alignment_report.json
        # rgb_frames = {path.stem for path in RGB_DIR.glob("*.png")}
        # seg_frames = {path.stem for path in SEG_DIR.glob("*.png")}
        # params = { ... }
        # report = { ... }
        # (OUTPUT_ROOT / "params.json").write_text(...)
        # (OUTPUT_ROOT / "alignment_report.json").write_text(...)

        pass

    finally:
        # 第 10 步：先关闭自动驾驶，再停止并销毁 actor，最后恢复原始世界设置
        # if traffic_manager is not None and ego_vehicle is not None:
        #     ego_vehicle.set_autopilot(False, traffic_manager.get_port())
        #     traffic_manager.set_synchronous_mode(False)
        for actor in reversed(actor_list):
            if isinstance(actor, carla.Sensor):
                actor.stop()
            actor.destroy()

        actor_list.clear()
        world.apply_settings(original_settings)


if __name__ == "__main__":
    main()
