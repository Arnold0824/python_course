import carla


try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    print("连接成功")
except Exception as e:
    print("连接失败：", e)
