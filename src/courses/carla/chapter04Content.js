export const chapter04Docs = [
  {
    title: "文档首页",
    text: "先确认课程使用的 CARLA 版本。",
    href: "https://carla.readthedocs.io/en/latest/",
  },
  {
    title: "World 与 Settings",
    text: "同步模式、固定步长、恢复设置都查这里。",
    href: "https://carla.readthedocs.io/en/latest/core_world/",
  },
  {
    title: "Sensors and data",
    text: "RGB 相机、语义分割相机、save_to_disk 都在这里。",
    href: "https://carla.readthedocs.io/en/latest/core_sensors/",
  },
  {
    title: "Synchrony and time-step",
    text: "这一章必须在同步模式下做实验。",
    href: "https://carla.readthedocs.io/en/latest/adv_synchrony_timestep/",
  },
  {
    title: "Python API",
    text: "类和方法拿不准时回到这里。",
    href: "https://carla.readthedocs.io/en/latest/python_api/",
  },
];

export const chapter04AlignmentCards = [
  { title: "同一车辆", text: "两路相机都挂在同一个 ego_vehicle 上。" },
  { title: "同一位姿", text: "两路相机共用同一个 camera_transform。" },
  { title: "同一内参", text: "image_size_x、image_size_y、fov 必须一致。" },
  { title: "同一帧号", text: "最终判断标准是 rgb.frame == seg.frame。" },
];

export const chapter04Slides = [
  {
    no: "01",
    outline: "代码段 1 常量",
    title: "代码段 1：先把实验参数集中定义",
    lead: "第一段不做连接，也不做采集。它的任务只有一个：把整章实验的关键参数全部锁定到一个地方。",
    code: String.raw`# 输出目录：按双通道数据集方式组织
OUTPUT_ROOT = Path("output/exp02")
RGB_DIR = OUTPUT_ROOT / "rgb"
SEG_DIR = OUTPUT_ROOT / "seg"

# 目标采样数量：最终保存 30 对图像
TARGET_PAIRS = 30

# 自动驾驶先热身 20 帧，让车真正跑起来
AUTOPILOT_WARMUP_TICKS = 20

# 正式阶段每隔 8 帧保存一次，避免 30 帧几乎一样
CAPTURE_INTERVAL_TICKS = 8

# 同步模式下每一帧对应 0.05 秒仿真时间
SYNC_DELTA = 0.05

# Traffic Manager 的端口号
TRAFFIC_MANAGER_PORT = 8000

# 让自动驾驶无视红灯，课堂演示更连续
IGNORE_LIGHTS_PERCENTAGE = 100.0

# 两路相机必须保持完全相同的成像参数
IMAGE_SIZE_X = "800"
IMAGE_SIZE_Y = "600"
CAMERA_FOV = "90"`,
    explain: "这一段统一管理输出目录、采集数量、自动驾驶热身时间、采样间隔、同步步长、TM 端口、忽略红灯比例和相机参数。后面所有逻辑都引用这些常量。",
    why: "教学里最怕参数散落各处。学生如果只改这一段，就能直接看到样本数量、采样节奏和自动驾驶效果的变化。",
    points: [
      "CAPTURE_INTERVAL_TICKS 控制“隔几帧再存一对”。",
      "IGNORE_LIGHTS_PERCENTAGE=100.0 让课堂演示更连续。",
      "IMAGE_SIZE 和 FOV 决定两路图像能否严格对应。",
    ],
    terms: [
      { title: "TARGET_PAIRS", text: "最终至少要保存多少对样本。" },
      { title: "AUTOPILOT_WARMUP_TICKS", text: "让车先跑起来，再进入正式采样。" },
      { title: "CAPTURE_INTERVAL_TICKS", text: "不是每 tick 都存，而是隔一段时间再存。" },
    ],
  },
  {
    no: "02",
    outline: "代码段 2 连接与共享变量",
    title: "代码段 2：连接 CARLA，并准备共享变量",
    lead: "第二段开始真正进入实验环境。它负责连接世界、准备目录、保存原始设置，并为后面的双通道监听准备两个队列。",
    code: String.raw`# 连接本地 CARLA 服务端
client = carla.Client("localhost", 2000)
client.set_timeout(10.0)

# 取得当前世界对象和蓝图库
world = client.get_world()
bp_lib = world.get_blueprint_library()

# 提前创建输出目录，避免保存时再报错
RGB_DIR.mkdir(parents=True, exist_ok=True)
SEG_DIR.mkdir(parents=True, exist_ok=True)

# 统一记录所有 actor，便于最后按顺序清理
actor_list = []

# 保存实验开始前的世界设置，结束时必须恢复
original_settings = world.get_settings()

# 两个独立队列分别接收 RGB 和语义分割图像
rgb_queue = queue.Queue(maxsize=1)
seg_queue = queue.Queue(maxsize=1)

# 先占位，后面会真正赋值
traffic_manager = None
ego_vehicle = None`,
    explain: "这里拿到了 world 和 bp_lib，也把 actor_list、original_settings、两个图像队列以及 traffic_manager、ego_vehicle 的占位变量都准备好了。",
    why: "如果不提前保存 original_settings，实验结束后就没法稳定恢复现场；如果不提前准备双队列，后面两路图像会很容易混在一起。",
    points: [
      "bp_lib 是后面查车辆和相机 blueprint 的入口。",
      "rgb_queue 和 seg_queue 必须分开。",
      "traffic_manager 和 ego_vehicle 先占位，后面开关自动驾驶更稳。",
    ],
    terms: [
      { title: "world", text: "当前仿真世界，设置和 actor 都从这里取。" },
      { title: "bp_lib", text: "blueprint library，所有模板都在里面。" },
      { title: "original_settings", text: "实验结束后恢复世界设置要靠它。" },
    ],
  },
  {
    no: "03",
    outline: "代码段 3 小工具",
    title: "代码段 3：先把实验的小工具函数写好",
    lead: "这一段是整章最值得学生仔细看的地方。主流程短不代表实验简单，真正稳定运行靠的是这些工具函数。",
    code: String.raw`def safe_destroy(actor):
    # 统一封装 destroy，避免个别 actor 已失效时直接中断实验
    if actor is None:
        return
    try:
        actor.destroy()
    except RuntimeError:
        pass


def push_latest(channel_queue, image):
    # 队列里如果还有旧图像，全部清掉，只保留最新一帧
    while not channel_queue.empty():
        try:
            channel_queue.get_nowait()
        except queue.Empty:
            break

    try:
        channel_queue.put_nowait(image)
    except queue.Full:
        pass


def wait_for_image(channel_queue, target_frame, timeout=2.0):
    # 在超时限制内持续等待，直到这一通道追上目标帧
    deadline = time.time() + timeout
    while time.time() < deadline:
        remaining = max(0.0, deadline - time.time())
        image = channel_queue.get(timeout=remaining)
        if image.frame >= target_frame:
            return image

    raise TimeoutError(f"等待目标帧 {target_frame} 超时")


def wait_for_aligned_pair(target_frame, timeout=3.0):
    # 先分别让两路都追上世界当前帧
    rgb_image = wait_for_image(rgb_queue, target_frame, timeout=timeout)
    seg_image = wait_for_image(seg_queue, target_frame, timeout=timeout)

    # 如果两路 frame 不一致，就继续追，直到完全相同
    while rgb_image.frame != seg_image.frame:
        if rgb_image.frame < seg_image.frame:
            rgb_image = wait_for_image(rgb_queue, seg_image.frame, timeout=timeout)
        else:
            seg_image = wait_for_image(seg_queue, rgb_image.frame, timeout=timeout)

    return rgb_image, seg_image


def cleanup():
    # 先关闭自动驾驶和 Traffic Manager 的同步状态
    if traffic_manager is not None and ego_vehicle is not None:
        ego_vehicle.set_autopilot(False, traffic_manager.get_port())
        traffic_manager.set_synchronous_mode(False)

    # 再停传感器、销毁 actor、恢复世界设置
    for actor in reversed(actor_list):
        if isinstance(actor, carla.Sensor):
            actor.stop()
        safe_destroy(actor)

    actor_list.clear()
    world.apply_settings(original_settings)`,
    explain: "这一页把整章最关键的辅助函数一次性补齐：safe_destroy 负责安全销毁，push_latest 负责保留最新帧，wait_for_image 负责追帧，wait_for_aligned_pair 负责同帧对齐，cleanup 负责最后恢复现场。",
    why: "如果没有这组函数，主流程里会充满重复逻辑。更重要的是，错帧问题、清理问题和异常退出问题都会很难排查，因为你不知道自己拿到的是不是旧图像，也不知道环境有没有恢复干净。",
    points: [
      "push_latest 的核心是丢掉旧帧。",
      "wait_for_aligned_pair 才是双通道对齐的关键。",
      "cleanup 不是收尾点缀，而是实验能否反复运行的保障。",
    ],
    terms: [
      { title: "safe_destroy", text: "让清理动作更稳，避免单个 actor 异常拖垮收尾。" },
      { title: "target_frame", text: "本次想追上的世界帧号。" },
      { title: "cleanup", text: "统一收口所有清理动作，保证实验结束后环境可复用。" },
    ],
  },
  {
    no: "04",
    outline: "代码段 4 同步模式与主车",
    title: "代码段 4：开启同步模式，并生成主车",
    lead: "第四段把世界切到同步模式，再稳妥地生成一辆主车。实验指导书要求的“固定步长同步推进”就是从这里开始落实的。",
    code: String.raw`# 取出当前设置，并切换到同步模式
settings = world.get_settings()
settings.synchronous_mode = True
settings.fixed_delta_seconds = SYNC_DELTA
world.apply_settings(settings)

# 选择一辆主车作为实验载体
vehicle_bp = bp_lib.find("vehicle.tesla.model3")
vehicle_bp.set_attribute("role_name", "hero")

# 取出所有出生点并打乱顺序，减少冲突失败概率
spawn_points = world.get_map().get_spawn_points()
random.shuffle(spawn_points)

# 逐个尝试生成主车，直到成功
for spawn_point in spawn_points:
    ego_vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
    if ego_vehicle is not None:
        break

# 如果所有出生点都失败，就直接报错
if ego_vehicle is None:
    raise RuntimeError("主车生成失败，请更换地图或重新运行")

# 主车也要加入 actor_list，方便最后统一清理
actor_list.append(ego_vehicle)`,
    explain: "先让世界进入同步模式和固定步长，再选择主车 blueprint，最后在多个出生点里循环尝试，直到成功生成一辆主车，并把它登记到 actor_list 中。",
    why: "如果不先打开同步模式，后面所有 tick、相机帧号和采样节奏都不好解释；如果只试一个出生点，课堂里很容易因为碰撞而生成失败。",
    points: [
      "synchronous_mode=True 表示后面每一步都由 world.tick() 驱动。",
      "try_spawn_actor 比直接 spawn_actor 更适合课堂实验。",
      "actor_list.append(ego_vehicle) 说明车辆也属于后面要回收的资源。",
    ],
    terms: [
      { title: "synchronous_mode", text: "同步模式是整章实验的基础。" },
      { title: "fixed_delta_seconds", text: "固定步长能让采样节奏可解释、可复现。" },
      { title: "role_name = hero", text: "把主车标记为 hero，便于后续系统识别。" },
    ],
  },
  {
    no: "05",
    outline: "代码段 5 双相机挂载",
    title: "代码段 5：准备双相机蓝图，并挂到主车上",
    lead: "这一段真正把“双通道”搭起来。它最重要的不是挂载动作本身，而是把同位姿、同内参写成代码事实。",
    code: String.raw`# 查找两路相机蓝图
rgb_bp = bp_lib.find("sensor.camera.rgb")
seg_bp = bp_lib.find("sensor.camera.semantic_segmentation")

# 强制两路相机使用同一套内参，保证画面可比较
for bp in (rgb_bp, seg_bp):
    bp.set_attribute("image_size_x", IMAGE_SIZE_X)
    bp.set_attribute("image_size_y", IMAGE_SIZE_Y)
    bp.set_attribute("fov", CAMERA_FOV)
    bp.set_attribute("sensor_tick", "0.0")

# 定义两路相机共同使用的安装位姿
CAMERA_TRANSFORM = carla.Transform(
    carla.Location(x=1.5, y=0.0, z=2.4),
    carla.Rotation(pitch=0.0, yaw=0.0, roll=0.0),
)

# 用同一个安装位姿把两路相机挂到主车上
rgb_camera = world.spawn_actor(
    rgb_bp,
    CAMERA_TRANSFORM,
    attach_to=ego_vehicle,
    attachment_type=carla.AttachmentType.Rigid,
)
seg_camera = world.spawn_actor(
    seg_bp,
    CAMERA_TRANSFORM,
    attach_to=ego_vehicle,
    attachment_type=carla.AttachmentType.Rigid,
)

# 记得把两路相机也放进 actor_list，便于最后统一销毁
actor_list.extend([rgb_camera, seg_camera])`,
    explain: "两路相机 blueprint 都被强制设置成相同分辨率、相同 FOV、相同采样节奏，再用同一个 CAMERA_TRANSFORM 挂到同一辆车上。",
    why: "如果两路的尺寸、视场角或安装位姿不同，后面的图像就算 frame 一样，也不算严格可比的数据对。",
    points: [
      "RGB 相机提供真实视觉外观。",
      "语义分割相机提供像素级语义标签。",
      "CAMERA_TRANSFORM 和 actor_list.extend 都是这一页必须讲透的细节。",
    ],
    terms: [
      { title: "CAMERA_TRANSFORM", text: "明确把双相机安装在同一辆车的同一位置。" },
      { title: "sensor.camera.semantic_segmentation", text: "标签通道。" },
      { title: "sensor_tick = 0.0", text: "每个仿真步都允许传感器出图。" },
    ],
  },
  {
    no: "06",
    outline: "代码段 6 监听与自动驾驶",
    title: "代码段 6：注册双监听，再让主车自动驾驶并无视红灯",
    lead: "这一段让整章真正“动起来”。相机开始持续送图，主车开始自动驾驶，无视红灯则让演示过程更连续。",
    code: String.raw`# 两路相机开始持续回调，把最新图像推进各自队列
rgb_camera.listen(lambda image: push_latest(rgb_queue, image))
seg_camera.listen(lambda image: push_latest(seg_queue, image))

# 获取 Traffic Manager，并让它也进入同步模式
traffic_manager = client.get_trafficmanager(TRAFFIC_MANAGER_PORT)
traffic_manager.set_synchronous_mode(True)

# 把主车交给自动驾驶系统管理
ego_vehicle.set_autopilot(True, traffic_manager.get_port())

# 设置主车无视红灯，提高样本变化速度
traffic_manager.ignore_lights_percentage(ego_vehicle, IGNORE_LIGHTS_PERCENTAGE)`,
    explain: "先让两路相机开始把最新图像推进各自队列，再获取 Traffic Manager，把它切到同步模式，并把主车注册进自动驾驶系统，最后设置无视红灯。",
    why: "如果车不动，30 对图像差异会很小；如果车老在路口停住，课堂演示节奏也会被打断。让它自动驾驶并无视红灯，会更适合教学展示。",
    points: [
      "listen 只是开始接图，不等于图像已经对齐。",
      "Traffic Manager 也要同步，否则节奏会错位。",
      "ignore_lights_percentage 是官方 API，不是自己胡乱改控制逻辑。",
    ],
    terms: [
      { title: "set_autopilot", text: "把车辆交给 Traffic Manager 管理。" },
      { title: "get_port()", text: "后面关闭自动驾驶时还要用同一个端口。" },
      { title: "ignore_lights_percentage", text: "设置车辆忽略红绿灯的概率，0 到 100。" },
    ],
  },
  {
    no: "07",
    outline: "代码段 7 热身",
    title: "代码段 7：先热身，让车和双相机一起稳定下来",
    lead: "第七段不保存正式样本，而是给系统一个稳定期。课堂上这一步很重要，因为它能让学生真正看到‘世界在跑、相机在追帧’。",
    code: String.raw`# 正式采样前，先让车辆在自动驾驶状态下热身
for warmup_index in range(AUTOPILOT_WARMUP_TICKS):
    # 推进世界一帧
    frame_id = world.tick()

    # 即使是热身阶段，也要确保双通道已经追到同一帧
    rgb_image, seg_image = wait_for_aligned_pair(frame_id)

    # 每 5 帧打印一次，便于课堂观察
    if (warmup_index + 1) % 5 == 0:
        print(
            f"warmup {warmup_index + 1}/{AUTOPILOT_WARMUP_TICKS}: "
            f"rgb={rgb_image.frame}, seg={seg_image.frame}"
        )`,
    explain: "这一段让主车先在自动驾驶状态下跑一会儿，同时每一帧都检查双通道是否已经对齐，但还不正式保存图片。",
    why: "刚切入自动驾驶时，车辆和传感器都需要一点时间进入稳定状态。热身之后再采样，更容易得到画面变化明显、节奏稳定的数据。",
    points: [
      "热身阶段也必须坚持做同帧校验。",
      "不是只有正式采样才关心 frame。",
      "每 5 帧打印一次，更适合课堂观察。",
    ],
    terms: [
      { title: "AUTOPILOT_WARMUP_TICKS", text: "控制正式采样前的热身长度。" },
      { title: "world.tick()", text: "同步模式下推进世界一帧的唯一入口。" },
      { title: "print 调试", text: "让学生真正看见帧号变化，是理解同步模式的关键。" },
    ],
  },
  {
    no: "08",
    outline: "代码段 8 间隔采样",
    title: "代码段 8：车辆持续前进，但只每隔几帧保存一对图像",
    lead: "第八段就是这章最有‘效果’的部分。世界在持续往前走，但我们只在合适的节奏点保存一对图像。",
    code: String.raw`# 记录已经成功保存的帧号
captured_frames = []

# 记录热身之后又额外行驶了多少帧
drive_ticks = 0

while len(captured_frames) < TARGET_PAIRS:
    # 世界继续前进，车辆也继续前进
    frame_id = world.tick()
    drive_ticks += 1

    # 每一帧都先做同帧对齐校验
    rgb_image, seg_image = wait_for_aligned_pair(frame_id)

    # 没到采样间隔就跳过，这一帧不保存
    if drive_ticks % CAPTURE_INTERVAL_TICKS != 0:
        continue

    # 用 frame 作为文件名，最利于后续自动配对
    frame_name = f"{rgb_image.frame:06d}.png"
    rgb_image.save_to_disk(str(RGB_DIR / frame_name))
    seg_image.save_to_disk(str(SEG_DIR / frame_name))
    captured_frames.append(rgb_image.frame)`,
    explain: "世界的每一帧都在继续运行，但只有当 drive_ticks 到达采样间隔时，才真正保存一对 RGB 和语义分割图像。",
    why: "如果每一帧都保存，30 对图像之间差异太小。间隔采样会让相邻样本变化更明显，同时又不牺牲同帧对齐。",
    points: [
      "drive_ticks 统计的是热身后又额外跑了多少帧。",
      "continue 的意思是这一帧继续运行，但这次不保存。",
      "每次保存的单位始终是一对图像，而不是单张。",
    ],
    terms: [
      { title: "while len(captured_frames) < TARGET_PAIRS", text: "以真实已保存对数作为结束条件。" },
      { title: "CAPTURE_INTERVAL_TICKS", text: "决定采样频率，不决定车辆是否继续前进。" },
      { title: "frame_name", text: "直接用 frame 作为文件名，是后续自动配对最稳的方法。" },
    ],
  },
  {
    no: "09",
    outline: "代码段 9 报告输出",
    title: "代码段 9：输出参数记录和对齐报告",
    lead: "第九段把‘看起来跑通了’变成‘别人可以复查这次实验到底怎么做的’。这一步是实验指导书明确要求的。",
    code: String.raw`# 读取两个目录下的所有帧号
rgb_frames = {path.stem for path in RGB_DIR.glob("*.png")}
seg_frames = {path.stem for path in SEG_DIR.glob("*.png")}

# 取交集，得到真正匹配成功的帧
matched_frames = sorted(rgb_frames & seg_frames)

# 记录实验关键参数，方便复现
params = {
    "fixed_delta_seconds": SYNC_DELTA,
    "ignore_lights_percentage": IGNORE_LIGHTS_PERCENTAGE,
    "capture_interval_ticks": CAPTURE_INTERVAL_TICKS,
}

# 记录对齐结果，说明有没有缺失帧
report = {
    "rgb_count": len(rgb_frames),
    "seg_count": len(seg_frames),
    "matched_count": len(matched_frames),
    "missing_in_seg": sorted(rgb_frames - seg_frames),
    "missing_in_rgb": sorted(seg_frames - rgb_frames),
    "is_aligned": len(rgb_frames) == len(seg_frames) == len(matched_frames),
}

# 把实验条件和对齐结果真正写入磁盘
(OUTPUT_ROOT / "params.json").write_text(
    json.dumps(params, indent=2, ensure_ascii=False),
    encoding="utf-8",
)
(OUTPUT_ROOT / "alignment_report.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False),
    encoding="utf-8",
)`,
    explain: "这一段先统计 rgb 和 seg 目录里的帧号集合，再求交集得到真正匹配成功的样本数。随后构造 params 和 report 两个字典，并真正写入 `params.json` 与 `alignment_report.json`。",
    why: "实验不应该只交图片。别人如果想复现，必须知道同步步长、采样间隔、是否忽略红灯、到底保存了多少对以及有没有缺失帧。",
    points: [
      "params.json 负责记录实验条件。",
      "alignment_report.json 负责记录结果是否对齐。",
      "write_text 说明这不是控制台打印，而是正式实验产出。",
    ],
    terms: [
      { title: "rgb_frames / seg_frames", text: "先比较集合，再判断是否完全一一对应。" },
      { title: "missing_in_seg", text: "表示 RGB 有、语义分割没有的帧。" },
      { title: "is_aligned", text: "最终布尔结论，True 才说明两路文件严格配对。" },
    ],
  },
  {
    no: "10",
    outline: "代码段 10 清理",
    title: "代码段 10：实验结束时，按顺序清理资源",
    lead: "最后一段不是收尾点缀，而是整章实验能不能长期复用的关键。很多课堂问题都不是代码不会写，而是环境没清干净。",
    code: String.raw`# 调用统一清理函数，关闭自动驾驶并恢复世界设置
cleanup()

# 给出完成提示，方便课堂观察脚本结束位置
print("第三章示例代码已清理完成")`,
    explain: "这一段调用 cleanup()，把自动驾驶、Traffic Manager、传感器、车辆和世界设置都恢复回实验前的状态。",
    why: "如果实验结束后还残留同步模式、自动驾驶车辆或相机 actor，下一次运行代码时就会出现很多连锁问题，而且很难解释。",
    points: [
      "先关自动驾驶，再停传感器，再销毁 actor，最后恢复 world settings。",
      "规范清理是工程习惯，不是可选动作。",
      "后续章节可以直接复用这套清理结构。",
    ],
    terms: [
      { title: "cleanup()", text: "把所有清理动作集中到一个函数里，主流程会更清楚。" },
      { title: "stop() 与 destroy()", text: "对相机这类传感器，通常先 stop 再 destroy 更稳。" },
      { title: "恢复现场", text: "实验结束后把世界恢复原状，是最基本的实验礼仪。" },
    ],
  },
];

export const chapter04Pitfalls = [
  { title: "只看图片像不像", text: "相似不代表同帧，对齐最终还是要看 frame 和文件名。" },
  { title: "让车动了，但没做对齐", text: "车辆运动越明显，错帧问题反而越容易暴露。" },
  { title: "每 tick 都存", text: "能运行，但 30 对样本变化不明显，课堂效果并不好。" },
  { title: "忘了清理环境", text: "同步模式、TM、传感器残留，会直接影响下次实验。" },
];

export const chapter04Resources = [
  {
    title: "实验报告下载",
    text: "第三章对应第二份实验报告模板。",
    href: "/courses/carla/exp/实验报告2：xxxx-学生姓名.docx",
    download: "实验报告2：xxxx-学生姓名.docx",
  },
  {
    title: "实验指导书",
    text: "实验项目二的目标和评分标准以此为准。",
    href: "/courses/carla/exp/《自动驾驶软件系统B》实验指导书（学院模板）-阴明旭.docx",
    download: "《自动驾驶软件系统B》实验指导书（学院模板）-阴明旭.docx",
  },
  {
    title: "实验模板",
    text: "按网页顺序补全空位即可。",
    href: "/courses/carla/ch04/exp02_rgb_seg_alignment_template.py",
    download: "exp02_rgb_seg_alignment_template.py",
  },
  {
    title: "实验答案",
    text: "完整可运行脚本，建议最后再对照。",
    href: "/courses/carla/ch04/exp02_rgb_seg_alignment_answer.py",
    download: "exp02_rgb_seg_alignment_answer.py",
  },
  {
    title: "整章总代码",
    text: "按 notebook 风格组织好的整章示例。",
    href: "/courses/carla/ch04/carla_ch04_all_examples.py",
    download: "carla_ch04_all_examples.py",
  },
  {
    title: "实验报告提交",
    text: "完成实验后通过此链接统一提交。",
    href: "https://f.wps.cn/g/beaYRGnd/",
  },
];
