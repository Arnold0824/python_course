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
  chapter08Pitfalls,
  chapter08Resources,
  chapter08Units,
} from "../chapter08Content.js";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const learningGoals = [
  "能用正确编码读取食堂消费数据，并说明记录数、字段数、学生人数和日期范围。",
  "能完成日期时间转换、消费交易筛选、异常线索标注和分析字段生成。",
  "能输出清洗后明细、统计表和脱敏学生汇总，并写出可复查的数据结论。",
];

const chapterMetrics = [
  { value: "12", label: "连续单元" },
  { value: "17313", label: "原始记录" },
  { value: "5", label: "输出表" },
];

const workflowPhases = [
  { no: "01", title: "提出问题", text: "先明确食堂消费流水要回答什么。" },
  { no: "02", title: "读入数据", text: "用 gb18030 正确读取中文 CSV。" },
  { no: "03", title: "清洗字段", text: "整理日期、时间、金额、交易类型和异常线索。" },
  { no: "04", title: "分组分析", text: "统计时间、支付方式、终端和脱敏学生汇总。" },
  { no: "05", title: "输出报告", text: "保存五张 CSV，并用具体数值支撑结论。" },
];

const workflowSteps = [
  "下载并读取食堂消费数据.csv。",
  "检查记录规模、字段类型、缺失值、重复值和交易名称。",
  "把记账日期、交易时间和金额字段转换成可分析格式。",
  "筛选普通消费交易，保留 0 元、非消费和余额差异记录作为复核线索。",
  "生成餐段、食堂楼层、支付方式和异常金额标记。",
  "输出清洗明细、每日统计、小时统计、支付方式统计和脱敏学生汇总。",
];

const caseQuestions = [
  "原始流水是否能被正确读取，中文字段是否正常？",
  "普通消费交易和非消费交易各有多少？",
  "学生主要集中在哪些小时和餐段消费？",
  "支付码、IC 卡和不同食堂终端有什么差异？",
  "哪些 0 元、非消费、余额不一致或高金额记录需要解释？",
  "学生层面的汇总结果怎样脱敏后再展示？",
];

const exp5ReportDownload = "实验报告5：清洗和预处理学生食堂消费数据（理实课程实验部分）-学生姓名.docx";
const exp5ReportHref = `/courses/python/exp_reports/${exp5ReportDownload}`;
const exp5MaterialDownload = "食堂消费数据.csv";
const exp5MaterialHref = `/courses/python/ch08/${exp5MaterialDownload}`;
const exp5SubmitHref = "https://f.wps.cn/g/FkK5Ns3v/";
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
              本章围绕一份真实的 <code>食堂消费数据.csv</code> 展开：把原始交易流水读进来、看清楚、清洗干净、
              统计汇总，并输出可以支撑实验报告的结果表。
            </p>
            <ul class="hero-checklist">
              <li>不把 NumPy 和 pandas 当作方法手册讲，只使用完成案例需要的操作。</li>
              <li>从编码、字段类型、交易状态、余额差异和隐私脱敏建立分析口径。</li>
              <li>代码段按顺序复制到 notebook 中运行，最后生成五张报告用 CSV。</li>
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
          <h2>本章路线：从一份消费流水到一组可复查报告表</h2>
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
          <h2>先把食堂消费数据放到项目文件夹</h2>
        </div>
        <p class="lesson-cue">
          后面的代码会从 <code>public/courses/python/ch08</code> 读取数据。开始学习前，先下载
          <code>食堂消费数据.csv</code>，并保持文件名不变。
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
          <h2>先理解交易流水，再选择必要的 pandas 操作</h2>
        </div>
        <p class="lesson-cue">
          本章只保留完成食堂消费分析所需的工具：读取、检查、类型转换、筛选、派生字段、分组统计和保存结果。
          NumPy 只在批量分类时作为辅助出现。
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
          <h2>本章所有代码都围绕食堂消费数据提出问题</h2>
        </div>
        <p class="lesson-cue">
          数据分析不是把所有函数都试一遍，而是带着问题去整理数据、选择方法和解释结果。
        </p>
        <div class="lesson-step-list">
          <span v-for="question in caseQuestions" :key="question">{{ question }}</span>
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
          数据分析的报错通常不是语法问题，而是编码、路径、字段、类型、交易口径和结论证据没有处理好。
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
        data-outline-level="1"
        data-outline-label="实验5报告与提交"
      >
        <div class="section-head">
          <p class="kicker">EXPERIMENT 05</p>
          <h2>实验报告 5：清洗和预处理学生食堂消费数据</h2>
        </div>
        <p class="lesson-cue">
          本次实验使用 <code>食堂消费数据.csv</code>，围绕学生食堂消费明细完成编码读取、字段检查、交易清洗、
          日期时间转换、分组统计、脱敏汇总和结果保存。完成代码运行和结果分析后，下载实验报告模板填写，再通过 WPS 收集表提交。
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
            <p>不要只粘贴代码。报告里要保留原始记录数、消费分析记录数、异常复核说明、五张输出表和带具体数值的结论。</p>
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
            <h3>读取主线</h3>
            <p>用 gb18030 正确读取中文 CSV，并先确认记录规模、字段和金额分布。</p>
          </article>
          <article class="concept-card">
            <h3>清洗主线</h3>
            <p>转换日期时间和金额字段，筛选普通消费交易，保留复核记录。</p>
          </article>
          <article class="concept-card">
            <h3>分析主线</h3>
            <p>围绕每日、小时、支付方式、食堂终端和学生脱敏汇总生成统计表。</p>
          </article>
          <article class="concept-card">
            <h3>学习底线</h3>
            <p>结论必须能回到数据文件核对，不能只凭主观感觉描述。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：拿到数据只是开始，能清洗、统计、脱敏并解释数据，才算完成分析。</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">代码已复制</div>
  </div>
</template>
