# %% [markdown]
# 第一章 环境搭建、运行机制与首次连接
# 建议把每一段复制到 Jupyter / IPython Notebook 的独立 cell 中顺序执行。


# %% Cell 1: 导入 CARLA 并建立最小连接
import carla

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)

world = client.get_world()
current_map = world.get_map()

print(world)
print(current_map.name)


# %% Cell 2: 查看 client 和 server 版本
print("client version:", client.get_client_version())
print("server version:", client.get_server_version())


# %% Cell 3: 读取当前世界的基础信息
settings = world.get_settings()
weather = world.get_weather()
spawn_points = current_map.get_spawn_points()

print("地图名：", current_map.name)
print("天气：", weather)
print("同步模式：", settings.synchronous_mode)
print("固定步长：", settings.fixed_delta_seconds)
print("出生点数量：", len(spawn_points))


# %% Cell 4: 用 try/except 包装连接流程
try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    print("client version:", client.get_client_version())
    print("server version:", client.get_server_version())

    world = client.get_world()
    print("连接成功")
except Exception as error:
    print("连接失败：", error)


# %% Cell 5: 写成一份完整的连接检测脚本
try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    world = client.get_world()
    current_map = world.get_map()
    settings = world.get_settings()
    weather = world.get_weather()
    spawn_points = current_map.get_spawn_points()

    print("client version:", client.get_client_version())
    print("server version:", client.get_server_version())
    print("地图名：", current_map.name)
    print("天气：", weather)
    print("同步模式：", settings.synchronous_mode)
    print("固定步长：", settings.fixed_delta_seconds)
    print("出生点数量：", len(spawn_points))
except Exception as error:
    print("连接失败：", error)

