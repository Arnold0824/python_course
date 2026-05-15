<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";
import {
  chapter08AssessmentCards,
  chapter08ConceptCards,
  chapter08Docs,
  chapter08MaterialSteps,
  chapter08NumpyMethods,
  chapter08PandasMethods,
  chapter08Pitfalls,
  chapter08Resources,
  chapter08Units,
} from "../chapter08Content.js";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const learningGoals = [
  "理解 NumPy 数组、形状、索引、向量化计算和常用统计函数。",
  "掌握 pandas 读取 CSV、查看数据、筛选、清洗、分组、透视和保存结果。",
  "能围绕第七章课表数据完成一条可复现的数据分析流程，并写出基于数据的结论。",
];

const chapterMetrics = [
  { value: "24", label: "教学单元" },
  { value: "2", label: "核心库" },
  { value: "CSV", label: "分析产出" },
];

const workflowPhases = [
  { no: "01", title: "先会看", text: "用 head、info、describe 认识数据结构。" },
  { no: "02", title: "再会算", text: "用 NumPy 理解数组、向量化、统计和缺失值。" },
  { no: "03", title: "然后会清洗", text: "用 pandas 处理字段、缺失、重复、文本和类型。" },
  { no: "04", title: "最后会分析", text: "用分组、透视、保存和文字结论形成完整报告。" },
];

const workflowSteps = [
  "准备 scores.csv 和 course_schedule_sample.csv 两份练习数据。",
  "从 NumPy 数组入门，理解批量计算和 axis。",
  "进入 pandas，掌握 Series、DataFrame、读取、选择和清洗。",
  "使用 groupby 和 pivot_table 完成统计汇总。",
  "把第七章课表 CSV 转化为清洗数据和统计结果。",
  "把统计结果写成可核对的分析结论。",
];

const caseQuestions = [
  "全校课表一共有多少条记录？",
  "哪些院系开课数量最多？",
  "哪些教师授课门数较多？",
  "不同校区的课程分布是否均衡？",
  "学分主要集中在哪些区间？",
  "数据里是否存在缺失、重复或异常记录？",
];

const exp5ReportDownload = "实验报告5：清洗和预处理学生食堂消费数据（理实课程实验部分）-学生姓名.docx";
const exp5ReportHref = `/courses/python/exp_reports/${exp5ReportDownload}`;
const exp5MaterialDownload = "食堂消费数据.csv";
const exp5MaterialHref = `/courses/python/ch08/${exp5MaterialDownload}`;
const exp5SubmitHref = "https://f.wps.cn/g/FkK5Ns3v/";

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
        <span class="brand-tag">Chapter 8</span>
        <strong>数据分析基础</strong>
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
            <p class="kicker">CHAPTER 08 DATA ANALYSIS BASICS</p>
            <h1>第八章 数据分析基础</h1>
            <p class="hero-intro">
              第七章把网页数据保存成 CSV，第八章继续往前走：用 NumPy 和 pandas 把数据读进来、看清楚、清洗干净、
              统计汇总，并把结果写成可以复查的分析结论。
            </p>
            <ul class="hero-checklist">
              <li>前半章用小型成绩表理解数组、表格和基础统计。</li>
              <li>后半章回到课表数据，完成清洗、分组、透视和保存。</li>
              <li>代码段按顺序复制到 notebook 中运行，变量和分析流程会逐步展开。</li>
            </ul>
          </div>
          <aside class="lesson-hero-panel">
            <span class="lesson-panel-label">从数据文件到分析结论</span>
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
          <h2>本章路线：先会看，再会算，然后会清洗，最后会分析</h2>
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
          <h2>先把两个 CSV 放到项目文件夹</h2>
        </div>
        <p class="lesson-cue">
          后面的代码会从 <code>public/courses/python/ch08</code> 读取数据。开始学习前，先下载两个 CSV，并放到这个目录。
        </p>
        <div class="lesson-phase-track">
          <article class="lesson-phase-card" v-for="step in chapter08MaterialSteps" :key="step.no">
            <span>{{ step.no }}</span>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </article>
        </div>
        <div class="command-layout lesson-link-grid">
          <article class="command-card" v-for="item in chapter08Resources" :key="`material-${item.title}`">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
            <a
              class="lesson-link"
              :href="item.href"
              :download="item.download"
            >
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
          <h2>NumPy 与 pandas 分工不同，但经常一起出现</h2>
        </div>
        <p class="lesson-cue">
          NumPy 更像“数值计算引擎”，pandas 更像“表格处理工具”。本章先用 NumPy 建立批量计算意识，
          再用 pandas 完成真实 CSV 数据分析。
        </p>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter08ConceptCards" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="文档入口"
      >
        <div class="section-head">
          <p class="kicker">DOCS</p>
          <h2>这一章可以反复查阅的资料入口</h2>
        </div>
        <div class="command-layout lesson-link-grid">
          <article class="command-card" v-for="doc in chapter08Docs" :key="doc.href">
            <h3>{{ doc.title }}</h3>
            <p>{{ doc.text }}</p>
            <a class="lesson-link" :href="doc.href" target="_blank" rel="noopener noreferrer">
              {{ doc.href }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="分析问题"
      >
        <div class="section-head">
          <p class="kicker">CASE QUESTIONS</p>
          <h2>本章综合案例围绕课表数据提出问题</h2>
        </div>
        <p class="lesson-cue">
          数据分析不是把所有函数都试一遍，而是带着问题去整理数据、选择方法和解释结果。
        </p>
        <div class="lesson-step-list">
          <span v-for="question in caseQuestions" :key="question">{{ question }}</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="NumPy 常用方法"
      >
        <div class="section-head">
          <p class="kicker">NUMPY CHEATSHEET</p>
          <h2>NumPy 先记住这些方法就够课堂使用</h2>
        </div>
        <div class="lesson-table-card">
          <table>
            <thead>
              <tr>
                <th>方法</th>
                <th>用途</th>
                <th>例子</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in chapter08NumpyMethods" :key="item.method">
                <td><code>{{ item.method }}</code></td>
                <td>{{ item.use }}</td>
                <td><code>{{ item.example }}</code></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="pandas 常用方法"
      >
        <div class="section-head">
          <p class="kicker">PANDAS CHEATSHEET</p>
          <h2>pandas 的重点是表格：读、看、选、清洗、统计、保存</h2>
        </div>
        <div class="lesson-table-card">
          <table>
            <thead>
              <tr>
                <th>方法</th>
                <th>用途</th>
                <th>例子</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in chapter08PandasMethods" :key="item.method">
                <td><code>{{ item.method }}</code></td>
                <td>{{ item.use }}</td>
                <td><code>{{ item.example }}</code></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section
        v-for="unit in chapter08Units"
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
        data-outline-label="常见卡点"
      >
        <div class="section-head">
          <p class="kicker">TROUBLESHOOTING</p>
          <h2>跟学时优先检查这些问题</h2>
        </div>
        <p class="lesson-cue">
          数据分析的报错通常不是语法问题，而是路径、字段、类型、缺失值和结论证据没有处理好。
          遇到错误时，先回到表格结构本身。
        </p>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter08Pitfalls" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.problem }}</p>
            <p>{{ item.fix }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="实验评价"
      >
        <div class="section-head">
          <p class="kicker">ASSESSMENT</p>
          <h2>实验任务：提交一份可复查的数据分析结果</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter08AssessmentCards" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
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
          <h2>本章只提供数据文件</h2>
        </div>
        <p class="lesson-cue">
          Python 代码不提供现成脚本下载。请按本章 24 个代码单元逐步运行，理解每一步为什么这样写。
        </p>
        <div class="command-layout lesson-link-grid">
          <article class="command-card" v-for="item in chapter08Resources" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
            <a
              class="lesson-link"
              :href="item.href"
              :download="item.download || null"
              :target="isExternalLink(item.href) ? '_blank' : null"
              :rel="isExternalLink(item.href) ? 'noopener noreferrer' : null"
            >
              下载 {{ item.download || item.title }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="实验5报告与提交"
      >
        <div class="section-head">
          <p class="kicker">EXPERIMENT 05</p>
          <h2>实验报告 5：清洗和预处理学生食堂消费数据</h2>
        </div>
        <p class="lesson-cue">
          本次实验使用 <code>食堂消费数据.csv</code>，围绕学生食堂消费明细完成读取、字段检查、缺失值处理、去重、
          金额字段整理和按学生汇总。完成代码运行和结果分析后，下载实验报告模板填写，再通过 WPS 收集表提交。
        </p>
        <div class="command-layout lesson-link-grid">
          <article class="command-card">
            <h3>实验报告 5 下载</h3>
            <p>下载模板后，按实验目的、实验过程、运行结果、结果分析和收获思考几个部分完成填写。</p>
            <a
              class="lesson-link"
              :href="exp5ReportHref"
              :download="exp5ReportDownload"
            >
              下载实验报告5：清洗和预处理学生食堂消费数据
            </a>
          </article>
          <article class="command-card">
            <h3>实验素材下载</h3>
            <p>使用 <code>食堂消费数据.csv</code> 作为本次实验数据源，读取后先检查字段、行数、缺失值和重复记录。</p>
            <a
              class="lesson-link"
              :href="exp5MaterialHref"
              :download="exp5MaterialDownload"
            >
              下载 食堂消费数据.csv
            </a>
          </article>
          <article class="command-card">
            <h3>报告填写要点</h3>
            <p>不要只粘贴代码。报告里要保留原始记录数、缺失值检查、去重后记录数、消费金额汇总结果和简短分析结论。</p>
          </article>
          <article class="command-card">
            <h3>实验报告提交</h3>
            <p>完成实验代码、运行截图、数据清洗结果和分析结论后，通过 WPS 收集表统一提交。</p>
            <a
              class="lesson-link"
              :href="exp5SubmitHref"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ exp5SubmitHref }}
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
          <h2>第八章的重点，是把数据变成可以解释的结果</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card">
            <h3>NumPy 主线</h3>
            <p>数组、形状、索引、向量化、统计函数和缺失值处理。</p>
          </article>
          <article class="concept-card">
            <h3>pandas 主线</h3>
            <p>读取、查看、选择、清洗、分组、透视、合并和保存。</p>
          </article>
          <article class="concept-card">
            <h3>实战主线</h3>
            <p>从课表 CSV 出发，产出清洗数据、统计表和文字结论。</p>
          </article>
          <article class="concept-card">
            <h3>学习底线</h3>
            <p>结论必须能回到数据文件核对，不能只凭主观感觉描述。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：爬到数据只是开始，能清洗、统计并解释数据，才算完成分析。</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">代码已复制</div>
  </div>
</template>
