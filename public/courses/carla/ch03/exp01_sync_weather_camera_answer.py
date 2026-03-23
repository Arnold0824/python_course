import os
import queue
import random
import time

import carla


def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    bp_lib = world.get_blueprint_library()

    os.makedirs("output/exp01", exist_ok=True)

    original_settings = world.get_settings()
    actor_list = []
    image_queue = queue.Queue(maxsize=1)

    try:
        def push_latest_image(image):
            while not image_queue.empty():
                try:
                    image_queue.get_nowait()
                except queue.Empty:
                    break

            try:
                image_queue.put_nowait(image)
            except queue.Full:
                pass

        def wait_for_image(target_frame, timeout=2.0):
            deadline = time.time() + timeout
            latest_image = None

            while time.time() < deadline:
                remaining = max(0.0, deadline - time.time())
                try:
                    image = image_queue.get(timeout=remaining)
                except queue.Empty:
                    break

                latest_image = image
                if image.frame >= target_frame:
                    return image

            if latest_image is not None:
                return latest_image

            raise TimeoutError("未在规定时间内收到相机图像")

        new_settings = world.get_settings()
        new_settings.synchronous_mode = True
        new_settings.fixed_delta_seconds = 0.05
        world.apply_settings(new_settings)

        vehicle_bp = bp_lib.find("vehicle.tesla.model3")
        vehicle_bp.set_attribute("role_name", "hero")

        spawn_points = world.get_map().get_spawn_points()
        random.shuffle(spawn_points)

        ego_vehicle = None
        for sp in spawn_points:
            ego_vehicle = world.try_spawn_actor(vehicle_bp, sp)
            if ego_vehicle is not None:
                break

        if ego_vehicle is None:
            raise RuntimeError("车辆生成失败")

        actor_list.append(ego_vehicle)

        sensor_bp = bp_lib.find("sensor.camera.rgb")
        sensor_bp.set_attribute("image_size_x", "800")
        sensor_bp.set_attribute("image_size_y", "600")
        sensor_bp.set_attribute("sensor_tick", "0.0")

        camera = world.spawn_actor(
            sensor_bp,
            carla.Transform(
                carla.Location(x=1.5, y=0.0, z=2.4),
                carla.Rotation(pitch=0.0, yaw=0.0, roll=0.0),
            ),
            attach_to=ego_vehicle,
            attachment_type=carla.AttachmentType.Rigid,
        )
        actor_list.append(camera)

        camera.listen(push_latest_image)

        weather_presets = [
            ("ClearNoon", carla.WeatherParameters.ClearNoon),
            ("CloudySunset", carla.WeatherParameters.CloudySunset),
            ("WetCloudyNoon", carla.WeatherParameters.WetCloudyNoon),
            ("HardRainNoon", carla.WeatherParameters.HardRainNoon),
        ]

        for label, weather in weather_presets:
            world.set_weather(weather)

            latest_image = None
            for _ in range(6):
                frame_id = world.tick()
                latest_image = wait_for_image(frame_id)

            save_path = f"output/exp01/{label}_{latest_image.frame:06d}.png"
            latest_image.save_to_disk(save_path)
            print(f"{label} 已保存：{save_path}")

    finally:
        world.apply_settings(original_settings)

        for actor in reversed(actor_list):
            if isinstance(actor, carla.Sensor):
                actor.stop()
            actor.destroy()


if __name__ == "__main__":
    main()
