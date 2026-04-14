<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";
import {
  chapter04AlignmentCards,
  chapter04Docs,
  chapter04Pitfalls,
  chapter04Resources,
  chapter04Slides,
} from "../chapter04Content.js";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const chapterAllCodeHref = "/courses/carla/ch04/carla_ch04_all_examples.py";

const learningGoals = [
  "能说明双通道采集为什么必须做同帧对齐，而不是各自保存图片。",
  "能独立写出同步模式、双监听、同帧等待、间隔采样和资源清理这条主线。",
  "能根据网页代码页顺序，自己搭出一份可运行的 RGB 与语义分割配对采集脚本。",
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
        <p class="kicker">DUAL-CHANNEL CAPTURE AND ALIGNMENT</p>
        <h1>第三章 RGB 与语义分割双通道采集对齐</h1>
        <p class="hero-intro">
          这一章不再停留在“能采到图”，而是正式进入“能采到一对严格对应的数据”。
          页面按代码段拆成独立讲授页，学生只要顺着网页从上到下阅读，就能理解每一步为什么写、解决什么问题、最后如何拼成完整实验。
        </p>
        <ul class="hero-checklist">
          <li>每个代码段单独成页，目录导航可以直接跳转到对应知识点。</li>
          <li>每一页都回答 3 个问题：这一段做什么、为什么这样写、学生最该记住什么。</li>
          <li>整章最终目标是产出 30 对会变化、可核验、可复现的 RGB 与语义分割样本。</li>
        </ul>
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
        <div class="chapter-four-rhythm">
          <span>参数锁定</span>
          <span>同步模式</span>
          <span>双相机对齐</span>
          <span>自动驾驶采样</span>
        </div>
        <div class="command-layout chapter-four-card-grid">
          <article class="command-card" v-for="step in workflowSteps" :key="step">
            <h3>教学步骤</h3>
            <p>{{ step }}</p>
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
          <h2>这一章真正需要反复查阅的官方入口</h2>
        </div>
        <div class="command-layout chapter-four-link-grid">
          <article class="command-card" v-for="doc in chapter04Docs" :key="doc.href">
            <h3>{{ doc.title }}</h3>
            <p>{{ doc.text }}</p>
            <a
              class="chapter-four-link"
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
          <h2>学生首先要建立的不是 API 记忆，而是对齐意识</h2>
        </div>
        <p class="chapter-four-cue">
          RGB 图像提供视觉外观，语义分割图像提供像素级标签。只有当两路数据来自同一辆车、同一位姿、同一套成像参数、同一帧号时，
          它们才是可以直接配对使用的数据对。
        </p>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card" v-for="item in chapter04AlignmentCards" :key="item.title">
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
          <h2>这一章建议学生从一开始就按“最小数据集”思维组织结果</h2>
        </div>
        <div class="command-layout chapter-four-2plus1">
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
        v-for="slide in chapter04Slides"
        :id="`slide-${slide.no}`"
        :key="slide.no"
        class="section reveal chapter-four-code-page"
        data-outline-level="1"
        :data-outline-label="slide.outline"
      >
        <div class="section-head">
          <p class="kicker">CODE SLIDE {{ slide.no }}</p>
          <h2>{{ slide.title }}</h2>
        </div>
        <p class="chapter-four-cue">{{ slide.lead }}</p>

        <div class="chapter-four-code-shell">
          <div class="chapter-four-code-meta">
            <span>代码讲授页</span>
            <span>{{ slide.outline }}</span>
            <span>建议课堂单独讲解</span>
          </div>
          <pre><code class="python">{{ slide.code }}</code></pre>
        </div>

        <div class="command-layout chapter-four-teach-grid">
          <article class="command-card chapter-four-teach-card">
            <h3>这一段在做什么</h3>
            <p>{{ slide.explain }}</p>
          </article>
          <article class="command-card chapter-four-teach-card">
            <h3>为什么这样写</h3>
            <p>{{ slide.why }}</p>
          </article>
          <article class="command-card chapter-four-teach-card">
            <h3>这一页最该记住</h3>
            <ul class="chapter-four-points">
              <li v-for="point in slide.points" :key="point">{{ point }}</li>
            </ul>
          </article>
        </div>

        <div class="concept-grid chapter-four-terms-grid">
          <article class="concept-card" v-for="term in slide.terms" :key="term.title">
            <h3>{{ term.title }}</h3>
            <p>{{ term.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="常见误区"
      >
        <div class="section-head">
          <p class="kicker">PITFALLS</p>
          <h2>把这几个坑讲清楚，学生就不容易把实验做成“只是能跑”</h2>
        </div>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card" v-for="item in chapter04Pitfalls" :key="item.title">
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
        <div class="command-layout chapter-four-card-grid">
          <article class="command-card">
            <h3>实验目标</h3>
            <p>在同步模式下，让主车自动驾驶并完成 RGB 与语义分割双通道采集对齐。</p>
          </article>
          <article class="command-card">
            <h3>最低成果</h3>
            <p>输出不少于 30 对双通道图像，并附带参数记录和对齐报告。</p>
          </article>
          <article class="command-card">
            <h3>课堂效果要求</h3>
            <p>车辆应持续移动，样本之间应有明显变化，不要出现 30 帧几乎一样的情况。</p>
          </article>
          <article class="command-card">
            <h3>工程要求</h3>
            <p>实验结束要恢复 world settings、关闭自动驾驶、停止并销毁传感器。</p>
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
        <div class="command-layout chapter-four-link-grid">
          <article class="command-card" v-for="item in chapter04Resources" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
            <a
              class="chapter-four-link"
              :href="item.href"
              :download="item.download || null"
              :target="isExternalLink(item.href) ? '_blank' : null"
              :rel="isExternalLink(item.href) ? 'noopener noreferrer' : null"
            >
              {{ item.href }}
            </a>
          </article>
          <article class="command-card chapter-four-highlight-card">
            <h3>整章总代码直达</h3>
            <p>如果学生已经完成逐页学习，可以直接下载整章脚本，对照网页把所有代码段重新串起来。</p>
            <a class="chapter-four-link" :href="chapterAllCodeHref" download="carla_ch04_all_examples.py">
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
          <h2>第三章的教学重心，是让学生第一次真正理解“数据配对”</h2>
        </div>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card">
            <h3>知识主线</h3>
            <p>同步模式决定节奏，双监听负责接图，同帧等待负责对齐，间隔采样负责效果。</p>
          </article>
          <article class="concept-card">
            <h3>代码主线</h3>
            <p>网页已经把完整实验拆成 10 个代码讲授页，学生可以逐页理解后再合并成完整脚本。</p>
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

<style scoped>
.page.is-slide-deck .chapter-four-rhythm {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.page.is-slide-deck .chapter-four-rhythm span {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(11, 98, 179, 0.2);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.95), rgba(245, 251, 255, 0.98));
  color: #0a5eaf;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
}

.page.is-slide-deck .chapter-four-cue {
  margin: 10px 0 0;
  padding: 12px 14px;
  border-left: 4px solid rgba(11, 98, 179, 0.42);
  border-radius: 12px;
  background: rgba(11, 98, 179, 0.06);
  color: var(--text-main);
  font-size: 0.96rem;
  line-height: 1.72;
}

.page.is-slide-deck .command-layout.chapter-four-card-grid,
.page.is-slide-deck .command-layout.chapter-four-link-grid,
.page.is-slide-deck .command-layout.chapter-four-teach-grid,
.page.is-slide-deck .command-layout.chapter-four-2plus1 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .command-layout.chapter-four-2plus1 > :last-child {
  grid-column: 1 / -1;
}

.page.is-slide-deck .concept-grid.chapter-four-quad-grid,
.page.is-slide-deck .concept-grid.chapter-four-terms-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .chapter-four-code-page {
  scroll-margin-top: 92px;
}

.page.is-slide-deck .chapter-four-code-shell {
  margin-top: 18px;
  border: 1px solid rgba(11, 98, 179, 0.16);
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(8, 16, 29, 0.97), rgba(14, 28, 48, 0.98));
  overflow: hidden;
  box-shadow: 0 20px 34px rgba(7, 25, 52, 0.14);
}

.page.is-slide-deck .chapter-four-code-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px 14px;
  border-bottom: 1px solid rgba(130, 170, 220, 0.2);
  background: rgba(117, 165, 222, 0.08);
}

.page.is-slide-deck .chapter-four-code-meta span {
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(218, 234, 252, 0.12);
  color: #cbe3ff;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.page.is-slide-deck .chapter-four-code-shell pre {
  margin: 0;
  padding: 18px;
  overflow-x: auto;
}

.page.is-slide-deck .chapter-four-code-shell code {
  color: #f4f8ff;
  line-height: 1.75;
}

.page.is-slide-deck .chapter-four-teach-card p {
  line-height: 1.72;
}

.page.is-slide-deck .chapter-four-points {
  margin: 0;
  padding-left: 18px;
  line-height: 1.72;
}

.page.is-slide-deck .chapter-four-points li + li {
  margin-top: 8px;
}

.page.is-slide-deck .chapter-four-link {
  display: block;
  margin-top: 10px;
  color: #0a5eaf;
  font-weight: 700;
  text-decoration: underline;
  word-break: break-all;
}

.page.is-slide-deck .chapter-four-highlight-card {
  grid-column: 1 / -1;
  border: 1px solid rgba(11, 98, 179, 0.26);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.96), rgba(248, 252, 255, 0.98));
  box-shadow: 0 16px 30px rgba(11, 98, 179, 0.08);
}

@media (max-width: 900px) {
  .page.is-slide-deck .chapter-four-rhythm,
  .page.is-slide-deck .command-layout.chapter-four-card-grid,
  .page.is-slide-deck .command-layout.chapter-four-link-grid,
  .page.is-slide-deck .command-layout.chapter-four-teach-grid,
  .page.is-slide-deck .command-layout.chapter-four-2plus1,
  .page.is-slide-deck .concept-grid.chapter-four-quad-grid,
  .page.is-slide-deck .concept-grid.chapter-four-terms-grid {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .command-layout.chapter-four-2plus1 > :last-child,
  .page.is-slide-deck .chapter-four-highlight-card {
    grid-column: span 1;
  }
}
</style>
