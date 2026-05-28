<script setup>
import { ref } from 'vue'
import CourseSwitcher from '../../../components/CourseSwitcher.vue'
import LessonOutlineSidebar from '../../../components/LessonOutlineSidebar.vue'
import { useLessonDeck } from '../../../composables/useLessonDeck'
import {
  chapter10BoundaryRows,
  chapter10ConceptCards,
  chapter10Docs,
  chapter10Pitfalls,
  chapter10PromptExamples,
  chapter10ReviewChecklist,
  chapter10SafetyRules,
  chapter10StudentRoute,
  chapter10SummaryCards,
  chapter10ToolCards,
  chapter10WorkflowPhases,
  chapter10WorkflowUnits,
} from '../chapter10Content.js'

const rootRef = ref(null)
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef)

const learningGoals = [
  '能把模糊想法写成 AI 能理解、自己能验证的编程需求。',
  '能阅读和修改 AI 生成的 Python 代码，而不是直接粘贴。',
  '能用运行结果、错误信息和检查清单判断代码是否可靠。',
]

const chapterMetrics = [
  { value: '7', label: '协作步骤' },
  { value: '6', label: '常用工具' },
  { value: '8', label: '审查要点' },
]
</script>

<template>
  <div ref="rootRef" class="course-page chapter-ten-page">
    <div class="bg-grid" aria-hidden="true"></div>

    <div class="progress-track" aria-hidden="true">
      <span id="scrollProgress"></span>
    </div>

    <header class="top-nav">
      <a class="brand" href="#top">
        <span class="brand-tag">Chapter 10</span>
        <strong>AI 协作编程</strong>
      </a>
      <CourseSwitcher />
    </header>

    <main id="top" class="page is-slide-deck">
      <section id="cover" class="hero reveal" data-outline-level="1" data-outline-label="章节封面">
        <div class="slide-card-body">
          <div class="lesson-hero-grid">
            <div class="lesson-hero-copy">
              <p class="kicker">CHAPTER 10 AI-ASSISTED PYTHON CODING</p>
              <h1>第十章 AI 协作编程</h1>
              <p class="hero-intro">
                AI 可以帮你解释代码、生成草稿、定位错误和整理思路，但它不能替你理解程序。
                本章学习如何把自然语言需求变成可运行的 Python 代码，并用检查和验证保证结果可信。
              </p>
              <ul class="hero-checklist">
                <li>先学会提出清楚需求，再让 AI 参与写代码。</li>
                <li>把 AI 生成的代码当作草稿，必须阅读、运行、检查和修改。</li>
                <li>任何结果都要能解释、能复查、能保护数据隐私。</li>
              </ul>
              <RouterLink class="chapter-ten-idea-entry" to="/python/ideas?chapter=10">
                进入匿名想法墙
              </RouterLink>
            </div>
            <aside class="lesson-hero-panel">
              <span class="lesson-panel-label">本章关注的不是复制答案，而是协作流程</span>
              <div class="lesson-metric" v-for="metric in chapterMetrics" :key="metric.label">
                <strong>{{ metric.value }}</strong>
                <span>{{ metric.label }}</span>
              </div>
            </aside>
          </div>
          <div class="goal-cards">
            <article v-for="goal in learningGoals" :key="goal">
              <h2>学习目标</h2>
              <p>{{ goal }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section reveal" data-outline-level="1" data-outline-label="核心概念">
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">CONCEPTS</p>
            <h2>AI 参与编程，但学生仍然是程序负责人</h2>
          </div>
          <p class="lesson-cue">
            这章里的“AI 协作”不是把作业交给 AI，而是把 AI 当作会给建议的编程伙伴。
            伙伴可以帮忙，但最终判断、修改、验证和解释都必须由你完成。
          </p>
          <div class="concept-grid lesson-quad-grid">
            <article class="concept-card" v-for="item in chapter10ConceptCards" :key="item.title">
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section reveal" data-outline-level="1" data-outline-label="常用工具">
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">TOOLS</p>
            <h2>常用 AI 编程工具，各自解决的问题不一样</h2>
          </div>
          <p class="lesson-cue">
            不同工具不是简单的“谁更强”。有的适合在编辑器里补代码，有的适合在终端里改项目，有的适合监督多个代理，有的负责管理模型和配置。
            选择工具前，先判断任务是小片段、单文件小游戏、完整项目、配置切换，还是长期维护。
          </p>
          <div class="chapter-ten-tool-grid">
            <article class="chapter-ten-tool-card" v-for="tool in chapter10ToolCards" :key="tool.name">
              <div class="chapter-ten-tool-head">
                <span>{{ tool.category }}</span>
                <h3>{{ tool.name }}</h3>
              </div>
              <dl class="chapter-ten-tool-list">
                <div>
                  <dt>主要作用</dt>
                  <dd>{{ tool.role }}</dd>
                </div>
                <div>
                  <dt>适合任务</dt>
                  <dd>{{ tool.bestFor }}</dd>
                </div>
                <div>
                  <dt>优势</dt>
                  <dd>{{ tool.strengths }}</dd>
                </div>
                <div>
                  <dt>注意</dt>
                  <dd>{{ tool.watchouts }}</dd>
                </div>
                <div>
                  <dt>课堂用法</dt>
                  <dd>{{ tool.classUse }}</dd>
                </div>
              </dl>
            </article>
          </div>
        </div>
      </section>

      <section class="section reveal" data-outline-level="1" data-outline-label="边界辨析">
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">BOUNDARY</p>
            <h2>先分清几种不同的“用 AI 写代码”</h2>
          </div>
          <div class="lesson-table-card">
            <table>
              <thead>
                <tr>
                  <th>方式</th>
                  <th>典型行为</th>
                  <th>学习价值与风险</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in chapter10BoundaryRows" :key="row.mode">
                  <td>{{ row.mode }}</td>
                  <td>{{ row.behavior }}</td>
                  <td>{{ row.value }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section class="section reveal" data-outline-level="1" data-outline-label="学习路线">
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">ROADMAP</p>
            <h2>从一句需求，到一段可靠代码</h2>
          </div>
          <div class="lesson-phase-track chapter-ten-phase-track">
            <article
              class="lesson-phase-card"
              v-for="phase in chapter10WorkflowPhases"
              :key="phase.no"
            >
              <span>{{ phase.no }}</span>
              <h3>{{ phase.title }}</h3>
              <p>{{ phase.text }}</p>
            </article>
          </div>
          <div class="lesson-step-list">
            <span v-for="step in chapter10StudentRoute" :key="step">{{ step }}</span>
          </div>
        </div>
      </section>

      <section
        v-for="unit in chapter10WorkflowUnits"
        :id="`unit-${unit.no}`"
        :key="unit.no"
        class="section reveal lesson-code-page"
        data-outline-level="1"
        :data-outline-label="unit.label"
      >
        <div class="slide-card-body">
          <div class="lesson-slide-layout">
            <div class="lesson-slide-notes">
              <div class="section-head">
                <p class="kicker">UNIT {{ unit.no }}</p>
                <h2>{{ unit.title }}</h2>
              </div>
              <p class="lesson-cue">{{ unit.lead }}</p>
              <div class="lesson-teach-stack">
                <article class="command-card lesson-teach-card">
                  <h3>这一部分在学什么</h3>
                  <p>{{ unit.explain }}</p>
                </article>
                <article class="command-card lesson-teach-card">
                  <h3>为什么重要</h3>
                  <p>{{ unit.why }}</p>
                </article>
                <article class="command-card lesson-teach-card">
                  <h3>课堂动作</h3>
                  <ul class="lesson-points">
                    <li v-for="action in unit.actions" :key="action">{{ action }}</li>
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

            <pre><code class="language-text">{{ unit.prompt }}</code></pre>
          </div>
        </div>
      </section>

      <section class="section reveal" data-outline-level="1" data-outline-label="提示词对照">
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">PROMPT PATTERNS</p>
            <h2>好的提示词，会让 AI 少猜一点，让你多掌控一点</h2>
          </div>
          <p class="lesson-cue">
            提示词不是越长越好，而是要把任务关键条件说完整。下面每组都可以直接对照自己的提问方式。
          </p>
          <div class="chapter-ten-prompt-grid">
            <article
              class="chapter-ten-prompt-card"
              v-for="example in chapter10PromptExamples"
              :key="example.title"
            >
              <h3>{{ example.title }}</h3>
              <div class="chapter-ten-prompt-block is-weak">
                <strong>不推荐</strong>
                <p>{{ example.bad }}</p>
              </div>
              <div class="chapter-ten-prompt-block is-strong">
                <strong>更好的问法</strong>
                <p>{{ example.good }}</p>
              </div>
              <p class="chapter-ten-prompt-reason">{{ example.reason }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section reveal" data-outline-level="1" data-outline-label="代码审查">
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">REVIEW CHECKLIST</p>
            <h2>AI 代码提交前，至少过一遍这张检查表</h2>
          </div>
          <div class="lesson-table-card">
            <table>
              <thead>
                <tr>
                  <th>检查项</th>
                  <th>应该确认什么</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in chapter10ReviewChecklist" :key="row.item">
                  <td>{{ row.item }}</td>
                  <td>{{ row.check }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section class="section reveal" data-outline-level="1" data-outline-label="常见误区">
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">PITFALLS</p>
            <h2>用 AI 写 Python 时，最常见的问题在这里</h2>
          </div>
          <div class="concept-grid lesson-quad-grid">
            <article class="concept-card" v-for="item in chapter10Pitfalls" :key="item.title">
              <h3>{{ item.title }}</h3>
              <p>{{ item.problem }}</p>
              <p>{{ item.fix }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section reveal" data-outline-level="1" data-outline-label="安全边界">
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">SAFETY</p>
            <h2>AI 编程也要守住数据和电脑安全边界</h2>
          </div>
          <div class="command-layout lesson-link-grid">
            <article class="command-card" v-for="rule in chapter10SafetyRules" :key="rule.title">
              <h3>{{ rule.title }}</h3>
              <p>{{ rule.text }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section reveal" data-outline-level="1" data-outline-label="文档入口">
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">REFERENCES</p>
            <h2>遇到关键问题，要回到可靠资料确认</h2>
          </div>
          <p class="lesson-cue">
            AI 可以帮你解释文档，但关键函数、参数和错误类型要学会查可靠资料。
            课堂代码、官方文档和真实运行结果，比一句看起来流畅的回答更可靠。
          </p>
          <div class="command-layout lesson-link-grid">
            <article class="command-card" v-for="doc in chapter10Docs" :key="doc.href">
              <h3>{{ doc.title }}</h3>
              <p>{{ doc.text }}</p>
              <a class="lesson-link" :href="doc.href" target="_blank" rel="noopener noreferrer">
                {{ doc.href }}
              </a>
            </article>
          </div>
        </div>
      </section>

      <section
        id="summary"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章总结"
      >
        <div class="slide-card-body">
          <div class="section-head">
            <p class="kicker">SUMMARY</p>
            <h2>第十章的重点，是让 AI 成为可控的编程助手</h2>
          </div>
          <div class="concept-grid lesson-quad-grid">
            <article class="concept-card" v-for="item in chapter10SummaryCards" :key="item.title">
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课程关键句：AI 可以帮你写代码，但不能替你理解、验证和负责。</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">代码已复制</div>
  </div>
</template>

<style scoped>
.chapter-ten-page :deep(.lesson-phase-track.chapter-ten-phase-track) {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.chapter-ten-prompt-grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.chapter-ten-idea-entry {
  display: inline-flex;
  width: fit-content;
  margin-top: 18px;
  border-radius: 12px;
  background: #0f6ac5;
  color: #ffffff;
  font-weight: 900;
  padding: 10px 16px;
  text-decoration: none;
  transition: background 0.18s ease, transform 0.12s ease;
}

.chapter-ten-idea-entry:hover {
  background: #0b5aab;
}

.chapter-ten-idea-entry:active {
  transform: translateY(1px);
}

.chapter-ten-tool-grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.chapter-ten-tool-card {
  min-width: 0;
  padding: 16px;
  border-radius: 16px;
  border: 1px solid rgba(15, 106, 197, 0.15);
  background: rgba(255, 255, 255, 0.96);
  display: grid;
  gap: 12px;
}

.chapter-ten-tool-head {
  display: grid;
  gap: 5px;
}

.chapter-ten-tool-head span {
  width: fit-content;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(15, 106, 197, 0.1);
  color: #0f5fa7;
  font-size: 0.76rem;
  font-weight: 800;
}

.chapter-ten-tool-head h3 {
  color: #173b58;
  font-size: 1.18rem;
}

.chapter-ten-tool-list {
  margin: 0;
  display: grid;
  gap: 8px;
}

.chapter-ten-tool-list div {
  display: grid;
  gap: 3px;
}

.chapter-ten-tool-list dt {
  color: #0f6ac5;
  font-size: 0.82rem;
  font-weight: 900;
}

.chapter-ten-tool-list dd {
  margin: 0;
  color: #3f5f78;
  line-height: 1.6;
}

.chapter-ten-prompt-card {
  min-width: 0;
  padding: 16px;
  border-radius: 16px;
  border: 1px solid rgba(15, 106, 197, 0.15);
  background: rgba(255, 255, 255, 0.96);
  display: grid;
  gap: 10px;
}

.chapter-ten-prompt-card h3 {
  color: #173b58;
  font-size: 1.08rem;
}

.chapter-ten-prompt-block {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(100, 116, 139, 0.18);
  display: grid;
  gap: 5px;
}

.chapter-ten-prompt-block strong {
  font-size: 0.82rem;
  color: #173b58;
}

.chapter-ten-prompt-block p,
.chapter-ten-prompt-reason {
  margin: 0;
  color: #3f5f78;
  line-height: 1.62;
}

.chapter-ten-prompt-block.is-weak {
  border-left: 4px solid rgba(214, 53, 53, 0.7);
  background: rgba(254, 242, 242, 0.72);
}

.chapter-ten-prompt-block.is-strong {
  border-left: 4px solid rgba(15, 118, 110, 0.7);
  background: rgba(236, 253, 245, 0.78);
}

.chapter-ten-prompt-reason {
  padding-top: 2px;
  font-size: 0.92rem;
}

@media (max-width: 900px) {
  .chapter-ten-page :deep(.lesson-phase-track.chapter-ten-phase-track),
  .chapter-ten-tool-grid,
  .chapter-ten-prompt-grid {
    grid-template-columns: 1fr;
  }
}
</style>
