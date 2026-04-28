<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";
import {
  chapter04Docs,
  chapter04MetricCards,
  chapter04ObserverCards,
  chapter04Pitfalls,
  chapter04Resources,
  chapter04ScenarioCards,
  chapter04Slides,
} from "../chapter04Content.js";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const chapterAllCodeHref = "/courses/carla/ch04/carla_ch04_all_examples.py";
const observerScriptHref = "/courses/carla/ch04/exp03_four_vehicle_observer.py";

const learningGoals = [
  "能用 Traffic Manager 配置不同的自动驾驶参数方案。",
  "能在相同运行条件下采集速度、位置和帧号等基础状态数据。",
  "能把多组方案统计成 CSV / JSON，并根据数据写出对比结论。",
];

const workflowSteps = [
  "把参数方案写成 SCENARIOS 数据表。",
  "统一同步模式、固定步长、运行时长和采样间隔。",
  "生成主车与少量背景车，让跟车和变道参数有观察空间。",
  "把每套方案应用到主车，运行同样的仿真时间。",
  "按固定间隔记录速度、位置、frame 和仿真时间。",
  "汇总平均速度、最高速度、低速样本占比与行驶距离。",
  "保存 summary.csv、samples.csv 和 summary.json。",
  "根据排行榜与统计表完成实验分析。",
];

const chapterMetrics = [
  { value: "4", label: "驾驶方案" },
  { value: "30s", label: "单组时长" },
  { value: "3", label: "结果文件" },
];

const workflowPhases = [
  { no: "01", title: "定方案", text: "先把保守、普通、赶时间、路口冒险四种驾驶性格写成参数表。" },
  { no: "02", title: "跑同场", text: "每组方案使用相同地图、相同同步步长和相同运行时长。" },
  { no: "03", title: "记数据", text: "按固定间隔记录速度、位置、frame 和仿真时间。" },
  { no: "04", title: "做比较", text: "用统计表和排行榜解释参数变化带来的行为差异。" },
];

const experimentRequirements = [
  { title: "基本要求", text: "至少设计两套参数方案，且每套方案至少包含两项参数差异。" },
  { title: "运行要求", text: "每套方案运行时间不少于 30 秒，并使用同步模式保证对比公平。" },
  { title: "统计要求", text: "至少输出样本数、平均速度、最高速度、最低速度等可读取统计结果。" },
  { title: "分析要求", text: "结论必须基于统计结果描述差异，不得只写主观感受。" },
];

function isExternalLink(href) {
  return /^https?:\/\//.test(href);
}
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
        <span class="brand-tag">CARLA 04</span>
        <strong>自动驾驶参数对比与统计分析</strong>
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
        <div class="lesson-hero-grid">
          <div class="lesson-hero-copy">
            <p class="kicker">AUTOPILOT PARAMETER LAB</p>
            <h1>第四章 自动驾驶参数对比与统计分析</h1>
            <p class="hero-intro">
              本章对应实验项目三。学习重点不是把算法做得更深，而是把自动驾驶参数变成一场可复查的小实验：
              换一组驾驶性格，跑同样的时间，记录同样的数据，再用统计结果解释车辆行为的变化。
            </p>
            <ul class="hero-checklist">
              <li>用四套参数方案扩展原实验：保守慢行、普通通勤、赶时间、路口冒险。</li>
              <li>每组方案都运行 30 秒，输出原始采样表和汇总统计表。</li>
              <li>最后用排行榜辅助观察，但实验结论必须回到数据本身。</li>
            </ul>
          </div>
          <aside class="lesson-hero-panel">
            <span class="lesson-panel-label">参数对比实验</span>
            <div class="lesson-metric" v-for="metric in chapterMetrics" :key="metric.label">
              <strong>{{ metric.value }}</strong>
              <span>{{ metric.label }}</span>
            </div>
          </aside>
        </div>
        <div class="goal-cards fly-in-seq">
          <article v-for="goal in learningGoals" :key="goal">
            <h2>学习目标</h2>
            <p>{{ goal }}</p>
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
          <h2>第四章按照“定方案、跑同场、记数据、做比较”的顺序推进</h2>
        </div>
        <div class="lesson-phase-track">
          <article class="lesson-phase-card" v-for="phase in workflowPhases" :key="phase.no">
            <span>{{ phase.no }}</span>
            <h3>{{ phase.title }}</h3>
            <p>{{ phase.text }}</p>
          </article>
        </div>
        <div class="lesson-step-list">
          <span v-for="step in workflowSteps" :key="step">{{ step }}</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="文档入口"
      >
        <div class="section-head">
          <p class="kicker">DOCS</p>
          <h2>这一章主要查 Traffic Manager 与同步模式</h2>
        </div>
        <div class="command-layout lesson-link-grid">
          <article class="command-card" v-for="doc in chapter04Docs" :key="doc.href">
            <h3>{{ doc.title }}</h3>
            <p>{{ doc.text }}</p>
            <a
              class="lesson-link"
              :href="doc.href"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ doc.href }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="实验目标"
      >
        <div class="section-head">
          <p class="kicker">EXPERIMENT 03</p>
          <h2>实验三的核心是“改参数、看变化、做总结”</h2>
        </div>
        <p class="lesson-cue">
          自动驾驶参数不会直接写在实验结论里，它要经过“设置参数、运行车辆、采集状态、统计结果”这条链路，
          最后才能变成可解释的数据差异。
        </p>
        <div class="command-layout lesson-card-grid">
          <article class="command-card" v-for="item in experimentRequirements" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="趣味方案"
      >
        <div class="section-head">
          <p class="kicker">SCENARIOS</p>
          <h2>把参数方案做成四种“驾驶性格”</h2>
        </div>
        <p class="lesson-cue">
          这些方案不增加技术难度，只增加观察角度。每组方案都只改 Traffic Manager 的基础参数，
          但最终可能在速度、停车比例和行驶距离上产生不同表现。
        </p>
        <div class="command-layout lesson-card-grid">
          <article class="command-card" v-for="scenario in chapter04ScenarioCards" :key="scenario.name">
            <h3>{{ scenario.name }}：{{ scenario.tag }}</h3>
            <p>{{ scenario.text }}</p>
            <ul class="lesson-points">
              <li>{{ scenario.speed }}</li>
              <li>{{ scenario.distance }}</li>
              <li>{{ scenario.lane }}</li>
              <li>{{ scenario.light }}</li>
            </ul>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="统计指标"
      >
        <div class="section-head">
          <p class="kicker">METRICS</p>
          <h2>统计指标不复杂，但要能支撑结论</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="metric in chapter04MetricCards" :key="metric.title">
            <h3>{{ metric.title }}</h3>
            <p>{{ metric.text }}</p>
          </article>
        </div>
        <div class="lesson-table-card">
          <table>
            <thead>
              <tr>
                <th>文件</th>
                <th>用途</th>
                <th>报告中怎么用</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>summary.csv</code></td>
                <td>每组方案一行，保存参数和汇总统计。</td>
                <td>放入报告，直接比较多组方案。</td>
              </tr>
              <tr>
                <td><code>samples.csv</code></td>
                <td>每次采样一行，保存速度、位置、帧号和时间。</td>
                <td>当某组结果异常时，用它回查原始过程。</td>
              </tr>
              <tr>
                <td><code>summary.json</code></td>
                <td>和 summary.csv 内容相近，但更适合后续程序读取。</td>
                <td>后续扩展绘图或自动分析时使用。</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section
        v-for="slide in chapter04Slides"
        :id="`slide-${slide.no}`"
        :key="slide.no"
        class="section reveal lesson-code-page"
        data-outline-level="1"
        :data-outline-label="slide.outline"
      >
        <div class="lesson-slide-layout">
          <div class="lesson-slide-notes">
            <div class="section-head">
              <p class="kicker">CODE SLIDE {{ slide.no }}</p>
              <h2>{{ slide.title }}</h2>
            </div>
            <p class="lesson-cue">{{ slide.lead }}</p>

            <div class="lesson-teach-stack">
              <article class="command-card lesson-teach-card">
                <h3>这一段在做什么</h3>
                <p>{{ slide.explain }}</p>
              </article>
              <article class="command-card lesson-teach-card">
                <h3>为什么这样写</h3>
                <p>{{ slide.why }}</p>
              </article>
              <article class="command-card lesson-teach-card">
                <h3>关键记忆点</h3>
                <ul class="lesson-points">
                  <li v-for="point in slide.points" :key="point">{{ point }}</li>
                </ul>
              </article>
            </div>

            <div class="lesson-terms-strip">
              <article v-for="term in slide.terms" :key="term.title">
                <h3>{{ term.title }}</h3>
                <p>{{ term.text }}</p>
              </article>
            </div>
          </div>

          <pre><code class="python">{{ slide.code }}</code></pre>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="常见误区"
      >
        <div class="section-head">
          <p class="kicker">PITFALLS</p>
          <h2>实验三最容易出问题的地方</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter04Pitfalls" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="趣味扩展"
      >
        <div class="section-head">
          <p class="kicker">OBSERVATION LAB</p>
          <h2>扩展挑战：四宫格观察四种驾驶风格</h2>
        </div>
        <p class="lesson-cue">
          这个扩展脚本会同时生成四辆主车，每辆主车代表一种驾驶风格，并在 pygame 窗口中显示四个第一视角。
          它适合课堂观察和讨论：哪辆车更容易发生碰撞，哪辆车更常压线，哪辆车看起来更稳。脚本提供 normal、high、extreme 三档观察模式，
          high 适合课堂演示，extreme 用于高密度交通与高风险参数观察。
        </p>
        <ol class="timeline">
          <li v-for="item in chapter04ObserverCards" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </li>
        </ol>
        <div class="command-layout lesson-2plus1">
          <article class="command-card">
            <h3>推荐运行命令</h3>
            <pre><code class="powershell">python exp03_four_vehicle_observer.py --risk-level high</code></pre>
          </article>
          <article class="command-card">
            <h3>高风险观察</h3>
            <pre><code class="powershell">python exp03_four_vehicle_observer.py --risk-level extreme</code></pre>
          </article>
          <article class="command-card">
            <h3>性能较弱时</h3>
            <pre><code class="powershell">python exp03_four_vehicle_observer.py --risk-level normal --background-vehicles 8 --walkers 4</code></pre>
          </article>
          <article class="command-card lesson-highlight-card">
            <h3>脚本下载</h3>
            <p>启动 CARLA 服务器后运行。窗口中按 ESC 或直接关闭窗口即可结束，脚本会自动清理车辆、行人和传感器。</p>
            <a class="lesson-link" :href="observerScriptHref" download="exp03_four_vehicle_observer.py">
              {{ observerScriptHref }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="资料下载"
      >
        <div class="section-head">
          <p class="kicker">RESOURCES</p>
          <h2>实验指导书、模板、答案和提交入口统一放在这里</h2>
        </div>
        <div class="command-layout lesson-link-grid">
          <article class="command-card" v-for="item in chapter04Resources" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
            <a
              class="lesson-link"
              :href="item.href"
              :download="item.download || null"
              :target="isExternalLink(item.href) ? '_blank' : null"
              :rel="isExternalLink(item.href) ? 'noopener noreferrer' : null"
            >
              {{ item.href }}
            </a>
          </article>
          <article class="command-card lesson-highlight-card">
            <h3>整章总代码直达</h3>
            <p>完成逐段学习后，可以直接下载整章脚本，对照前面的代码段重新串起完整流程。</p>
            <a class="lesson-link" :href="chapterAllCodeHref" download="carla_ch04_all_examples.py">
              {{ chapterAllCodeHref }}
            </a>
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
          <h2>第四章的重点，是让实验结论有数据支撑</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card">
            <h3>知识主线</h3>
            <p>Traffic Manager 参数决定自动驾驶倾向，同步模式保证对比公平，统计文件支撑实验结论。</p>
          </article>
          <article class="concept-card">
            <h3>代码主线</h3>
            <p>方案表、工具函数、单组运行、多组循环、保存文件共同构成完整实验流程。</p>
          </article>
          <article class="concept-card">
            <h3>实验主线</h3>
            <p>最终交付应包含代码、summary.csv、samples.csv、summary.json 和基于数据的文字分析。</p>
          </article>
          <article class="concept-card">
            <h3>扩展价值</h3>
            <p>“驾驶性格”让实验更有趣，但没有引入额外算法负担，适合课堂观察和报告讨论。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：参数实验不是比谁跑得快，而是用同样的方法观察参数变化带来的行为差异。</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">命令已复制</div>
  </div>
</template>
