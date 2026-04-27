import os
import queue
import time

import carla


def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    bp_lib = world.get_blueprint_library()

    # 第 1 步：准备输出目录
    os.makedirs("output/exp01", exist_ok=True)

    # 第 2 步：保存原始世界设置，实验结束后要恢复
    original_settings = world.get_settings()
    actor_list = []
    image_queue = queue.Queue(maxsize=1)

    try:
        # 第 3 步之前：先准备两个小工具
        # 提示：
        # 1. push_latest_image(image) 负责把旧帧丢掉，只保留最新帧
        # 2. wait_for_image(target_frame) 负责在 tick 之后等待对应的新图像
        #
        # def push_latest_image(image):
        #     while not image_queue.empty():
        #         try:
        #             image_queue.get_nowait()
        #         except queue.Empty:
        #             break
        #     try:
        #         image_queue.put_nowait(image)
        #     except queue.Full:
        #         pass
        #
        # def wait_for_image(target_frame, timeout=2.0):
        #     deadline = time.time() + timeout
        #     latest_image = None
        #     while time.time() < deadline:
        #         remaining = max(0.0, deadline - time.time())
        #         try:
        #             image = image_queue.get(timeout=remaining)
        #         except queue.Empty:
        #             break
        #         latest_image = image
        #         if image.frame >= target_frame:
        #             return image
        #     if latest_image is not None:
        #         return latest_image
        #     raise TimeoutError("未在规定时间内收到相机图像")

        # 第 3 步：开启同步模式和固定步长
        # 提示：同步模式设为 True，固定步长建议 0.05
        # new_settings = world.get_settings()
        # new_settings.synchronous_mode = __________________
        # new_settings.fixed_delta_seconds = ______________
        # world.apply_settings(new_settings)

        # 第 4 步：选择一辆主车蓝图
        # 提示：建议使用 vehicle.tesla.model3，并设置 role_name 为 hero
        # vehicle_bp = ____________________________________
        # vehicle_bp.set_attribute("role_name", "hero")

        # 第 5 步：使用第一个出生点生成主车
        # 提示：先获取 spawn_points，再用 spawn_points[0] 尝试生成
        # spawn_points = __________________________________
        # ego_vehicle = _________________________________

        # if ego_vehicle is None:
        #     raise RuntimeError("车辆生成失败")
        # actor_list.append(ego_vehicle)

        # 第 6 步：获取 RGB 相机蓝图并设置属性
        # 提示：设置图像分辨率和 sensor_tick
        # sensor_bp = _____________________________________
        # sensor_bp.set_attribute("image_size_x", "800")
        # sensor_bp.set_attribute("image_size_y", "600")
        # sensor_bp.set_attribute("sensor_tick", "0.0")

        # 第 7 步：把相机挂到主车上
        # 提示：使用 attach_to=ego_vehicle，位置建议 x=1.5, z=2.4
        # camera = world.spawn_actor(
        #     sensor_bp,
        #     carla.Transform(
        #         carla.Location(x=____, y=____, z=____),
        #         carla.Rotation(pitch=____, yaw=____, roll=____),
        #     ),
        #     attach_to=______________________,
        #     attachment_type=carla.AttachmentType.Rigid,
        # )
        # actor_list.append(camera)

        # 第 8 步：注册相机监听，把“最新图像”送入队列
        # camera.listen(__________________________)

        # 第 9 步：准备天气列表
        # 提示：至少选择三种天气
        # weather_presets = [
        #     ("ClearNoon", carla.WeatherParameters.ClearNoon),
        #     ("CloudySunset", carla.WeatherParameters.CloudySunset),
        #     ("HardRainNoon", carla.WeatherParameters.HardRainNoon),
        # ]

        # 第 10 步：依次切换天气并保存图像
        # 提示：
        # 1. 先调用 world.set_weather(weather)
        # 2. 为了等 GPU 相机稳定，可以连续 tick 几帧
        # 3. 每次 tick 后，不要直接拿旧帧，要调用 wait_for_image(frame_id)
        #
        # for label, weather in weather_presets:
        #     world.set_weather(weather)
        #     latest_image = None
        #     for _ in range(6):
        #         frame_id = world.tick()
        #         latest_image = wait_for_image(frame_id)
        #
        #     save_path = f"output/exp01/{label}_{latest_image.frame:06d}.png"
        #     latest_image.save_to_disk(save_path)
        #     print(f"{label} 已保存：{save_path}")

        pass

    finally:
        # 第 11 步：先恢复世界设置，再销毁 actor
        world.apply_settings(original_settings)

        for actor in reversed(actor_list):
            if isinstance(actor, carla.Sensor):
                actor.stop()
            actor.destroy()


if __name__ == "__main__":
    main()
