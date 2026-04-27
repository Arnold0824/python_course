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


def push_latest(channel_queue, image):
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


def wait_for_aligned_pair(rgb_queue, seg_queue, target_frame, timeout=3.0):
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


def safe_destroy(actor):
    if actor is None:
        return
    try:
        actor.destroy()
    except RuntimeError:
        pass


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

    camera_transform = carla.Transform(
        carla.Location(x=1.5, y=0.0, z=2.4),
        carla.Rotation(pitch=0.0, yaw=0.0, roll=0.0),
    )

    try:
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = SYNC_DELTA
        world.apply_settings(settings)

        vehicle_bp = bp_lib.find("vehicle.tesla.model3")
        vehicle_bp.set_attribute("role_name", "hero")

        spawn_points = world.get_map().get_spawn_points()
        random.shuffle(spawn_points)

        for spawn_point in spawn_points:
            ego_vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
            if ego_vehicle is not None:
                break

        if ego_vehicle is None:
            raise RuntimeError("主车生成失败，请重试")

        actor_list.append(ego_vehicle)

        rgb_bp = bp_lib.find("sensor.camera.rgb")
        seg_bp = bp_lib.find("sensor.camera.semantic_segmentation")

        for bp in (rgb_bp, seg_bp):
            bp.set_attribute("image_size_x", IMAGE_SIZE_X)
            bp.set_attribute("image_size_y", IMAGE_SIZE_Y)
            bp.set_attribute("fov", CAMERA_FOV)
            bp.set_attribute("sensor_tick", "0.0")

        rgb_camera = world.spawn_actor(
            rgb_bp,
            camera_transform,
            attach_to=ego_vehicle,
            attachment_type=carla.AttachmentType.Rigid,
        )
        seg_camera = world.spawn_actor(
            seg_bp,
            camera_transform,
            attach_to=ego_vehicle,
            attachment_type=carla.AttachmentType.Rigid,
        )
        actor_list.extend([rgb_camera, seg_camera])

        rgb_camera.listen(lambda image: push_latest(rgb_queue, image))
        seg_camera.listen(lambda image: push_latest(seg_queue, image))

        traffic_manager = client.get_trafficmanager(TRAFFIC_MANAGER_PORT)
        traffic_manager.set_synchronous_mode(True)
        ego_vehicle.set_autopilot(True, traffic_manager.get_port())
        traffic_manager.ignore_lights_percentage(ego_vehicle, IGNORE_LIGHTS_PERCENTAGE)

        for _ in range(AUTOPILOT_WARMUP_TICKS):
            frame_id = world.tick()
            wait_for_aligned_pair(rgb_queue, seg_queue, frame_id)

        captured_frames = []
        drive_ticks = 0
        while len(captured_frames) < TARGET_PAIRS:
            frame_id = world.tick()
            drive_ticks += 1
            rgb_image, seg_image = wait_for_aligned_pair(
                rgb_queue, seg_queue, frame_id
            )

            if drive_ticks % CAPTURE_INTERVAL_TICKS != 0:
                continue

            frame_name = f"{rgb_image.frame:06d}.png"
            rgb_image.save_to_disk(str(RGB_DIR / frame_name))
            seg_image.save_to_disk(str(SEG_DIR / frame_name))
            captured_frames.append(rgb_image.frame)

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
                "x": camera_transform.location.x,
                "y": camera_transform.location.y,
                "z": camera_transform.location.z,
                "pitch": camera_transform.rotation.pitch,
                "yaw": camera_transform.rotation.yaw,
                "roll": camera_transform.rotation.roll,
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

        print("采集完成，共保存配对帧：", len(captured_frames))
        print(report)

    finally:
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


if __name__ == "__main__":
    main()
