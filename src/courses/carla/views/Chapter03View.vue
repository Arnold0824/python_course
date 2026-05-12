<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";
import {
  chapter03AlignmentCards,
  chapter03Docs,
  chapter03Pitfalls,
  chapter03Resources,
  chapter03Slides,
} from "../chapter03Content.js";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const chapterAllCodeHref = "/courses/carla/ch03/carla_ch03_all_examples.py";
const exp02OutputZipHref = "/courses/carla/ch03/ch03_exp02_run_results.zip";

const exp02ResultSamples = [
  {
    title: "样本 1：起始路段",
    frame: "454933",
    rgb: "/courses/carla/ch03/output/exp02/rgb/454933.png",
    seg: "/courses/carla/ch03/output/exp02/seg/454933.png",
  },
  {
    title: "样本 15：中段路口",
    frame: "455045",
    rgb: "/courses/carla/ch03/output/exp02/rgb/455045.png",
    seg: "/courses/carla/ch03/output/exp02/seg/455045.png",
  },
  {
    title: "样本 30：末段道路",
    frame: "455165",
    rgb: "/courses/carla/ch03/output/exp02/rgb/455165.png",
    seg: "/courses/carla/ch03/output/exp02/seg/455165.png",
  },
];

const exp02ResultStats = [
  { title: "配对数量", text: "本站发布的抽样版本含 7 对 RGB+Seg；原始运行采集 30 对，已抽样以减小下载体积。" },
  { title: "命名方式", text: "每一对样本都使用 CARLA frame 作为文件名，例如 454933.png。" },
];

const learningGoals = [
  "能说明双通道采集为什么必须做同帧对齐，而不是各自保存图片。",
  "能独立写出同步模式、双监听、同帧等待、间隔采样和资源清理这条主线。",
  "能按代码段顺序，自己搭出一份可运行的 RGB 与语义分割配对采集脚本。",
];

const workflowSteps = [
  "先把实验参数集中管理，明确采样节奏。",
  "连接 CARLA，准备 world、blueprint library、输出目录和双队列。",
  "写好 push_latest、wait_for_image、wait_for_aligned_pair 三个关键函数。",
  "开启同步模式并生成主车。",
  "挂 RGB 与语义分割相机，锁定同位姿和同内参。",
  "启动监听和自动驾驶，让车辆连续前进。",
  "热身后进行间隔采样，保存 30 对图像。",
  "输出参数记录和对齐报告，最后清理环境。",
];

const chapterMetrics = [
  { value: "2", label: "采集通道" },
  { value: "30+", label: "配对样本" },
  { value: "10", label: "代码段" },
];

const workflowPhases = [
  { no: "01", title: "搭底座", text: "参数、连接、队列与工具函数先准备好。" },
  { no: "02", title: "做对齐", text: "同步模式、双相机、同位姿和同内参统一锁定。" },
  { no: "03", title: "跑采样", text: "自动驾驶热身后，按间隔保存配对图像。" },
  { no: "04", title: "可复查", text: "输出参数记录、对齐报告，并清理仿真环境。" },
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
        <span class="brand-tag">CARLA 03</span>
        <strong>RGB 与语义分割双通道采集对齐</strong>
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
            <p class="kicker">DUAL-CHANNEL CAPTURE AND ALIGNMENT</p>
            <h1>第三章 RGB 与语义分割双通道采集对齐</h1>
            <p class="hero-intro">
              这一章不再停留在“能采到图”，而是正式进入“能采到一对严格对应的数据”。
              本章按代码段拆成连续学习单元，顺着页面从上到下阅读，就能理解每一步为什么写、解决什么问题、最后如何拼成完整实验。
            </p>
            <ul class="hero-checklist">
              <li>每个代码段单独成页，目录导航可以直接跳转到对应知识点。</li>
              <li>每一段都回答 3 个问题：这一段做什么、为什么这样写、关键记忆点是什么。</li>
              <li>整章最终目标是产出 30 对会变化、可核验、可复现的 RGB 与语义分割样本。</li>
            </ul>
          </div>
          <aside class="lesson-hero-panel">
            <span class="lesson-panel-label">最小可用视觉数据集</span>
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
          <h2>第三章按照“搭底座、做对齐、再采样”的顺序推进</h2>
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
          <h2>这一章真正需要反复查阅的官方入口</h2>
        </div>
        <div class="command-layout lesson-link-grid">
          <article class="command-card" v-for="doc in chapter03Docs" :key="doc.href">
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
        data-outline-label="对齐目标"
      >
        <div class="section-head">
          <p class="kicker">ALIGNMENT</p>
          <h2>首先要建立的不是 API 记忆，而是对齐意识</h2>
        </div>
        <p class="lesson-cue">
          RGB 图像提供视觉外观，语义分割图像提供像素级标签。只有当两路数据来自同一辆车、同一位姿、同一套成像参数、同一帧号时，
          它们才是可以直接配对使用的数据对。
        </p>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter03AlignmentCards" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="数据集结构"
      >
        <div class="section-head">
          <p class="kicker">OUTPUT</p>
          <h2>这一章从一开始就按“最小数据集”思维组织结果</h2>
        </div>
        <div class="command-layout lesson-2plus1">
          <article class="command-card">
            <h3>输出目录</h3>
            <pre><code class="text">output/exp02/
  rgb/
  seg/
  params.json
  alignment_report.json</code></pre>
          </article>
          <article class="command-card">
            <h3>配对命名</h3>
            <pre><code class="text">rgb/000123.png
seg/000123.png</code></pre>
          </article>
          <article class="command-card">
            <h3>为什么只用帧号命名</h3>
            <p>
              因为这一章的核心任务是“证明两路图像属于同一时刻”。文件名直接使用 frame，
              后续自动统计匹配数量、缺失帧和错帧会最直接。
            </p>
          </article>
        </div>
      </section>

      <section
        v-for="slide in chapter03Slides"
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
          <h2>避开这几个坑，实验就不容易停在“只是能跑”</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card" v-for="item in chapter03Pitfalls" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="实验要求"
      >
        <div class="section-head">
          <p class="kicker">EXPERIMENT 02</p>
          <h2>实验项目二最后要交出的，不只是图片，而是一套可解释结果</h2>
        </div>
        <div class="command-layout lesson-card-grid">
          <article class="command-card">
            <h3>实验目标</h3>
            <p>在同步模式下，让主车自动驾驶并完成 RGB 与语义分割双通道采集对齐。</p>
          </article>
          <article class="command-card">
            <h3>最低成果</h3>
            <p>输出不少于 30 对双通道图像，并附带参数记录和对齐报告。</p>
          </article>
          <article class="command-card">
            <h3>采集效果要求</h3>
            <p>车辆应持续移动，样本之间应有明显变化，不要出现 30 帧几乎一样的情况。</p>
          </article>
          <article class="command-card">
            <h3>工程要求</h3>
            <p>实验结束要恢复 world settings、关闭自动驾驶、停止并销毁传感器。</p>
          </article>
        </div>
      </section>

      <section
        id="run-results"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="运行结果"
      >
        <div class="section-head">
          <p class="kicker">RESULTS</p>
          <h2>运行结果：RGB 与语义分割样本已经成对生成</h2>
        </div>
        <p class="lesson-cue">
          下面展示的是一次完整运行后得到的样本片段。每组样本使用同一个 frame 文件名，
          左侧为 RGB 图像，右侧为对应的语义分割图像。
        </p>
        <div class="lesson-result-grid">
          <article class="lesson-result-card" v-for="sample in exp02ResultSamples" :key="sample.frame">
            <h3>{{ sample.title }}</h3>
            <p>frame = {{ sample.frame }}</p>
            <div class="lesson-result-images">
              <figure>
                <img :src="sample.rgb" :alt="`${sample.title} 的 RGB 图像`" loading="lazy" />
                <figcaption>RGB</figcaption>
              </figure>
              <figure>
                <img :src="sample.seg" :alt="`${sample.title} 的语义分割图像`" loading="lazy" />
                <figcaption>Semantic Segmentation</figcaption>
              </figure>
            </div>
          </article>
        </div>
        <div class="command-layout lesson-card-grid">
          <article class="command-card" v-for="item in exp02ResultStats" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
          <article class="command-card lesson-highlight-card">
            <h3>结果文件下载</h3>
            <p>下载完整 exp02 结果包，压缩包包含 rgb/ 与 seg/ 两个目录，可直接用于复查和后续分析。</p>
            <a class="lesson-download-link" :href="exp02OutputZipHref" download="ch03_exp02_run_results.zip">
              下载 ch03_exp02_run_results.zip（约 5.7 MB，含 7 对抽样 RGB+Seg、对齐报告）
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
          <article class="command-card" v-for="item in chapter03Resources" :key="item.title">
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
            <a class="lesson-link" :href="chapterAllCodeHref" download="carla_ch03_all_examples.py">
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
          <h2>第三章的重点，是第一次真正理解“数据配对”</h2>
        </div>
        <div class="concept-grid lesson-quad-grid">
          <article class="concept-card">
            <h3>知识主线</h3>
            <p>同步模式决定节奏，双监听负责接图，同帧等待负责对齐，间隔采样负责效果。</p>
          </article>
          <article class="concept-card">
            <h3>代码主线</h3>
            <p>完整实验已经拆成 10 个代码段，按顺序理解后再合并成完整脚本。</p>
          </article>
          <article class="concept-card">
            <h3>实验主线</h3>
            <p>最终交付应同时包括图像、参数说明、对齐报告和实验分析，不再只是单纯截图。</p>
          </article>
          <article class="concept-card">
            <h3>课程价值</h3>
            <p>这一章把“会调 API”推进到“会组织一套最小可用视觉数据集”。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：双通道采集的核心不是“多挂一个相机”，而是“证明两路数据属于同一帧”。</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">命令已复制</div>
  </div>
</template>

