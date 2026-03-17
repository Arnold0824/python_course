import carla


def main():
    try:
        # 第 1 步：创建 client
        # 提示：地址写 "localhost"，端口写 2000
        # client = carla.Client("localhost", 2000)

        # 第 2 步：设置超时时间
        # 提示：这一章课堂统一使用 10.0 秒
        # client.set_timeout(10.0)

        # 第 3 步：从 client 获取当前 world
        # world = ______________________________

        # 第 4 步：从 world 继续获取 map、settings 和 weather
        # 提示：本节至少要用到这 3 个对象
        # current_map = ________________________
        # settings = ___________________________
        # weather = ____________________________

        # 第 5 步：完成基础输出
        # 提示 1：地图名来自 current_map.name
        # 提示 2：出生点数量来自 len(current_map.get_spawn_points())
        # 提示 3：同步模式和固定步长都在 settings 里面
        # print("地图名：", ____________________)
        # print("出生点数量：", ________________)
        # print("是否是同步模式：", ____________)
        # print("固定步长：", __________________)
        # print("天气：", ______________________)

        # 加分项：检查客户端和服务端版本
        # print("客户端版本：", __________________)
        # print("服务端版本：", __________________)
        pass
    except Exception as e:
        print("连接失败：", e)


if __name__ == "__main__":
    main()
