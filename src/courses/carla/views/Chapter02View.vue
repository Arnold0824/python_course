<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const docsHome = "https://carla.readthedocs.io/en/latest/";
const quickStartDocs = "https://carla.readthedocs.io/en/latest/start_quickstart/";
const coreWorldDocs = "https://carla.readthedocs.io/en/latest/core_world/";
const pythonApiDocs = "https://carla.readthedocs.io/en/latest/python_api/";

const chapterAllCodeHref = "/courses/carla/ch02/carla_ch02_all_examples.py";
const homeworkAnswerHref = "/courses/carla/ch02/04_connection_check_answer.py";
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
        <strong>CARLA运行机制与首次连接</strong>
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
        <p class="kicker">CARLA WORLD CONNECTION</p>
        <h1>第二章 CARLA运行机制与首次连接</h1>
        <p class="hero-intro">
          这一章先不生成车辆，也不挂载相机。先把最基础的一条链路打通：
          Python 客户端怎样连接仿真器服务端，怎样拿到 <code>world</code>，
          再从 <code>world</code> 里读出地图、天气、同步模式和出生点数量。
        </p>
        <ul class="hero-checklist">
          <li>理解 CARLA 不是普通 Python 库，而是服务端加客户端的结构。</li>
          <li>掌握 <code>client -&gt; world -&gt; map/settings</code> 的基本访问链路。</li>
          <li>能够写出带异常处理的连接检测脚本，判断当前世界是否可正常使用。</li>
        </ul>
        <div class="goal-cards fly-in-seq">
          <article>
            <h2>课时安排</h2>
            <p>2 学时，重点只放在运行机制、首次连接和基础信息读取。</p>
          </article>
          <article>
            <h2>本章成果</h2>
            <p>能打印地图名、同步模式状态和出生点数量，并说清 client 和 world 的区别。</p>
          </article>
          <article>
            <h2>代码方式</h2>
            <p>页面里的代码按 notebook 单元拆成代码段，可以一段一段复制到 cell 里运行。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="为什么先做连接"
      >
        <div class="section-head">
          <p class="kicker">WHY THIS CHAPTER FIRST</p>
          <h2>为什么这一章先不做车和相机</h2>
        </div>
        <p class="chapter-two-cue">
          如果还没分清“服务端”和“客户端”，后面看到车辆、传感器和交通脚本时，
          很容易误以为所有功能都在本地 Python 脚本里完成。第二章的目标就是先把对象关系理顺。
        </p>
        <div class="command-layout chapter-two-2plus1">
          <article class="command-card">
            <h3>先建立入口</h3>
            <p>
              后面生成车辆、切换天气、挂载相机、读取图像，都要先拿到
              <code>world</code>。如果入口没建立，后面的代码都没有落点。
            </p>
          </article>
          <article class="command-card">
            <h3>先分清角色</h3>
            <p>
              CARLA 窗口负责跑仿真；Python 负责发请求、取信息、做控制。
              这一层关系不清楚，代码就只能停留在照抄。
            </p>
          </article>
          <article class="command-card">
            <h3>先保证脚本能稳</h3>
            <p>
              连接失败、端口错误、超时、服务端未启动，都是最常见的问题。
              先把异常处理补上，后面的实验才不会因为一个连接问题整段中断。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="本章参考文档"
      >
        <h3>本章直接参考的官方文档入口</h3>
        <div class="command-layout chapter-two-link-grid chapter-two-link-grid--balanced">
          <article class="command-card">
            <h3>文档首页</h3>
            <p>用来确认当前文档版本和整体结构，后面几页内容都从这里展开。</p>
            <a class="chapter-two-link" :href="docsHome" target="_blank" rel="noopener noreferrer">
              {{ docsHome }}
            </a>
          </article>
          <article class="command-card">
            <h3>Quick start</h3>
            <p>用来确认环境、默认端口、安装方式和服务端启动顺序。</p>
            <a class="chapter-two-link" :href="quickStartDocs" target="_blank" rel="noopener noreferrer">
              {{ quickStartDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>Core world</h3>
            <p>这一页直接解释了 client-server 结构，以及 world、map、actor 等核心概念。</p>
            <a class="chapter-two-link" :href="coreWorldDocs" target="_blank" rel="noopener noreferrer">
              {{ coreWorldDocs }}
            </a>
          </article>
          <article class="command-card">
            <h3>Python API</h3>
            <p>本章涉及的 <code>carla.Client</code>、<code>world.get_map()</code>、<code>world.get_settings()</code> 都在这里可查。</p>
            <a class="chapter-two-link" :href="pythonApiDocs" target="_blank" rel="noopener noreferrer">
              {{ pythonApiDocs }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="不是普通 Python 库"
      >
        <h2>CARLA 不是普通 Python 库</h2>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>普通 Python 库</h3>
            <p>导入之后，功能通常就在本地 Python 进程里执行，数据和计算都在当前程序内部。</p>
          </article>
          <article class="concept-card">
            <h3>CARLA 的方式</h3>
            <p>Python API 只是一层客户端接口；真正的仿真世界、物理和渲染运行在服务端。</p>
          </article>
          <article class="concept-card">
            <h3>直接结果</h3>
            <p>即使已经 <code>import carla</code> 成功，也不等于当前已经连上可用世界。</p>
          </article>
          <article class="concept-card">
            <h3>默认端口</h3>
            <p>官方 Quick start 提到默认 RPC 端口是 <code>2000</code>，另一个相关端口通常是 <code>2001</code>。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="服务端与客户端"
      >
        <h2>服务端和客户端分别做什么</h2>
        <p class="chapter-two-cue">
          <strong>一句话先记住：</strong>CARLA 窗口负责“把世界跑起来”，Python 脚本负责“连进去、问问题、发控制”。
        </p>
        <div class="command-layout chapter-two-2plus1">
          <article class="command-card">
            <h3>服务端 Server</h3>
            <p>负责世界更新、物理计算、地图加载、车辆状态变化、传感器渲染，通常更依赖 GPU。</p>
          </article>
          <article class="command-card">
            <h3>客户端 Client</h3>
            <p>负责连接服务端，读取当前世界对象，再通过 API 访问地图、设置、天气、车辆和传感器。</p>
          </article>
          <article class="command-card">
            <h3>这一章只做到哪里</h3>
            <p>这一章先停在 <code>client</code>、<code>world</code> 和 <code>map</code>，先保证入口稳，再进入生成 Actor。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="连接链路"
      >
        <h3>第一次连接时，脑子里要有这条链路</h3>
        <div class="chapter-two-rhythm">
          <span>启动 CARLA 服务端</span>
          <span>创建 client</span>
          <span>获取 world</span>
          <span>读取 map 和 settings</span>
        </div>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>client</h3>
            <p>连接入口。先有它，后面才能拿到世界。</p>
          </article>
          <article class="concept-card">
            <h3>world</h3>
            <p>当前仿真世界对象，是后续几乎所有操作的总入口。</p>
          </article>
          <article class="concept-card">
            <h3>map</h3>
            <p>地图对象，负责提供当前地图名和推荐出生点。</p>
          </article>
          <article class="concept-card">
            <h3>settings</h3>
            <p>世界运行设置，可以查看同步模式和固定步长等状态。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="启动顺序"
      >
        <h3>启动顺序必须稳定</h3>
        <div class="command-layout chapter-two-code-grid">
          <article class="command-card">
            <h3>步骤 1：先启动服务端</h3>
            <pre><code class="bash">CarlaUE4.exe</code></pre>
            <p>如果服务端没有先运行，下面的 Python 连接代码大概率只会超时或报错。</p>
          </article>
          <article class="command-card">
            <h3>步骤 2：再运行 Python 或 Notebook</h3>
            <pre><code class="bash">python script.py

# 或者打开 Jupyter / IPython Notebook
# 然后按顺序执行下面的代码段</code></pre>
            <p>这一章的课堂代码按代码段拆开，可以逐段复制到不同的 cell 中运行。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="代码段使用方式"
      >
        <h3>这一章的代码按 notebook 单元来组织</h3>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>代码段 1</h3>
            <p>先连接服务端，建立 <code>client</code>、<code>world</code> 等变量。</p>
          </article>
          <article class="concept-card">
            <h3>代码段 2</h3>
            <p>在前一个 cell 已经成功执行的基础上，继续读取地图、设置和天气。</p>
          </article>
          <article class="concept-card">
            <h3>代码段 3</h3>
            <p>单独输出某类结果，方便观察每一步到底拿到了什么对象。</p>
          </article>
          <article class="concept-card">
            <h3>整章代码</h3>
            <p>最后只保留一个整章总代码下载，便于统一保存和课后复习。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="代码 01：连接世界"
      >
        <div class="section-head">
          <p class="kicker">CODE SEGMENTS</p>
          <h2>代码 01：第一次连上当前世界</h2>
        </div>
        <p class="chapter-two-cue">
          下面三段代码可以按顺序复制到三个 notebook 单元中运行。每一段都只做一个动作，便于观察结果。
        </p>
        <div class="chapter-two-code-stack">
          <article class="command-card chapter-two-cell-card">
            <p class="chapter-two-cell-tag">代码段 1</p>
            <h3>导入模块并创建 client</h3>
            <pre><code class="python">import carla

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)</code></pre>
          </article>
          <article class="command-card chapter-two-cell-card">
            <p class="chapter-two-cell-tag">代码段 2</p>
            <h3>获取当前 world 和 map</h3>
            <pre><code class="python">world = client.get_world()
current_map = world.get_map()</code></pre>
          </article>
          <article class="command-card chapter-two-cell-card">
            <p class="chapter-two-cell-tag">代码段 3</p>
            <h3>打印 world 和地图名</h3>
            <pre><code class="python">print(world)
print(current_map.name)</code></pre>
          </article>
        </div>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>先观察什么</h3>
            <p>先看 <code>world</code> 是否能正常打印出来，再看地图名是否是一个合理的字符串。</p>
          </article>
          <article class="concept-card">
            <h3>成功标准</h3>
            <p>真正的成功不是“没有报错”，而是能拿到世界对象和地图名这两项有效信息。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="代码逐行理解"
      >
        <h3>逐行理解：不要只会照抄</h3>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3><code>carla.Client</code></h3>
            <p>创建客户端入口。地址写 <code>localhost</code>，表示连接本机；端口写 <code>2000</code>，表示连接默认 RPC 端口。</p>
          </article>
          <article class="concept-card">
            <h3><code>set_timeout(10.0)</code></h3>
            <p>给网络调用一个上限时间。连接不上时，不会一直卡住，而是抛出异常，方便定位问题。</p>
          </article>
          <article class="concept-card">
            <h3><code>get_world()</code></h3>
            <p>读取当前正在运行的世界对象。没有 <code>world</code>，后面的地图、设置、天气都无从谈起。</p>
          </article>
          <article class="concept-card">
            <h3><code>get_map()</code></h3>
            <p>获取当前地图对象。官方 Python API 特别提醒这是一次昂贵调用，取到之后更适合保存成变量反复使用。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="为什么要异常处理"
      >
        <h2>为什么连接代码必须带异常处理</h2>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>服务端未启动</h3>
            <p>最常见。脚本本身没错，但连接对象根本不存在。</p>
          </article>
          <article class="concept-card">
            <h3>端口或地址错误</h3>
            <p>把 <code>2000</code> 写错，或者本来要连远端却还在写 <code>localhost</code>，都会导致连接失败。</p>
          </article>
          <article class="concept-card">
            <h3>超时</h3>
            <p>服务端启动过慢、网络有问题或进程卡住时，调用可能在超时后抛出异常。</p>
          </article>
          <article class="concept-card">
            <h3>版本不匹配</h3>
            <p>官方 API 提醒过 client 和 server 版本最好一致，否则可能出现兼容问题。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="代码 02：安全连接"
      >
        <h3>代码 02：先接住错误，再看原因</h3>
        <p class="chapter-two-cue">
          这段代码更适合直接作为一个完整 cell 运行，因为 <code>try / except</code> 本来就是一个整体结构。
        </p>
        <div class="chapter-two-code-stack">
          <article class="command-card chapter-two-cell-card">
            <p class="chapter-two-cell-tag">代码段 4</p>
            <h3>带异常处理的连接写法</h3>
            <pre><code class="python">import carla

try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    print("连接成功")
except Exception as e:
    print("连接失败：", e)</code></pre>
          </article>
        </div>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>这段代码多了什么</h3>
            <p>它不是让错误“消失”，而是让错误变得可读。连接失败时，可以先看到原因，再决定排查哪一层。</p>
          </article>
          <article class="concept-card">
            <h3>课堂演示建议</h3>
            <p>可以先故意不打开服务端运行一次，再重新启动服务端，观察输出结果的变化。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="代码 03：世界信息"
      >
        <div class="section-head">
          <p class="kicker">WORLD INFO</p>
          <h2>代码 03：读取地图、天气和基础设置</h2>
        </div>
        <p class="chapter-two-cue">
          连接成功之后，不要立刻去生成车辆。先读一遍当前世界最重要的状态，判断仿真环境是否处在预期模式下。
        </p>
        <div class="chapter-two-code-stack">
          <article class="command-card chapter-two-cell-card">
            <p class="chapter-two-cell-tag">代码段 5</p>
            <h3>获取 map、settings 和 weather</h3>
            <pre><code class="python">world = client.get_world()
current_map = world.get_map()
settings = world.get_settings()
weather = world.get_weather()</code></pre>
          </article>
          <article class="command-card chapter-two-cell-card">
            <p class="chapter-two-cell-tag">代码段 6</p>
            <h3>打印本节最重要的 5 项信息</h3>
            <pre><code class="python">print("地图名：", current_map.name)
print("天气：", weather)
print("同步模式：", settings.synchronous_mode)
print("固定步长：", settings.fixed_delta_seconds)
print("出生点数量：", len(current_map.get_spawn_points()))</code></pre>
          </article>
        </div>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>最低检查项</h3>
            <p>地图名、同步模式、固定步长、出生点数量，这四项是本章最低限度要会读出来的信息。</p>
          </article>
          <article class="concept-card">
            <h3>天气为什么也要看</h3>
            <p>天气会影响视觉效果和传感器结果。现在先学会读取，后续章节再学习如何修改。</p>
          </article>
          <article class="concept-card">
            <h3>spawn points 是什么</h3>
            <p>它是一组推荐的出生位置。后面生成车辆时，往往会从这里挑一个作为初始位置。</p>
          </article>
          <article class="concept-card">
            <h3>为什么先读不先改</h3>
            <p>先确认当前世界到底是什么状态，再决定是否切换同步模式、地图或天气，调试会清楚很多。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="本节必须掌握的 API"
      >
        <h3>本节必须掌握的 API</h3>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3><code>carla.Client</code></h3>
            <p>创建连接入口，负责连到具体主机和端口。</p>
          </article>
          <article class="concept-card">
            <h3><code>client.set_timeout</code></h3>
            <p>给网络调用设置上限时间，避免脚本无限等待。</p>
          </article>
          <article class="concept-card">
            <h3><code>client.get_world</code></h3>
            <p>拿到当前世界对象，后面的地图、设置和天气都要从它开始。</p>
          </article>
          <article class="concept-card">
            <h3><code>world.get_map</code></h3>
            <p>获取当前地图对象，用来读地图名和出生点。</p>
          </article>
          <article class="concept-card">
            <h3><code>world.get_settings</code></h3>
            <p>读取同步模式、固定步长等世界运行参数。</p>
          </article>
          <article class="concept-card">
            <h3><code>world.get_weather</code></h3>
            <p>读取当前天气对象，用来确认环境条件。</p>
          </article>
          <article class="concept-card">
            <h3><code>map.get_spawn_points</code></h3>
            <p>返回推荐出生点列表，后面生成车辆时会直接用到。</p>
          </article>
          <article class="concept-card">
            <h3>版本检查 API</h3>
            <p><code>client.get_client_version()</code> 和 <code>client.get_server_version()</code> 可用来确认两端版本是否一致。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="client 与 world 的区别"
      >
        <h3><code>client</code> 和 <code>world</code> 的区别，一定要说清</h3>
        <div class="command-layout chapter-two-2plus1">
          <article class="command-card">
            <h3>client 是入口</h3>
            <p>它负责连接服务端、设置超时、读取版本、请求当前世界。它更像“和 CARLA 通话的电话”。</p>
          </article>
          <article class="command-card">
            <h3>world 是当前场景</h3>
            <p>它代表正在运行的仿真世界。地图、设置、天气、Actor 和蓝图库等内容，都从这里继续往下拿。</p>
          </article>
          <article class="command-card">
            <h3>map 不是 world 本身</h3>
            <p>地图只是世界里的一个组成部分。先有 <code>world</code>，再通过 <code>world.get_map()</code> 拿到当前地图。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="同步模式与固定步长"
      >
        <h3>同步模式和固定步长，先认识，不急着改</h3>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>同步模式</h3>
            <p><code>settings.synchronous_mode</code> 为真时，世界推进更强调受控；为假时，服务端会尽可能快地自己运行。</p>
          </article>
          <article class="concept-card">
            <h3>固定步长</h3>
            <p><code>settings.fixed_delta_seconds</code> 表示每一步模拟时间长度。后续做数据采集时，这个值非常重要。</p>
          </article>
          <article class="concept-card">
            <h3>这一章先做什么</h3>
            <p>先会读，不先改。先知道当前世界是不是同步模式，固定步长有没有被显式设置。</p>
          </article>
          <article class="concept-card">
            <h3>为什么现在就要看</h3>
            <p>同一段后续实验脚本，在不同同步状态下可能表现不同。先读出状态，后面分析结果时才有依据。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="连接检测作业"
      >
        <div class="section-head">
          <p class="kicker">HOMEWORK</p>
          <h2>本节作业：编写一个连接检测脚本</h2>
        </div>
        <p class="chapter-two-cue">
          作业目标不是“多写几行”，而是把本节最基础也最关键的能力独立串起来。
          先根据提示补全逻辑，再用答案文件对照检查。
        </p>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>必须输出</h3>
            <p>地图名、出生点数量、是否是同步模式、固定步长。</p>
          </article>
          <article class="concept-card">
            <h3>建议输出</h3>
            <p>天气对象。这样能更完整地描述当前世界状态。</p>
          </article>
          <article class="concept-card">
            <h3>加分项</h3>
            <p>输出客户端版本和服务端版本，判断两端是否一致。</p>
          </article>
          <article class="concept-card">
            <h3>排查顺序</h3>
            <p>先检查服务端是否已启动，再检查端口，然后再看异常输出内容。</p>
          </article>
        </div>
        <div class="chapter-two-code-stack">
          <article class="command-card chapter-two-cell-card">
            <p class="chapter-two-cell-tag">作业模板</p>
            <h3>根据注释补全逻辑</h3>
            <pre><code class="python">import carla

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
        # current_map = ________________________
        # settings = ___________________________
        # weather = ____________________________

        # 第 5 步：完成基础输出
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
    main()</code></pre>
          </article>
        </div>
        <div class="chapter-two-download-strip">
          <article class="command-card">
            <h3>作业答案版本</h3>
            <p>先独立补全，再下载答案对照。答案文件额外保留了版本检查的加分项。</p>
            <a class="chapter-two-link" :href="homeworkAnswerHref" download="04_connection_check_answer.py">
              下载 04_connection_check_answer.py
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="本章输出成果"
      >
        <h3>本章结束时，应该已经做到这些事</h3>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>成果 1</h3>
            <p>能正确打印当前地图名，而不是只会运行脚本。</p>
          </article>
          <article class="concept-card">
            <h3>成果 2</h3>
            <p>能打印同步模式状态和固定步长，并知道这两项不是普通文本，而是世界运行设置。</p>
          </article>
          <article class="concept-card">
            <h3>成果 3</h3>
            <p>能说清 <code>client</code> 是入口，<code>world</code> 是当前世界对象，<code>map</code> 是从 world 里拿到的。</p>
          </article>
          <article class="concept-card">
            <h3>成果 4</h3>
            <p>能在连接失败时输出异常信息，而不是让脚本直接报错退出。</p>
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
          <h2>第二章总结：先把入口打通，再进入世界控制</h2>
        </div>
        <div class="concept-grid chapter-two-quad-grid">
          <article class="concept-card">
            <h3>结构结论</h3>
            <p>CARLA 是服务端加客户端的结构，不是导入后就直接在本地跑完整仿真的普通库。</p>
          </article>
          <article class="concept-card">
            <h3>代码入口</h3>
            <p>先创建 <code>client</code>，再拿到 <code>world</code>，接着再读取 map、settings、weather 等信息。</p>
          </article>
          <article class="concept-card">
            <h3>工程习惯</h3>
            <p>连接代码必须带异常处理，最基本的超时和失败提示不能省略。</p>
          </article>
          <article class="concept-card">
            <h3>后续衔接</h3>
            <p>下一章可以自然过渡到蓝图库、车辆生成、出生点选择和更具体的世界控制。</p>
          </article>
        </div>
        <div class="command-layout chapter-two-link-grid chapter-two-link-grid--balanced">
          <article class="command-card">
            <h3>整章总代码下载</h3>
            <p>包含本章课堂用到的 3 组核心示例，已按 notebook 代码段顺序整理到一个文件里。</p>
            <a class="chapter-two-link" :href="chapterAllCodeHref" download="carla_ch02_all_examples.py">
              下载 carla_ch02_all_examples.py
            </a>
          </article>
          <article class="command-card">
            <h3>作业答案下载</h3>
            <p>先根据模板独立补全，再用答案版本对照。答案文件额外包含版本检查加分项。</p>
            <a class="chapter-two-link" :href="homeworkAnswerHref" download="04_connection_check_answer.py">
              下载 04_connection_check_answer.py
            </a>
          </article>
          <article class="command-card">
            <h3>继续查文档</h3>
            <a class="chapter-two-link" :href="coreWorldDocs" target="_blank" rel="noopener noreferrer">
              Core world
            </a>
            <a class="chapter-two-link" :href="pythonApiDocs" target="_blank" rel="noopener noreferrer">
              Python API
            </a>
          </article>
          <article class="command-card">
            <h3>一条最小记忆线</h3>
            <p><code>client</code> 负责连接，<code>world</code> 代表当前世界，<code>map</code> 和 <code>settings</code> 都从 world 往下拿。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：先连上 world，再谈地图、天气、出生点和后续控制。</p>
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
.page.is-slide-deck .chapter-two-rhythm {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.page.is-slide-deck .chapter-two-rhythm span {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(11, 98, 179, 0.2);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.95), rgba(245, 251, 255, 0.98));
  color: #0a5eaf;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
}

.page.is-slide-deck .chapter-two-cue {
  margin: 10px 0 0;
  padding: 10px 12px;
  border-left: 4px solid rgba(11, 98, 179, 0.42);
  border-radius: 10px;
  background: rgba(11, 98, 179, 0.06);
  color: var(--text-main);
  font-size: 0.95rem;
  line-height: 1.68;
}

.page.is-slide-deck .command-layout.chapter-two-2plus1 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .command-layout.chapter-two-2plus1 > :last-child {
  grid-column: 1 / -1;
}

.page.is-slide-deck .concept-grid.chapter-two-quad-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .concept-grid.chapter-two-quad-grid > .concept-card {
  grid-column: span 1;
}

.page.is-slide-deck .command-layout.chapter-two-link-grid,
.page.is-slide-deck .command-layout.chapter-two-code-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: start;
}

.page.is-slide-deck .command-layout.chapter-two-link-grid.chapter-two-link-grid--balanced > :last-child,
.page.is-slide-deck .command-layout.chapter-two-link-grid.chapter-two-link-grid--balanced > :nth-last-child(2) {
  grid-column: span 1;
}

.page.is-slide-deck .chapter-two-code-stack {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
  margin-top: 18px;
}

.page.is-slide-deck .chapter-two-download-strip {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
  margin-top: 16px;
}

.page.is-slide-deck .chapter-two-cell-card {
  width: 100%;
}

.page.is-slide-deck .chapter-two-cell-tag {
  margin: 0 0 8px;
  color: #0a5eaf;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.page.is-slide-deck .chapter-two-link {
  display: block;
  margin-top: 10px;
  color: #0a5eaf;
  font-weight: 700;
  text-decoration: underline;
  word-break: break-all;
}

@media (max-width: 900px) {
  .page.is-slide-deck .chapter-two-rhythm,
  .page.is-slide-deck .command-layout.chapter-two-2plus1,
  .page.is-slide-deck .concept-grid.chapter-two-quad-grid,
  .page.is-slide-deck .command-layout.chapter-two-link-grid,
  .page.is-slide-deck .command-layout.chapter-two-code-grid {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .command-layout.chapter-two-2plus1 > :last-child,
  .page.is-slide-deck .concept-grid.chapter-two-quad-grid > .concept-card,
  .page.is-slide-deck .command-layout.chapter-two-link-grid.chapter-two-link-grid--balanced > :last-child,
  .page.is-slide-deck .command-layout.chapter-two-link-grid.chapter-two-link-grid--balanced > :nth-last-child(2) {
    grid-column: span 1;
  }
}
</style>
