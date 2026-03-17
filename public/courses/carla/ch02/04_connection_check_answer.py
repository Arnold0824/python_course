import carla


def main():
    try:
        # 第 1 步：连接本机 CARLA 服务端
        client = carla.Client("localhost", 2000)
        client.set_timeout(10.0)

        # 第 2 步：获取当前世界和基础对象
        world = client.get_world()
        current_map = world.get_map()
        settings = world.get_settings()
        weather = world.get_weather()

        # 第 3 步：输出本节要求的信息
        print("地图名：", current_map.name)
        print("出生点数量：", len(current_map.get_spawn_points()))
        print("是否是同步模式：", settings.synchronous_mode)
        print("固定步长：", settings.fixed_delta_seconds)
        print("天气：", weather)

        # 加分项：检查客户端和服务端版本
        print("客户端版本：", client.get_client_version())
        print("服务端版本：", client.get_server_version())
    except Exception as e:
        print("连接失败：", e)


if __name__ == "__main__":
    main()
