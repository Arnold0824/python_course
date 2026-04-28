export const chapter04Docs = [
  {
    title: "Traffic Manager",
    text: "自动驾驶车辆的速度差、跟车距离、变道、红灯忽略等参数主要查这里。",
    href: "https://carla.readthedocs.io/en/latest/adv_traffic_manager/",
  },
  {
    title: "Synchrony and time-step",
    text: "不同方案要公平对比，就要使用同步模式和固定步长。",
    href: "https://carla.readthedocs.io/en/latest/adv_synchrony_timestep/",
  },
  {
    title: "Python API",
    text: "车辆速度、位置、Traffic Manager 方法名不确定时回到这里核对。",
    href: "https://carla.readthedocs.io/en/latest/python_api/",
  },
];

export const chapter04ScenarioCards = [
  {
    name: "保守慢行",
    tag: "车距优先",
    speed: "速度差 +35%",
    distance: "跟车距离 6 m",
    lane: "不主动变道",
    light: "遵守红灯",
    text: "像刚拿驾照时的谨慎驾驶：车距更大、速度更慢，结果通常更稳定但效率偏低。",
  },
  {
    name: "普通通勤",
    tag: "基准方案",
    speed: "速度差 0%",
    distance: "跟车距离 3 m",
    lane: "允许变道",
    light: "遵守红灯",
    text: "作为对照组使用。后面的结论都要和它比较，而不是只看某一组的单独表现。",
  },
  {
    name: "赶时间",
    tag: "效率优先",
    speed: "速度差 -20%",
    distance: "跟车距离 2 m",
    lane: "允许变道",
    light: "遵守红灯",
    text: "负速度差表示尝试比道路限速更快。它不一定总能成功跑快，因为路况也会限制车辆。",
  },
  {
    name: "路口冒险",
    tag: "趣味观察",
    speed: "速度差 -10%",
    distance: "跟车距离 2 m",
    lane: "允许变道",
    light: "80% 概率忽略红灯",
    text: "只用于观察参数对连续行驶的影响。结论要落在数据变化上，不鼓励现实驾驶模仿。",
  },
];

export const chapter04MetricCards = [
  {
    title: "平均速度",
    text: "最直观地观察某组参数整体偏快还是偏慢。",
  },
  {
    title: "最高速度",
    text: "用于观察激进参数是否真的带来更高速度上限。",
  },
  {
    title: "低速样本占比",
    text: "速度低于 1 km/h 的样本越多，说明停车或拥堵时间越长。",
  },
  {
    title: "行驶距离",
    text: "同样运行 30 秒，谁走得更远，谁的效率就更高。",
  },
];

export const chapter04ObserverCards = [
  {
    title: "四宫格第一视角",
    text: "pygame 窗口被分成 2×2 四个区域，每个区域显示一辆主车的第三人称追车视角，可以看到主车本体。",
  },
  {
    title: "四种驾驶风格同时运行",
    text: "保守慢行、普通通勤、赶时间、路口冒险四辆主车会在同一个世界中一起自动驾驶，其中“赶时间”使用 Mustang，目标速度约 80 mph。",
  },
  {
    title: "实时观察事件",
    text: "每辆车都会显示速度、均速、最高速度、行驶距离、碰撞次数、压线次数和红灯状态。",
  },
  {
    title: "碰撞是事件观察",
    text: "碰撞传感器记录的是碰撞发生和冲量强度。CARLA 更偏交通与传感器仿真，不会像破坏游戏一样稳定出现车辆碎裂或行人被撞飞。",
  },
  {
    title: "观察实验不替代统计实验",
    text: "四辆车同时运行会互相影响，所以它适合课堂观察；正式结论仍以 summary.csv 等统计文件为准。",
  },
  {
    title: "三档风险模式",
    text: "normal 适合低配置机器，high 适合课堂演示，extreme 会提高交通密度、行人过街概率和激进车辆忽略避让的比例。",
  },
  {
    title: "低速脱困",
    text: "如果某辆主车连续几秒低速不动，脚本会短暂人工给油，再交回 Traffic Manager，避免观察窗口长期静止。",
  },
];

export const chapter04Slides = [
  {
    no: "01",
    outline: "代码段 1 参数方案",
    title: "代码段 1：先把实验方案写成数据表",
    lead: "这一章从一开始就把“要对比什么”写清楚。参数方案不散落在代码中，而是集中放在 SCENARIOS 列表里。",
    code: String.raw`import csv
import json
import math
from pathlib import Path

import carla

OUTPUT_ROOT = Path("output/exp03")

FIXED_DELTA_SECONDS = 0.05
RUN_SECONDS = 30
WARMUP_TICKS = 30
SAMPLE_EVERY_TICKS = 5
RUN_TICKS = int(RUN_SECONDS / FIXED_DELTA_SECONDS)

TRAFFIC_MANAGER_PORT = 8000
BACKGROUND_VEHICLE_COUNT = 12

SCENARIOS = [
    {
        "name": "保守慢行",
        "speed_difference": 35.0,
        "distance_to_leading_vehicle": 6.0,
        "auto_lane_change": False,
        "ignore_lights_percentage": 0.0,
        "note": "车距更大、速度更慢，观察是否更稳但效率较低。",
    },
    {
        "name": "普通通勤",
        "speed_difference": 0.0,
        "distance_to_leading_vehicle": 3.0,
        "auto_lane_change": True,
        "ignore_lights_percentage": 0.0,
        "note": "作为基准方案，用来和其他方案比较。",
    },
    {
        "name": "赶时间",
        "speed_difference": -20.0,
        "distance_to_leading_vehicle": 2.0,
        "auto_lane_change": True,
        "ignore_lights_percentage": 0.0,
        "note": "尝试更快行驶，但仍然遵守交通灯。",
    },
    {
        "name": "路口冒险",
        "speed_difference": -10.0,
        "distance_to_leading_vehicle": 2.0,
        "auto_lane_change": True,
        "ignore_lights_percentage": 80.0,
        "note": "提高连续行驶概率，用来观察参数改变后的统计差异。",
    },
]`,
    explain: "这一段导入 csv、json、math、Path 和 carla，并集中定义输出目录、运行时长、同步步长、采样间隔、Traffic Manager 端口以及四套参数方案。",
    why: "实验三不是写一辆车跑起来，而是比较不同参数方案。把方案写成列表，后面就可以用循环逐组运行，学生也更容易自己增加新方案。",
    points: [
      "speed_difference 为正表示更慢，为负表示尝试更快。",
      "每个方案至少包含速度差、跟车距离、变道、红灯忽略概率。",
      "RUN_SECONDS 保证每组方案运行时间一致。",
    ],
    terms: [
      { title: "SCENARIOS", text: "实验方案表，后面每一组都会循环执行。" },
      { title: "RUN_TICKS", text: "把运行秒数换算成同步模式下的 tick 数。" },
      { title: "BACKGROUND_VEHICLE_COUNT", text: "背景车让跟车距离和变道参数更容易产生可观察差异。" },
    ],
  },
  {
    no: "02",
    outline: "代码段 2 统计工具",
    title: "代码段 2：把速度、距离和趣味标签封装成工具函数",
    lead: "参数对比必须落到数字上。第二段先准备基础统计工具，让后面的主流程保持清楚。",
    code: String.raw`def speed_kmh(actor):
    velocity = actor.get_velocity()
    speed_mps = math.sqrt(
        velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2
    )
    return speed_mps * 3.6


def point_from_actor(actor):
    location = actor.get_location()
    return (location.x, location.y, location.z)


def walked_distance(points):
    total = 0.0
    for current, following in zip(points, points[1:]):
        dx = following[0] - current[0]
        dy = following[1] - current[1]
        dz = following[2] - current[2]
        total += math.sqrt(dx * dx + dy * dy + dz * dz)
    return total


def fun_label(avg_speed, distance_m, low_speed_ratio):
    if low_speed_ratio > 0.4:
        return "等待型"
    if avg_speed >= 32 and distance_m >= 250:
        return "冲刺型"
    if avg_speed <= 12:
        return "慢热型"
    return "均衡型"`,
    explain: "speed_kmh 把 CARLA 的三维速度向量换算成 km/h，walked_distance 根据连续位置估算行驶距离，fun_label 根据统计结果生成一个便于讨论的标签。",
    why: "先把计算逻辑封装好，后面每一组方案都能复用同一套统计规则，避免每组写出不一致的计算方法。",
    points: [
      "速度向量不能直接当作车速，要先求模再乘 3.6。",
      "行驶距离来自连续位置点之间的距离累加。",
      "趣味标签只是帮助观察，最终结论仍然要看统计数据。",
    ],
    terms: [
      { title: "velocity", text: "车辆在 x、y、z 三个方向上的速度分量。" },
      { title: "低速样本占比", text: "速度低于 1 km/h 的样本占全部样本的比例。" },
      { title: "fun_label", text: "把数字结果转成更容易讨论的分类标签。" },
    ],
  },
  {
    no: "03",
    outline: "代码段 3 同步模式",
    title: "代码段 3：每组实验都用同样的同步设置",
    lead: "公平对比的第一步，是让每组方案的仿真节奏完全一致。同步模式和固定步长是本章的底座。",
    code: String.raw`def enable_sync_mode(world):
    original_settings = world.get_settings()

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = FIXED_DELTA_SECONDS
    world.apply_settings(settings)

    return original_settings


def restore_world(world, traffic_manager, original_settings):
    if traffic_manager is not None:
        traffic_manager.set_synchronous_mode(False)
    world.apply_settings(original_settings)


def safe_destroy(actor):
    if actor is None:
        return
    try:
        actor.destroy()
    except RuntimeError:
        pass


def tick_world(world, timeout=10.0):
    # world.tick() 默认可能长时间等待；加 timeout 后，异常会更明确
    return world.tick(timeout)`,
    explain: "enable_sync_mode 负责进入同步模式并返回原始设置，restore_world 负责实验后恢复世界，safe_destroy 负责安全销毁 actor，tick_world 负责带超时推进仿真。",
    why: "每组方案都要经历“进入同步模式、运行、恢复设置”。把这组动作封装好，后面循环运行多组方案时不容易把环境弄乱。world.tick 加上超时后，CARLA 状态异常时会报错，不会让 notebook 看起来一直卡住。",
    points: [
      "original_settings 一定要先保存，最后才能恢复。",
      "Traffic Manager 也有同步状态，不能只恢复 world。",
      "tick_world(world) 比直接 world.tick() 更适合课堂调试。",
    ],
    terms: [
      { title: "synchronous_mode", text: "由代码主动推进仿真，而不是让世界自由运行。" },
      { title: "fixed_delta_seconds", text: "每个 tick 代表固定仿真时间。" },
      { title: "tick_world", text: "带超时推进一帧，避免异常状态下长时间等待。" },
    ],
  },
  {
    no: "04",
    outline: "代码段 4 车辆生成",
    title: "代码段 4：生成主车和背景车",
    lead: "如果只有一辆车，跟车距离和变道参数不容易体现出来。这一段加入少量背景车，让参数变化更有观察价值。",
    code: String.raw`def spawn_ego_vehicle(world, bp_lib, spawn_points):
    ego_bp = bp_lib.find("vehicle.tesla.model3")
    ego_bp.set_attribute("role_name", "hero")

    for spawn_point in spawn_points:
        ego_vehicle = world.try_spawn_actor(ego_bp, spawn_point)
        if ego_vehicle is not None:
            return ego_vehicle

    raise RuntimeError("主车生成失败，请重新运行或更换地图")


def spawn_background_vehicles(world, bp_lib, spawn_points, traffic_manager):
    vehicle_bps = bp_lib.filter("vehicle.*")
    background_vehicles = []

    for spawn_point in spawn_points:
        if len(background_vehicles) >= BACKGROUND_VEHICLE_COUNT:
            break

        vehicle_bp = vehicle_bps[len(background_vehicles) % len(vehicle_bps)]
        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        if vehicle is None:
            continue

        vehicle.set_autopilot(True, traffic_manager.get_port())
        traffic_manager.vehicle_percentage_speed_difference(vehicle, 10.0)
        background_vehicles.append(vehicle)

    return background_vehicles`,
    explain: "spawn_ego_vehicle 生成主车，spawn_background_vehicles 生成背景车并交给 Traffic Manager 自动驾驶。",
    why: "实验三关注参数影响。背景车会让主车遇到更真实的跟车与变道情境，学生更容易看到平均速度、低速占比、行驶距离之间的差异。",
    points: [
      "主车和背景车都属于 actor，结束时都要清理。",
      "背景车数量不宜太多，否则课堂运行压力会增大。",
      "背景车只用于制造交通环境，不是本章分析对象。",
    ],
    terms: [
      { title: "ego_vehicle", text: "本章唯一被统计分析的主车。" },
      { title: "background_vehicles", text: "帮助形成交通环境的背景车辆。" },
      { title: "try_spawn_actor", text: "生成失败时返回 None，适合反复尝试出生点。" },
    ],
  },
  {
    no: "05",
    outline: "代码段 5 应用参数",
    title: "代码段 5：把一套方案真正应用到主车上",
    lead: "这一段是实验三的核心。方案表里的数字只有交给 Traffic Manager，才会变成车辆行为。",
    code: String.raw`def apply_scenario(traffic_manager, ego_vehicle, scenario):
    ego_vehicle.set_autopilot(True, traffic_manager.get_port())

    traffic_manager.vehicle_percentage_speed_difference(
        ego_vehicle,
        scenario["speed_difference"],
    )
    traffic_manager.distance_to_leading_vehicle(
        ego_vehicle,
        scenario["distance_to_leading_vehicle"],
    )
    traffic_manager.auto_lane_change(
        ego_vehicle,
        scenario["auto_lane_change"],
    )
    traffic_manager.ignore_lights_percentage(
        ego_vehicle,
        scenario["ignore_lights_percentage"],
    )`,
    explain: "apply_scenario 从当前方案中取出速度差、跟车距离、自动变道和忽略红灯概率，并逐项设置到主车上。",
    why: "把参数应用过程写成一个函数，主流程只需要传入不同 scenario。这样学生可以专注观察“换方案后数据怎么变”，而不是每次复制一堆设置代码。",
    points: [
      "set_autopilot 必须指定 Traffic Manager 的端口。",
      "vehicle_percentage_speed_difference 是百分比，不是 km/h。",
      "ignore_lights_percentage 只用于仿真实验观察，不代表现实驾驶建议。",
    ],
    terms: [
      { title: "speed_difference", text: "正数更慢，负数更快。" },
      { title: "distance_to_leading_vehicle", text: "主车与前车保持的目标距离。" },
      { title: "auto_lane_change", text: "控制 Traffic Manager 是否允许自动变道。" },
    ],
  },
  {
    no: "06",
    outline: "代码段 6 运行单组",
    title: "代码段 6：运行一组方案并记录样本",
    lead: "这一段把车辆跑起来，并按固定间隔记录速度和位置。每条记录都会带上方案名称，方便最后合并统计。",
    code: String.raw`def collect_samples(world, ego_vehicle, scenario, run_ticks=RUN_TICKS):
    samples = []
    positions = []

    for _ in range(WARMUP_TICKS):
        tick_world(world)

    progress_step = max(1, run_ticks // 5)

    for tick_index in range(run_ticks):
        frame_id = tick_world(world)

        if (tick_index + 1) % progress_step == 0 or tick_index == run_ticks - 1:
            percent = (tick_index + 1) / run_ticks * 100
            print(f"  {scenario['name']} 进度 {percent:5.1f}%")

        if tick_index % SAMPLE_EVERY_TICKS != 0:
            continue

        speed = speed_kmh(ego_vehicle)
        point = point_from_actor(ego_vehicle)
        positions.append(point)

        samples.append(
            {
                "scenario": scenario["name"],
                "tick": tick_index,
                "sim_time_s": round(tick_index * FIXED_DELTA_SECONDS, 2),
                "frame": frame_id,
                "speed_kmh": round(speed, 2),
                "x": round(point[0], 2),
                "y": round(point[1], 2),
                "z": round(point[2], 2),
            }
        )

    return samples, positions`,
    explain: "先热身，再正式运行 run_ticks 帧。程序不是每一帧都保存，而是每隔 SAMPLE_EVERY_TICKS 帧记录一次速度、位置和帧号，并每 20% 打印一次进度。",
    why: "统计不需要每帧都存。间隔记录可以减少文件体积，同时保留足够观察趋势的数据。进度输出能让 notebook 中的长时间运行状态更清楚。",
    points: [
      "热身样本不参与统计，避免刚起步阶段影响结果。",
      "每条样本都带 scenario 字段，后面合并 CSV 时不会混淆。",
      "run_ticks 可以由 main 根据 run_seconds 动态计算。",
    ],
    terms: [
      { title: "samples", text: "每次采样得到的一行数据。" },
      { title: "positions", text: "用于估算行驶距离的位置序列。" },
      { title: "进度输出", text: "避免最后一段在 notebook 中看起来像没有响应。" },
    ],
  },
  {
    no: "07",
    outline: "代码段 7 汇总统计",
    title: "代码段 7：把一组样本汇总成结果行",
    lead: "这一段把几十到几百条采样数据压缩成一行统计结果，后面才能做方案对比。",
    code: String.raw`def summarize_scenario(scenario, samples, positions):
    speeds = [row["speed_kmh"] for row in samples]
    low_speed_count = sum(1 for speed in speeds if speed < 1.0)
    avg_speed = sum(speeds) / len(speeds)
    distance_m = walked_distance(positions)

    return {
        "方案": scenario["name"],
        "速度差%": scenario["speed_difference"],
        "跟车距离m": scenario["distance_to_leading_vehicle"],
        "允许自动变道": scenario["auto_lane_change"],
        "忽略红灯%": scenario["ignore_lights_percentage"],
        "样本数": len(samples),
        "平均速度kmh": round(avg_speed, 2),
        "最高速度kmh": round(max(speeds), 2),
        "最低速度kmh": round(min(speeds), 2),
        "行驶距离m": round(distance_m, 2),
        "低速样本占比": round(low_speed_count / len(speeds), 3),
        "趣味标签": fun_label(avg_speed, distance_m, low_speed_count / len(speeds)),
        "说明": scenario["note"],
    }`,
    explain: "summarize_scenario 计算样本数、平均速度、最高速度、最低速度、行驶距离、低速样本占比，并把参数值和统计值放进同一个结果字典。",
    why: "实验报告最需要的是“参数 结果 解释”的闭环。把参数和结果放在同一行，学生写分析时就不用来回翻代码。",
    points: [
      "统计结果必须能对应回原始参数。",
      "低速样本占比能反映等待、拥堵或频繁停车。",
      "趣味标签帮助讨论，但不能替代数据。",
    ],
    terms: [
      { title: "结果行", text: "一个方案最终只对应 summary CSV 中的一行。" },
      { title: "round", text: "让结果文件更适合阅读，不保留过多小数。" },
      { title: "说明", text: "保留方案设计意图，便于写实验报告。" },
    ],
  },
  {
    no: "08",
    outline: "代码段 8 保存文件",
    title: "代码段 8：把原始样本和汇总结果都保存下来",
    lead: "统计结果要能复查。只保存最终表格还不够，原始采样数据也应该一起留下。",
    code: String.raw`SUMMARY_FIELDS = [
    "方案", "速度差%", "跟车距离m", "允许自动变道", "忽略红灯%",
    "样本数", "平均速度kmh", "最高速度kmh", "最低速度kmh",
    "行驶距离m", "低速样本占比", "趣味标签", "说明",
]

SAMPLE_FIELDS = [
    "scenario", "tick", "sim_time_s", "frame",
    "speed_kmh", "x", "y", "z",
]


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_outputs(summary_rows, sample_rows):
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUT_ROOT / "summary.csv", summary_rows, SUMMARY_FIELDS)
    write_csv(OUTPUT_ROOT / "samples.csv", sample_rows, SAMPLE_FIELDS)

    (OUTPUT_ROOT / "summary.json").write_text(
        json.dumps(summary_rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )`,
    explain: "summary.csv 保存每组方案的统计结果，samples.csv 保存每次采样的原始速度和位置，summary.json 方便程序再次读取。",
    why: "实验报告里常用 summary.csv；如果结果看起来异常，就回到 samples.csv 查具体采样过程。",
    points: [
      "utf-8-sig 可以让 Excel 更稳定地识别中文表头。",
      "summary 和 samples 分开保存，既方便阅读，也方便复查。",
      "JSON 适合后续继续用 Python 自动分析。",
    ],
    terms: [
      { title: "DictWriter", text: "按字段名写出 CSV 表格。" },
      { title: "SUMMARY_FIELDS", text: "控制汇总表格的列顺序。" },
      { title: "SAMPLE_FIELDS", text: "控制原始样本表格的列顺序。" },
    ],
  },
  {
    no: "09",
    outline: "代码段 9 循环运行",
    title: "代码段 9：循环运行所有方案",
    lead: "前面的函数都准备好后，真正的多方案对比反而很短：循环方案表，逐组运行、逐组汇总。",
    code: String.raw`def run_one_scenario(client, scenario, run_ticks=RUN_TICKS):
    world = client.get_world()
    bp_lib = world.get_blueprint_library()
    traffic_manager = client.get_trafficmanager(TRAFFIC_MANAGER_PORT)
    original_settings = enable_sync_mode(world)
    traffic_manager.set_synchronous_mode(True)

    actors = []
    try:
        spawn_points = list(world.get_map().get_spawn_points())
        if len(spawn_points) < 2:
            raise RuntimeError("地图出生点不足，无法完成实验")

        ego_vehicle = spawn_ego_vehicle(world, bp_lib, spawn_points)
        actors.append(ego_vehicle)

        background_vehicles = spawn_background_vehicles(
            world,
            bp_lib,
            spawn_points[1:],
            traffic_manager,
        )
        actors.extend(background_vehicles)

        tick_world(world)
        apply_scenario(traffic_manager, ego_vehicle, scenario)
        samples, positions = collect_samples(world, ego_vehicle, scenario, run_ticks)
        summary = summarize_scenario(scenario, samples, positions)
        return summary, samples

    finally:
        for actor in actors:
            if isinstance(actor, carla.Vehicle):
                try:
                    actor.set_autopilot(False, traffic_manager.get_port())
                except RuntimeError:
                    pass

        for actor in reversed(actors):
            safe_destroy(actor)
        restore_world(world, traffic_manager, original_settings)`,
    explain: "run_one_scenario 把一组方案从环境准备、车辆生成、参数应用、采样统计到资源清理完整跑一遍。run_ticks 会从 main 传入。",
    why: "每组方案都独立清理环境，能减少上一组残留对下一组的影响，也更符合实验对比的公平性要求。",
    points: [
      "finally 确保出错时也尽量清理 actor。",
      "背景车使用 spawn_points[1:]，主车和背景车不抢同一个出生点。",
      "销毁车辆前先关闭自动驾驶，可以减少 Traffic Manager 状态残留。",
    ],
    terms: [
      { title: "run_one_scenario", text: "本章最重要的流程函数。" },
      { title: "actors", text: "记录本组实验创建的所有车辆，方便统一销毁。" },
      { title: "finally", text: "无论是否异常，都执行清理逻辑。" },
    ],
  },
  {
    no: "10",
    outline: "代码段 10 排行榜",
    title: "代码段 10：输出排行榜，让结论更容易写",
    lead: "最后一段把多组结果保存并打印成简短排行榜。实验报告可以围绕排行榜写分析，但结论必须回到统计表。",
    code: String.raw`def print_leaderboard(summary_rows):
    ranked = sorted(
        summary_rows,
        key=lambda row: row["行驶距离m"],
        reverse=True,
    )

    print("\n=== 参数方案行驶距离排行榜 ===")
    for index, row in enumerate(ranked, start=1):
        print(
            f"{index}. {row['方案']} | "
            f"距离 {row['行驶距离m']} m | "
            f"均速 {row['平均速度kmh']} km/h | "
            f"标签 {row['趣味标签']}"
        )


def main(run_seconds=RUN_SECONDS, scenario_limit=None):
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    summary_rows = []
    sample_rows = []
    run_ticks = int(run_seconds / FIXED_DELTA_SECONDS)
    scenarios = SCENARIOS if scenario_limit is None else SCENARIOS[:scenario_limit]

    print(f"本次运行 {len(scenarios)} 组方案，每组 {run_seconds} 秒，约 {run_ticks} ticks")

    for index, scenario in enumerate(scenarios, start=1):
        print(f"\n开始运行方案 {index}/{len(scenarios)}：{scenario['name']}")
        summary, samples = run_one_scenario(client, scenario, run_ticks)
        summary_rows.append(summary)
        sample_rows.extend(samples)

    save_outputs(summary_rows, sample_rows)
    print_leaderboard(summary_rows)
    print(f"\n结果已保存到：{OUTPUT_ROOT.resolve()}")


# 在 notebook 里逐段复制时，建议先跑短演示，确认流程能结束
try:
    get_ipython
    main(run_seconds=8, scenario_limit=2)
except NameError:
    main()`,
    explain: "main 连接 CARLA，循环运行方案，保存 CSV 和 JSON，并按行驶距离打印排行榜。run_seconds 控制每组运行时长，scenario_limit 控制先跑几组。",
    why: "notebook 里逐段复制时，最后一段会直接运行。先跑 8 秒、2 组方案能快速验证流程；提交实验前再改成 main(run_seconds=30) 运行完整四组。",
    points: [
      "summary_rows 是汇总结果列表。",
      "sample_rows 是全部原始采样记录。",
      "notebook 中先跑短演示，避免把长时间运行误认为死循环。",
    ],
    terms: [
      { title: "main(run_seconds=8, scenario_limit=2)", text: "notebook 里先验证流程是否能正常结束。" },
      { title: "排行榜", text: "帮助快速发现差异，不代替实验结论。" },
      { title: "OUTPUT_ROOT.resolve()", text: "打印结果目录的绝对路径，便于找到文件。" },
    ],
  },
];

export const chapter04Pitfalls = [
  { title: "只跑一组方案", text: "实验三的重点是对比。至少两组，建议四组，才容易写出差异分析。" },
  { title: "每组运行时长不同", text: "运行时间不同会直接影响行驶距离，结论就不公平。" },
  { title: "只写主观感受", text: "报告里不能只写“感觉更快”。要引用平均速度、最高速度、低速占比或行驶距离。" },
  { title: "忽略清理", text: "上一组车辆残留会影响下一组实验，最后一定要销毁 actor 并恢复同步设置。" },
];

export const chapter04Resources = [
  {
    title: "实验报告下载",
    text: "第四章对应实验项目三的报告模板。",
    href: "/courses/carla/exp/实验报告3：xxxx-学生姓名.docx",
    download: "实验报告3：xxxx-学生姓名.docx",
  },
  {
    title: "实验指导书",
    text: "实验项目三的目标、要求和评分标准以此为准。",
    href: "/courses/carla/exp/《自动驾驶软件系统B》实验指导书（学院模板）-阴明旭.docx",
    download: "《自动驾驶软件系统B》实验指导书（学院模板）-阴明旭.docx",
  },
  {
    title: "实验模板",
    text: "保留完整结构，在关键位置补全参数方案和统计逻辑。",
    href: "/courses/carla/ch04/exp03_autopilot_stats_template.py",
    download: "exp03_autopilot_stats_template.py",
  },
  {
    title: "实验答案",
    text: "完整可运行脚本，建议先独立完成模板后再对照。",
    href: "/courses/carla/ch04/exp03_autopilot_stats_answer.py",
    download: "exp03_autopilot_stats_answer.py",
  },
  {
    title: "整章总代码",
    text: "按本章代码段顺序整理好的完整示例。",
    href: "/courses/carla/ch04/carla_ch04_all_examples.py",
    download: "carla_ch04_all_examples.py",
  },
  {
    title: "趣味扩展：四车观察脚本",
    text: "用 pygame 四宫格同时观察四种驾驶风格，并记录碰撞、压线、速度和距离。",
    href: "/courses/carla/ch04/exp03_four_vehicle_observer.py",
    download: "exp03_four_vehicle_observer.py",
  },
  {
    title: "实验报告提交",
    text: "完成实验后通过此链接统一提交。",
    href: "https://f.wps.cn/g/vc9PoTwr/",
  },
];
