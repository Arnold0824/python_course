<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const docsHome = "https://carla.readthedocs.io/en/latest/";
const coreWorldDocs = "https://carla.readthedocs.io/en/latest/core_world/";
const sensorsDocs = "https://carla.readthedocs.io/en/latest/core_sensors/";
const synchronyDocs = "https://carla.readthedocs.io/en/latest/adv_synchrony_timestep/";
const trafficManagerDocs = "https://carla.readthedocs.io/en/latest/adv_traffic_manager/";
const pythonApiDocs = "https://carla.readthedocs.io/en/latest/python_api/";

const chapterAllCodeHref = "/courses/carla/ch03/carla_ch03_all_examples.py";
const expTemplateHref = "/courses/carla/ch03/exp01_sync_weather_camera_template.py";
const expAnswerHref = "/courses/carla/ch03/exp01_sync_weather_camera_answer.py";
const expGuideHref = "/courses/carla/exp/《自动驾驶软件系统B》实验指导书（学院模板）-阴明旭.docx";
const expReportHref = "/courses/carla/exp/实验报告1：xxxx-学生姓名.docx";
const expSubmitHref = "https://f.wps.cn/g/8Oy5FwrA/";
const expSubmitQrHref = "/courses/carla/ch03/自动驾驶软件系统B_ 实验报告1.png";
</script>

<template>
  <div ref="rootRef" class="course-page">
    <div class="bg-orb orb-a" aria-hidden="true"></div>
    <div class="bg-orb orb-b" aria-hidden="true"></div>
    <div class="bg-grid" aria-hidden="true"></div>

    <div class="progress-track" aria-hidden="true">
      <span id="scrollProgress"></span>
    </div>

    <header class="top-nav">
      <a class="brand" href="#top">
        <span class="brand-tag">CARLA 02</span>
        <strong>车辆生成、传感器挂载与自动采图</strong>
      </a>
      <CourseSwitcher />
    </header>

    <main id="top" class="page is-slide-deck">
      <section
        id="cover"
        class="hero reveal"
        data-outline-level="1"
        data-outline-label="章节封面"
      >
        <p class="kicker">ACTORS, SENSORS AND DATA CAPTURE</p>
        <h1>第二章 车辆生成、传感器挂载与自动采图</h1>
        <p class="hero-intro">
          这一章从“能连接世界”推进到“能在世界里生成主车、把相机挂到车上、稳定拿到图像数据”。
          所有代码都按 notebook 代码段来设计，每一步都先看现象，再继续下一步。
        </p>
        <ul class="hero-checklist">
          <li>理解车辆和相机本质上都是 Actor，对象要先生成，后续才可以操作。</li>
          <li>掌握 <code>attach_to</code>、相对坐标、<code>listen()</code>、同步模式和 <code>sensor_tick</code>。</li>
          <li>完成实验项目一：同步天气控制与相机数据采集。</li>
        </ul>
        <div class="goal-cards fly-in-seq">
          <article>
            <h2>能力目标 1</h2>
            <p>能稳定生成一辆主车，并解释 blueprint、spawn point 和 Actor 的关系。</p>
          </article>
          <article>
            <h2>能力目标 2</h2>
            <p>能把 RGB 相机正确挂到车上，理解位置、姿态和回调采集逻辑。</p>
          </article>
          <article>
            <h2>能力目标 3</h2>
            <p>能在同步模式下切换天气并采集图像，独立完成实验模板。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章路线"
      >
        <div class="section-head">
          <p class="kicker">ROADMAP</p>
          <h2>这一章的学习路线</h2>
        </div>
        <div class="chapter-three-rhythm">
          <span>先生成主车</span>
          <span>再挂载相机</span>
          <span>再监听图像</span>
          <span>最后做同步天气实验</span>
        </div>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>任务 1</h3>
            <p>理解 Actor 和 Blueprint，稳定生成 <code>ego_vehicle</code>。</p>
          </article>
          <article class="concept-card">
            <h3>任务 2</h3>
            <p>把 RGB 相机挂到车上，讲清 <code>attach_to</code> 和相对位姿。</p>
          </article>
          <article class="concept-card">
            <h3>任务 3</h3>
            <p>让相机真正出图，讲清 <code>listen()</code>、回调、同步模式和 <code>world.tick()</code>。</p>
          </article>
          <article class="concept-card">
            <h3>任务 4</h3>
            <p>完成“实验项目一：同步天气控制与相机数据采集”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="官方文档入口"
      >
        <h3>本章直接会用到的官方文档入口</h3>
        <div class="command-layout chapter-three-link-grid chapter-three-link-grid--balanced">
          <article class="command-card">
            <h3>文档首页</h3>
            <p>用来确认当前文档版本和整体结构。</p>
            <a class="chapter-three-link" :href="docsHome" target="_blank" rel="noopener noreferrer">
              {{ docsHome }}
            </a>
          </article>
          <article class="command-card">
            <h3>World 与 Weather</h3>
            <p>本章会用到世界、天气和 Actor 相关说明。</p>
            <a class="chapter-three-link" :href="coreWorldDocs" target="_blank" rel="noopener noreferrer">
              {{ coreWorldDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>Sensors and data</h3>
            <p>这里明确讲了传感器设置、生成、监听和 <code>sensor_tick</code>。</p>
            <a class="chapter-three-link" :href="sensorsDocs" target="_blank" rel="noopener noreferrer">
              {{ sensorsDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>Synchrony and time-step</h3>
            <p>同步模式、固定步长和 GPU 相机延迟，本章都会用到。</p>
            <a class="chapter-three-link" :href="synchronyDocs" target="_blank" rel="noopener noreferrer">
              {{ synchronyDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>Traffic Manager</h3>
            <p>自动驾驶扩展部分会涉及 TM 的同步和自动驾驶注册。</p>
            <a class="chapter-three-link" :href="trafficManagerDocs" target="_blank" rel="noopener noreferrer">
              {{ trafficManagerDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>Python API</h3>
            <p>需要精确查类和方法时，最后都回到 Python API。</p>
            <a class="chapter-three-link" :href="pythonApiDocs" target="_blank" rel="noopener noreferrer">
              {{ pythonApiDocs }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="为什么先学车与相机"
      >
        <h2>为什么第二章先学车与相机，而不是先读官方大脚本</h2>
        <p class="chapter-three-cue">
          <strong>这一章的原则：</strong>先从最小原生 API 跑通“车 + 相机 + 图像”，再去看
          <code>manual_control.py</code> 或 <code>automatic_control.py</code> 这类大脚本。先建立对象关系，再读大型工程代码。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>先感受对象关系</h3>
            <p>车是 Actor，相机也是 Actor；先生成主车，再把相机挂到主车上，这一层关系必须先真正感受到。</p>
          </article>
          <article class="command-card">
            <h3>先看最小现象</h3>
            <p>学生最需要的是“多了一辆车”“相机开始出帧”“磁盘里多了图片”这类可观察结果，而不是大脚本里复杂的类结构。</p>
          </article>
          <article class="command-card">
            <h3>先会原理，再会扩展</h3>
            <p>如果现在直接改官方脚本，很多变量和类都只能机械照抄；先把原生流程走通，后面看官方脚本才知道每一层在做什么。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="Actor 与 Blueprint"
      >
        <h2>先把两个核心词记住：Actor 和 Blueprint</h2>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>Actor</h3>
            <p>Actor 是仿真世界里真正存在的对象。车辆、相机、雷达、行人、交通灯都属于 Actor。</p>
          </article>
          <article class="concept-card">
            <h3>Blueprint</h3>
            <p>Blueprint 是生成 Actor 前使用的模板。先选模板，再把模板生成到世界里。</p>
          </article>
          <article class="concept-card">
            <h3>world 的角色</h3>
            <p><code>world</code> 负责把 Blueprint 转成真的 Actor，也负责保存当前世界里所有 Actor 的状态。</p>
          </article>
          <article class="concept-card">
            <h3>本章的第一条链路</h3>
            <p><code>bp_lib -&gt; vehicle_bp -&gt; spawn_point -&gt; ego_vehicle</code>，这是主车生成链路。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="生成车辆的链路"
      >
        <h3>生成第一辆主车之前，脑子里要先有这条链路</h3>
        <div class="chapter-three-rhythm">
          <span>拿蓝图库</span>
          <span>选车辆蓝图</span>
          <span>找出生点</span>
          <span>生成 ego_vehicle</span>
        </div>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>蓝图库</h3>
            <p>蓝图库是“所有可用模板的集合”。车、传感器、行人都从这里找模板。</p>
          </article>
          <article class="command-card">
            <h3>出生点</h3>
            <p>出生点是一组推荐的 <code>Transform</code>，适合用来生成车辆，但并不保证一定不冲突。</p>
          </article>
          <article class="command-card">
            <h3>ego_vehicle</h3>
            <p><code>ego_vehicle</code> 只是变量名，不是特殊语法。它保存的是你生成出来的那辆主车对象。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 1：生成主车"
      >
        <div class="section-head">
          <p class="kicker">TASK 1</p>
          <h2>任务 1：一步一步生成第一辆主车</h2>
        </div>
        <p class="chapter-three-cue">
          下面 6 段代码建议在 notebook 中按顺序执行。先把环境初始化好，再去生成主车。这样后面的相机、队列、同步模式和资源清理都能直接复用。
        </p>
        <div class="chapter-three-code-stack">
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 1</p>
            <h3>导入依赖并连接 CARLA</h3>
            <pre><code class="python">import os
import queue
import random
import time

import carla

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)
world = client.get_world()

print("当前地图：", world.get_map().name)</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 2</p>
            <h3>准备共享变量和清理函数</h3>
            <pre><code class="python">os.makedirs("output/ch03", exist_ok=True)

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

    raise TimeoutError("未在规定时间内收到目标图像帧")

print("输出目录已准备：output/ch03")</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 3</p>
            <h3>获取蓝图库</h3>
            <pre><code class="python">bp_lib = world.get_blueprint_library()
print(bp_lib)</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 4</p>
            <h3>选择车辆蓝图并查看出生点</h3>
            <pre><code class="python">vehicle_bp = bp_lib.find("vehicle.tesla.model3")
vehicle_bp.set_attribute("role_name", "hero")

spawn_points = world.get_map().get_spawn_points()
print("出生点数量：", len(spawn_points))
print("第一个出生点：", spawn_points[0])</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 5</p>
            <h3>先用第一个出生点尝试一次</h3>
            <pre><code class="python">ego_vehicle = world.try_spawn_actor(vehicle_bp, spawn_points[0])
print("ego_vehicle =", ego_vehicle)

if ego_vehicle is not None:
    actor_list.append(ego_vehicle)</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 6</p>
            <h3>升级成稳妥版主车生成逻辑</h3>
            <pre><code class="python">if ego_vehicle is not None:
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
print("车辆位姿：", ego_vehicle.get_transform())</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="API 讲解：主车生成"
      >
        <h3>任务 1 涉及的 API，要逐个讲清楚</h3>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3><code>world.get_blueprint_library()</code></h3>
            <p>返回当前世界可用的蓝图库对象，后续所有车辆和传感器模板都从这里查。</p>
          </article>
          <article class="concept-card">
            <h3><code>bp_lib.find(...)</code></h3>
            <p>根据 blueprint id 精确查找模板。车辆常见如 <code>vehicle.tesla.model3</code>，相机常见如 <code>sensor.camera.rgb</code>。</p>
          </article>
          <article class="concept-card">
            <h3><code>world.get_map().get_spawn_points()</code></h3>
            <p>返回推荐出生点列表。每个元素本质上是一个 <code>carla.Transform</code>。</p>
          </article>
          <article class="concept-card">
            <h3><code>vehicle_bp.set_attribute("role_name", "hero")</code></h3>
            <p>给车辆增加角色标记。不是必须，但对主车识别和后续实验习惯都很有帮助。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="spawn_actor 与 try_spawn_actor"
      >
        <h3><code>spawn_actor()</code> 和 <code>try_spawn_actor()</code> 的区别，必须说清</h3>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3><code>spawn_actor()</code></h3>
            <p>生成失败时直接抛异常。优点是错误暴露早，缺点是如果点位冲突，脚本会立刻中断。</p>
          </article>
          <article class="command-card">
            <h3><code>try_spawn_actor()</code></h3>
            <p>生成失败时返回 <code>None</code>，脚本不会自动中断。优点是适合自己写“多个出生点逐个尝试”的逻辑。</p>
          </article>
          <article class="command-card">
            <h3>这一章推荐用谁</h3>
            <p>课堂演示和实验更推荐 <code>try_spawn_actor()</code>，因为它更适合做稳妥版生成流程，也更方便讲清 <code>NoneType</code> 错误的来源。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="NoneType 排查"
      >
        <h3>为什么会出现 <code>AttributeError: 'NoneType' object ...</code></h3>
        <p class="chapter-three-cue">
          第二章最常见的错误不是 <code>get_transform()</code> 本身有问题，而是前面的
          <code>ego_vehicle</code> 根本没有生成成功。
        </p>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>根因 1</h3>
            <p>当前出生点被占用，车辆生成失败，<code>try_spawn_actor()</code> 返回了 <code>None</code>。</p>
          </article>
          <article class="concept-card">
            <h3>根因 2</h3>
            <p>后面又直接写了 <code>ego_vehicle.get_transform()</code>，于是就把“前面失败”的问题延迟成了一个属性错误。</p>
          </article>
          <article class="concept-card">
            <h3>正确排查顺序</h3>
            <p>先打印 <code>ego_vehicle = ...</code>，确认对象是否存在，再去看后面的挂载和控制逻辑。</p>
          </article>
          <article class="concept-card">
            <h3>稳妥写法</h3>
            <p>遍历多个出生点，直到生成成功；如果全部失败，就明确抛出一条“车辆生成失败”的错误。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="为什么要稳妥版"
      >
        <h2>为什么生成主车时，要从“单点尝试”升级到“稳妥版流程”</h2>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>先做单点尝试</h3>
            <p>先用第一个出生点试一次，是为了让学生直接看到 <code>try_spawn_actor()</code> 的返回结果。这样后面讲 <code>None</code> 才不会抽象。</p>
          </article>
          <article class="command-card">
            <h3>再做稳妥生成</h3>
            <p>真实实验更适合先打乱出生点，再逐个尝试。这样脚本稳定性更高，也更符合工程场景。</p>
          </article>
          <article class="command-card">
            <h3>顺序执行时怎么处理</h3>
            <p>如果前面那次单点尝试已经生成了一辆车，升级到稳妥版之前要先销毁旧车，再把新的主车重新放进 <code>actor_list</code> 里。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="相机也是 Actor"
      >
        <h2>传感器不是“功能”，它也是 Actor</h2>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>RGB 相机</h3>
            <p><code>sensor.camera.rgb</code> 是相机蓝图，不是图片本身。它先是模板，生成后才是一个真正的相机 Actor。</p>
          </article>
          <article class="concept-card">
            <h3>传感器也要生成</h3>
            <p>和车辆一样，相机也要通过 <code>world.spawn_actor()</code> 生成，不能只写一个配置对象就假定它已经存在。</p>
          </article>
          <article class="concept-card">
            <h3>传感器也有父对象</h3>
            <p>相机通常会挂到车辆上。挂上以后，相机会跟着主车一起移动，但仍然是独立 Actor。</p>
          </article>
          <article class="concept-card">
            <h3>第二条链路</h3>
            <p><code>sensor_bp -&gt; camera_transform -&gt; camera -&gt; attach_to=ego_vehicle</code>，这是相机挂载链路。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="attach_to 的含义"
      >
        <h3><code>attach_to=ego_vehicle</code> 到底是什么意思</h3>
        <p class="chapter-three-cue">
          <strong>一句话记住：</strong>这不是“把相机的画面给主车”，而是“把相机这个 Actor 挂到主车这个 Actor 上”。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>有 <code>attach_to</code></h3>
            <p>相机的 <code>Transform</code> 会被解释成相对于主车局部坐标系的位置和姿态。</p>
          </article>
          <article class="command-card">
            <h3>没有 <code>attach_to</code></h3>
            <p>相机的 <code>Transform</code> 会被解释成世界坐标中的绝对位置，和车辆没有父子关系。</p>
          </article>
          <article class="command-card">
            <h3>重要结论</h3>
            <p>挂载成功后，相机会随着车辆移动；但游戏窗口看哪里，和相机是否挂成功，是两套不同机制。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="Location 与 Rotation"
      >
        <h3>安装位姿为什么重要：位置和角度决定相机真正看哪里</h3>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3><code>x / y / z</code></h3>
            <p><code>x</code> 控前后，<code>y</code> 控左右，<code>z</code> 控上下。前视相机常用 <code>x=1.5, y=0.0, z=2.4</code>。</p>
          </article>
          <article class="concept-card">
            <h3><code>yaw</code></h3>
            <p>控制左右转头。<code>yaw=0</code> 通常表示看车头方向，<code>yaw=90</code> 更偏右侧。</p>
          </article>
          <article class="concept-card">
            <h3><code>pitch</code></h3>
            <p>控制抬头和低头。前视略向下的相机，通常会给一个负的 <code>pitch</code>。</p>
          </article>
          <article class="concept-card">
            <h3><code>roll</code></h3>
            <p>控制画面侧倾。普通车载相机一般保持 <code>roll=0.0</code>。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 2：挂载 RGB 相机"
      >
        <div class="section-head">
          <p class="kicker">TASK 2</p>
          <h2>任务 2：把 RGB 相机挂到主车上</h2>
        </div>
        <div class="chapter-three-code-stack">
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 7</p>
            <h3>准备 RGB 相机蓝图</h3>
            <pre><code class="python">sensor_bp = bp_lib.find("sensor.camera.rgb")
sensor_bp.set_attribute("image_size_x", "800")
sensor_bp.set_attribute("image_size_y", "600")
sensor_bp.set_attribute("fov", "90")
sensor_bp.set_attribute("sensor_tick", "0.0")</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 8</p>
            <h3>定义相机安装位姿</h3>
            <pre><code class="python">camera_transform = carla.Transform(
    carla.Location(x=1.5, y=0.0, z=2.4),
    carla.Rotation(pitch=0.0, yaw=0.0, roll=0.0)
)</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 9</p>
            <h3>把相机挂到主车上</h3>
            <pre><code class="python">camera = world.spawn_actor(
    sensor_bp,
    camera_transform,
    attach_to=ego_vehicle,
    attachment_type=carla.AttachmentType.Rigid
)

actor_list.append(camera)
print("camera =", camera)</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="如何判断挂载成功"
      >
        <h3>如何判断“相机已经装在车上了”</h3>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>先看对象是否存在</h3>
            <p>先看 <code>print("camera =", camera)</code> 的结果。只要相机对象成功返回，说明 Actor 已经生成出来了。</p>
          </article>
          <article class="command-card">
            <h3>再看保存下来的图片</h3>
            <p>保存出来的图像如果会随着车辆移动而变化，说明相机已经跟着车在走。</p>
          </article>
          <article class="command-card">
            <h3>不要拿 spectator 当判断标准</h3>
            <p>游戏窗口默认是观察者视角，窗口没切到车头并不等于相机没挂上。是否挂载成功，要看传感器本身产出的图像。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="listen 与回调"
      >
        <h2><code>camera.listen(...)</code> 到底在做什么</h2>
        <p class="chapter-three-cue">
          <strong>一句话记住：</strong><code>listen()</code> 不是“立即拿到图片”，而是“注册一个回调函数，以后每来一帧图像就执行一次”。
        </p>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>传感器数据流</h3>
            <p>相机不会把每一帧直接塞到主程序里，而是通过监听回调把新数据送回来。</p>
          </article>
          <article class="concept-card">
            <h3><code>lambda image: ...</code></h3>
            <p>这是一种简短写法，表示“每来一张图像，就把这张图像交给我指定的处理逻辑”。</p>
          </article>
          <article class="concept-card">
            <h3><code>image.frame</code></h3>
            <p>表示当前图像所属的帧号。初学阶段先打印它，是最容易验证相机是否真的在持续出图的方法。</p>
          </article>
          <article class="concept-card">
            <h3>推荐顺序</h3>
            <p>先学会打印帧号，再学会存队列，再学会保存图片。顺序不能反，否则一出问题就不知道卡在哪一层。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 3：让相机出图"
      >
        <div class="section-head">
          <p class="kicker">TASK 3</p>
          <h2>任务 3：先让相机真的开始出图</h2>
        </div>
        <div class="chapter-three-code-stack">
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 10</p>
            <h3>最小监听：先打印帧号</h3>
            <pre><code class="python">camera.listen(lambda image: print("frame =", image.frame))</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 11</p>
            <h3>先观察几帧，再停止预览监听</h3>
            <pre><code class="python"># 这里只做一个短暂预览，确认相机真的开始出图
settings = world.get_settings()
print("synchronous_mode =", settings.synchronous_mode)

if settings.synchronous_mode:
    for _ in range(5):
        world.tick()
else:
    time.sleep(1.0)

camera.stop()
print("帧号预览结束，准备切换到队列模式")</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="为什么没输出"
      >
        <h3>为什么 <code>camera.listen(lambda image: print(image.frame))</code> 之后可能没输出</h3>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>原因 1</h3>
            <p>同步模式下没有调用 <code>world.tick()</code>，仿真根本没有继续向前走。</p>
          </article>
          <article class="concept-card">
            <h3>原因 2</h3>
            <p>脚本注册完监听后立刻结束，回调函数来不及执行。</p>
          </article>
          <article class="concept-card">
            <h3>原因 3</h3>
            <p>相机没有成功生成，或者根本没挂成功，导致后面的监听对象不是一个正常的传感器。</p>
          </article>
          <article class="concept-card">
            <h3>原因 4</h3>
            <p><code>sensor_tick</code> 设置太大，而等待时间又太短，看起来就像“没有任何输出”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="同步模式与 tick"
      >
        <h3>为什么同步模式下必须 <code>world.tick()</code></h3>
        <p class="chapter-three-cue">
          官方文档明确说明：同步模式下，服务端会等待客户端发出 tick，收到 tick 之后才推进到下一帧。没有 tick，车不动，传感器也不会持续更新。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>异步模式</h3>
            <p>服务端自己尽可能快地往前跑，客户端只是在不断接收最新状态。</p>
          </article>
          <article class="command-card">
            <h3>同步模式</h3>
            <p>客户端决定“下一步什么时候开始”，每调用一次 <code>world.tick()</code>，仿真才推进一帧。</p>
          </article>
          <article class="command-card">
            <h3>对采图的意义</h3>
            <p>同步模式加固定步长，是最适合做可重复采集和多传感器对齐的方式。本章实验就是围绕这一点展开。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="fixed_delta 与 sensor_tick"
      >
        <h3><code>fixed_delta_seconds</code> 和 <code>sensor_tick</code>，不要混在一起</h3>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3><code>fixed_delta_seconds</code></h3>
            <p>控制每一步仿真时间跨度。比如 <code>0.05</code> 表示每一步仿真推进 0.05 秒。</p>
          </article>
          <article class="concept-card">
            <h3><code>sensor_tick</code></h3>
            <p>控制传感器多久采样一次。比如设为 <code>2.0</code>，表示相机每 2 秒采一帧。</p>
          </article>
          <article class="concept-card">
            <h3>两者的关系</h3>
            <p>一个控制世界步进节奏，一个控制传感器采样节奏。两者都和时间有关，但不是同一个层级。</p>
          </article>
          <article class="concept-card">
            <h3>本章实验怎么用</h3>
            <p>实验里会先固定世界步长，再通过 tick 连续推进，确保天气切换后的图像采样更稳定。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="用队列接图像"
      >
        <h2>为什么这一章更推荐用队列接图像，而不是直接在回调里堆很多逻辑</h2>
        <div class="chapter-three-code-stack">
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 12</p>
            <h3>更稳的方式：让相机把图像送入队列</h3>
            <pre><code class="python">image_queue = queue.Queue(maxsize=1)
camera.listen(push_latest_image)
print("相机已切换到队列模式")</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 13</p>
            <h3>每 tick 一次，再从队列取一帧</h3>
            <pre><code class="python">settings = world.get_settings()
settings.synchronous_mode = True
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

latest_image = None
for _ in range(5):
    frame_id = world.tick()
    latest_image = wait_for_image(frame_id)

image = latest_image
print("当前图像帧号：", image.frame)</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="保存图片"
      >
        <h3><code>image.save_to_disk(...)</code> 这句代码到底做了什么</h3>
        <div class="chapter-three-code-stack">
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 14</p>
            <h3>保存一张当前图像</h3>
            <pre><code class="python">os.makedirs("output/ch03", exist_ok=True)
filename = f"output/ch03/frame_{image.frame:06d}.png"
image.save_to_disk(filename)
print("已保存：", filename)</code></pre>
          </article>
        </div>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3><code>output/ch03</code></h3>
            <p>表示保存目录。先创建目录，再保存文件，是更稳妥的习惯。</p>
          </article>
          <article class="concept-card">
            <h3><code>{image.frame:06d}</code></h3>
            <p>表示把帧号格式化成 6 位数字，不足前面补 0。这样文件名自然有顺序，也方便后续整理数据集。</p>
          </article>
          <article class="concept-card">
            <h3>为什么先保存 1 张</h3>
            <p>先用一张图片验证相机已经正常工作，再进入批量采集。先确认一张成功，后面的排错会简单很多。</p>
          </article>
          <article class="concept-card">
            <h3>图片没变化怎么办</h3>
            <p>如果车没有动、天气也没变，保存出来的图片很像是正常现象，不一定说明保存逻辑有错。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="天气控制"
      >
        <h2>第二章为什么要把天气控制放进来</h2>
        <p class="chapter-three-cue">
          这一章的综合实验定为“同步天气控制与相机数据采集”。天气控制不是为了炫效果，而是为了让学生看到：
          同一个相机，在不同天气下会得到不同的视觉数据，这才是真正的数据采集场景。
        </p>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3><code>world.get_weather()</code></h3>
            <p>读取当前天气对象。第二章已经认识过，这一章开始真正控制它。</p>
          </article>
          <article class="concept-card">
            <h3><code>world.set_weather(...)</code></h3>
            <p>把新的天气应用到当前世界。既可以用预设，也可以自定义参数。</p>
          </article>
          <article class="concept-card">
            <h3><code>carla.WeatherParameters</code></h3>
            <p>官方给出的天气参数类。常见预设如 <code>ClearNoon</code>、<code>CloudySunset</code>、<code>HardRainNoon</code>。</p>
          </article>
          <article class="concept-card">
            <h3>重要认知</h3>
            <p>天气变化影响的是视觉效果，不会直接替学生省略同步模式和采集节奏问题。真正难点仍然是“切完天气以后，何时才保存图像”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="任务 4：同步天气采集"
      >
        <div class="section-head">
          <p class="kicker">TASK 4</p>
          <h2>任务 4：在同步模式下切换天气并保存图像</h2>
        </div>
        <p class="chapter-three-cue">
          这组代码会把前面的知识串起来：同步模式、固定步长、图像队列、天气控制和图片保存。这里也是实验项目一的核心思路。
        </p>
        <div class="chapter-three-code-stack">
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 15</p>
            <h3>准备天气预设列表</h3>
            <pre><code class="python">weather_presets = [
    ("ClearNoon", carla.WeatherParameters.ClearNoon),
    ("CloudySunset", carla.WeatherParameters.CloudySunset),
    ("WetCloudyNoon", carla.WeatherParameters.WetCloudyNoon),
    ("HardRainNoon", carla.WeatherParameters.HardRainNoon),
]</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 16</p>
            <h3>定义“切天气 + tick 几帧 + 保存一张图”的函数</h3>
            <pre><code class="python">def capture_weather_frame(label, weather):
    world.set_weather(weather)

    latest_image = None
    for _ in range(6):
        frame_id = world.tick()
        latest_image = wait_for_image(frame_id)

    path = f"output/ch03/{label}_{latest_image.frame:06d}.png"
    latest_image.save_to_disk(path)
    print(f"{label} 已保存：{path}")</code></pre>
          </article>
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 17</p>
            <h3>依次采集多种天气下的图像</h3>
            <pre><code class="python">for label, weather in weather_presets:
    capture_weather_frame(label, weather)</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="为什么要多 tick 几帧"
      >
        <h3>为什么切换天气后，不是立刻保存，而是先连续 tick 几帧</h3>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>官方提醒</h3>
            <p>官方同步模式文档特别提到，GPU 传感器，尤其是相机，通常会有几帧延迟。</p>
          </article>
          <article class="command-card">
            <h3>实验里的含义</h3>
            <p>如果切完天气立刻保存，有可能拿到的还是上一种天气对应的旧帧。先连续 tick 几帧，更容易让相机数据和当前世界状态对齐。</p>
          </article>
          <article class="command-card">
            <h3>为什么这一步适合教学</h3>
            <p>这能让学生第一次真正意识到：传感器数据不是“立刻同步出现”的，采集要考虑仿真节奏和数据延迟。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="spectator 误区"
      >
        <h3>常见误区：不想固定游戏视角，就不要去动 spectator</h3>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>spectator 是什么</h3>
            <p>它只是游戏窗口的观察者，决定“你在窗口里看到什么”。</p>
          </article>
          <article class="concept-card">
            <h3>相机挂载是什么</h3>
            <p>相机挂载是传感器 Actor 和父 Actor 的关系，决定的是“相机从哪里采图”。</p>
          </article>
          <article class="concept-card">
            <h3>两者无关</h3>
            <p>你不去改 spectator，相机依然可以正常挂在车上并保存图片。学生非常容易把这两件事混成一件事。</p>
          </article>
          <article class="concept-card">
            <h3>本章建议</h3>
            <p>实验主线不依赖 spectator，先把资源集中在“相机真的能稳定采到图”这件事上。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="扩展：自动驾驶"
      >
        <h3>扩展任务：让主车自动驾驶起来，再继续采图</h3>
        <p class="chapter-three-cue">
          自动驾驶不是本章实验一的必做内容，但它是第二章最自然的扩展。只要主车、相机和同步模式已经跑通，再把车交给 Traffic Manager 即可。
        </p>
        <div class="chapter-three-code-stack">
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 18</p>
            <h3>让主车自动驾驶，并每隔几步保存一张图</h3>
            <pre><code class="python">traffic_manager = client.get_trafficmanager(8000)
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
traffic_manager = None</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="资源清理"
      >
        <h3>主线代码全部跑完以后，要把资源清理掉</h3>
        <div class="chapter-three-code-stack">
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">代码段 19</p>
            <h3>停止传感器、销毁 Actor，并恢复原始世界设置</h3>
            <pre><code class="python">cleanup()
print("第二章主线代码已清理完成")</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="实验项目一"
      >
        <div class="section-head">
          <p class="kicker">EXPERIMENT 01</p>
          <h2>实验项目一：同步天气控制与相机数据采集</h2>
        </div>
        <p class="chapter-three-cue">
          这个实验是第二章的综合收束。只要前面的车、相机、同步模式和天气控制都理解了，这个实验就能独立完成。
        </p>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>实验目标</h3>
            <p>在同步模式下生成主车和前视 RGB 相机，切换多种天气，并保存对应图像。</p>
          </article>
          <article class="concept-card">
            <h3>实验成果</h3>
            <p>至少得到 3 到 4 种天气下的采集图片，并且文件名能够区分天气类型和帧号。</p>
          </article>
          <article class="concept-card">
            <h3>实验难点</h3>
            <p>不是天气切换本身，而是“同步模式 + tick + 相机延迟 + 保存时机”这几件事如何配合。</p>
          </article>
          <article class="concept-card">
            <h3>实验价值</h3>
            <p>这已经是一条很真实的数据采集流程：控制环境条件，然后获取相机数据。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验步骤"
      >
        <h3>实验项目一建议按这 6 步完成</h3>
        <div class="chapter-three-rhythm">
          <span>开同步模式</span>
          <span>生成主车</span>
          <span>挂载相机</span>
          <span>监听图像</span>
          <span>切换天气</span>
          <span>保存图片</span>
        </div>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>步骤 1 和 2</h3>
            <p>先保存原始设置，再开启同步模式和固定步长；然后用稳妥方式生成主车。</p>
          </article>
          <article class="command-card">
            <h3>步骤 3 和 4</h3>
            <p>挂载 RGB 相机，并用队列接收图像。先别急着保存，先确保每 tick 一次真的能拿到新图像。</p>
          </article>
          <article class="command-card">
            <h3>步骤 5 和 6</h3>
            <p>准备天气预设列表，依次切换天气；每次切换后 tick 几帧，再把最新图像保存到磁盘。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="实验模板"
      >
        <h2>实验模板：按注释补全逻辑</h2>
        <p class="chapter-three-cue">
          这份模板刻意留了关键空位，但注释已经把每一步的目标说清。只要前面页面认真跟下来，模板可以独立补全出来。
        </p>
        <div class="chapter-three-code-stack">
          <article class="command-card chapter-three-cell-card">
            <p class="chapter-three-cell-tag">实验模板</p>
            <h3>同步天气控制与相机数据采集</h3>
            <pre><code class="python">import os
import queue
import random
import time

import carla

def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    bp_lib = world.get_blueprint_library()

    os.makedirs("output/exp01", exist_ok=True)

    original_settings = world.get_settings()
    actor_list = []
    image_queue = queue.Queue(maxsize=1)

    try:
        # 第 0 步：先准备两个小工具
        # def push_latest_image(image): 只保留最新帧，避免旧图像在队列里堆积
        # def wait_for_image(target_frame): 在 tick 之后等待对应的新图像

        # 第 1 步：开启同步模式和固定步长
        # new_settings = world.get_settings()
        # new_settings.synchronous_mode = __________
        # new_settings.fixed_delta_seconds = ______
        # world.apply_settings(new_settings)

        # 第 2 步：生成主车
        # vehicle_bp = _____________________________
        # vehicle_bp.set_attribute("role_name", "hero")
        # spawn_points = ___________________________
        # random.shuffle(spawn_points)
        # ego_vehicle = None
        # for sp in spawn_points:
        #     ego_vehicle = _______________________
        #     if ego_vehicle is not None:
        #         break

        # 第 3 步：挂载相机
        # sensor_bp = _____________________________
        # camera = world.spawn_actor(..., attach_to=ego_vehicle, ...)
        # actor_list.append(ego_vehicle)
        # actor_list.append(camera)

        # 第 4 步：注册图像监听
        # 提示：推荐使用 push_latest_image，而不是直接 image_queue.put
        # camera.listen(___________________________)

        # 第 5 步：准备天气预设列表
        # weather_presets = [
        #     ("ClearNoon", carla.WeatherParameters.ClearNoon),
        #     ("CloudySunset", carla.WeatherParameters.CloudySunset),
        #     ("HardRainNoon", carla.WeatherParameters.HardRainNoon),
        # ]

        # 第 6 步：依次切换天气并保存图像
        # for label, weather in weather_presets:
        #     world.set_weather(weather)
        #     latest_image = None
        #     for _ in range(6):
        #         frame_id = world.tick()
        #         latest_image = wait_for_image(frame_id)
        #
        #     save_path = f"output/exp01/{label}_{latest_image.frame:06d}.png"
        #     latest_image.save_to_disk(save_path)
        #     print(f"{label} 已保存：{save_path}")

        pass
    finally:
        world.apply_settings(original_settings)
        for actor in reversed(actor_list):
            if isinstance(actor, carla.Sensor):
                actor.stop()
            actor.destroy()

if __name__ == "__main__":
    main()</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验下载"
      >
        <h3>实验指导书、实验报告、模板和答案统一放在这里</h3>
        <div class="command-layout chapter-three-link-grid chapter-three-link-grid--balanced">
          <article class="command-card chapter-three-highlight-card">
            <h3>实验报告下载</h3>
            <p>先下载实验报告模板，再按照实验指导书或实验模板里的要求完成自主实验。这一项需要重点保留，实验结束后直接基于它整理结果。</p>
            <a class="chapter-three-link" :href="expReportHref" download="实验报告1：xxxx-学生姓名.docx">
              下载实验报告1：xxxx-学生姓名.docx
            </a>
          </article>
          <article class="command-card">
            <h3>实验指导书</h3>
            <p>这是整门课程的实验指导书，实验项目一也以它为统一依据。</p>
            <a class="chapter-three-link" :href="expGuideHref" download="《自动驾驶软件系统B》实验指导书（学院模板）-阴明旭.docx">
              下载实验指导书
            </a>
          </article>
          <article class="command-card">
            <h3>实验模板</h3>
            <p>模板保留了关键提示性注释，适合先独立补全，再对照答案检查。</p>
            <a class="chapter-three-link" :href="expTemplateHref" download="exp01_sync_weather_camera_template.py">
              下载实验模板
            </a>
          </article>
          <article class="command-card">
            <h3>实验答案</h3>
            <p>答案版本是完整可运行脚本。建议先独立完成模板，再打开答案。</p>
            <a class="chapter-three-link" :href="expAnswerHref" download="exp01_sync_weather_camera_answer.py">
              下载实验答案
            </a>
          </article>
          <article class="command-card">
            <h3>自主学习建议</h3>
            <p>先完成主线：主车生成、相机挂载、同步模式、天气采图。扩展任务再看自动驾驶采图，不要一开始把所有目标混在一起。</p>
          </article>
          <article class="command-card chapter-three-submit-card">
            <div class="chapter-three-submit-grid">
              <div>
                <h3>实验报告提交</h3>
                <p>按照实验指导书或实验模板的内容完成自主实验，整理好实验报告后，通过下面的 WPS 表单提交。</p>
                <a class="chapter-three-link" :href="expSubmitHref" target="_blank" rel="noopener noreferrer">
                  {{ expSubmitHref }}
                </a>
              </div>
              <figure class="chapter-three-submit-qr">
                <img :src="expSubmitQrHref" alt="实验报告提交二维码" />
                <figcaption>扫码提交实验报告</figcaption>
              </figure>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="整章下载"
      >
        <div class="section-head">
          <p class="kicker">DOWNLOADS</p>
          <h2>整章总代码与自学建议</h2>
        </div>
        <div class="command-layout chapter-three-link-grid chapter-three-link-grid--balanced">
          <article class="command-card">
            <h3>整章总代码</h3>
            <p>整章代码已经按 notebook 代码段风格整理到一个文件里，适合课后按顺序拆分到 cell 继续练习。</p>
            <a class="chapter-three-link" :href="chapterAllCodeHref" download="carla_ch03_all_examples.py">
              下载 carla_ch03_all_examples.py
            </a>
          </article>
          <article class="command-card">
            <h3>建议练习顺序</h3>
            <p>先跑“生成主车”，再跑“挂载相机”，再跑“相机出图”，最后再进“同步天气实验”。顺序不要倒。</p>
          </article>
          <article class="command-card">
            <h3>调试第一原则</h3>
            <p>每一步都先打印当前对象：<code>ego_vehicle</code>、<code>camera</code>、<code>settings</code>、<code>image.frame</code>。不要让错误拖到后面才暴露。</p>
          </article>
          <article class="command-card">
            <h3>资源清理</h3>
            <p>实验结束后记得先停止传感器，再销毁相机和车辆，最后恢复原始世界设置。这一步是工程习惯，不是可选项。</p>
          </article>
        </div>
      </section>

      <section
        id="summary"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章总结"
      >
        <div class="section-head">
          <p class="kicker">SUMMARY</p>
          <h2>第二章总结：从生成主车，到真正采到数据</h2>
        </div>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>对象关系</h3>
            <p>车辆和相机都是 Actor，先选 Blueprint，再生成到世界里，后续所有操作都围绕这些对象展开。</p>
          </article>
          <article class="concept-card">
            <h3>挂载关系</h3>
            <p><code>attach_to=ego_vehicle</code> 表示相机相对于主车安装，位置和姿态由相对 <code>Transform</code> 决定。</p>
          </article>
          <article class="concept-card">
            <h3>采集关系</h3>
            <p><code>listen()</code> 负责接收图像，<code>world.tick()</code> 负责推进同步仿真，<code>save_to_disk()</code> 负责把图像落盘。</p>
          </article>
          <article class="concept-card">
            <h3>实验关系</h3>
            <p>同步模式、固定步长、天气控制和相机采样共同构成了第二章的实验主线，也是真实数据采集的基础思路。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：先把车和相机变成真实对象，再去讨论回调、同步模式和数据采集。</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">命令已复制</div>
  </div>
</template>

<style scoped>
.page.is-slide-deck .chapter-three-rhythm {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.page.is-slide-deck .chapter-three-rhythm span {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(11, 98, 179, 0.2);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.95), rgba(245, 251, 255, 0.98));
  color: #0a5eaf;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
}

.page.is-slide-deck .chapter-three-cue {
  margin: 10px 0 0;
  padding: 10px 12px;
  border-left: 4px solid rgba(11, 98, 179, 0.42);
  border-radius: 10px;
  background: rgba(11, 98, 179, 0.06);
  color: var(--text-main);
  font-size: 0.95rem;
  line-height: 1.68;
}

.page.is-slide-deck .command-layout.chapter-three-2plus1 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .command-layout.chapter-three-2plus1 > :last-child {
  grid-column: 1 / -1;
}

.page.is-slide-deck .concept-grid.chapter-three-quad-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .concept-grid.chapter-three-quad-grid > .concept-card {
  grid-column: span 1;
}

.page.is-slide-deck .chapter-three-highlight-card,
.page.is-slide-deck .chapter-three-submit-card {
  grid-column: 1 / -1;
}

.page.is-slide-deck .chapter-three-highlight-card {
  border: 1px solid rgba(11, 98, 179, 0.26);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.96), rgba(248, 252, 255, 0.98));
  box-shadow: 0 16px 30px rgba(11, 98, 179, 0.08);
}

.page.is-slide-deck .chapter-three-submit-card {
  margin-top: 6px;
}

.page.is-slide-deck .chapter-three-submit-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 180px;
  gap: 18px;
  align-items: center;
}

.page.is-slide-deck .chapter-three-submit-qr {
  margin: 0;
  text-align: center;
}

.page.is-slide-deck .chapter-three-submit-qr img {
  display: block;
  width: 100%;
  max-width: 180px;
  margin: 0 auto;
  border-radius: 12px;
  border: 1px solid rgba(11, 98, 179, 0.18);
  background: #fff;
}

.page.is-slide-deck .chapter-three-submit-qr figcaption {
  margin-top: 8px;
  color: var(--text-soft);
  font-size: 0.86rem;
}

@media (max-width: 900px) {
  .page.is-slide-deck .chapter-three-submit-grid {
    grid-template-columns: 1fr;
    align-items: start;
  }

  .page.is-slide-deck .chapter-three-submit-qr img {
    max-width: 220px;
  }
}

.page.is-slide-deck .command-layout.chapter-three-link-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: start;
}

.page.is-slide-deck .command-layout.chapter-three-link-grid.chapter-three-link-grid--balanced > :last-child:not(.chapter-three-highlight-card):not(.chapter-three-submit-card),
.page.is-slide-deck .command-layout.chapter-three-link-grid.chapter-three-link-grid--balanced > :nth-last-child(2):not(.chapter-three-highlight-card):not(.chapter-three-submit-card) {
  grid-column: span 1;
}

.page.is-slide-deck .chapter-three-code-stack {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
  margin-top: 18px;
}

.page.is-slide-deck .chapter-three-cell-card {
  width: 100%;
}

.page.is-slide-deck .chapter-three-cell-tag {
  margin: 0 0 8px;
  color: #0a5eaf;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.page.is-slide-deck .chapter-three-link {
  display: block;
  margin-top: 10px;
  color: #0a5eaf;
  font-weight: 700;
  text-decoration: underline;
  word-break: break-all;
}

@media (max-width: 900px) {
  .page.is-slide-deck .chapter-three-rhythm,
  .page.is-slide-deck .command-layout.chapter-three-2plus1,
  .page.is-slide-deck .concept-grid.chapter-three-quad-grid,
  .page.is-slide-deck .command-layout.chapter-three-link-grid {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .command-layout.chapter-three-2plus1 > :last-child,
  .page.is-slide-deck .concept-grid.chapter-three-quad-grid > .concept-card,
  .page.is-slide-deck .command-layout.chapter-three-link-grid.chapter-three-link-grid--balanced > :last-child,
  .page.is-slide-deck .command-layout.chapter-three-link-grid.chapter-three-link-grid--balanced > :nth-last-child(2) {
    grid-column: span 1;
  }
}
</style>
