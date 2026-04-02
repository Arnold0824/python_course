<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const officialWebsite = "https://carla.org/";
const officialDocs = "https://carla.readthedocs.io/en/latest/";
const quickStartDocs = "https://carla.readthedocs.io/en/latest/start_quickstart/";
const pythonApiDocs = "https://carla.readthedocs.io/en/latest/python_api/";
const python310Download = "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe";
const vscodeDownload = "https://code.visualstudio.com/Download";
const vscodePythonExt =
  "https://marketplace.visualstudio.com/items?itemName=ms-python.python";
const vscodeJupyterExt =
  "https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter";
const carla0915WindowsDownload = "https://tiny.carla.org/carla-0-9-15-windows";
const pypiCarla = "https://pypi.org/project/carla/0.9.15/";

const chapterAllCodeHref = "/courses/carla/ch01/carla_ch01_all_examples.py";
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
        <strong>环境搭建、运行机制与首次连接</strong>
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
        <p class="kicker">SETUP, ARCHITECTURE AND FIRST CONNECTION</p>
        <h1>第一章 环境搭建、运行机制与首次连接</h1>
        <p class="hero-intro">
          这一章把原来的“认识 CARLA”和“首次连接 CARLA”合并成一条完整主线：
          先把 Windows 环境安装到可用，再分清服务端和 Python 客户端，最后真正连上世界并读出地图、天气和仿真设置。
        </p>
        <ul class="hero-checklist">
          <li>只讲 Windows 平台，避免把安装流程讲散。</li>
          <li>先完成 Python、VS Code、扩展和 CARLA Python 包安装，再启动仿真器。</li>
          <li>学完后应能独立写出一份连接检测脚本，并解释 client、world、map 的关系。</li>
        </ul>
        <div class="goal-cards fly-in-seq">
          <article>
            <h2>能力目标 1</h2>
            <p>能独立完成 Windows 平台的 CARLA 基础环境搭建。</p>
          </article>
          <article>
            <h2>能力目标 2</h2>
            <p>能说清楚 CARLA 为什么不是普通 Python 库，而是服务端加客户端的结构。</p>
          </article>
          <article>
            <h2>能力目标 3</h2>
            <p>能打印当前地图名、同步模式、固定步长和出生点数量。</p>
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
        <div class="carla-rhythm carla-rhythm--four">
          <span>先搭环境</span>
          <span>再分清结构</span>
          <span>再启动服务端</span>
          <span>最后连上 world</span>
        </div>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>任务 1</h3>
            <p>准备 Windows 版 CARLA、Python 3.10、VS Code 和必需扩展。</p>
          </article>
          <article class="concept-card">
            <h3>任务 2</h3>
            <p>理解 client-server 结构，分清脚本、服务端、world、map 和 settings。</p>
          </article>
          <article class="concept-card">
            <h3>任务 3</h3>
            <p>启动低画质 CARLA 服务端，确认窗口能稳定运行。</p>
          </article>
          <article class="concept-card">
            <h3>任务 4</h3>
            <p>在 Python 里连接当前世界，并读取基础信息。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="官方入口"
      >
        <div class="section-head">
          <p class="kicker">OFFICIAL LINKS</p>
          <h2>先看官方入口，再动手安装</h2>
        </div>
        <div class="command-layout carla-link-grid carla-link-grid--balanced">
          <article class="command-card">
            <h3>CARLA 官网</h3>
            <p>先从官网确认平台定位、版本入口和下载方式。</p>
            <a class="carla-link" :href="officialWebsite" target="_blank" rel="noopener noreferrer">
              {{ officialWebsite }}
            </a>
          </article>
          <article class="command-card">
            <h3>官方文档首页</h3>
            <p>后面讲到环境、world、Python API 时，都以这里为准。</p>
            <a class="carla-link" :href="officialDocs" target="_blank" rel="noopener noreferrer">
              {{ officialDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>Quickstart</h3>
            <p>安装 CARLA、启动服务端、安装 Python client library 的核心入口。</p>
            <a class="carla-link" :href="quickStartDocs" target="_blank" rel="noopener noreferrer">
              {{ quickStartDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>Python API</h3>
            <p>查类、方法、属性时最后都回到 Python API 文档。</p>
            <a class="carla-link" :href="pythonApiDocs" target="_blank" rel="noopener noreferrer">
              {{ pythonApiDocs }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="CARLA 是什么"
      >
        <h2>CARLA 是什么，为什么这一章要把安装和连接放在一起讲</h2>
        <p class="carla-cue">
          <strong>先记住一句话：</strong>CARLA 是面向自动驾驶研发、训练、测试和验证的开源仿真平台。
          如果只讲“它是什么”而不把环境和首次连接一并打通，学生很容易停留在概念层，无法真正进入后续实验。
        </p>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>它不是普通 Python 包</h3>
            <p>
              Python 代码只是在写客户端。真正的城市环境、车辆、传感器和物理仿真，都运行在 CARLA 服务端窗口里。
            </p>
          </article>
          <article class="command-card">
            <h3>它也不是单纯游戏窗口</h3>
            <p>
              窗口只说明仿真器已经启动。是否能被 Python 脚本控制，还要看客户端是否成功连接到了服务端。
            </p>
          </article>
          <article class="command-card">
            <h3>为什么本章合并</h3>
            <p>
              先把软件安装、服务端启动和首次连接串成一条线，后面讲车辆、传感器和天气控制时，所有对象关系都会更清楚。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="Windows 环境"
      >
        <div class="section-head">
          <p class="kicker">WINDOWS ONLY</p>
          <h2>本章只使用 Windows 平台流程</h2>
        </div>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>平台范围</h3>
            <p>这套课件只覆盖 Windows。Linux 和源码编译流程一律不展开，避免增加无关难度。</p>
          </article>
          <article class="concept-card">
            <h3>推荐版本</h3>
            <p>课堂统一使用 CARLA 0.9.15，Python 统一使用 3.10，减少版本不一致导致的兼容问题。</p>
          </article>
          <article class="concept-card">
            <h3>编辑器</h3>
            <p>统一使用 VS Code，并安装 Python 和 Jupyter 扩展，方便运行 .py 与 .ipynb。</p>
          </article>
          <article class="concept-card">
            <h3>硬件现实</h3>
            <p>大部分机器显卡性能有限，服务端启动命令应直接加入低画质参数，先保证能稳定打开和运行。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="步骤 1 下载 CARLA"
      >
        <h3>步骤 1：下载 Windows 版 CARLA 0.9.15</h3>
        <div class="command-layout carla-link-grid">
          <article class="command-card carla-highlight-card">
            <h3>Windows 下载地址</h3>
            <p>课堂统一版本。下载后解压到一个英文路径目录，例如 <code>D:\\CARLA_0.9.15</code>。</p>
            <a
              class="carla-link"
              :href="carla0915WindowsDownload"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ carla0915WindowsDownload }}
            </a>
          </article>
          <article class="command-card">
            <h3>目录建议</h3>
            <p>不要把 CARLA 解压到桌面、中文路径或层级过深的位置。稳定的做法是单独放在数据盘根目录附近。</p>
          </article>
          <article class="command-card">
            <h3>先不要急着双击运行</h3>
            <p>先把 Python、VS Code 和扩展准备好，再统一启动服务端，这样后面的连接检测可以一次走通。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="步骤 2 安装 Python"
      >
        <h3>步骤 2：安装 Python 3.10</h3>
        <p class="carla-cue">
          本章统一指定 <strong>Python 3.10</strong>。原因很简单：课堂环境要可控，CARLA 0.9.15 的 PyPI 页面提供了
          <code>cp310</code> 的 Windows wheel，课堂部署更稳。
        </p>
        <div class="command-layout carla-link-grid">
          <article class="command-card carla-highlight-card">
            <h3>Python 3.10 官方下载</h3>
            <p>这里直接给出 64 位 Windows 安装包直链，下载后直接运行即可。</p>
            <a
              class="carla-link"
              :href="python310Download"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ python310Download }}
            </a>
          </article>
          <article class="command-card">
            <h3>安装时要勾选什么</h3>
            <p>
              至少要勾选 <code>Add python.exe to PATH</code>。
              安装完成后，终端里应该可以直接识别 <code>python</code> 命令。
            </p>
          </article>
          <article class="command-card">
            <h3>安装后先验证</h3>
            <pre><code class="bash">python --version</code></pre>
            <p>
              看到 <code>Python 3.10.x</code> 再继续后面的步骤。
              如果命令不存在，先修正环境变量，不要直接往下装包。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="步骤 3 安装 VS Code"
      >
        <h3>步骤 3：安装 VS Code</h3>
        <div class="command-layout carla-link-grid">
          <article class="command-card carla-highlight-card">
            <h3>VS Code 官方下载</h3>
            <p>建议直接选择 Windows x64 User Installer，课堂环境更统一。</p>
            <a class="carla-link" :href="vscodeDownload" target="_blank" rel="noopener noreferrer">
              {{ vscodeDownload }}
            </a>
          </article>
          <article class="command-card">
            <h3>为什么选 VS Code</h3>
            <p>它同时适合运行单文件 Python 脚本和 Jupyter Notebook，后面做分段实验更方便。</p>
          </article>
          <article class="command-card">
            <h3>打开项目方式</h3>
            <p>安装完成后，使用 <code>File -> Open Folder</code> 打开自己的实验文件夹，不建议每次只开一个单文件。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="步骤 4 安装扩展"
      >
        <h3>步骤 4：安装 Python 扩展和 Jupyter 扩展</h3>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>Python 扩展</h3>
            <p>打开 VS Code 后按 <code>Ctrl + Shift + X</code>，搜索 <code>Python</code>，安装发布者为 Microsoft 的扩展。</p>
            <a class="carla-link" :href="vscodePythonExt" target="_blank" rel="noopener noreferrer">
              {{ vscodePythonExt }}
            </a>
          </article>
          <article class="command-card">
            <h3>Jupyter 扩展</h3>
            <p>同样在扩展市场中搜索 <code>Jupyter</code>，安装发布者为 Microsoft 的扩展。</p>
            <a class="carla-link" :href="vscodeJupyterExt" target="_blank" rel="noopener noreferrer">
              {{ vscodeJupyterExt }}
            </a>
          </article>
          <article class="command-card">
            <h3>安装完成后的检查</h3>
            <ol class="carla-steps">
              <li>新建一个 <code>test.py</code> 文件，右上角能看到 Python 解释器选择入口。</li>
              <li>新建一个 <code>test.ipynb</code> 文件，顶部能看到内核选择入口。</li>
              <li>如果这两个入口都正常出现，说明扩展已经接管成功。</li>
            </ol>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="步骤 5 安装包"
      >
        <h3>步骤 5：安装 CARLA Python 包和 Notebook 运行依赖</h3>
        <p class="carla-cue">
          Quickstart 文档给出的正式发布版安装方式是通过 PIP 安装 Python client library。课堂统一使用 PowerShell 执行下面这组命令。
        </p>
        <div class="command-layout carla-single-code">
          <article class="command-card">
            <h3>推荐命令</h3>
            <pre><code class="bash">python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple carla==0.9.15 jupyter ipykernel</code></pre>
            <p>这一条命令会通过清华源一次性安装 CARLA、Jupyter 和 ipykernel，适合课堂环境直接使用。</p>
          </article>
        </div>
        <p class="carla-inline-link">
          PyPI 版本页：
          <a :href="pypiCarla" target="_blank" rel="noopener noreferrer">{{ pypiCarla }}</a>
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="安装验证"
      >
        <h3>安装完成后先做两项验证</h3>
        <div class="command-layout carla-link-grid">
          <article class="command-card">
            <h3>验证 1：先确认 python 可用</h3>
            <pre><code class="bash">python --version</code></pre>
            <p>如果这里失败，不要继续装包，先修正环境变量里的 Python 配置。</p>
          </article>
          <article class="command-card">
            <h3>验证 2：pip 是否看到 carla</h3>
            <pre><code class="bash">python -m pip show carla</code></pre>
            <p>能打印版本信息，说明 Python 侧已装好 client library。</p>
          </article>
          <article class="command-card">
            <h3>验证 3：VS Code 解释器是否正确</h3>
            <p>在 VS Code 右下角或命令面板里选择 <code>Python 3.10</code> 解释器，避免误用其他版本。</p>
          </article>
          <article class="command-card">
            <h3>Notebook 内核也要一致</h3>
            <p>打开 <code>.ipynb</code> 后，Kernel 要明确选择为 Python 3.10 对应环境。解释器和内核混乱，会直接导致后面导包失败。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="启动服务端"
      >
        <div class="section-head">
          <p class="kicker">START SERVER</p>
          <h2>启动 CARLA 服务端时直接使用低画质参数</h2>
        </div>
        <p class="carla-cue">
          这一条命令必须直接放进课堂主线。大部分机器显卡性能不足，如果默认高画质启动，最先出现的问题不是 Python 代码报错，而是服务端窗口本身打不开或运行不稳定。
        </p>
        <div class="command-layout carla-single-code">
          <article class="command-card carla-highlight-card">
            <h3>PowerShell 启动命令</h3>
            <pre><code class="bash">.\CarlaUE4.exe -dx11 -quality-level=Low</code></pre>
            <p>
              先在 PowerShell 中进入 <code>D:\CARLA_0.9.15\WindowsNoEditor</code> 目录，再执行这一条启动命令。
              <code>-dx11</code> 强制使用 DirectX 11，<code>-quality-level=Low</code> 直接降低画质，优先保证能打开和稳定运行。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="运行机制"
      >
        <h3>启动成功后，先分清 CARLA 的运行机制</h3>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>服务端 Server</h3>
            <p>负责运行仿真世界、地图、车辆、传感器、物理计算和渲染窗口。窗口打不开，后面的 Python 连接一定失败。</p>
          </article>
          <article class="command-card">
            <h3>客户端 Client</h3>
            <p>Python 脚本通过 <code>carla.Client("localhost", 2000)</code> 去连接服务端，再请求当前 world。</p>
          </article>
          <article class="command-card">
            <h3>最重要的结论</h3>
            <p>导入了 <code>carla</code> 模块，不等于仿真已经启动；打开了 CARLA 窗口，也不等于 Python 已经能控制它。两边都要成功，链路才算完整。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="对象链路"
      >
        <h3>第一次连接时最重要的对象链路</h3>
        <div class="carla-rhythm carla-rhythm--five">
          <span>Python 脚本</span>
          <span>carla.Client</span>
          <span>world</span>
          <span>map</span>
          <span>settings</span>
        </div>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>client</h3>
            <p>连接入口。负责连到服务端、设置超时、请求当前世界。</p>
          </article>
          <article class="concept-card">
            <h3>world</h3>
            <p>当前正在运行的仿真世界。后面天气、车辆、传感器都从这里展开。</p>
          </article>
          <article class="concept-card">
            <h3>map</h3>
            <p>当前世界对应的道路地图信息，可以读取地图名和 spawn points。</p>
          </article>
          <article class="concept-card">
            <h3>settings</h3>
            <p>当前世界的仿真设置，例如是否同步模式、固定步长是多少。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="代码段 1"
      >
        <h2>代码段 1：最小连接代码</h2>
        <div class="command-layout carla-single-code">
          <article class="command-card">
            <h3>把这一段直接复制到第一个 cell 里运行</h3>
            <pre><code class="python">import carla

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)

world = client.get_world()
current_map = world.get_map()

print(world)
print(current_map.name)</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="代码段 1 讲解"
      >
        <h3>代码段 1 逐行讲解</h3>
        <div class="command-layout carla-link-grid carla-link-grid--balanced">
          <article class="command-card">
            <h3><code>import carla</code></h3>
            <p>导入 Python client library。这里成功，只能说明本地 Python 环境已装好模块。</p>
          </article>
          <article class="command-card">
            <h3><code>carla.Client("localhost", 2000)</code></h3>
            <p>连接本机 2000 端口的 CARLA 服务端。默认情况下，CARLA 会占用 2000 和 2001 两个端口。</p>
          </article>
          <article class="command-card">
            <h3><code>client.set_timeout(10.0)</code></h3>
            <p>给网络请求设置超时时间，避免服务端没开时脚本一直卡住。</p>
          </article>
          <article class="command-card">
            <h3><code>client.get_world()</code></h3>
            <p>请求当前活动世界。后面所有核心操作几乎都从 <code>world</code> 开始。</p>
          </article>
          <article class="command-card">
            <h3><code>world.get_map()</code></h3>
            <p>取得当前地图对象。拿到一次后保存为变量，不要反复调用。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="代码段 2"
      >
        <h2>代码段 2：先把异常处理补上</h2>
        <p class="carla-cue">
          连接脚本不能只写“成功路径”。服务端没开、端口不对、版本不匹配、超时，这些都是真实环境里高频出现的问题。
        </p>
        <div class="command-layout carla-single-code">
          <article class="command-card">
            <h3>把这一段作为第二个 cell 运行</h3>
            <pre><code class="python">import carla

try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    print("连接成功")
except Exception as error:
    print("连接失败：", error)</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="异常处理解释"
      >
        <h3>这段异常处理到底解决了什么</h3>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>服务端未启动</h3>
            <p>如果 CARLA 窗口还没打开，连接请求会失败。异常信息能直接告诉你问题发生在“连不上”，而不是后面的 world 逻辑。</p>
          </article>
          <article class="command-card">
            <h3>端口或超时问题</h3>
            <p>地址、端口、网络调用超时都属于连接阶段问题，应该在这里被尽早发现。</p>
          </article>
          <article class="command-card">
            <h3>版本检查也放在这一层</h3>
            <p>CARLA 的 Python client 和服务端版本最好保持一致。连接成功后，先打印 client/server version，再进入后面的 world 读取最稳。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="代码段 3"
      >
        <h2>代码段 3：读取当前世界的基础信息</h2>
        <div class="command-layout carla-single-code">
          <article class="command-card">
            <h3>把这一段作为第三个 cell 运行</h3>
            <pre><code class="python">import carla

try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    print("client version:", client.get_client_version())
    print("server version:", client.get_server_version())

    world = client.get_world()
    current_map = world.get_map()
    settings = world.get_settings()
    weather = world.get_weather()
    spawn_points = current_map.get_spawn_points()

    print("地图名：", current_map.name)
    print("天气：", weather)
    print("同步模式：", settings.synchronous_mode)
    print("固定步长：", settings.fixed_delta_seconds)
    print("出生点数量：", len(spawn_points))
except Exception as error:
    print("连接失败：", error)</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="API 详细解释"
      >
        <h3>本章必须掌握的 API 与知识点</h3>
        <div class="command-layout carla-link-grid carla-link-grid--balanced">
          <article class="command-card">
            <h3><code>carla.Client</code></h3>
            <p>创建与服务端通信的客户端对象。没有它，就没有后面的 world。</p>
          </article>
          <article class="command-card">
            <h3><code>client.set_timeout</code></h3>
            <p>限制网络调用最长等待时间。课堂脚本里必须保留，避免“看起来像死机”。</p>
          </article>
          <article class="command-card">
            <h3><code>client.get_world</code></h3>
            <p>请求当前活动世界，这是进入仿真数据结构的真正入口。</p>
          </article>
          <article class="command-card">
            <h3><code>world.get_map</code></h3>
            <p>返回当前地图对象，可以读取地图名和出生点。拿到后保存为 <code>current_map</code> 即可。</p>
          </article>
          <article class="command-card">
            <h3><code>world.get_settings</code></h3>
            <p>读取同步模式和固定步长。后面做传感器和自动驾驶时，这两个设置非常关键。</p>
          </article>
          <article class="command-card">
            <h3><code>current_map.get_spawn_points()</code></h3>
            <p>返回推荐出生点列表。下一章生成车辆时，会直接从这里选择变换位姿。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="VS Code 运行"
      >
        <h3>在 VS Code 里如何顺利运行 .py 和 .ipynb</h3>
        <div class="command-layout carla-2plus1">
          <article class="command-card">
            <h3>运行 .py 文件</h3>
            <p>先确认右下角解释器是 Python 3.10，再点击右上角运行按钮，或者在终端中执行 <code>python 文件名.py</code>。</p>
          </article>
          <article class="command-card">
            <h3>运行 .ipynb 文件</h3>
            <p>先选择正确的 Kernel，再按 cell 顺序逐段执行。解释器和内核不一致，是初学阶段最高频的问题之一。</p>
          </article>
          <article class="command-card">
            <h3>为什么这一章代码都按代码段组织</h3>
            <p>因为课堂和实验都会用到 Jupyter 风格的逐段执行。每段代码只完成一个动作，更适合观察“这一段做了什么”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="常见问题"
      >
        <div class="section-head">
          <p class="kicker">TROUBLESHOOTING</p>
          <h2>第一次搭环境和连接时最常见的问题</h2>
        </div>
        <div class="concept-grid carla-quad-grid">
          <article class="concept-card">
            <h3>问题 1：<code>import carla</code> 失败</h3>
            <p>说明当前解释器里没有安装 carla 包，或者 VS Code 选错了解释器。</p>
          </article>
          <article class="concept-card">
            <h3>问题 2：连接超时</h3>
            <p>先检查 CARLA 服务端窗口是否真的已经启动，再确认端口是否还是默认 2000。</p>
          </article>
          <article class="concept-card">
            <h3>问题 3：窗口打不开或卡死</h3>
            <p>优先使用 <code>.\CarlaUE4.exe -dx11 -quality-level=Low</code>，不要先用默认高画质。</p>
          </article>
          <article class="concept-card">
            <h3>问题 4：Notebook 能开但跑不动</h3>
            <p>大概率不是 CARLA 本身，而是内核没选到 Python 3.10，或者 <code>ipykernel</code> 没安装。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="下载与总结"
      >
        <div class="section-head">
          <p class="kicker">DOWNLOADS AND SUMMARY</p>
          <h2>本章下载与收束</h2>
        </div>
        <div class="command-layout carla-link-grid">
          <article class="command-card carla-highlight-card">
            <h3>本章总代码下载</h3>
            <p>包含本章的连接示例、世界信息读取和连接检测脚本，可直接下载后在 VS Code 或 Notebook 中运行。</p>
            <a class="carla-link" :href="chapterAllCodeHref" download>
              下载 carla_ch01_all_examples.py
            </a>
          </article>
          <article class="command-card">
            <h3>本章结论 1</h3>
            <p>CARLA 不是普通 Python 库，而是服务端与客户端协同工作的仿真系统。</p>
          </article>
          <article class="command-card">
            <h3>本章结论 2</h3>
            <p>先搭好 Windows 环境，再启动低画质服务端，再写连接检测脚本，这才是课堂最稳的顺序。</p>
          </article>
          <article class="command-card">
            <h3>本章结论 3</h3>
            <p>一旦 <code>client -&gt; world -&gt; map/settings</code> 这条链路打通，后面的车辆、天气、传感器和自动驾驶就都有了落点。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键词：先把环境和连接链路打通，再进入车辆、传感器和实验任务。</p>
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

.page.is-slide-deck .carla-rhythm--four {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.page.is-slide-deck .carla-rhythm--five {
  grid-template-columns: repeat(5, minmax(0, 1fr));
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

.page.is-slide-deck .command-layout.carla-link-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: start;
}

.page.is-slide-deck .command-layout.carla-link-grid.carla-link-grid--balanced > :last-child,
.page.is-slide-deck .command-layout.carla-link-grid.carla-link-grid--balanced > :nth-last-child(2) {
  grid-column: span 1;
}

.page.is-slide-deck .command-layout.carla-single-code {
  grid-template-columns: 1fr;
}

.page.is-slide-deck .carla-highlight-card {
  border-color: rgba(13, 123, 232, 0.28);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.94), rgba(255, 255, 255, 0.98));
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

.page.is-slide-deck .carla-inline-link {
  margin: 10px 0 0;
  color: var(--text-secondary);
  font-size: 0.92rem;
}

.page.is-slide-deck .carla-inline-link a {
  color: #0a5eaf;
  font-weight: 700;
  text-decoration: underline;
  word-break: break-all;
}

.page.is-slide-deck .carla-steps {
  margin: 10px 0 0;
  padding-left: 20px;
}

.page.is-slide-deck .carla-steps li + li {
  margin-top: 8px;
}

@media (max-width: 900px) {
  .page.is-slide-deck .carla-rhythm,
  .page.is-slide-deck .carla-rhythm--four,
  .page.is-slide-deck .carla-rhythm--five,
  .page.is-slide-deck .command-layout.carla-2plus1,
  .page.is-slide-deck .concept-grid.carla-quad-grid,
  .page.is-slide-deck .command-layout.carla-link-grid {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .command-layout.carla-2plus1 > :last-child,
  .page.is-slide-deck .concept-grid.carla-quad-grid > .concept-card,
  .page.is-slide-deck .command-layout.carla-link-grid.carla-link-grid--balanced > :last-child,
  .page.is-slide-deck .command-layout.carla-link-grid.carla-link-grid--balanced > :nth-last-child(2) {
    grid-column: span 1;
  }
}
</style>
