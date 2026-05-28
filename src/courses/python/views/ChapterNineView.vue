<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";
import {
  chartDecisionCards,
  chapter09AssessmentCards,
  chapter09ConceptCards,
  chapter09Docs,
  chapter09MaterialSteps,
  chapter09Pitfalls,
  chapter09Resources,
  chapter09Units,
  referenceCharts,
} from "../chapter09Content.js";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const learningGoals = [
  "理解图表服务数据问题，而不是为了装饰报告。",
  "能围绕小时消费高峰图说明为什么画、怎么画、怎么解释。",
  "能把同一套 matplotlib 结构迁移到折线图、柱状图、散点图和直方图。",
];

const chapterMetrics = [
  { value: "1", label: "主讲图" },
  { value: "5", label: "参考图" },
  { value: "PNG", label: "报告图片" },
];

const workflowPhases = [
  { no: "01", title: "先问问题", text: "图表必须回答一个数据问题。" },
  { no: "02", title: "再选图型", text: "趋势、比较、构成、分布、关系对应不同图。" },
  { no: "03", title: "讲透主图", text: "用小时消费高峰图完整讲解 matplotlib 结构。" },
  { no: "04", title: "迁移代码", text: "其他图型给参考代码，学生按问题自主改造。" },
  { no: "05", title: "写进报告", text: "每张图都要配具体字段和数值结论。" },
];

const workflowSteps = [
  "读取第八章 output 目录中的统计 CSV。",
  "判断图表要回答趋势、比较、构成、分布还是关系问题。",
  "重点完成 hour_peak.png：小时消费高峰柱状图。",
  "参考代码生成 daily_trend.png、payment_compare.png、student_scatter.png、amount_hist.png。",
  "可选生成 terminal_top10.png，观察 POS 终端使用差异。",
  "把图表、代码和解释整理进实验报告 6。",
];

const exp6SubmitHref = "https://f.wps.cn/g/Bpu5vC6C/";
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
        <span class="brand-tag">Chapter 9</span>
        <strong>数据可视化基础</strong>
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
            <p class="kicker">CHAPTER 09 MATPLOTLIB VISUALIZATION</p>
            <h1>第九章 数据可视化基础</h1>
            <p class="hero-intro">
              第八章已经把食堂消费流水整理成统计表。第九章继续往前走：用 matplotlib 把一个数据问题讲清楚。
              本章重点不是“会画很多图”，而是先说明为什么画这张图，再解释怎么画这张图。
            </p>
            <ul class="hero-checklist">
              <li>主讲图只讲一张：学生食堂消费小时高峰图。</li>
              <li>围绕问题、字段、图型、坐标轴、颜色、标注和结论组织代码。</li>
              <li>其他图型只给参考代码，用来训练学生自主迁移。</li>
            </ul>
          </div>
          <aside class="lesson-hero-panel">
            <span class="lesson-panel-label">从统计表到报告图片</span>
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
          <h2>本章路线：先问问题，再选图型，最后写结论</h2>
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
        data-outline-level="1"
        data-outline-label="素材准备"
      >
        <div class="section-head">
          <p class="kicker">MATERIALS</p>
          <h2>第九章直接使用第八章的输出表</h2>
        </div>
        <p class="lesson-cue">
          如果 <code>public/courses/python/ch08/output</code> 下缺少统计 CSV，先回到第八章运行完整流程。
          第九章只负责把结果画成能支撑报告结论的图片。
        </p>
        <div class="lesson-phase-track">
          <article class="lesson-phase-card" v-for="step in chapter09MaterialSteps" :key="step.no">
            <span>{{ step.no }}</span>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </article>
        </div>
        <div class="command-layout lesson-link-grid">
          <article class="command-card" v-for="item in chapter09Resources" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
            <a class="lesson-link" :href="item.href" :download="item.download">
              下载 {{ item.download }}
            </a>
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
          <h2>图表的贡献，是让数据问题更容易被看懂</h2>
        </div>
        <p class="lesson-cue">
          matplotlib 是工具，不是目的。本章所有代码都围绕“图回答什么问题”展开。
        </p>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter09ConceptCards" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="选图原则"
      >
        <div class="section-head">
          <p class="kicker">CHART DECISION</p>
          <h2>问题类型决定图表类型</h2>
        </div>
        <div class="lesson-table-card">
          <table>
            <thead>
              <tr>
                <th>问题类型</th>
                <th>适合图表</th>
                <th>要回答的问题</th>
                <th>食堂消费例子</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in chartDecisionCards" :key="item.type">
                <td>{{ item.type }}</td>
                <td>{{ item.chart }}</td>
                <td>{{ item.question }}</td>
                <td>{{ item.example }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="文档入口"
      >
        <div class="section-head">
          <p class="kicker">DOCS</p>
          <h2>查资料时不要只搜“怎么画”，先找相似问题</h2>
        </div>
        <div class="command-layout lesson-link-grid">
          <article class="command-card" v-for="doc in chapter09Docs" :key="doc.href">
            <h3>{{ doc.title }}</h3>
            <p>{{ doc.text }}</p>
            <a class="lesson-link" :href="doc.href" target="_blank" rel="noopener noreferrer">
              {{ doc.href }}
            </a>
          </article>
        </div>
      </section>

      <section
        v-for="unit in chapter09Units"
        :id="`unit-${unit.no}`"
        :key="unit.no"
        class="section reveal lesson-code-page"
        data-outline-level="1"
        :data-outline-label="unit.label"
      >
        <div class="lesson-slide-layout">
          <div class="lesson-slide-notes">
            <div class="section-head">
              <p class="kicker">UNIT {{ unit.no }}</p>
              <h2>{{ unit.title }}</h2>
            </div>
            <p class="lesson-cue">{{ unit.lead }}</p>
            <div class="lesson-teach-stack">
              <article class="command-card lesson-teach-card">
                <h3>这一段在做什么</h3>
                <p>{{ unit.explain }}</p>
              </article>
              <article class="command-card lesson-teach-card">
                <h3>为什么这样写</h3>
                <p>{{ unit.why }}</p>
              </article>
              <article class="command-card lesson-teach-card">
                <h3>关键记忆点</h3>
                <ul class="lesson-points">
                  <li v-for="point in unit.points" :key="point">{{ point }}</li>
                </ul>
              </article>
            </div>
            <div class="lesson-terms-strip">
              <article v-for="term in unit.terms" :key="term.title">
                <h3>{{ term.title }}</h3>
                <p>{{ term.text }}</p>
              </article>
            </div>
          </div>

          <pre><code class="python">{{ unit.code }}</code></pre>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="参考代码"
      >
        <div class="section-head">
          <p class="kicker">REFERENCE CHARTS</p>
          <h2>其他图型只给参考代码，按问题自主迁移</h2>
        </div>
        <p class="lesson-cue">
          下面的代码块不再扩展成新的课堂主线，但代码内部已经加入详细注释。
          学生要先说清楚它回答什么问题，再顺着注释运行、修改和写结论。
        </p>
      </section>

      <section
        v-for="chart in referenceCharts"
        :id="`reference-${chart.no}`"
        :key="chart.no"
        class="section reveal lesson-code-page"
        data-outline-level="2"
        :data-outline-label="chart.label"
      >
        <div class="lesson-slide-layout">
          <div class="lesson-slide-notes">
            <div class="section-head">
              <p class="kicker">REFERENCE {{ chart.no }}</p>
              <h2>{{ chart.title }}</h2>
            </div>
            <div class="lesson-teach-stack">
              <article class="command-card lesson-teach-card">
                <h3>这张图回答什么</h3>
                <p>{{ chart.question }}</p>
              </article>
              <article class="command-card lesson-teach-card">
                <h3>为什么用这种图</h3>
                <p>{{ chart.why }}</p>
              </article>
              <article class="command-card lesson-teach-card">
                <h3>输入与输出</h3>
                <p>读取 <code>{{ chart.data }}</code>，输出 <code>{{ chart.output }}</code>。</p>
              </article>
            </div>
          </div>

          <pre><code class="python">{{ chart.code }}</code></pre>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="常见卡点"
      >
        <div class="section-head">
          <p class="kicker">TROUBLESHOOTING</p>
          <h2>图画出来以后，优先检查这些问题</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter09Pitfalls" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.problem }}</p>
            <p>{{ item.fix }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="实验6报告"
      >
        <div class="section-head">
          <p class="kicker">EXPERIMENT 06</p>
          <h2>实验报告 6：学生食堂消费数据可视化</h2>
        </div>
        <p class="lesson-cue">
          实验 6 至少提交三张图。每张图都要写清楚：它回答的问题、使用的数据字段、观察到的具体数值。
          不要把姓名和学号放进图表。
        </p>
        <div class="command-layout lesson-link-grid">
          <article class="command-card">
            <h3>实验报告提交</h3>
            <p>完成代码、PNG 图片和实验报告后，通过此 WPS 收集表统一提交。</p>
            <a
              class="lesson-link"
              :href="exp6SubmitHref"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ exp6SubmitHref }}
            </a>
          </article>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter09AssessmentCards" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
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
          <h2>第九章的重点，是用图表把数据问题讲清楚</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card">
            <h3>主图</h3>
            <p>小时消费高峰图讲清楚“为什么画、怎么画、怎么解释”。</p>
          </article>
          <article class="concept-card">
            <h3>方法</h3>
            <p>掌握 fig、ax、bar、标题、坐标轴、网格、标注和 savefig。</p>
          </article>
          <article class="concept-card">
            <h3>迁移</h3>
            <p>其他图型按问题类型选择：趋势、比较、构成、分布、关系。</p>
          </article>
          <article class="concept-card">
            <h3>底线</h3>
            <p>图后面必须有具体数值结论，并且继续保护学生个人信息。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：不是为了画图而画图，而是为了让一个数据问题被看清楚。</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">代码已复制</div>
  </div>
</template>
