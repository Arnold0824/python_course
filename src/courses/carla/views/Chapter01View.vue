<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const officialWebsite = "https://carla.org/";
const officialDocs = "https://carla.readthedocs.io/en/latest/";
const carla0916WindowsDownload = "https://tiny.carla.org/carla-0-9-16-windows";
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
        <span class="brand-tag">CARLA 01</span>
        <strong>认识CARLA与基础使用</strong>
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
        <p class="kicker">CARLA AUTONOMOUS DRIVING SIMULATION</p>
        <h1>Carla自动驾驶仿真：<br />认识平台与基础使用</h1>
        <p class="hero-intro">
          第一章先解决三个最基础的问题：CARLA 到底是什么，它为什么适合自动驾驶教学与实验，
          以及第一次接触时应该按什么顺序启动、连接、观察和调用它。
        </p>
        <ul class="hero-checklist">
          <li>认识 CARLA 的定位：自动驾驶研发、训练、测试与验证用的开源仿真平台。</li>
          <li>理解 CARLA 的基本结构：服务器、客户端、世界、Actor、地图、传感器。</li>
          <li>掌握最小使用流程：准备环境、启动服务端、连接 Python 客户端、运行官方示例。</li>
        </ul>
        <div class="goal-cards fly-in-seq">
          <article>
            <h2>能力目标 1</h2>
            <p>能说清 CARLA 与真实车辆实验、普通游戏引擎演示之间的差别。</p>
          </article>
          <article>
            <h2>能力目标 2</h2>
            <p>会读懂官方文档首页、Quick start、Foundations、Sensors 和 Scripts 这些入口。</p>
          </article>
          <article>
            <h2>能力目标 3</h2>
            <p>会按标准流程启动 CARLA，并写出最小 Python 连接代码。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="官方入口"
      >
        <div class="section-head">
          <p class="kicker">OFFICIAL RESOURCES</p>
          <h2>官方入口：先看官网，再看文档</h2>
        </div>
        <div class="command-layout carla-link-grid">
          <article class="command-card">
            <h3>CARLA 官网</h3>
            <p>官网适合快速了解平台定位、核心特性、项目入口和最新资源导航。</p>
            <a
              class="carla-link"
              :href="officialWebsite"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ officialWebsite }}
            </a>
          </article>
          <article class="command-card">
            <h3>官方文档首页</h3>
            <p>文档适合系统学习安装、基础概念、Python API、地图、传感器、脚本和高级功能。</p>
            <a
              class="carla-link"
              :href="officialDocs"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ officialDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>读文档时先确认版本</h3>
            <p>
              官方首页当前提示：该入口展示的是 Unreal Engine 4.26 版本文档。如果实际安装的是 UE5
              版本，阅读时要先确认文档分支是否对应。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="CARLA 是什么"
      >
        <h2>CARLA 是什么</h2>
        <p class="carla-cue">
          <strong>先用一句话记住：</strong>CARLA 是面向自动驾驶研究、训练、测试与验证的开源仿真平台，
          不是单纯用来“开车玩”的地图程序。
        </p>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>官方定位</h3>
            <p>
              官网介绍中明确指出，CARLA 从一开始就是为自动驾驶系统的开发、训练和验证而构建，
              并提供开放的城市布局、建筑、车辆等数字资产。
            </p>
          </article>
          <article class="command-card">
            <h3>平台核心</h3>
            <p>
              官方文档介绍中强调，CARLA 是一个模块化、灵活、可通过 Python 和 C++ API 控制的自动驾驶仿真器，
              基于 Unreal Engine 运行，并使用 ASAM OpenDRIVE 描述道路和城市场景。
            </p>
          </article>
          <article class="command-card">
            <h3>为什么适合课程</h3>
            <p>
              它同时支持地图、车辆、行人、天气、交通、传感器和脚本控制，既能做演示，也能做数据采集、
              控制实验和自动驾驶流程训练。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="CARLA 能做什么"
      >
        <h3>CARLA 能做什么</h3>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>训练数据生成</h3>
            <p>可以模拟城市、道路、车辆和传感器，用来生成机器学习和感知算法需要的数据。</p>
          </article>
          <article class="concept-card">
            <h3>算法验证</h3>
            <p>可以把自动驾驶代理部署到仿真环境中，在更低风险条件下观察行为和结果。</p>
          </article>
          <article class="concept-card">
            <h3>环境控制</h3>
            <p>可以控制天气、交通、地图、NPC、传感器和世界状态，适合做可重复实验。</p>
          </article>
          <article class="concept-card">
            <h3>脚本化控制</h3>
            <p>可以通过 Python 脚本连接客户端，加载地图、生成车辆、挂载传感器并读取数据。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="为什么学 CARLA"
      >
        <h2>为什么自动驾驶课程常常先学 CARLA</h2>
        <div class="carla-rhythm">
          <span>先在仿真里理解系统</span>
          <span>再在仿真里做可重复实验</span>
          <span>最后再进入更复杂的真实任务</span>
        </div>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>低风险</h3>
            <p>不会直接碰到真实道路安全问题，适合先做控制逻辑与传感器流程训练。</p>
          </article>
          <article class="concept-card">
            <h3>可复现</h3>
            <p>同一张地图、同一组天气、同一辆车、同一个脚本可以重复运行和对比。</p>
          </article>
          <article class="concept-card">
            <h3>可观察</h3>
            <p>能同时看到世界、车辆和传感器结果，方便理解“感知到什么”和“控制了什么”。</p>
          </article>
          <article class="concept-card">
            <h3>可扩展</h3>
            <p>后续可以继续接入 ROS、Traffic Manager、Recorder、Scenario Runner 等生态能力。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="基本结构"
      >
        <h2>基本结构：先分清服务器和客户端</h2>
        <p class="carla-cue">
          <strong>理解 CARLA 的第一把钥匙：</strong>它采用客户端-服务器结构。服务器负责跑仿真，
          客户端通过 API 发出请求、读取世界和传感器数据。
        </p>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>服务端 Server</h3>
            <p>
              负责渲染传感器、计算物理、更新世界状态和 Actor 状态。仿真本身在这里运行，通常更依赖 GPU。
            </p>
          </article>
          <article class="command-card">
            <h3>客户端 Client</h3>
            <p>
              负责通过 Python 或 C++ API 连接服务端，请求信息、修改环境、控制车辆、挂载传感器。
            </p>
          </article>
          <article class="command-card">
            <h3>最重要的结果</h3>
            <p>
              “装好了 CARLA 包”不等于“脚本已经连上世界”；“打开了 CARLA 窗口”也不等于“Python 已经开始控制仿真”。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="四个最关键对象"
      >
        <h3>四个最关键对象：Client、World、Actor、Blueprint</h3>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>Client</h3>
            <p>客户端入口。负责连接服务端，还可以加载地图、录制回放、初始化交通管理器。</p>
          </article>
          <article class="concept-card">
            <h3>World</h3>
            <p>当前仿真世界对象。通过它可以访问地图、天气、蓝图库、车辆、行人和传感器。</p>
          </article>
          <article class="concept-card">
            <h3>Actor</h3>
            <p>世界里的实体对象。车辆、行人、交通灯、传感器都属于 Actor。</p>
          </article>
          <article class="concept-card">
            <h3>Blueprint</h3>
            <p>生成 Actor 前的模板。要先从蓝图库里找到蓝图，再生成真正的对象。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="地图、资产与脚本"
      >
        <h3>地图、资产与脚本</h3>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>地图与资产</h3>
            <p>
              官方 catalogue 页面说明，CARLA 提供预构建地图、车辆、行人和其他 3D 资产，
              可以在运行时用来搭建不同仿真环境。
            </p>
          </article>
          <article class="command-card">
            <h3>传感器</h3>
            <p>
              官方 Sensors and data 页面指出，传感器本质上也是 Actor，
              可以被设置属性、生成、监听并持续输出数据。
            </p>
          </article>
          <article class="command-card">
            <h3>示例脚本</h3>
            <p>
              官方 scripts catalogue 提供了 `manual_control.py`、`generate_traffic.py`、
              `automatic_control.py` 等脚本，是最适合新手上手的平台入口。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="使用前准备"
      >
        <h2>使用前准备：官方 Quick start 提到的基本要求</h2>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>操作系统</h3>
            <p>官方 Quick start 当前列出支持 Windows 10/11 和 Ubuntu 20.04/22.04。</p>
          </article>
          <article class="concept-card">
            <h3>硬件</h3>
            <p>官方建议有独立 GPU，推荐性能等级大致相当于 NVIDIA 2070 或更高，并至少 8GB 显存。</p>
          </article>
          <article class="concept-card">
            <h3>磁盘与端口</h3>
            <p>约 20GB 磁盘空间，默认会用到 2000 和 2001 两个 TCP 端口。</p>
          </article>
          <article class="concept-card">
            <h3>Python 与 PIP</h3>
            <p>官方 Quick start 当前列出 Python 3.7 到 3.12，且要求 PIP 版本不低于 20.3。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="安装路线：包安装还是源码构建"
      >
        <h3>安装路线：包安装还是源码构建</h3>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>优先选择：Package 安装</h3>
            <p>
              如果本章目标是先学会用 CARLA，最稳的路线是使用官方 package 安装。
              官方 Quick start 明确说明，这条路线适合快速开始使用模拟器。
            </p>
          </article>
          <article class="command-card">
            <h3>什么时候再考虑源码构建</h3>
            <p>
              只有在需要修改引擎、扩展功能、自己制作内容或深度开发时，再进入 build from source。
            </p>
          </article>
          <article class="command-card">
            <h3>本课程建议</h3>
            <p>教学起步阶段先统一用 package 版，避免把大量时间消耗在复杂构建问题上。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="最小启动流程"
      >
        <h2>最小启动流程：先启动服务端，再运行 Python 客户端</h2>
        <div class="carla-rhythm">
          <span>下载安装包</span>
          <span>启动服务端</span>
          <span>连接客户端脚本</span>
        </div>
        <div class="command-layout carla-code-grid">
          <article class="command-card">
            <h3>安装 Python 客户端</h3>
            <pre><code class="bash">python3 -m pip install carla
cd PythonAPI/examples
python3 -m pip install -r requirements.txt</code></pre>
            <p>官方 Quick start 说明：package 版包含服务端和 Python 客户端库，示例脚本依赖额外 requirements。</p>
          </article>
          <article class="command-card">
            <h3>启动 CARLA 服务端</h3>
            <pre><code class="bash"># Ubuntu
cd path/to/carla/root
./CarlaUE4.sh

# Windows
cd path\\to\\carla\\root
CarlaUE4.exe</code></pre>
            <p>服务端启动后，会打开默认城市地图的观察窗口。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="最小 Python 连接代码"
      >
        <h3>最小 Python 连接代码</h3>
        <p class="carla-cue">
          <strong>第一段最该会读的代码：</strong>只做两件事，连接 CARLA 服务端，拿到当前世界对象。
        </p>
        <pre><code class="python">import carla

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)

world = client.get_world()
print(world.get_map().name)</code></pre>
        <p class="section-note">
          这里的 <code>localhost</code> 和 <code>2000</code> 对应默认本机和默认端口。
          拿到 <code>world</code> 之后，后面的地图、天气、蓝图、车辆和传感器操作才有入口。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="官方示例脚本从哪里开始"
      >
        <h3>官方示例脚本从哪里开始</h3>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3><code>manual_control.py</code></h3>
            <pre><code class="bash">python3 manual_control.py --res 800x600 --sync</code></pre>
            <p>
              官方 scripts catalogue 明确指出，这是新用户最应该先尝试的脚本之一，
              适合熟悉地图、车辆和传感器显示效果。
            </p>
          </article>
          <article class="command-card">
            <h3><code>generate_traffic.py</code></h3>
            <pre><code class="bash">python3 generate_traffic.py</code></pre>
            <p>可以快速生成交通流量，适合把空地图变成更接近真实道路的交通环境。</p>
          </article>
          <article class="command-card">
            <h3><code>automatic_control.py</code></h3>
            <pre><code class="bash">python3 automatic_control.py --agent Basic --loop</code></pre>
            <p>用内置代理自动控制车辆，适合快速观察 CARLA Agents 的基础能力。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="config.py 和常用启动选项"
      >
        <h3><code>config.py</code> 和常用启动选项</h3>
        <div class="command-layout carla-code-grid">
          <article class="command-card">
            <h3>服务端启动参数</h3>
            <pre><code class="bash">./CarlaUE4.sh -carla-rpc-port=3000
./CarlaUE4.sh -quality-level=Low
./CarlaUE4.sh --ros2</code></pre>
            <p>官方 Quickstart extras 页面列出了端口、画质和 ROS2 等常见命令行参数。</p>
          </article>
          <article class="command-card">
            <h3>配置脚本</h3>
            <pre><code class="bash">cd PythonAPI/util
python3 config.py --map Town05
python3 config.py --weather ClearNoon
python3 config.py --no-rendering</code></pre>
            <p>官方文档建议在服务端已经启动后再运行这个脚本，用来切地图、改天气和关闭渲染。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="传感器基础认识"
      >
        <h2>传感器基础认识：它们本质上也是 Actor</h2>
        <p class="carla-cue">
          <strong>官方 Sensors and data 页面给出的核心认识：</strong>传感器是特殊的 Actor，
          需要先设置 blueprint，再生成，再通过 <code>listen()</code> 接收数据。
        </p>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>设置属性</h3>
            <pre><code class="python">sensor_bp = world.get_blueprint_library().find(
    "sensor.camera.rgb"
)
sensor_bp.set_attribute("image_size_x", "1280")
sensor_bp.set_attribute("image_size_y", "720")</code></pre>
            <p>先从蓝图库里找传感器模板，再设置分辨率、FOV、采样周期等属性。</p>
          </article>
          <article class="command-card">
            <h3>生成并监听</h3>
            <pre><code class="python">camera = world.spawn_actor(
    sensor_bp,
    carla.Transform(carla.Location(z=1.5)),
    attach_to=ego_vehicle,
)
camera.listen(lambda image: print(image.frame))</code></pre>
            <p>生成后并不会自动保存数据，要显式注册 <code>listen()</code> 回调。</p>
          </article>
          <article class="command-card">
            <h3>为什么这一页重要</h3>
            <p>后面不管是 RGB 相机、LIDAR、IMU 还是 GNSS，基本使用流程都离不开“找蓝图、生成、监听”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="异步与同步模式"
      >
        <h3>异步与同步模式：为什么做实验时要关心它</h3>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>异步模式</h3>
            <p>官方 Foundations 页面指出，默认是异步模式。服务端尽可能快地运行，适合先浏览和搭环境。</p>
          </article>
          <article class="concept-card">
            <h3>同步模式</h3>
            <p>当需要更强的控制性、可预测性和多传感器对齐时，官方建议改用同步模式。</p>
          </article>
          <article class="concept-card">
            <h3>为什么重要</h3>
            <p>多传感器数据采集时，如果不同步，就很难保证拿到的是同一时刻的世界状态。</p>
          </article>
          <article class="concept-card">
            <h3>多客户端提醒</h3>
            <p>官方说明里特别强调：多客户端架构下，只应该有一个客户端负责 tick。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="最常见的三个误区"
      >
        <h3>最常见的三个误区</h3>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>误区 1</h3>
            <p>以为 <code>pip install carla</code> 后就能直接看到仿真世界。实际上还需要启动 CARLA 服务端。</p>
          </article>
          <article class="concept-card">
            <h3>误区 2</h3>
            <p>以为打开了 CARLA 窗口，Python 脚本就自动连接成功。实际上客户端需要显式创建 <code>carla.Client</code>。</p>
          </article>
          <article class="concept-card">
            <h3>误区 3</h3>
            <p>以为传感器是“天然存在”的。实际上传感器也要先找蓝图、再生成、再监听。</p>
          </article>
          <article class="concept-card">
            <h3>课程建议</h3>
            <p>学习 CARLA 时，任何操作都先判断自己是在“服务端”、还是在“Python 客户端”这一侧。</p>
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
          <h2>第一章总结：先认清平台，再进入编程控制</h2>
        </div>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>CARLA 的定位</h3>
            <p>面向自动驾驶研发、训练、测试和验证的开源仿真平台。</p>
          </article>
          <article class="concept-card">
            <h3>CARLA 的结构</h3>
            <p>客户端-服务器架构，核心对象包括 Client、World、Actor、Blueprint 和 Sensor。</p>
          </article>
          <article class="concept-card">
            <h3>CARLA 的起步方式</h3>
            <p>先 package 安装，启动服务端，再用 Python API 连接并运行官方示例脚本。</p>
          </article>
          <article class="concept-card">
            <h3>CARLA 的学习路径</h3>
            <p>第一章先认识平台，后续再进入地图、车辆、传感器、交通和数据采集实验。</p>
          </article>
        </div>
        <div class="command-layout carla-link-grid carla-link-grid--balanced">
          <article class="command-card">
            <h3>官网地址</h3>
            <a
              class="carla-link"
              :href="officialWebsite"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ officialWebsite }}
            </a>
          </article>
          <article class="command-card">
            <h3>官方文档</h3>
            <a
              class="carla-link"
              :href="officialDocs"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ officialDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>CARLA 0.9.16 Windows 下载</h3>
            <p>课程当前建议使用这一版安装包完成环境搭建，再配合官方文档进行后续实验。</p>
            <a
              class="carla-link"
              :href="carla0916WindowsDownload"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ carla0916WindowsDownload }}
            </a>
          </article>
          <article class="command-card">
            <h3>一页带走的最小代码</h3>
            <pre><code class="python">import carla
client = carla.Client("localhost", 2000)
world = client.get_world()</code></pre>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：先分清服务端和客户端，再去理解地图、车辆、传感器和数据流。</p>
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
.page.is-slide-deck .carla-rhythm {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.page.is-slide-deck .carla-rhythm span {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(13, 123, 232, 0.18);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.95), rgba(245, 251, 255, 0.98));
  color: #0b4f88;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
}

.page.is-slide-deck .carla-cue {
  margin: 10px 0 0;
  padding: 10px 12px;
  border-left: 4px solid rgba(13, 123, 232, 0.45);
  border-radius: 10px;
  background: rgba(13, 123, 232, 0.06);
  color: var(--text-main);
  font-size: 0.94rem;
  line-height: 1.65;
}

.page.is-slide-deck .carla-cue strong {
  color: #0a5eaf;
}

.page.is-slide-deck .command-layout.carla-2plus1 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .command-layout.carla-2plus1 > :last-child {
  grid-column: 1 / -1;
}

.page.is-slide-deck .concept-grid.carla-quad-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .concept-grid.carla-quad-grid > .concept-card {
  grid-column: span 1;
}

.page.is-slide-deck .command-layout.carla-link-grid,
.page.is-slide-deck .command-layout.carla-code-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: start;
}

.page.is-slide-deck .command-layout.carla-link-grid > :last-child,
.page.is-slide-deck .command-layout.carla-code-grid > :last-child {
  grid-column: 1 / -1;
}

.page.is-slide-deck .command-layout.carla-link-grid.carla-link-grid--balanced > :last-child {
  grid-column: span 1;
}

.page.is-slide-deck .carla-link {
  display: inline-flex;
  align-items: center;
  min-height: 36px;
  margin-top: 10px;
  color: #0a5eaf;
  font-weight: 700;
  text-decoration: underline;
  word-break: break-all;
}

@media (max-width: 900px) {
  .page.is-slide-deck .carla-rhythm,
  .page.is-slide-deck .command-layout.carla-2plus1,
  .page.is-slide-deck .concept-grid.carla-quad-grid,
  .page.is-slide-deck .command-layout.carla-link-grid,
  .page.is-slide-deck .command-layout.carla-code-grid {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .command-layout.carla-2plus1 > :last-child,
  .page.is-slide-deck .concept-grid.carla-quad-grid > .concept-card,
  .page.is-slide-deck .command-layout.carla-link-grid > :last-child,
  .page.is-slide-deck .command-layout.carla-code-grid > :last-child {
    grid-column: span 1;
  }
}
</style>
