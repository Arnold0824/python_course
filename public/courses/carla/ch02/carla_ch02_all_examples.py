# %% [markdown]
# 第二章 CARLA运行机制与首次连接
# 建议按顺序把每一段代码复制到 Jupyter / IPython Notebook 的不同 cell 中运行。


# %% Cell 1: 导入 carla 并连接当前世界
import carla

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)

world = client.get_world()
current_map = world.get_map()

print(world)
print(current_map.name)


# %% Cell 2: 用 try/except 包装连接过程
try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    print("连接成功")
except Exception as e:
    print("连接失败：", e)


# %% Cell 3: 读取当前世界的基础信息
try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    world = client.get_world()
    current_map = world.get_map()
    settings = world.get_settings()
    weather = world.get_weather()

    print("地图名：", current_map.name)
    print("天气：", weather)
    print("同步模式：", settings.synchronous_mode)
    print("固定步长：", settings.fixed_delta_seconds)
    print("出生点数量：", len(current_map.get_spawn_points()))
except Exception as e:
    print("连接失败：", e)
