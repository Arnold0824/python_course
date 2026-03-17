import carla


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
