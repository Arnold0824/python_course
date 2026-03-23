# %% [markdown]
# 第三章 车辆生成、传感器挂载与自动采图
# 建议在 Jupyter / IPython Notebook 中按顺序逐段执行。
# 每个代码段只做一个动作，先看现象，再继续下一段。

# %% Cell 1: 导入依赖并连接 CARLA
import os
import queue
import random
import time

import carla

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)
world = client.get_world()

print("当前地图：", world.get_map().name)


# %% Cell 2: 准备共享变量和清理函数
os.makedirs("output/ch03", exist_ok=True)

actor_list = []
image_queue = queue.Queue(maxsize=1)
original_settings = world.get_settings()
traffic_manager = None


def safe_destroy(actor):
    if actor is None:
        return
    try:
        actor.destroy()
    except RuntimeError:
        pass


def cleanup():
    global traffic_manager

    for actor in reversed(actor_list):
        if isinstance(actor, carla.Sensor):
            actor.stop()
        safe_destroy(actor)

    actor_list.clear()
    world.apply_settings(original_settings)

    if traffic_manager is not None:
        traffic_manager.set_synchronous_mode(False)
        traffic_manager = None


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

    raise TimeoutError(f"未在 {timeout} 秒内收到目标图像帧")


print("输出目录已准备：output/ch03")


# %% Cell 3: 获取蓝图库
bp_lib = world.get_blueprint_library()
print(bp_lib)


# %% Cell 4: 选择车辆蓝图并查看出生点
vehicle_bp = bp_lib.find("vehicle.tesla.model3")
vehicle_bp.set_attribute("role_name", "hero")

spawn_points = world.get_map().get_spawn_points()
print("出生点数量：", len(spawn_points))
print("第一个出生点：", spawn_points[0])


# %% Cell 5: 先用第一个出生点尝试一次
ego_vehicle = world.try_spawn_actor(vehicle_bp, spawn_points[0])
print("ego_vehicle =", ego_vehicle)

if ego_vehicle is not None:
    actor_list.append(ego_vehicle)


# %% Cell 6: 升级成稳妥版主车生成逻辑
if ego_vehicle is not None:
    safe_destroy(ego_vehicle)
    actor_list.clear()

random.shuffle(spawn_points)

ego_vehicle = None
for sp in spawn_points:
    ego_vehicle = world.try_spawn_actor(vehicle_bp, sp)
    if ego_vehicle is not None:
        break

if ego_vehicle is None:
    raise RuntimeError("车辆生成失败：请更换地图或重试")

actor_list.append(ego_vehicle)
print("ego_vehicle =", ego_vehicle)
print("车辆位姿：", ego_vehicle.get_transform())


# %% Cell 7: 准备 RGB 相机蓝图
sensor_bp = bp_lib.find("sensor.camera.rgb")
sensor_bp.set_attribute("image_size_x", "800")
sensor_bp.set_attribute("image_size_y", "600")
sensor_bp.set_attribute("fov", "90")
sensor_bp.set_attribute("sensor_tick", "0.0")


# %% Cell 8: 定义相机安装位姿
camera_transform = carla.Transform(
    carla.Location(x=1.5, y=0.0, z=2.4),
    carla.Rotation(pitch=0.0, yaw=0.0, roll=0.0),
)


# %% Cell 9: 把相机挂到主车上
camera = world.spawn_actor(
    sensor_bp,
    camera_transform,
    attach_to=ego_vehicle,
    attachment_type=carla.AttachmentType.Rigid,
)

actor_list.append(camera)
print("camera =", camera)


# %% Cell 10: 最小监听，先打印帧号
camera.listen(lambda image: print("frame =", image.frame))


# %% Cell 11: 先观察几帧，再停止预览监听
settings = world.get_settings()
print("synchronous_mode =", settings.synchronous_mode)

if settings.synchronous_mode:
    for _ in range(5):
        world.tick()
else:
    time.sleep(1.0)

camera.stop()
print("帧号预览结束，准备切换到队列模式")


# %% Cell 12: 切换到“只保留最新帧”的队列模式
image_queue = queue.Queue(maxsize=1)
camera.listen(push_latest_image)
print("相机已切换到队列模式")


# %% Cell 13: 进入同步模式并稳定取一帧
settings = world.get_settings()
settings.synchronous_mode = True
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

latest_image = None
for _ in range(5):
    frame_id = world.tick()
    latest_image = wait_for_image(frame_id)

image = latest_image
print("当前图像帧号：", image.frame)


# %% Cell 14: 保存一张当前图像
os.makedirs("output/ch03", exist_ok=True)
filename = f"output/ch03/frame_{image.frame:06d}.png"
image.save_to_disk(filename)
print("已保存：", filename)


# %% Cell 15: 准备天气预设列表
weather_presets = [
    ("ClearNoon", carla.WeatherParameters.ClearNoon),
    ("CloudySunset", carla.WeatherParameters.CloudySunset),
    ("WetCloudyNoon", carla.WeatherParameters.WetCloudyNoon),
    ("HardRainNoon", carla.WeatherParameters.HardRainNoon),
]


# %% Cell 16: 定义“切天气 + tick 几帧 + 保存一张图”的函数
def capture_weather_frame(label, weather):
    world.set_weather(weather)

    latest_image = None
    for _ in range(6):
        frame_id = world.tick()
        latest_image = wait_for_image(frame_id)

    path = f"output/ch03/{label}_{latest_image.frame:06d}.png"
    latest_image.save_to_disk(path)
    print(f"{label} 已保存：{path}")


# %% Cell 17: 依次采集多种天气下的图像
for label, weather in weather_presets:
    capture_weather_frame(label, weather)


# %% Cell 18: 可选扩展，让主车自动驾驶并继续采图
traffic_manager = client.get_trafficmanager(8000)
traffic_manager.set_synchronous_mode(True)
ego_vehicle.set_autopilot(True, traffic_manager.get_port())

for step in range(20):
    frame_id = world.tick()
    image = wait_for_image(frame_id)
    if step % 5 == 0:
        path = f"output/ch03/autopilot_{image.frame:06d}.png"
        image.save_to_disk(path)
        print("自动驾驶采图：", path)

ego_vehicle.set_autopilot(False, traffic_manager.get_port())
traffic_manager.set_synchronous_mode(False)
traffic_manager = None


# %% Cell 19: 清理资源
cleanup()
print("第三章示例资源已清理")
