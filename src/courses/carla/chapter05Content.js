export const chapter05Docs = [
  {
    title: "Traffic lights and signs",
    text: "如何在 CARLA 中拿到交通灯对象、读取颜色状态，本章主要查这里。",
    href: "https://carla.readthedocs.io/en/latest/core_actors/#traffic-signs-and-traffic-lights",
  },
  {
    title: "Synchrony and time-step",
    text: "事件日志要可复现，前提是同步模式 + 固定步长。",
    href: "https://carla.readthedocs.io/en/latest/adv_synchrony_timestep/",
  },
  {
    title: "Python API",
    text: "TrafficLightState、Actor.get_location、get_actors 等接口拿不准时回到这里。",
    href: "https://carla.readthedocs.io/en/latest/python_api/",
  },
];

export const chapter05ConceptCards = [
  {
    name: "触发阈值",
    tag: "TRIGGER_DISTANCE_M",
    detail: "默认 25 m",
    role: "近距离触发",
    extra: "可按地图调",
    text: "只在车辆靠近交通灯一定距离内才写日志，避免全程记录导致日志冗余。",
  },
  {
    name: "最近交通灯",
    tag: "find_nearest_traffic_light",
    detail: "遍历距离取最小",
    role: "每帧观察对象",
    extra: "返回 (light, distance)",
    text: "每一帧都重新选择当前观察的交通灯，让车辆穿过路口时也能跟得上。",
  },
  {
    name: "状态字符串",
    tag: "TrafficLightState",
    detail: "Red / Yellow / Green / Off / Unknown",
    role: "便于统计",
    extra: "中文也行，关键是统一",
    text: "把 carla.TrafficLightState 翻译成统一的字符串后，CSV 与统计代码都更直观。",
  },
  {
    name: "事件去抖",
    tag: "EVENT_COOLDOWN_TICKS",
    detail: "默认 20 ticks",
    role: "避免刷屏",
    extra: "换灯则立即触发",
    text: "同一盏交通灯短时间内不重复记录；换到下一个交通灯立刻记录一条新事件。",
  },
];

export const chapter05MetricCards = [
  {
    title: "总事件数",
    text: "反映整个运行过程中触发记录的次数，可以验证阈值是否过大或过小。",
  },
  {
    title: "红灯事件数",
    text: "实验四的核心结论字段，直接对应指导书中的“红灯相关记录条数”。",
  },
  {
    title: "红灯占比",
    text: "红灯事件 / 总事件，结合运行时长能反映本次行驶遇红灯的频率。",
  },
  {
    title: "红灯时平均车速",
    text: "用来观察自动驾驶在接近红灯时是否真的减速，是写结论时的有力证据。",
  },
];

export const chapter05ObserverCards = [
  {
    title: "矢量 SVG 可视化",
    text: "用纯标准库生成 1080×760 的 SVG 矢量图，浏览器直接打开，放大不糊；不依赖 matplotlib、pandas。",
  },
  {
    title: "面板 1：俯视轨迹散点",
    text: "把 events.csv 中的 ego_x / ego_y 画成俯视散点图，每个点按 Red / Yellow / Green 着色，并标出起点和终点。",
  },
  {
    title: "面板 2：事件时间线",
    text: "x 轴是仿真时间，y 轴是 light_id，每条事件落到对应行；一眼能看出主车遇到几盏灯、各灯的事件密度。",
  },
  {
    title: "面板 3：行为标签条形图",
    text: "闯红灯嫌疑、红灯前停车、红灯慢速接近、红灯远观察、黄灯加速/减速、绿灯通行，8 类标签数量对比一目了然。",
  },
  {
    title: "面板 4：红灯速度直方图",
    text: "对所有红灯事件按速度分桶 (<1, 1-5, 5-10, 10-20, 20-40, ≥40 km/h)，验证自动驾驶是否真的在红灯前减速。",
  },
  {
    title: "同时落 Markdown 报告",
    text: "除了 SVG，还会输出 analysis_report.md：行为分布、闯红灯嫌疑表、最长红灯等待序列、Top 3 最常遇路口。",
  },
  {
    title: "纯离线、可反复跑",
    text: "不需要 CARLA 服务器；改阈值后再生成一份新 events.csv，用同一个可视化器跑一遍，就能得到对比报告与 SVG。",
  },
];

export const chapter05Slides = [
  {
    no: "01",
    outline: "代码段 1 参数常量",
    title: "代码段 1：把阈值、运行时长和字段集中写在文件顶部",
    lead: "实验四的关键不是算法，而是几个可控参数。把它们写在文件顶部，调阈值时不用再翻代码。",
    code: String.raw`import csv
import json
import math
from pathlib import Path

import carla


OUTPUT_ROOT = Path("output/exp04")

FIXED_DELTA_SECONDS = 0.05
RUN_SECONDS = 60
WARMUP_TICKS = 30
RUN_TICKS = int(RUN_SECONDS / FIXED_DELTA_SECONDS)

TRAFFIC_MANAGER_PORT = 8000

TRIGGER_DISTANCE_M = 25.0
EVENT_COOLDOWN_TICKS = 20

EVENT_FIELDS = [
    "frame", "tick", "sim_time_s", "speed_kmh",
    "light_state", "distance_m", "light_id", "ego_x", "ego_y",
]

LIGHT_STATE_LABELS = {
    carla.TrafficLightState.Red: "Red",
    carla.TrafficLightState.Yellow: "Yellow",
    carla.TrafficLightState.Green: "Green",
    carla.TrafficLightState.Off: "Off",
    carla.TrafficLightState.Unknown: "Unknown",
}`,
    explain: "这一段定义输出目录、仿真步长、运行时长、Traffic Manager 端口、触发阈值、事件冷却时间、日志字段顺序，并把 carla.TrafficLightState 翻译成统一的字符串。",
    why: "实验四要求“说明触发阈值设置依据”。把 TRIGGER_DISTANCE_M 和 EVENT_COOLDOWN_TICKS 提到顶部，学生在调参时只改这一处，写报告时也容易引用具体数值。",
    points: [
      "TRIGGER_DISTANCE_M 控制写日志的距离边界，过大会冗余、过小会漏记。",
      "EVENT_COOLDOWN_TICKS 用来去抖，避免同一盏红灯每帧都记一条。",
      "LIGHT_STATE_LABELS 把状态翻成字符串后，CSV 与 JSON 更直观。",
    ],
    terms: [
      { title: "OUTPUT_ROOT", text: "本章结果保存在 output/exp04/ 下。" },
      { title: "FIXED_DELTA_SECONDS", text: "0.05 表示每 tick 仿真 50 ms。" },
      { title: "EVENT_FIELDS", text: "CSV 字段顺序，写入和读取时都用它。" },
    ],
  },
  {
    no: "02",
    outline: "代码段 2 工具函数",
    title: "代码段 2：速度、距离与状态翻译三个小工具",
    lead: "事件日志写出去之前，要先准备好“怎么算速度”“怎么算距离”“怎么读状态”三件事。",
    code: String.raw`def speed_kmh(actor):
    velocity = actor.get_velocity()
    speed_mps = math.sqrt(
        velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2
    )
    return speed_mps * 3.6


def distance_between(actor_a, actor_b):
    loc_a = actor_a.get_location()
    loc_b = actor_b.get_location()
    dx = loc_a.x - loc_b.x
    dy = loc_a.y - loc_b.y
    dz = loc_a.z - loc_b.z
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def light_state_label(state):
    return LIGHT_STATE_LABELS.get(state, "Unknown")`,
    explain: "speed_kmh 把三维速度向量换算成 km/h，distance_between 直接算两个 actor 之间的欧氏距离，light_state_label 把 TrafficLightState 翻译成字符串。",
    why: "把三件事写成函数，主循环里只剩“判断 + 记录”这两步，调试和维护都更轻松；翻译状态时用 dict.get，缺省返回 Unknown 也不会崩。",
    points: [
      "速度向量不能直接当车速，要先求模再乘 3.6。",
      "距离计算包含 z 轴，避免高架桥上的灯被误算为最近。",
      "状态翻译用查表更安全，少写 if/elif 的层级。",
    ],
    terms: [
      { title: "get_velocity", text: "返回三维速度向量，单位 m/s。" },
      { title: "get_location", text: "返回 actor 当前位置，包含 x/y/z。" },
      { title: "TrafficLightState", text: "Red/Yellow/Green/Off/Unknown 的枚举。" },
    ],
  },
  {
    no: "03",
    outline: "代码段 3 同步模式",
    title: "代码段 3：进入同步模式，并准备好恢复世界的开关",
    lead: "事件日志要可复现，必须保证仿真节奏稳定，这一段把同步模式封装成一组对称的函数。",
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
    return world.tick(timeout)`,
    explain: "enable_sync_mode 进入同步模式并返回原始设置；restore_world 在最后把 Traffic Manager 和 world 都还原；safe_destroy 处理已被销毁 actor 的边缘情况；tick_world 带超时，防止异常下长时间卡住。",
    why: "实验四要求“事件记录可复现”。同步模式和固定步长是“可复现”的最底层条件。把开/关都封装好，主流程的 try/finally 里就能保证退出时一定恢复。",
    points: [
      "original_settings 要先保存，最后才能恢复。",
      "Traffic Manager 也有同步状态，不能只恢复 world。",
      "tick 加超时后，CARLA 异常时会直接报错，比一直卡住更利于调试。",
    ],
    terms: [
      { title: "synchronous_mode", text: "由代码主动推进世界，节奏稳定。" },
      { title: "fixed_delta_seconds", text: "每个 tick 代表固定仿真时间。" },
      { title: "safe_destroy", text: "对已销毁 actor 调用 destroy 不会抛错。" },
    ],
  },
  {
    no: "04",
    outline: "代码段 4 主车与交通灯",
    title: "代码段 4：生成主车并一次性拿到所有交通灯",
    lead: "本章只需要一辆主车，但需要拿到地图里的全部交通灯，后面才能找“离得最近”的那一盏。",
    code: String.raw`def spawn_ego_vehicle(world, bp_lib, spawn_points):
    ego_bp = bp_lib.find("vehicle.tesla.model3")
    ego_bp.set_attribute("role_name", "hero")

    for spawn_point in spawn_points:
        ego_vehicle = world.try_spawn_actor(ego_bp, spawn_point)
        if ego_vehicle is not None:
            return ego_vehicle

    raise RuntimeError("主车生成失败，请重新运行或更换地图")


def get_traffic_lights(world):
    lights = list(world.get_actors().filter("traffic.traffic_light*"))
    if not lights:
        raise RuntimeError(
            "当前地图没有交通灯，请切换到 Town03 / Town05 等城市地图"
        )
    return lights`,
    explain: "spawn_ego_vehicle 依次尝试出生点直到主车成功生成；get_traffic_lights 用 filter(\"traffic.traffic_light*\") 一次性拿到地图中所有的交通灯 actor。",
    why: "交通灯属于世界中的静态 actor，开局拿到一份引用即可，循环里不需要每帧重新查询。如果在 Town01/Town04 这种少灯地图运行会直接报错，提示切换地图。",
    points: [
      "try_spawn_actor 失败返回 None，可以反复尝试出生点。",
      "filter 通配符 \"traffic.traffic_light*\" 才能匹配带后缀的型号。",
      "建议在 Town03、Town05 等城市地图中运行，红灯样本更多。",
    ],
    terms: [
      { title: "role_name=hero", text: "Carla 中常用的主车标识。" },
      { title: "world.get_actors", text: "返回当前世界所有 actor 的句柄。" },
      { title: "filter", text: "通过蓝图 ID 通配符筛选 actor。" },
    ],
  },
  {
    no: "05",
    outline: "代码段 5 最近交通灯",
    title: "代码段 5：每帧找一次离主车最近的交通灯",
    lead: "“事件触发”要先有“当前观察对象”。这一段就负责每帧选出最近的那一盏交通灯。",
    code: String.raw`def find_nearest_traffic_light(ego_vehicle, traffic_lights):
    nearest_light = None
    nearest_distance = float("inf")

    for light in traffic_lights:
        distance = distance_between(ego_vehicle, light)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_light = light

    return nearest_light, nearest_distance`,
    explain: "遍历地图中所有交通灯，找出距离最小的那一盏，同时返回它的距离。",
    why: "事件日志只有在“当前观察的交通灯距离 < 阈值”时才写出。每帧重新选最近灯，可以避免主车开过红灯之后还在记上一盏灯的状态。",
    points: [
      "返回值是 (light, distance)，调用方一次拿全。",
      "用 float(\"inf\") 作为初始值，比一开始就取第一个简单。",
      "若 traffic_lights 为空，返回 (None, inf)，调用方需要先判 None。",
    ],
    terms: [
      { title: "nearest_light", text: "当前帧距离最近的交通灯。" },
      { title: "nearest_distance", text: "对应的欧氏距离，单位米。" },
      { title: "距离阈值", text: "用来判断这个最近灯是否值得记录。" },
    ],
  },
  {
    no: "06",
    outline: "代码段 6 事件采集",
    title: "代码段 6：主循环里完成触发判断与事件去抖",
    lead: "这一段是实验四的核心。所谓“去抖”，就是“同一盏灯短时间内不重复记录”——这样日志才不会因为车辆停在红灯前而被同一条状态刷屏。它把“近距离触发”和“同灯去抖”两个要求一起落到代码里。",
    code: String.raw`def collect_events(world, ego_vehicle, traffic_lights, run_ticks=RUN_TICKS):
    events = []
    last_event_tick = -EVENT_COOLDOWN_TICKS
    last_light_id = None

    for _ in range(WARMUP_TICKS):
        tick_world(world)

    progress_step = max(1, run_ticks // 5)

    for tick_index in range(run_ticks):
        frame_id = tick_world(world)

        if (tick_index + 1) % progress_step == 0 or tick_index == run_ticks - 1:
            percent = (tick_index + 1) / run_ticks * 100
            print(
                f"  红灯监测进度 {percent:5.1f}%  |  已记录事件 {len(events)} 条"
            )

        nearest_light, nearest_distance = find_nearest_traffic_light(
            ego_vehicle, traffic_lights
        )
        if nearest_light is None:
            continue
        if nearest_distance >= TRIGGER_DISTANCE_M:
            continue

        is_new_light = nearest_light.id != last_light_id
        is_cooled_down = tick_index - last_event_tick >= EVENT_COOLDOWN_TICKS
        if not (is_new_light or is_cooled_down):
            continue

        location = ego_vehicle.get_location()
        events.append(
            {
                "frame": frame_id,
                "tick": tick_index,
                "sim_time_s": round(tick_index * FIXED_DELTA_SECONDS, 2),
                "speed_kmh": round(speed_kmh(ego_vehicle), 2),
                "light_state": light_state_label(nearest_light.get_state()),
                "distance_m": round(nearest_distance, 2),
                "light_id": nearest_light.id,
                "ego_x": round(location.x, 2),
                "ego_y": round(location.y, 2),
            }
        )
        last_event_tick = tick_index
        last_light_id = nearest_light.id

    return events`,
    explain: "热身后逐 tick 推进，先用最近交通灯算距离；超过阈值跳过；处在同一盏灯时只有“冷却结束”才记录；换到新的一盏灯时立即记录。每条事件包含帧号、仿真时间、速度、状态、距离、灯 id 和位置。",
    why: "实验四要求“避免无效刷屏记录”。同一盏灯每个 tick 都记一条会产出几百条相同状态的日志；用 last_event_tick 与 last_light_id 实现的去抖既能记新事件，又不丢“同一盏灯状态变化”这种关键瞬间。",
    points: [
      "热身 ticks 不参与触发，避免起步阶段被记录。",
      "is_new_light 优先于冷却判断，确保换灯不会被静默丢弃。",
      "事件字段包含 light_id，便于后续按灯分组分析。",
    ],
    terms: [
      { title: "is_new_light", text: "当前最近灯与上次记录的不是同一盏。" },
      { title: "is_cooled_down", text: "距离上次事件已超过 EVENT_COOLDOWN_TICKS。" },
      { title: "events", text: "本章最终要写入 events.csv 的列表。" },
    ],
  },
  {
    no: "07",
    outline: "代码段 7 写日志",
    title: "代码段 7：把事件列表写成可复查的 CSV",
    lead: "事件结构准备好后，落盘只需要一个 DictWriter。重点在于字段顺序和编码方式。",
    code: String.raw`def write_events_csv(path, events):
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=EVENT_FIELDS)
        writer.writeheader()
        writer.writerows(events)`,
    explain: "用 EVENT_FIELDS 控制列顺序，utf-8-sig 让 Excel 打开时能正确识别中文表头。所有事件一次性写入。",
    why: "events.csv 是实验四的主交付物，必须能直接被 Excel 或 pandas 读取。把字段集中在 EVENT_FIELDS 常量里，可以避免某一行少写一个字段导致整列错位。",
    points: [
      "newline=\"\" 是 csv 模块在 Windows 上的官方推荐写法。",
      "utf-8-sig 兼容 Excel 简体中文环境。",
      "DictWriter 自动按字段名取值，缺失字段会留空。",
    ],
    terms: [
      { title: "EVENT_FIELDS", text: "决定 CSV 列顺序。" },
      { title: "writeheader", text: "写表头一次，避免遗漏。" },
      { title: "utf-8-sig", text: "带 BOM 的 UTF-8，避免乱码。" },
    ],
  },
  {
    no: "08",
    outline: "代码段 8 汇总统计",
    title: "代码段 8：从事件列表算出红灯条数与占比",
    lead: "实验四明确要求“给出红灯相关记录条数与总记录条数”，这一段就是把要求变成具体字段。",
    code: String.raw`def summarize_events(events, run_seconds):
    total = len(events)
    state_counts = {"Red": 0, "Yellow": 0, "Green": 0, "Off": 0, "Unknown": 0}
    for event in events:
        state_counts[event["light_state"]] = state_counts.get(event["light_state"], 0) + 1

    red_count = state_counts["Red"]
    red_ratio = round(red_count / total, 3) if total else 0.0

    speed_when_red = [event["speed_kmh"] for event in events if event["light_state"] == "Red"]
    avg_red_speed = round(sum(speed_when_red) / len(speed_when_red), 2) if speed_when_red else 0.0

    return {
        "run_seconds": run_seconds,
        "trigger_distance_m": TRIGGER_DISTANCE_M,
        "event_cooldown_ticks": EVENT_COOLDOWN_TICKS,
        "total_events": total,
        "red_events": red_count,
        "yellow_events": state_counts["Yellow"],
        "green_events": state_counts["Green"],
        "red_ratio": red_ratio,
        "avg_speed_when_red_kmh": avg_red_speed,
    }


def save_outputs(events, summary):
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    write_events_csv(OUTPUT_ROOT / "events.csv", events)

    (OUTPUT_ROOT / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "实验四 红灯状态监测与事件日志分析 汇总",
        f"运行时长（秒）: {summary['run_seconds']}",
        f"触发阈值（米）: {summary['trigger_distance_m']}",
        f"事件冷却（ticks）: {summary['event_cooldown_ticks']}",
        f"总事件数: {summary['total_events']}",
        f"红灯事件: {summary['red_events']}",
        f"黄灯事件: {summary['yellow_events']}",
        f"绿灯事件: {summary['green_events']}",
        f"红灯占比: {summary['red_ratio']}",
        f"红灯时平均车速 (km/h): {summary['avg_speed_when_red_kmh']}",
    ]
    (OUTPUT_ROOT / "summary.txt").write_text("\n".join(lines), encoding="utf-8")`,
    explain: "summarize_events 数一遍各状态事件、计算红灯占比和红灯时平均速度；save_outputs 把事件落到 CSV，把汇总同时写入 summary.json（程序读）与 summary.txt（人读）。",
    why: "实验四的结论要写在报告里，最好同时有 JSON（自动读取）和 TXT（人眼快速核对）。把 TRIGGER_DISTANCE_M 与 EVENT_COOLDOWN_TICKS 也写进 summary，方便后续复查触发依据。",
    points: [
      "事件数为 0 时要返回 0.0，避免除零异常。",
      "红灯平均速度能反映自动驾驶在接近红灯时是否减速。",
      "summary 同时写 JSON 和 TXT，兼顾自动分析与人读核对。",
    ],
    terms: [
      { title: "state_counts", text: "按交通灯状态分组的计数表。" },
      { title: "red_ratio", text: "红灯事件占总事件的比例。" },
      { title: "avg_speed_when_red_kmh", text: "仅在红灯事件下统计的平均速度。" },
    ],
  },
  {
    no: "09",
    outline: "代码段 9 主流程",
    title: "代码段 9：main 串起整套流程，并在 finally 里回收资源",
    lead: "前面所有函数都准备好后，真正运行实验的代码很短。这一段把同步设置、车辆、采集、保存全部串起来，并保证 finally 一定执行。",
    code: String.raw`def main(run_seconds=RUN_SECONDS):
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

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
        ego_vehicle.set_autopilot(True, traffic_manager.get_port())

        traffic_lights = get_traffic_lights(world)
        print(f"地图中共发现 {len(traffic_lights)} 个交通灯对象")

        run_ticks = int(run_seconds / FIXED_DELTA_SECONDS)
        print(f"本次运行 {run_seconds} 秒，约 {run_ticks} ticks")

        events = collect_events(world, ego_vehicle, traffic_lights, run_ticks)
        summary = summarize_events(events, run_seconds)
        save_outputs(events, summary)

        print("\n=== 实验四 汇总 ===")
        for key, value in summary.items():
            print(f"{key}: {value}")
        print(f"\n结果已保存到：{OUTPUT_ROOT.resolve()}")

    finally:
        for actor in actors:
            if isinstance(actor, carla.Vehicle):
                try:
                    actor.set_autopilot(False, traffic_manager.get_port())
                except RuntimeError:
                    pass

        for actor in reversed(actors):
            safe_destroy(actor)

        restore_world(world, traffic_manager, original_settings)


# 在 notebook 里逐段复制时，建议先跑短演示，确认流程能结束
try:
    get_ipython
    main(run_seconds=10)
except NameError:
    main()`,
    explain: "main 连接 CARLA、进入同步模式、生成主车、拿到交通灯、跑采样、落盘、打印汇总；finally 把自动驾驶关掉、销毁所有 actor、恢复世界设置。",
    why: "课堂演示常常因为异常退出而留下脏环境，下一次再运行就报错。把所有清理写在 finally 里，可以最大限度保证“即使中途按 Ctrl+C 也不会破坏世界状态”。notebook 里则先跑 10 秒短演示，验证流程能正常结束。",
    points: [
      "finally 必须能在任何分支上都执行清理。",
      "销毁车辆前先关自动驾驶，减少 Traffic Manager 状态残留。",
      "notebook 中先 main(run_seconds=10) 验证，再 main() 提交。",
    ],
    terms: [
      { title: "client.set_timeout", text: "连接 CARLA 的最长等待时间。" },
      { title: "actors", text: "本次实验创建的所有 actor，用于统一销毁。" },
      { title: "get_ipython", text: "存在则说明运行在 notebook 中。" },
    ],
  },
];

export const chapter05Pitfalls = [
  {
    title: "全程记录",
    text: "不设阈值或阈值过大会把每个 tick 都记一条，几千行红灯事件不利于分析。",
  },
  {
    title: "忘了去抖",
    text: "同一盏红灯每帧都写一条不仅冗余，还会让“红灯占比”偏高。",
  },
  {
    title: "在没红灯的地图上跑",
    text: "Town01 / Town04 / Town06 红绿灯较少。建议在 Town03 / Town05 / Town10HD 等城市地图运行。",
  },
  {
    title: "看到 87% 红灯占比就以为出 bug",
    text: "短时间运行 + 自动驾驶倾向停红灯 + 出生点靠近路口，常导致红灯占比偏高。这是 CARLA 的正常行为，不是代码错误；运行更长时间会回归合理范围。",
  },
  {
    title: "结论只写主观感受",
    text: "“感觉红灯很多”不算结论。要引用 total_events、red_events、red_ratio 中至少两项。",
  },
];

export const chapter05Resources = [
  {
    title: "实验报告下载",
    text: "第五章对应实验项目四的报告模板。",
    href: "/courses/carla/exp/实验报告4：xxxx-学生姓名.docx",
    download: "实验报告4：xxxx-学生姓名.docx",
  },
  {
    title: "实验指导书",
    text: "实验项目四的目标、要求和评分标准以此为准。",
    href: "/courses/carla/exp/《自动驾驶软件系统B》实验指导书（学院模板）-阴明旭.docx",
    download: "《自动驾驶软件系统B》实验指导书（学院模板）-阴明旭.docx",
  },
  {
    title: "实验模板",
    text: "保留主流程，把最近交通灯查找、触发判断、汇总统计三处挖空给学生完成。",
    href: "/courses/carla/ch05/exp04_traffic_light_log_template.py",
    download: "exp04_traffic_light_log_template.py",
  },
  {
    title: "实验答案",
    text: "完整可运行脚本，建议独立完成模板后再对照。",
    href: "/courses/carla/ch05/exp04_traffic_light_log_answer.py",
    download: "exp04_traffic_light_log_answer.py",
  },
  {
    title: "整章总代码",
    text: "按本章 9 段顺序整理好的完整示例，可直接 python 运行。",
    href: "/courses/carla/ch05/carla_ch05_all_examples.py",
    download: "carla_ch05_all_examples.py",
  },
  {
    title: "趣味扩展：事件日志可视化分析器",
    text: "读取 events.csv，输出 SVG 矢量四面板图（轨迹 / 时间线 / 标签条 / 红灯速度直方图）+ Markdown 报告。纯标准库，浏览器直接打开 SVG。",
    href: "/courses/carla/ch05/exp04_event_log_visualizer.py",
    download: "exp04_event_log_visualizer.py",
  },
  {
    title: "样例运行结果（ZIP）",
    text: "上机运行 90 秒得到的真实输出：events.csv、summary.json、summary.txt、analysis_report.md、events_visualization.svg 一键打包。",
    href: "/courses/carla/ch05/ch05_exp04_run_results.zip",
    download: "ch05_exp04_run_results.zip",
  },
  {
    title: "实验报告提交",
    text: "完成实验后通过此链接统一提交。",
    href: "https://f.wps.cn/g/WC2Du94Z/",
  },
];
