<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";
import {
  chapter05ConceptCards,
  chapter05Docs,
  chapter05MetricCards,
  chapter05ObserverCards,
  chapter05Pitfalls,
  chapter05Resources,
  chapter05Slides,
} from "../chapter05Content.js";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const chapterAllCodeHref = "/courses/carla/ch05/carla_ch05_all_examples.py";
const visualizerScriptHref = "/courses/carla/ch05/exp04_event_log_visualizer.py";
const sampleSvgHref = "/courses/carla/ch05/output/exp04/events_visualization.svg";
const sampleReportHref = "/courses/carla/ch05/output/exp04/analysis_report.md";
const sampleEventsCsvHref = "/courses/carla/ch05/output/exp04/events.csv";
const sampleSummaryJsonHref = "/courses/carla/ch05/output/exp04/summary.json";
const runResultsZipHref = "/courses/carla/ch05/ch05_exp04_run_results.zip";

const learningGoals = [
  "能在同步模式下生成自动驾驶车辆，并拿到地图中全部交通灯。",
  "能按“近距离触发 + 同灯去抖”的思路记录红灯相关事件。",
  "能把事件日志汇总成红/黄/绿事件数与红灯占比，并据此写出结论。",
];

const workflowSteps = [
  "定义触发阈值、事件冷却时间与日志字段。",
  "封装速度、距离、状态翻译三个工具函数。",
  "开启同步模式并准备好回滚开关。",
  "生成主车，并一次性拿到所有交通灯 actor。",
  "每帧找最近交通灯，距离低于阈值时触发判断。",
  "用 last_light_id + cooldown 做事件去抖。",
  "把事件列表写入 events.csv，汇总写入 summary.json/txt。",
  "根据红灯条数、红灯占比、红灯时车速完成实验结论。",
];

const chapterMetrics = [
  { value: "25 m", label: "触发阈值" },
  { value: "20", label: "冷却 ticks" },
  { value: "3", label: "结果文件" },
];

const workflowPhases = [
  { no: "01", title: "定阈值", text: "把距离阈值、冷却 ticks、日志字段集中在文件顶部。" },
  { no: "02", title: "找最近灯", text: "每帧遍历交通灯列表，选出离主车最近的那一盏。" },
  { no: "03", title: "做去抖", text: "同灯走冷却，换灯立即触发，避免日志刷屏。" },
  { no: "04", title: "出结论", text: "用 events.csv 与 summary.json 支撑实验结论。" },
];

const experimentRequirements = [
  { title: "运行要求", text: "实验必须在同步模式下进行，固定步长推进仿真，事件可复现。" },
  { title: "日志要求", text: "日志按时间或帧号顺序记录，字段清晰，能用于后续统计。" },
  { title: "统计要求", text: "需给出红灯相关条数与总记录条数，并说明触发阈值设置依据。" },
  { title: "分析要求", text: "结论必须基于日志与统计结果描述，不得只写主观判断。" },
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
        <span class="brand-tag">CARLA 05</span>
        <strong>红灯状态监测与事件日志分析</strong>
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
            <p class="kicker">TRAFFIC LIGHT EVENT LAB</p>
            <h1>第五章 红灯状态监测与事件日志分析</h1>
            <p class="hero-intro">
              第四章用 Traffic Manager 改变了车辆的“开车风格”，本章则把车辆放回普通状态，
              专门观察它和红绿灯的关系。重点不是写复杂算法，而是用一段“近距离触发 + 同灯去抖”的循环，
              把车辆与最近交通灯的关系记录成可复查的事件日志，再用红灯条数与红灯占比写出结论。
            </p>
            <ul class="hero-checklist">
              <li>每帧选出最近交通灯，只有靠近时才写日志。</li>
              <li>用 last_light_id + cooldown 避免同灯刷屏。</li>
              <li>输出 events.csv、summary.json 与 summary.txt，便于报告引用。</li>
            </ul>
          </div>
          <aside class="lesson-hero-panel">
            <span class="lesson-panel-label">红灯事件日志</span>
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
          <h2>第五章按照“定阈值、找最近灯、做去抖、出结论”推进</h2>
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
          <h2>这一章主要查交通灯对象与同步模式</h2>
        </div>
        <div class="command-layout lesson-link-grid">
          <article class="command-card" v-for="doc in chapter05Docs" :key="doc.href">
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
          <p class="kicker">EXPERIMENT 04</p>
          <h2>实验四的核心是“近距离触发 + 同灯去抖 + 数据支撑结论”</h2>
        </div>
        <p class="lesson-cue">
          自动驾驶在仿真里会自然遇到红绿灯。本章不去改变它的行为，而是把“车辆与最近交通灯的关系”
          按要求记录下来，最后用红灯条数与占比写出结论。
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
        data-outline-label="核心概念"
      >
        <div class="section-head">
          <p class="kicker">CONCEPTS</p>
          <h2>四个概念把“事件日志”讲清楚</h2>
        </div>
        <p class="lesson-cue">
          阈值、最近交通灯、状态字符串、去抖。这四个概念都不复杂，但合在一起决定了日志的质量。
          没有阈值会冗余，没有去抖会刷屏；没有“最近灯”就抓不住关键事件。
        </p>
        <div class="command-layout lesson-card-grid">
          <article class="command-card" v-for="concept in chapter05ConceptCards" :key="concept.name">
            <h3>{{ concept.name }}：{{ concept.tag }}</h3>
            <p>{{ concept.text }}</p>
            <ul class="lesson-points">
              <li>{{ concept.detail }}</li>
              <li>{{ concept.role }}</li>
              <li>{{ concept.extra }}</li>
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
          <h2>统计指标围绕“红灯”展开</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="metric in chapter05MetricCards" :key="metric.title">
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
                <td><code>events.csv</code></td>
                <td>每条事件一行：帧号、仿真时间、速度、状态、距离、灯 id、位置。</td>
                <td>报告附件；结论中引用具体某一条事件时回看。</td>
              </tr>
              <tr>
                <td><code>summary.json</code></td>
                <td>总事件数、红/黄/绿事件、红灯占比、红灯时平均车速等汇总字段。</td>
                <td>程序读取或自动化分析。</td>
              </tr>
              <tr>
                <td><code>summary.txt</code></td>
                <td>与 summary.json 相同内容的人读版本。</td>
                <td>提交报告时直接粘贴到“实验结论”一节。</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section
        v-for="slide in chapter05Slides"
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
          <h2>实验四最容易出问题的地方</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter05Pitfalls" :key="item.title">
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
          <p class="kicker">VISUALIZATION LAB</p>
          <h2>扩展挑战：把事件日志变成 SVG 可视化报告</h2>
        </div>
        <p class="lesson-cue">
          本章主线是“事件日志分析”，要让分析有说服力，光看数字不够，需要看到图。
          这个扩展脚本纯离线、零第三方依赖，读取上一次实验生成的 <code>events.csv</code> 与 <code>summary.json</code>，
          一次输出 4 面板矢量 <strong>SVG 可视化</strong>（俯视轨迹散点 / 事件时间线 / 行为标签条形图 / 红灯速度直方图）
          以及 Markdown 报告。SVG 用浏览器直接打开，缩放不糊，可贴进实验报告。
        </p>

        <figure class="ch05-viz-preview">
          <img
            :src="sampleSvgHref"
            alt="实验四 事件日志可视化样例：俯视轨迹散点、事件时间线、行为标签条形图、红灯速度直方图"
            loading="lazy"
          />
          <figcaption>
            ↑ 上机运行 90 秒（Town10HD，63 个事件、41 个红灯）后生成的真实样例。
            <a :href="sampleSvgHref" target="_blank" rel="noopener noreferrer">单独打开 SVG</a> ·
            <a :href="sampleReportHref" target="_blank" rel="noopener noreferrer">查看 Markdown 报告</a>
          </figcaption>
        </figure>

        <ol class="timeline">
          <li v-for="item in chapter05ObserverCards" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </li>
        </ol>
        <div class="command-layout lesson-2plus1">
          <article class="command-card">
            <h3>默认运行</h3>
            <pre><code class="powershell">python exp04_event_log_visualizer.py</code></pre>
          </article>
          <article class="command-card">
            <h3>指定输入目录</h3>
            <pre><code class="powershell">python exp04_event_log_visualizer.py --input output/exp04</code></pre>
          </article>
          <article class="command-card">
            <h3>输出到其他目录</h3>
            <pre><code class="powershell">python exp04_event_log_visualizer.py --output-dir reports/run_v2</code></pre>
          </article>
          <article class="command-card lesson-highlight-card">
            <h3>脚本下载</h3>
            <p>仅依赖 Python 标准库；在不同阈值生成的 events.csv 上反复运行，可生成多份 SVG 做参数对比。</p>
            <a class="lesson-link" :href="visualizerScriptHref" download="exp04_event_log_visualizer.py">
              {{ visualizerScriptHref }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="运行结果下载"
      >
        <div class="section-head">
          <p class="kicker">SAMPLE RUN</p>
          <h2>样例运行结果：直接看真实输出长什么样</h2>
        </div>
        <p class="lesson-cue">
          下面是 Town10HD 上跑 90 秒、配置 <code>TRIGGER_DISTANCE_M=25</code> / <code>EVENT_COOLDOWN_TICKS=20</code>
          得到的一份真实输出。你可以单独下载任意一个文件查看格式，也可以下载 ZIP 一并保存。
        </p>
        <div class="command-layout lesson-link-grid">
          <article class="command-card">
            <h3>events.csv</h3>
            <p>事件日志原始数据，共 63 条记录。</p>
            <a class="lesson-link" :href="sampleEventsCsvHref" download="events.csv">{{ sampleEventsCsvHref }}</a>
          </article>
          <article class="command-card">
            <h3>summary.json</h3>
            <p>汇总字段：触发阈值、总事件、红/黄/绿事件数、红灯占比、红灯时平均车速。</p>
            <a class="lesson-link" :href="sampleSummaryJsonHref" download="summary.json">{{ sampleSummaryJsonHref }}</a>
          </article>
          <article class="command-card">
            <h3>analysis_report.md</h3>
            <p>事件日志可视化分析器输出的文字报告，含 ASCII 条形图与 Top 3 路口。</p>
            <a class="lesson-link" :href="sampleReportHref" download="analysis_report.md">{{ sampleReportHref }}</a>
          </article>
          <article class="command-card">
            <h3>events_visualization.svg</h3>
            <p>4 面板矢量可视化；浏览器直接打开缩放不糊，可截图贴入报告。</p>
            <a class="lesson-link" :href="sampleSvgHref" download="events_visualization.svg">{{ sampleSvgHref }}</a>
          </article>
          <article class="command-card lesson-highlight-card">
            <h3>一键打包下载（ZIP）</h3>
            <p>events.csv、summary.json、summary.txt、analysis_report.md、events_visualization.svg 全部打包。</p>
            <a class="lesson-link" :href="runResultsZipHref" download="ch05_exp04_run_results.zip">{{ runResultsZipHref }}</a>
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
          <article class="command-card" v-for="item in chapter05Resources" :key="item.title">
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
            <a class="lesson-link" :href="chapterAllCodeHref" download="carla_ch05_all_examples.py">
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
          <h2>第五章的重点，是让红灯事件可复现、可统计</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card">
            <h3>知识主线</h3>
            <p>同步模式 + 固定步长保证事件可复现；最近交通灯 + 阈值 + 去抖决定事件日志的质量。</p>
          </article>
          <article class="concept-card">
            <h3>代码主线</h3>
            <p>常量、工具函数、主车与交通灯、最近灯查找、事件采集、写日志、汇总、main 串成完整流程。</p>
          </article>
          <article class="concept-card">
            <h3>实验主线</h3>
            <p>最终交付应包含代码、events.csv、summary.json/txt 与基于红灯条数的文字分析。</p>
          </article>
          <article class="concept-card">
            <h3>扩展价值</h3>
            <p>SVG 可视化让“车辆在地图哪里遇到红灯、什么时间触发、速度分布如何”一图说清，便于课堂讨论与对比观察。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：事件日志不是越多越好，关键是“近距离触发、同灯去抖、有数据支撑结论”。</p>
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
.ch05-viz-preview {
  margin: 1.5rem 0 2rem;
  padding: 1rem;
  background: #fafafa;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  text-align: center;
}
.ch05-viz-preview img {
  width: 100%;
  max-width: 1080px;
  height: auto;
  display: block;
  margin: 0 auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.ch05-viz-preview figcaption {
  margin-top: 0.75rem;
  font-size: 0.875rem;
  color: #555;
}
.ch05-viz-preview figcaption a {
  color: #1976d2;
  text-decoration: none;
}
.ch05-viz-preview figcaption a:hover {
  text-decoration: underline;
}
</style>
