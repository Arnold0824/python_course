<script setup>
import { ref } from "vue";
import LessonOutlineSidebar from "../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);
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
        <span class="brand-tag">Chapter 3</span>
        <strong>运算符与控制流程</strong>
      </a>
      <nav class="nav-links" aria-label="页面目录">
        <a href="#cover">章节封面</a>
        <a href="#what-you-learn">学什么</a>
        <a href="#what-you-build">能做什么</a>
      </nav>
    </header>

    <main id="top" class="page is-slide-deck">
      <section
        id="cover"
        class="hero reveal"
        data-outline-level="1"
        data-outline-label="章节封面"
      >
        <p class="kicker">CHAPTER 03 PREVIEW</p>
        <h1>运算符与控制流程</h1>
        <p class="hero-intro">
          这一章会把“会写语句”升级为“会写逻辑”。从表达式计算到条件判断与循环，让程序可以根据输入自动做决定。
        </p>
        <div class="goal-cards">
          <article>
            <h2>知识主线</h2>
            <p>算术、比较、逻辑、赋值、成员与身份运算符。</p>
          </article>
          <article>
            <h2>核心结构</h2>
            <p>if / elif / else、for、while、break、continue。</p>
          </article>
          <article>
            <h2>章节目标</h2>
            <p>写出可判断、可循环、可调试的小程序流程。</p>
          </article>
        </div>
      </section>

      <section
        id="what-you-learn"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="学什么"
      >
        <div class="section-head">
          <p class="kicker">WHAT YOU WILL LEARN</p>
          <h2>你将掌握的关键知识</h2>
        </div>
        <div class="concept-grid">
          <article class="concept-card">
            <h3>运算符组合</h3>
            <p>理解表达式执行顺序，学会用括号和优先级写出可预期结果。</p>
          </article>
          <article class="concept-card">
            <h3>条件分支</h3>
            <p>把“如果…那么…”规则写成 if/elif/else，让代码能做选择。</p>
          </article>
          <article class="concept-card">
            <h3>循环控制</h3>
            <p>用 for/while 实现重复任务，并通过 break/continue 精细控制流程。</p>
          </article>
          <article class="concept-card">
            <h3>流程调试</h3>
            <p>借助 print 与断点定位逻辑分支错误，快速修复控制流程问题。</p>
          </article>
        </div>
      </section>

      <section
        id="what-you-build"
        class="section reveal summary"
        data-outline-level="1"
        data-outline-label="能做什么"
      >
        <div class="section-head">
          <p class="kicker">WHAT YOU CAN BUILD</p>
          <h2>学完后你可以完成的程序</h2>
        </div>
        <div class="flow">
          <span>成绩评级器</span>
          <span>猜数字游戏</span>
          <span>菜单循环程序</span>
          <span>简单回合战斗</span>
        </div>
        <pre class="final-snippet"><code class="python">score = int(input("score: "))
if score &gt;= 90:
    level = "A"
elif score &gt;= 75:
    level = "B"
else:
    level = "C"
print("level:", level)</code></pre>
        <p class="section-note">
          这就是本章目标：把现实规则翻译成程序流程，让程序按条件自动运行。
        </p>
      </section>
    </main>

    <footer class="footer">
      <p>Chapter 3 当前为封面预览版，后续会补充完整课件内容。</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">命令已复制</div>
  </div>
</template>
