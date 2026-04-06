<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);
const missionLogHref = "/courses/python/ch06/mission_log.txt";
const exp3ReportHref = encodeURI(
  "/courses/python/exp_reports/实验报告3：词云展示2022年政府工作报告关键词（理实课程实验部分）-学生姓名.docx",
);
const exp3SubmitHref = "https://f.wps.cn/g/4WJfPt8S/";
const exp3TextHref = encodeURI("/courses/python/ch06/2022年政府工作报告.txt");
const jiebaMemeSrc = encodeURI("/courses/python/ch06/jieba-danding-dingzhen-meme.jpg");
const wordcloudMaskDemoHref = encodeURI("/courses/python/ch06/wordcloud_mask_demo.py");
const wordcloudStopwordsHref = encodeURI("/courses/python/ch06/stopwords_basic.txt");
const wordcloudMaskSourcesHref = encodeURI("/courses/python/ch06/mask_sources.txt");
const wordcloudMaskCards = [
  {
    title: "云朵 mask",
    imageSrc: encodeURI("/courses/python/ch06/mask_cloud.png"),
    downloadHref: encodeURI("/courses/python/ch06/mask_cloud.png"),
    desc: "留白大、轮廓明显，适合课程反馈、班级总结这类主题。",
  },
  {
    title: "星形 mask",
    imageSrc: encodeURI("/courses/python/ch06/mask_star.png"),
    downloadHref: encodeURI("/courses/python/ch06/mask_star.png"),
    desc: "适合人工智能、比赛、目标、成就这类关键词比较集中的文本。",
  },
  {
    title: "叶片 mask",
    imageSrc: encodeURI("/courses/python/ch06/mask_leaf.png"),
    downloadHref: encodeURI("/courses/python/ch06/mask_leaf.png"),
    desc: "适合校园生活、环保活动、春季主题、自然观察这类内容。",
  },
  {
    title: "书本 mask",
    imageSrc: encodeURI("/courses/python/ch06/mask_book.png"),
    downloadHref: encodeURI("/courses/python/ch06/mask_book.png"),
    desc: "适合阅读笔记、文学作品、课程总结、读书报告等文本。",
  },
];
const wordcloudTextCards = [
  {
    title: "课程反馈文本",
    downloadHref: encodeURI("/courses/python/ch06/text_course_feedback.txt"),
    desc: "适合练习课程评价词云，关键词集中在课程、模块、练习、案例。",
  },
  {
    title: "人工智能主题文本",
    downloadHref: encodeURI("/courses/python/ch06/text_ai_topics.txt"),
    desc: "适合练习主题词云，关键词集中在数据、模型、训练、算法。",
  },
  {
    title: "校园生活文本",
    downloadHref: encodeURI("/courses/python/ch06/text_campus_life.txt"),
    desc: "适合练习校园活动词云，关键词集中在图书馆、自习、比赛、社团。",
  },
  {
    title: "阅读笔记文本",
    downloadHref: encodeURI("/courses/python/ch06/text_reading_notes.txt"),
    desc: "适合练习读书报告词云，关键词集中在人物、主题、情节、表达。",
  },
  {
    title: "但丁丁真梗图文本",
    downloadHref: encodeURI("/courses/python/ch06/text_dingzhen_meme.txt"),
    desc: "适合先做分词，再观察歧义文本进入词云后的结果。",
  },
];
const wordcloudDemoCards = [
  {
    title: "云朵课程反馈词云",
    imageSrc: encodeURI("/courses/python/ch06/demo_wordcloud_cloud.png"),
    downloadHref: encodeURI("/courses/python/ch06/demo_wordcloud_cloud.png"),
  },
  {
    title: "星形人工智能词云",
    imageSrc: encodeURI("/courses/python/ch06/demo_wordcloud_star.png"),
    downloadHref: encodeURI("/courses/python/ch06/demo_wordcloud_star.png"),
  },
  {
    title: "叶片校园生活词云",
    imageSrc: encodeURI("/courses/python/ch06/demo_wordcloud_leaf.png"),
    downloadHref: encodeURI("/courses/python/ch06/demo_wordcloud_leaf.png"),
  },
  {
    title: "书本阅读笔记词云",
    imageSrc: encodeURI("/courses/python/ch06/demo_wordcloud_book.png"),
    downloadHref: encodeURI("/courses/python/ch06/demo_wordcloud_book.png"),
  },
];
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
        <span class="brand-tag">Chapter 6</span>
        <strong>文件操作与模块</strong>
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
        <p class="kicker">CHAPTER 06 FILES AND MODULES</p>
        <h1>文件操作与模块<br />让程序能够保存、拆分和扩展</h1>
        <p class="hero-intro">
          前五章解决的是“程序能不能跑起来”。到了第六章，重点变成另外两件事：程序如何把结果留下来，
          程序如何把功能拆开并重复使用。文件操作负责保存数据，模块负责组织代码，
          而模块库会把程序从“会写”推进到“会用工具写”。
        </p>
        <ul class="hero-checklist">
          <li>掌握文本文件的读取、写入、追加、路径与编码，避免“程序能算但保存不下来”。</li>
          <li>掌握模块的创建与导入，能分清 <code>import</code>、<code>import as</code>、<code>from import</code> 的差异。</li>
          <li>逐步学会内置模块与外置模块，形成“遇到任务先想有没有现成工具”的编程习惯。</li>
        </ul>
        <div class="goal-cards fly-in-seq">
          <article>
            <h2>能力目标 1</h2>
            <p>能把程序结果写入文件，并能再次读回进行处理。</p>
          </article>
          <article>
            <h2>能力目标 2</h2>
            <p>能把常用函数拆进模块，避免把整个程序挤在一个文件里。</p>
          </article>
          <article>
            <h2>能力目标 3</h2>
            <p>能调用常用模块解决数学、随机、时间、路径、文本分析和词云问题。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章路线"
      >
        <h2>本章路线：先保存数据，再组织代码，最后接入模块工具链</h2>
        <p class="section-note">
          整章按一条清晰主线推进：先解决“数据如何进出文件”，再解决“代码如何拆进模块”，
          最后把常用模块接进程序，形成一条真正能做事的开发链路。
        </p>
        <div class="chapter-six-rhythm chapter-six-rhythm--four">
          <span>文件是什么</span>
          <span>模块怎么拆</span>
          <span>内置模块怎么用</span>
          <span>外置模块怎么接进程序</span>
        </div>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>第一部分</h3>
            <p>文件操作：读取、写入、追加、路径、编码与异常现象。</p>
          </article>
          <article class="concept-card">
            <h3>第二部分</h3>
            <p>模块基础：创建模块、导入模块、起别名、按需导入、自测入口。</p>
          </article>
          <article class="concept-card">
            <h3>第三部分</h3>
            <p>内置模块：math、random、time、sys、os、turtle 逐步上难度。</p>
          </article>
          <article class="concept-card">
            <h3>第四部分</h3>
            <p>外置模块：faker、jieba、wordcloud，最终接成一个完整案例。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="为什么要学文件与模块"
      >
        <h2>为什么程序到这里必须学文件和模块</h2>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>没有文件</h3>
            <p>程序每次运行完，计算结果都会随着终端窗口一起消失。输入、输出和结果都无法留档，也就无法做后续分析。</p>
          </article>
          <article class="command-card">
            <h3>没有模块</h3>
            <p>所有函数都堆在一个文件里，程序一变长就难以定位功能、难以复用，也不利于多人协作。</p>
          </article>
          <article class="command-card">
            <h3>这一章真正解决的问题</h3>
            <p>把“程序算出来的结果”放进文件，把“程序里常用的功能”拆成模块，再借助模块库提升开发速度。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="文件操作"
      >
        <div class="section-head">
          <p class="kicker">FILES</p>
          <h2>文件操作：先让程序拥有“记忆”</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>先看本质。</strong> 文件不是 Python 独有概念，它是操作系统里真实存在的数据容器。
          Python 只是通过 <code>open()</code> 拿到一个文件对象，再通过这个对象完成读取、写入和关闭。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>文件路径</h3>
            <p>决定程序去哪里找文件，或者把文件保存到哪里。</p>
          </article>
          <article class="concept-card">
            <h3>打开模式</h3>
            <p><code>r</code> 读取，<code>w</code> 覆盖写入，<code>a</code> 追加写入。</p>
          </article>
          <article class="concept-card">
            <h3>编码</h3>
            <p>中文文本通常要显式写成 <code>encoding="utf-8"</code>，否则容易乱码。</p>
          </article>
          <article class="concept-card">
            <h3>关闭文件</h3>
            <p>打开后要关闭，最稳的写法是 <code>with open(...)</code>。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实操案例文件"
      >
        <h3>文件操作实操案例：先下载任务日志，再按步骤生成任务简报</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card chapter-six-highlight-card">
            <h3>案例文件下载</h3>
            <p>先下载这份 <code>mission_log.txt</code>，并把它放到当前代码文件同目录。后面的读取、拆分、统计、写入练习都围绕这一个文件展开。</p>
            <a class="chapter-six-link" :href="missionLogHref" download>
              下载案例文件：mission_log.txt
            </a>
          </article>
          <article class="command-card">
            <h3>渐进式实操顺序</h3>
            <p>先读取全部内容看清日志结构，再改成逐行读取，然后拆出时间、小队、事件三列，最后统计并写成任务简报。</p>
          </article>
          <article class="command-card">
            <h3>这一页的目标</h3>
            <p>让后面的文件操作不是在空文件名上练语法，而是在真实日志文件上一步一步完成完整流程。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="案例文件结构"
      >
        <h3>案例文件结构：先看懂一行日志里到底放了什么</h3>
        <pre><code class="text">08:00,侦察组,出发前往北门区域
08:12,侦察组,发现异常脚印
08:20,通信组,向指挥中心上报情况</code></pre>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>第 1 列：时间</h3>
            <p>表示事件发生的时间。读取后可以直接打印，也可以后续按时间排序或筛选。</p>
          </article>
          <article class="command-card">
            <h3>第 2 列：小队名称</h3>
            <p>这是后面统计的关键字段。要把每条记录对应到侦察组、通信组、突击组等具体小队上。</p>
          </article>
          <article class="command-card">
            <h3>第 3 列：事件内容</h3>
            <p>这是任务描述文本。前面的文件操作阶段先不做复杂分析，先把它作为日志内容完整保留。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="第一次读取文件"
      >
        <h3>第一次读取文件：先把整份任务日志完整读出来</h3>
        <pre><code class="python">file = open("mission_log.txt", "r", encoding="utf-8")
content = file.read()
print(content)
file.close()</code></pre>
        <p class="section-note">
          这一段先不做统计，只看清文件长什么样。把原始日志整体读出来，学生才能建立“文件里到底存着什么”的直觉。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="open 和 read"
      >
        <h3><code>open()</code> 和 <code>read()</code> 到底各做了什么</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3><code>open(...)</code></h3>
            <p>负责把一个真实文件接进程序，返回一个文件对象。后面的所有读写动作都要通过这个对象进行。</p>
          </article>
          <article class="command-card">
            <h3><code>read()</code></h3>
            <p>一次性把整个文件内容读成一个字符串。如果文件很大，就不适合直接用这种方式。</p>
          </article>
          <article class="command-card">
            <h3>为什么要显式写编码</h3>
            <p>因为课堂场景经常会读写中文内容。显式写出 <code>encoding="utf-8"</code>，能明显减少乱码和跨环境差异。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="逐行读取"
      >
        <h3>日志变长后，逐行读取更稳</h3>
        <div class="command-layout chapter-six-code-grid">
          <article class="command-card chapter-six-code-card">
            <h3><code>readline()</code></h3>
            <pre><code class="python">file = open("mission_log.txt", "r", encoding="utf-8")
line1 = file.readline()
line2 = file.readline()
print(line1.strip())
print(line2.strip())
file.close()</code></pre>
          </article>
          <article class="command-card chapter-six-code-card">
            <h3><code>readlines()</code></h3>
            <pre><code class="python">file = open("mission_log.txt", "r", encoding="utf-8")
lines = file.readlines()
for line in lines:
    print(line.strip())
file.close()</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>readline()</code> 适合按行推进，<code>readlines()</code> 适合先把所有行拿进列表再处理。
          二者都会保留换行符，所以实际显示时常配合 <code>strip()</code> 使用。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="with open"
      >
        <h3>更推荐的写法：<code>with open(...)</code></h3>
        <pre><code class="python">with open("mission_log.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())</code></pre>
        <p class="chapter-six-cue">
          <strong>这一页要记牢。</strong> 使用 <code>with</code> 后，即使中间出现异常，文件也会在代码块结束时自动关闭。
          这比手动 <code>close()</code> 更稳，也更符合工程写法。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="拆分日志字段"
      >
        <h3>读取之后，还要学会把一行日志拆成多个字段</h3>
        <pre><code class="python">with open("mission_log.txt", "r", encoding="utf-8") as file:
    for line in file:
        time_text, team, event = line.strip().split(",")
        print("时间：", time_text)
        print("小队：", team)
        print("事件：", event)
        print("-" * 20)</code></pre>
        <p class="section-note">
          这一页是文件操作真正变得“有用”的起点。日志不再只是整行字符串，而是可以拆成结构化字段，再进入统计和分析流程。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="写入文件"
      >
        <h3>写入文件：把任务结果写成一份真正能交付的简报</h3>
        <div class="command-layout chapter-six-code-grid">
          <article class="command-card chapter-six-code-card">
            <h3>覆盖写入 <code>w</code></h3>
            <pre><code class="python">with open("mission_report.txt", "w", encoding="utf-8") as file:
    file.write("任务简报\\n")
    file.write("任务状态：已完成\\n")</code></pre>
          </article>
          <article class="command-card chapter-six-code-card">
            <h3>追加写入 <code>a</code></h3>
            <pre><code class="python">with open("mission_report.txt", "a", encoding="utf-8") as file:
    file.write("任务总结：目标区域已清理\\n")
    file.write("建议：补充通信记录\\n")</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>w</code> 会清空原文件再写入，<code>a</code> 会从文件末尾继续追加。这个差别非常关键，真实项目里经常因为选错模式导致原数据被覆盖。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="文件操作进阶"
      >
        <h3>文件操作进阶：读取日志、统计小队次数，再输出简报</h3>
        <pre><code class="python">team_counts = {}

with open("mission_log.txt", "r", encoding="utf-8") as file:
    for line in file:
        _, team, _ = line.strip().split(",")
        team_counts[team] = team_counts.get(team, 0) + 1

with open("mission_report.txt", "w", encoding="utf-8") as file:
    file.write("任务小队统计\\n")
    for team, count in team_counts.items():
        file.write(f"{team}：{count} 条记录\\n")</code></pre>
        <p class="section-note">
          从这一页开始，文件不再只是“打印出来看看”，而是直接参与程序计算、统计和结果输出。
          这才是真正完整的数据流。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="文件常见错误"
      >
        <h3>文件操作最常见的三个问题</h3>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>路径写错</h3>
            <p><code>FileNotFoundError</code> 最常见。文件不在当前目录，或文件名拼错。</p>
          </article>
          <article class="concept-card">
            <h3>模式选错</h3>
            <p>把 <code>w</code> 当成追加模式使用，会把原文件内容清空。</p>
          </article>
          <article class="concept-card">
            <h3>编码没写</h3>
            <p>中文文本读取和写入容易乱码，尤其在不同电脑之间移动文件时更明显。</p>
          </article>
          <article class="concept-card">
            <h3>忘了处理换行</h3>
            <p>逐行读取时，很多字符串末尾都带着 <code>\n</code>，需要 <code>strip()</code>。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="文件练习"
      >
        <h3>课堂练习：根据任务日志生成一份小队统计简报</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>任务要求</h3>
            <p>读取 <code>mission_log.txt</code>，把每一行拆成“时间、小队、事件”三个字段，然后统计每个小队一共出现了多少次，最后把结果写到 <code>mission_report.txt</code>。</p>
          </article>
          <article class="command-card">
            <h3>建议操作顺序</h3>
            <ol>
              <li>先写 <code>with open(..., "r")</code>，逐行读取日志。</li>
              <li>对每一行使用 <code>strip()</code> 去掉换行。</li>
              <li>再用 <code>split(",")</code> 拆出三个字段。</li>
              <li>准备一个字典，用 <code>dict.get()</code> 统计小队次数。</li>
              <li>最后再打开 <code>mission_report.txt</code>，把统计结果逐行写进去。</li>
            </ol>
          </article>
          <article class="command-card">
            <h3>关键提示</h3>
            <p>这一题的关键不是算法难度，而是把“读取文件 -> 拆分字段 -> 统计 -> 再写入文件”四个动作真正串起来。</p>
            <p>建议先在终端里 <code>print(team)</code> 看看拆分是否成功，再开始写统计代码。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="文件练习答案"
      >
        <h3>文件练习参考答案：任务日志生成小队统计简报</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">team_counts = {}

with open("mission_log.txt", "r", encoding="utf-8") as file:
    for line in file:
        time_text, team, event = line.strip().split(",")
        team_counts[team] = team_counts.get(team, 0) + 1

with open("mission_report.txt", "w", encoding="utf-8") as file:
    file.write("任务小队统计\\n")
    for team, count in team_counts.items():
        file.write(f"{team}：{count} 条记录\\n")</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="模块基础"
      >
        <div class="section-head">
          <p class="kicker">MODULES</p>
          <h2>模块基础：把代码从“一个大文件”拆成“多个功能块”</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>模块的核心价值不是语法，而是组织。</strong> 当某一组函数会反复使用，
          或者某一个文件已经开始过长时，就应该考虑把它们拆成独立模块。
        </p>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>模块是什么</h3>
            <p>本质上就是一个 <code>.py</code> 文件，只不过这个文件里保存的是可以被其他程序导入和复用的代码。</p>
          </article>
          <article class="command-card">
            <h3>模块解决什么问题</h3>
            <p>减少重复、拆分职责、提高可维护性，让“成绩分析”“路径处理”“词云生成”各自待在自己的文件里。</p>
          </article>
          <article class="command-card">
            <h3>这一部分要掌握什么</h3>
            <p>创建模块、导入模块、起别名、按需导入，以及如何让模块既能被导入又能自己测试。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="创建模块"
      >
        <h3>自己创建第一个模块</h3>
        <div class="command-layout chapter-six-code-grid">
          <article class="command-card chapter-six-code-card">
            <h3><code>my_tools.py</code></h3>
            <pre><code class="python">def add(a, b):
    return a + b


def average(numbers):
    return sum(numbers) / len(numbers)</code></pre>
          </article>
          <article class="command-card chapter-six-code-card">
            <h3><code>main.py</code></h3>
            <pre><code class="python">import my_tools

print(my_tools.add(3, 5))
print(my_tools.average([80, 92, 88]))</code></pre>
          </article>
        </div>
        <p class="section-note">
          模块的第一层理解就是：把几个常用函数放进另一个 <code>.py</code> 文件里，再在主程序中导入使用。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="import"
      >
        <h3><code>import</code>：导入整个模块</h3>
        <pre><code class="python">import my_tools

result = my_tools.add(10, 20)
print(result)</code></pre>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>优点</h3>
            <p>调用时会带上模块名，代码来源清楚，适合模块内容较多的情况。</p>
          </article>
          <article class="command-card">
            <h3>书写方式</h3>
            <p>使用时必须写成 <code>模块名.函数名</code>，例如 <code>my_tools.add()</code>。</p>
          </article>
          <article class="command-card">
            <h3>适用场景</h3>
            <p>模块里函数较多，或者希望调用来源更清晰时，优先使用这种写法。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="import as"
      >
        <h3><code>import as</code>：给模块起一个更短的名字</h3>
        <pre><code class="python">import my_tools as mt

print(mt.add(6, 7))
print(mt.average([75, 85, 95]))</code></pre>
        <p class="section-note">
          当模块名较长、调用频繁时，起别名会更方便。后面学 <code>wordcloud</code> 这类名字较长的模块时，这种写法会更常见。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="from import"
      >
        <h3><code>from import</code>：只导入需要的内容</h3>
        <pre><code class="python">from my_tools import add, average

print(add(1, 2))
print(average([90, 91, 92]))</code></pre>
        <div class="chapter-six-cue">
          <strong>要看清权衡。</strong> 这种写法最短，但函数来源不如 <code>模块名.函数名</code> 清楚。
          当导入内容很多时，可读性反而会下降。
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="模块自测"
      >
        <h3>一个模块如何既能被导入，又能自己测试</h3>
        <pre><code class="python">def add(a, b):
    return a + b


def average(numbers):
    return sum(numbers) / len(numbers)


if __name__ == "__main__":
    print(add(3, 4))
    print(average([80, 90, 100]))</code></pre>
        <p class="section-note">
          当模块被直接运行时，<code>__name__</code> 的值是 <code>"__main__"</code>；
          当模块被别的文件导入时，这一段自测代码不会执行。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="模块练习"
      >
        <h3>课堂练习：把任务统计函数拆进模块</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>任务要求</h3>
            <p>把和任务日志有关的两个功能拆进 <code>log_tools.py</code> 模块：一个函数统计总行数，一个函数返回最后一条日志。然后在主程序里导入模块并调用它们。</p>
          </article>
          <article class="command-card">
            <h3>建议操作顺序</h3>
            <ol>
              <li>先新建 <code>log_tools.py</code>。</li>
              <li>写 <code>count_lines(filename)</code>，逐行计数并返回总数。</li>
              <li>写 <code>last_line(filename)</code>，逐行更新变量，最终保留最后一条。</li>
              <li>在 <code>main.py</code> 中使用 <code>import log_tools as lt</code>。</li>
              <li>调用模块函数并打印结果。</li>
            </ol>
          </article>
          <article class="command-card">
            <h3>关键提示</h3>
            <p>模块文件里先写函数，主程序里再导入。不要把测试代码直接混在模块顶部，否则导入时会一起执行。</p>
            <p>如果要检查是否导入成功，可以先只调用一个函数再逐步增加。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="模块练习答案"
      >
        <h3>模块练习参考答案：把任务统计函数拆进模块</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python"># log_tools.py
def count_lines(filename):
    total = 0
    with open(filename, "r", encoding="utf-8") as file:
        for _ in file:
            total += 1
    return total


def last_line(filename):
    result = ""
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            result = line.strip()
    return result


# main.py
import log_tools as lt

print(lt.count_lines("mission_log.txt"))
print(lt.last_line("mission_log.txt"))</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="内置模块总览"
      >
        <h2>内置模块总览：不是所有功能都要自己从零写</h2>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>math</h3>
            <p>负责数学计算，适合平方根、圆周率、三角函数、向上取整等场景。</p>
          </article>
          <article class="concept-card">
            <h3>random</h3>
            <p>负责随机数和随机选择，适合抽奖、模拟、密码生成。</p>
          </article>
          <article class="concept-card">
            <h3>time</h3>
            <p>负责时间戳、格式化时间、暂停等待，适合日志和节奏控制。</p>
          </article>
          <article class="concept-card">
            <h3>sys / os / turtle</h3>
            <p>分别负责解释器信息、系统路径与目录、图形绘制，是很典型的标准库代表。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="math 模块"
      >
        <div class="section-head">
          <p class="kicker">MATH</p>
          <h2><code>math</code>：当数学计算开始变得正规</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>这一部分不要只背函数名。</strong> 真正要建立的是“函数和公式之间的对应关系”。
          看到 <code>math.sqrt()</code> 时，要想到平方根；看到 <code>math.pi</code> 时，要想到圆；
          看到 <code>ceil()</code> 和 <code>floor()</code> 时，要想到向上和向下取整。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3><code>math.pi</code></h3>
            <p>圆周率常量。只要公式里出现圆的周长或面积，通常都会用到它。</p>
          </article>
          <article class="concept-card">
            <h3><code>math.sqrt(x)</code></h3>
            <p>平方根。最常见于勾股定理、距离公式和各种几何长度计算。</p>
          </article>
          <article class="concept-card">
            <h3><code>math.ceil(x)</code></h3>
            <p>向上取整。只要结果必须取“至少这么多”，就常常会用到它。</p>
          </article>
          <article class="concept-card">
            <h3><code>math.floor(x)</code></h3>
            <p>向下取整。只要结果必须取“不超过这么多”，就常常会用到它。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="math 公式理解"
      >
        <h3>把函数和数学公式对上号</h3>
        <div class="command-layout chapter-six-math-grid">
          <article class="command-card">
            <h3>圆的周长与面积</h3>
            <p><strong>周长公式：</strong><code>C = 2πr</code></p>
            <p><strong>面积公式：</strong><code>S = πr²</code></p>
            <p>在代码里，<code>π</code> 通常写成 <code>math.pi</code>。</p>
          </article>
          <article class="command-card">
            <h3>勾股定理</h3>
            <p><strong>公式：</strong><code>c = √(a² + b²)</code></p>
            <p>在代码里，平方根写成 <code>math.sqrt(...)</code>。</p>
            <p>平面两点距离公式本质上就是勾股定理的直接应用。</p>
          </article>
          <article class="command-card">
            <h3>向上与向下取整</h3>
            <p><strong>向上取整：</strong><code>ceil(8.2) = 9</code></p>
            <p><strong>向下取整：</strong><code>floor(8.9) = 8</code></p>
            <p>这类函数常用于“人数分组”“车辆装载”“任务批次数”之类必须取整数的场景。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="math 图形辅助"
      >
        <h3>图形辅助理解：把公式和图形连起来</h3>
        <div class="command-layout chapter-six-math-grid">
          <article class="command-card chapter-six-figure-card">
            <h3>直角三角形与平方根</h3>
            <svg viewBox="0 0 220 160" class="chapter-six-figure" aria-hidden="true">
              <line x1="30" y1="130" x2="170" y2="130" />
              <line x1="30" y1="130" x2="30" y2="30" />
              <line x1="30" y1="30" x2="170" y2="130" />
              <rect x="30" y="115" width="15" height="15" />
              <text x="92" y="147">a</text>
              <text x="10" y="82">b</text>
              <text x="110" y="72">c</text>
            </svg>
            <p>如果底边是 <code>a</code>，高是 <code>b</code>，斜边 <code>c</code> 就要用 <code>math.sqrt(a**2 + b**2)</code> 算出来。</p>
          </article>
          <article class="command-card chapter-six-figure-card">
            <h3>圆与 <code>math.pi</code></h3>
            <svg viewBox="0 0 220 160" class="chapter-six-figure" aria-hidden="true">
              <circle cx="95" cy="80" r="48" />
              <line x1="95" y1="80" x2="143" y2="80" />
              <text x="112" y="72">r</text>
              <text x="156" y="84">圆周</text>
            </svg>
            <p>圆的周长和面积都离不开 <code>π</code>。所以代码里只要在算圆，通常第一反应就是 <code>math.pi</code>。</p>
          </article>
          <article class="command-card chapter-six-figure-card">
            <h3>数轴与取整</h3>
            <svg viewBox="0 0 220 110" class="chapter-six-figure" aria-hidden="true">
              <line x1="20" y1="60" x2="200" y2="60" />
              <line x1="60" y1="50" x2="60" y2="70" />
              <line x1="140" y1="50" x2="140" y2="70" />
              <circle cx="108" cy="60" r="5" />
              <text x="56" y="88">8</text>
              <text x="136" y="88">9</text>
              <text x="96" y="45">8.6</text>
            </svg>
            <p>像 <code>8.6</code> 这样的数，向上取整得到 9，向下取整得到 8。图上看清位置，函数就不容易记混。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="math 基础示例"
      >
        <h3>基础示例：先把常量、开方和取整跑一遍</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import math

print("圆周率：", math.pi)
print("144 的平方根：", math.sqrt(144))
print("8.2 向上取整：", math.ceil(8.2))
print("8.9 向下取整：", math.floor(8.9))</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一页先不追求复杂，只要求把每个函数和它背后的数学含义对应起来。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="math 圆形示例"
      >
        <h3>进阶示例 1：把圆的公式翻译成代码</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import math

r = 6
circumference = 2 * math.pi * r
area = math.pi * r ** 2

print("半径：", r)
print("周长：", circumference)
print("面积：", area)</code></pre>
          </article>
        </div>
        <p class="section-note">
          公式写成代码时，变量和常量的角色要分清：<code>r</code> 是输入，<code>math.pi</code> 是固定数学常量。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="math 距离示例"
      >
        <h3>进阶示例 2：平面两点距离</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import math

x1, y1 = 2, 3
x2, y2 = 10, 9

dx = x2 - x1
dy = y2 - y1
distance = math.sqrt(dx ** 2 + dy ** 2)

print("横向变化：", dx)
print("纵向变化：", dy)
print("两点距离：", distance)</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一页要看懂的是“先求横向和纵向差值，再套勾股定理”。这样以后碰到坐标、位移和速度分解时就不会乱。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="math 练习"
      >
        <h3>练习：计算警戒区周长、两点距离和物资车数量</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>任务要求</h3>
            <p>
              已知圆形警戒区半径 <code>r = 7</code> 米，先计算警戒区周长和面积。再给出两个巡检点
              <code>A(2, 3)</code> 和 <code>B(14, 11)</code>，计算两点直线距离。最后假设每隔 3 米要放置 1
              个警示锥，每辆物资车最多运 6 个警示锥，计算至少需要几辆物资车。
            </p>
          </article>
          <article class="command-card">
            <h3>建议操作顺序</h3>
            <ol>
              <li>先导入 <code>math</code>，定义半径和两组坐标。</li>
              <li>用 <code>2 * math.pi * r</code> 计算周长，用 <code>math.pi * r ** 2</code> 计算面积。</li>
              <li>分别求出 <code>dx</code> 和 <code>dy</code>，再用 <code>math.sqrt(dx ** 2 + dy ** 2)</code> 计算距离。</li>
              <li>用 <code>周长 / 3</code> 计算需要多少个警示锥。</li>
              <li>再用 <code>math.ceil(锥桶数量 / 6)</code> 计算至少需要几辆物资车。</li>
            </ol>
          </article>
          <article class="command-card">
            <h3>关键提示</h3>
            <p>
              这一题把 <code>math.pi</code>、<code>math.sqrt()</code> 和 <code>math.ceil()</code>
              串到了一起。关键不是把结果背下来，而是先认清每一个公式分别解决什么问题。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="math 练习答案"
      >
        <h3>math 练习参考答案：警戒区与巡检路线计算</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import math

r = 7
x1, y1 = 2, 3
x2, y2 = 14, 11

circumference = 2 * math.pi * r
area = math.pi * r ** 2

dx = x2 - x1
dy = y2 - y1
distance = math.sqrt(dx ** 2 + dy ** 2)

cone_count = math.ceil(circumference / 3)
truck_count = math.ceil(cone_count / 6)

print("警戒区周长：", circumference)
print("警戒区面积：", area)
print("两点直线距离：", distance)
print("需要警示锥数量：", cone_count)
print("至少需要物资车：", truck_count)</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="random 模块"
      >
        <div class="section-head">
          <p class="kicker">RANDOM</p>
          <h2><code>random</code>：从一个随机数，到一套随机流程</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>random 不只是“随机出一个整数”。</strong> 真正要会的是：什么时候该用随机整数，什么时候该从列表里抽一个，
          什么时候该无重复抽取，什么时候该打乱顺序，什么时候又要按概率分布来抽。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3><code>randint(a, b)</code></h3>
            <p>适合生成整数范围内的随机结果，例如掷骰子、随机分数、随机题号。</p>
          </article>
          <article class="concept-card">
            <h3><code>choice(seq)</code></h3>
            <p>适合从一组候选项里抽一个，例如随机点名、随机队长、随机口令。</p>
          </article>
          <article class="concept-card">
            <h3><code>sample(seq, k)</code></h3>
            <p>适合无重复抽取，例如抽奖名单、抽考名单、随机座位。</p>
          </article>
          <article class="concept-card">
            <h3><code>shuffle(list)</code> / <code>choices()</code></h3>
            <p>前者负责打乱顺序，后者适合按权重抽样，常见于随机分组和概率模拟。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="random 场景"
      >
        <h3>把 random 放进实际场景里看</h3>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>课堂点名</h3>
            <p>从学生名单里随机抽一人，最适合用 <code>random.choice()</code>。</p>
          </article>
          <article class="concept-card">
            <h3>抽奖与抽签</h3>
            <p>如果同一个人不能重复中奖，就应该使用 <code>random.sample()</code>。</p>
          </article>
          <article class="concept-card">
            <h3>随机分组</h3>
            <p>先把名单 <code>shuffle()</code> 打乱，再按人数切片分成若干组。</p>
          </article>
          <article class="concept-card">
            <h3>概率模拟</h3>
            <p>奖品掉落、抽卡、天气事件，更适合用 <code>random.choices()</code> 做权重控制。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="random 数字示例"
      >
        <h3>基础示例：先分清整数、浮点数和步长</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import random

print("掷骰子：", random.randint(1, 6))
print("随机偶数座位号：", random.randrange(2, 22, 2))
print("0 到 1 之间的小数：", round(random.random(), 4))
print("随机体温：", round(random.uniform(36.3, 37.2), 2))</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>randint()</code> 适合整数区间，<code>randrange()</code> 适合“带步长”的整数序列，<code>random()</code>
          和 <code>uniform()</code> 更适合生成浮点数。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="random 列表示例"
      >
        <h3>列表示例：抽一个、抽多个、打乱顺序</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import random

students = ["李雷", "韩梅梅", "王强", "赵敏", "陈晨", "周宇"]

print("随机点名：", random.choice(students))
print("抽两名值日生：", random.sample(students, 2))

random.shuffle(students)
print("打乱后的名单：", students)</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>choice()</code> 取 1 个，<code>sample()</code> 取多个且不重复，<code>shuffle()</code>
          直接把原列表顺序打乱。它们解决的是三类不同问题。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="random 分组示例"
      >
        <h3>进阶示例 1：随机分组</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import random

students = [
    "李雷", "韩梅梅", "王强", "赵敏",
    "陈晨", "周宇", "林雪", "唐宁",
    "高远", "宋佳", "谢婷", "苏航"
]

random.shuffle(students)

group_size = 4
for i in range(0, len(students), group_size):
    group = students[i:i + group_size]
    print(f"第{i // group_size + 1}组：", group)</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一类题目在课堂活动、实验分组、随机座位安排里都很常见。先 <code>shuffle()</code>，再按步长切片，是最稳的基础写法。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="random 概率示例"
      >
        <h3>进阶示例 2：按权重模拟抽奖结果</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import random

prizes = ["一等奖", "二等奖", "三等奖", "谢谢参与"]
weights = [1, 3, 6, 20]

for i in range(5):
    result = random.choices(prizes, weights=weights, k=1)[0]
    print(f"第{i + 1}次抽奖结果：", result)</code></pre>
          </article>
        </div>
        <p class="section-note">
          如果所有结果出现概率都一样，就用 <code>choice()</code>。如果不同结果概率不同，就应该考虑 <code>choices()</code> 和 <code>weights</code>。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="random 练习"
      >
        <h3>练习：编写班级团建抽签脚本</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>任务要求</h3>
            <p>
              已知 12 名同学名单，先随机打乱顺序，再平均分成 3 组。每组随机抽 1 名组长，最后再从全班同学中无重复抽出 2 名幸运同学。
              运行结果至少要打印：分组结果、每组组长、幸运同学名单。
            </p>
          </article>
          <article class="command-card">
            <h3>建议操作顺序</h3>
            <ol>
              <li>先准备 12 个姓名组成的列表。</li>
              <li>用 <code>random.shuffle()</code> 打乱原列表顺序。</li>
              <li>按每组 4 人切片，得到 3 个小组。</li>
              <li>对每个小组使用 <code>random.choice()</code> 抽组长。</li>
              <li>最后对全班名单使用 <code>random.sample()</code> 抽 2 名幸运同学。</li>
            </ol>
          </article>
          <article class="command-card">
            <h3>关键提示</h3>
            <p>
              这道题最适合同时练习三件事：<code>shuffle()</code> 改顺序，<code>choice()</code> 抽单个结果，
              <code>sample()</code> 做无重复抽取。每个函数解决的问题都不一样，不要混用。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="random 练习答案"
      >
        <h3>random 练习参考答案：班级团建抽签脚本</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import random

students = [
    "李雷", "韩梅梅", "王强", "赵敏",
    "陈晨", "周宇", "林雪", "唐宁",
    "高远", "宋佳", "谢婷", "苏航"
]

random.shuffle(students)

group_size = 4
groups = []

for i in range(0, len(students), group_size):
    group = students[i:i + group_size]
    groups.append(group)

for index, group in enumerate(groups, start=1):
    leader = random.choice(group)
    print(f"第{index}组：{group}")
    print(f"第{index}组组长：{leader}")

lucky_students = random.sample(students, 2)
print("幸运同学：", lucky_students)</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="time 模块"
      >
        <div class="section-head">
          <p class="kicker">TIME</p>
          <h2><code>time</code>：把程序和真实时间接起来</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>time 最常见的作用不是“显示一下当前时间”。</strong>
          它真正有价值的地方在于：给日志加时间、控制程序节奏、统计程序耗时、生成带时间戳的文件名。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3><code>time.time()</code></h3>
            <p>返回当前时间戳，适合做时间差比较和简单的计时。</p>
          </article>
          <article class="concept-card">
            <h3><code>time.strftime()</code></h3>
            <p>把当前时间格式化成字符串，常用于日志和文件名。</p>
          </article>
          <article class="concept-card">
            <h3><code>time.sleep()</code></h3>
            <p>让程序暂停一段时间，适合做倒计时、轮询和节奏控制。</p>
          </article>
          <article class="concept-card">
            <h3><code>time.perf_counter()</code></h3>
            <p>更适合精确测量代码运行耗时，比简单时间戳更稳定。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="time 场景"
      >
        <h3>把 time 放进实际场景里看</h3>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>日志时间</h3>
            <p>给每条日志加上 <code>2026-04-04 10:30:25</code> 这样的时间，方便排查问题。</p>
          </article>
          <article class="concept-card">
            <h3>倒计时与等待</h3>
            <p>抢答、发令、轮询设备状态，通常都要用到 <code>sleep()</code>。</p>
          </article>
          <article class="concept-card">
            <h3>程序性能统计</h3>
            <p>测某段代码运行了多久，更适合使用 <code>perf_counter()</code>。</p>
          </article>
          <article class="concept-card">
            <h3>时间戳文件名</h3>
            <p>导出报表、实验记录、运行结果时，常用时间戳避免文件名重复。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="time 基础示例"
      >
        <h3>基础示例：当前时间、格式化时间和文件名时间戳</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import time

timestamp = time.time()
now_text = time.strftime("%Y-%m-%d %H:%M:%S")
file_text = time.strftime("%Y%m%d_%H%M%S")

print("时间戳：", timestamp)
print("格式化时间：", now_text)
print("适合文件名的时间戳：", file_text)</code></pre>
          </article>
        </div>
        <p class="section-note">
          如果字符串要作为 Windows 文件名的一部分，通常不要直接使用 <code>:</code>，所以更适合写成
          <code>%Y%m%d_%H%M%S</code> 这种格式。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="time 倒计时示例"
      >
        <h3>进阶示例 1：倒计时与节奏控制</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import time

for second in range(5, 0, -1):
    print(f"倒计时：{second}")
    time.sleep(1)

print("开始执行")</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>sleep(1)</code> 的意思是每次循环暂停 1 秒。没有它的话，倒计时会在极短时间内直接跑完。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="time 计时示例"
      >
        <h3>进阶示例 2：统计一段代码执行耗时</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import time

start = time.perf_counter()

total = 0
for i in range(1, 1000001):
    total += i

end = time.perf_counter()

print("求和结果：", total)
print("耗时：", round(end - start, 6), "秒")</code></pre>
          </article>
        </div>
        <p class="section-note">
          做性能统计时，重点不是“当前几点了”，而是“前后相差了多久”。这时 <code>perf_counter()</code> 比直接看格式化时间更合适。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="sys 模块"
      >
        <div class="section-head">
          <p class="kicker">SYS</p>
          <h2><code>sys</code>：查看解释器和运行环境</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>sys 更像“程序运行环境的说明书”。</strong>
          当你需要确认 Python 版本、解释器位置、命令行参数、模块搜索路径时，最直接的入口通常就是 <code>sys</code>。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3><code>sys.version</code></h3>
            <p>查看当前 Python 版本，排查“版本不一致”时非常常用。</p>
          </article>
          <article class="concept-card">
            <h3><code>sys.executable</code></h3>
            <p>查看当前到底是哪个 Python 在运行，特别适合排查虚拟环境问题。</p>
          </article>
          <article class="concept-card">
            <h3><code>sys.argv</code></h3>
            <p>读取命令行参数，让同一个脚本接收不同输入。</p>
          </article>
          <article class="concept-card">
            <h3><code>sys.path</code> / <code>sys.exit()</code></h3>
            <p>前者看模块搜索路径，后者在发现致命错误时主动结束程序。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="sys 场景"
      >
        <h3>把 sys 放进实际场景里看</h3>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>确认解释器版本</h3>
            <p>课堂上最常见的问题之一，就是同学运行的 Python 版本和示例环境不一致。</p>
          </article>
          <article class="concept-card">
            <h3>确认是否在 Windows</h3>
            <p>在 Windows 下，<code>sys.platform</code> 常见结果是 <code>win32</code>。</p>
          </article>
          <article class="concept-card">
            <h3>接收命令行输入</h3>
            <p>让脚本从命令行接收文件名、用户名或配置项，不再把数据写死在代码里。</p>
          </article>
          <article class="concept-card">
            <h3>排查导入失败</h3>
            <p>模块明明存在却导入不到，常常要先检查 <code>sys.path</code>。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="sys 基础示例"
      >
        <h3>基础示例：查看版本、平台和解释器位置</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import sys

print("Python 版本：", sys.version)
print("平台：", sys.platform)
print("解释器路径：", sys.executable)</code></pre>
          </article>
        </div>
        <p class="section-note">
          在 Windows 上，<code>sys.platform</code> 一般显示为 <code>win32</code>。这不是错误，它是 Python 历史沿用下来的平台标识。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="sys 参数示例"
      >
        <h3>进阶示例 1：读取命令行参数</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import sys

print("脚本名：", sys.argv[0])
print("参数列表：", sys.argv[1:])

if len(sys.argv) < 2:
    print("用法：python tool.py 文件名")
else:
    print("准备处理文件：", sys.argv[1])</code></pre>
          </article>
        </div>
        <p class="section-note">
          例如在 Windows 终端里执行 <code>python tool.py mission_log.txt</code>，那么 <code>sys.argv[1]</code> 就是
          <code>mission_log.txt</code>。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="sys 路径示例"
      >
        <h3>进阶示例 2：检查模块搜索路径并在必要时退出</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import sys

print("前 5 个模块搜索路径：")
for path in sys.path[:5]:
    print(path)

config_file = "config.txt"
if config_file not in ["config.txt", "settings.txt"]:
    sys.exit("配置文件名不合法，程序结束。")

print("配置检查通过")</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>sys.path</code> 适合排查“为什么 import 不到模块”，<code>sys.exit()</code> 适合在发现明显错误时主动终止程序。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="os 模块"
      >
        <div class="section-head">
          <p class="kicker">OS</p>
          <h2><code>os</code>：让程序真正和操作系统打交道</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>这一部分按 Windows 环境来理解最合适。</strong>
          重点不是死记函数，而是学会让程序知道“自己现在在哪个文件夹、目标文件在哪、目录要不要创建、路径要怎么安全拼接”。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3><code>os.getcwd()</code> / <code>listdir()</code></h3>
            <p>先搞清当前工作目录和目录下有什么文件，这是文件操作的起点。</p>
          </article>
          <article class="concept-card">
            <h3><code>os.path.join()</code></h3>
            <p>在 Windows 下也不建议手写一长串反斜杠，拼路径更稳的方式是 <code>join()</code>。</p>
          </article>
          <article class="concept-card">
            <h3><code>exists()</code> / <code>isfile()</code> / <code>isdir()</code></h3>
            <p>先判断对象是否存在、是文件还是文件夹，再进行下一步操作。</p>
          </article>
          <article class="concept-card">
            <h3><code>mkdir()</code> / <code>makedirs()</code> / <code>startfile()</code></h3>
            <p>创建目录、批量创建多级目录，或者在 Windows 中直接打开目标文件。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="os 场景"
      >
        <h3>把 os 放进 Windows 实际场景里看</h3>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>找当前目录</h3>
            <p>运行脚本后文件找不到，第一反应应该先看 <code>os.getcwd()</code>。</p>
          </article>
          <article class="concept-card">
            <h3>构造 Windows 路径</h3>
            <p>例如 <code>output\\daily\\report.txt</code> 这种路径，更适合用 <code>os.path.join()</code> 生成。</p>
          </article>
          <article class="concept-card">
            <h3>创建输出目录</h3>
            <p>导出成绩、日志、报表时，常常要先检查目标目录是否存在。</p>
          </article>
          <article class="concept-card">
            <h3>筛选指定类型文件</h3>
            <p>批量处理当前目录中的 <code>.txt</code>、<code>.py</code> 文件，是很典型的自动化任务。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="os 基础示例"
      >
        <h3>基础示例：查看当前目录和目录内容</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import os

print("当前工作目录：", os.getcwd())
print("当前目录内容：")

for name in os.listdir("."):
    print(name)</code></pre>
          </article>
        </div>
        <p class="section-note">
          文件找不到时，不要先怀疑 Python 语法，先确认“脚本当前到底在哪个目录里运行”。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="os 路径示例"
      >
        <h3>进阶示例 1：安全拼接 Windows 路径</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import os

base_folder = "output"
sub_folder = "daily_report"
file_name = "report.txt"

folder_path = os.path.join(base_folder, sub_folder)
file_path = os.path.join(folder_path, file_name)

print("文件夹路径：", folder_path)
print("文件完整路径：", file_path)</code></pre>
          </article>
        </div>
        <p class="section-note">
          在 Windows 上手写反斜杠容易出错，也容易和转义符混淆。路径拼接优先用 <code>os.path.join()</code>。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="os 目录示例"
      >
        <h3>进阶示例 2：检查目录、创建多级目录并写入文件</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import os

folder_path = os.path.join("output", "daily_report")

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = os.path.join(folder_path, "report.txt")

with open(file_path, "w", encoding="utf-8") as file:
    file.write("第六章模块学习记录\\n")
    file.write("time / sys / os 已完成\\n")

print("文件已写入：", file_path)</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>makedirs()</code> 比 <code>mkdir()</code> 更适合创建多级目录。像 <code>output/daily_report</code> 这种结构，用它更稳。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="os 文件筛选示例"
      >
        <h3>进阶示例 3：筛选当前目录中的文本文件</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import os

print("当前目录中的 txt 文件：")

for name in os.listdir("."):
    if os.path.isfile(name) and name.endswith(".txt"):
        print(name)</code></pre>
          </article>
        </div>
        <p class="section-note">
          这类写法很适合做“批量处理指定类型文件”的前置筛选。先判断 <code>isfile()</code>，再判断扩展名，逻辑会更清楚。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="turtle 模块"
      >
        <div class="section-head">
          <p class="kicker">TURTLE</p>
          <h2><code>turtle</code>：把循环、函数和图形绘制连起来</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>turtle 不只是“画一个图形”。</strong>
          它适合把程序控制、重复结构、坐标思想和事件交互一起讲清楚。学这一部分时，要把“海龟怎么移动”想成“程序怎么一步一步控制画笔”。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>命令式画图</h3>
            <p>使用 <code>forward()</code>、<code>left()</code>、<code>right()</code> 逐步控制海龟移动和转向。</p>
          </article>
          <article class="concept-card">
            <h3>循环画图</h3>
            <p>规则图形最适合用 <code>for</code> 循环重复绘制，角度关系也更容易总结。</p>
          </article>
          <article class="concept-card">
            <h3>坐标画图</h3>
            <p>使用 <code>goto(x, y)</code>、<code>setheading()</code> 和 <code>circle()</code>，更适合画数学曲线和精确位置图形。</p>
          </article>
          <article class="concept-card">
            <h3>交互画图</h3>
            <p>通过键盘、鼠标和输入框，让图形程序从“自动执行”升级到“可操作的小游戏或画板”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 画图方式"
      >
        <h3>先分清 4 种典型画图方式</h3>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>方式 1：一步一步走</h3>
            <p>最适合入门，看到海龟前进和转向，就能理解程序命令的执行顺序。</p>
          </article>
          <article class="concept-card">
            <h3>方式 2：循环重复</h3>
            <p>正多边形、花瓣、螺旋线最适合用循环，因为每一步都符合相同规律。</p>
          </article>
          <article class="concept-card">
            <h3>方式 3：按坐标定位</h3>
            <p>如果图形和数学坐标有关，就更适合直接走到某个点，而不是只靠前进和转弯。</p>
          </article>
          <article class="concept-card">
            <h3>方式 4：事件交互</h3>
            <p>按键、点击和输入框可以让图形响应用户操作，这时程序会更像一个完整作品。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 图形灵感"
      >
        <h3>除了基础图形，turtle 还能继续走多远</h3>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>花瓣与曼陀罗</h3>
            <p>圆弧、旋转和填充色结合起来后，很容易生成具有装饰感的花形图案。</p>
          </article>
          <article class="concept-card">
            <h3>螺旋与几何叠加</h3>
            <p>长度逐渐变化、角度保持规律时，简单命令也能堆叠出非常丰富的视觉效果。</p>
          </article>
          <article class="concept-card">
            <h3>数学曲线</h3>
            <p>当公式可以给出一系列坐标点时，turtle 就能把这些点连成真正的曲线。</p>
          </article>
          <article class="concept-card">
            <h3>递归分形</h3>
            <p>像分形树这种“局部和整体相似”的图形，非常适合用递归来生成。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 基础命令"
      >
        <h3>基础命令：先把画笔控制清楚</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 把海龟外形显示出来，方便观察方向
turtle.shape("turtle")
# 设置画笔粗细和初始颜色
turtle.pensize(3)
turtle.color("navy")

# 向前移动，再左转 90 度继续画
turtle.forward(120)
turtle.left(90)
turtle.forward(80)
# 抬笔移动，不留下线条
turtle.penup()
turtle.goto(-40, -40)
# 落笔后继续画，并切换颜色
turtle.pendown()
turtle.color("crimson")
turtle.backward(60)

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一页要重点看懂的是：<code>penup()</code> 和 <code>pendown()</code> 会影响“移动时是否留下线条”，
          <code>goto()</code> 可以直接跳到指定坐标。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 多边形"
      >
        <h3>示例 1：用角度公式画正多边形</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 设置边数和边长
sides = 6
length = 90
# 正多边形每次转角 = 360 / 边数
turn_angle = 360 / sides

# 设置线条样式
turtle.pensize(3)
turtle.color("teal")

# 重复“前进 + 转角”
for _ in range(sides):
    turtle.forward(length)
    turtle.right(turn_angle)

# 显示结果窗口
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          正多边形最适合把数学和程序连起来：边数是 <code>sides</code>，每次转角就是 <code>360 / sides</code>。
          改变边数，就能得到三角形、五边形、八边形等不同图形。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 填充图形"
      >
        <h3>示例 2：颜色、填充与函数封装</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 定义函数：在指定位置画一个带填充色的正方形
def draw_square(x, y, size, line_color, fill_color):
    # 先移动到目标位置
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    # 同时设置线条颜色和填充颜色
    turtle.color(line_color, fill_color)
    # 开始填充
    turtle.begin_fill()

    # 连续画四条边
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)

    # 结束填充
    turtle.end_fill()

# 提高绘图速度
turtle.speed(0)
# 连续调用函数，画出三个不同颜色的方块
draw_square(-160, 80, 80, "midnightblue", "lightblue")
draw_square(-40, 80, 80, "darkgreen", "lightgreen")
draw_square(80, 80, 80, "darkred", "mistyrose")

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一页要感受的是：当同一类图形要画很多次时，最稳的方式是写成函数，而不是复制粘贴三遍。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 有趣图形"
      >
        <h3>示例 3：旋转方形，形成几何花纹</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 提高速度，设置背景和线宽
turtle.speed(0)
turtle.bgcolor("black")
turtle.pensize(2)

# 准备循环使用的颜色
colors = ["#ffcc00", "#ff6699", "#66ccff", "#99ff66"]

# 每次画一个正方形，再整体旋转一点点
for i in range(40):
    turtle.color(colors[i % len(colors)])
    for _ in range(4):
        turtle.forward(120)
        turtle.right(90)
    # 每次多转 9 度，图案就会逐渐叠加
    turtle.right(9)

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          图形本身仍然是正方形，但每次旋转一个小角度后继续画，就会叠加出带数学节奏感的图案。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 花瓣图形"
      >
        <h3>示例 4：用圆弧画彩色花瓣图</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 提高绘图速度并设置背景
turtle.speed(0)
turtle.bgcolor("#fffaf0")
turtle.pensize(2)

# 准备循环使用的颜色
colors = ["#ff6b6b", "#ffd93d", "#6bcB77", "#4d96ff", "#b983ff"]

# 连续旋转并使用圆弧，就能形成花瓣
for i in range(18):
    turtle.color(colors[i % len(colors)])
    turtle.circle(100, 60)
    turtle.left(120)
    turtle.circle(100, 60)
    turtle.left(160)

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>circle(100, 60)</code> 的意思不是画完整圆，而是画半径为 100、转过 60 度的一段圆弧。两个圆弧拼起来，就很像一个花瓣。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 数学曲线"
      >
        <h3>示例 5：把 <code>math</code> 和 <code>turtle</code> 结合，画正弦曲线</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle
import math

# 提高绘图速度并设置线条样式
turtle.speed(0)
turtle.pensize(2)
turtle.color("purple")
# 抬笔准备移动到起点
turtle.penup()

# 让 x 从 -180 变化到 180，计算每个点对应的 y
for x in range(-180, 181):
    # 先把角度转成弧度，再求正弦值
    y = math.sin(math.radians(x)) * 80
    if x == -180:
        # 第一个点：先移动过去，再落笔
        turtle.goto(x, y)
        turtle.pendown()
    else:
        # 后续点：直接连线
        turtle.goto(x, y)

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          这页最重要的不是把正弦公式背下来，而是看懂：当数学函数能给出一系列点坐标时，就可以用 <code>goto()</code> 把曲线画出来。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 螺旋图形"
      >
        <h3>示例 6：螺旋线与渐变节奏</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 设置背景和画笔
turtle.speed(0)
turtle.bgcolor("navy")
turtle.pensize(2)
colors = ["cyan", "white", "gold", "tomato"]

# 前进距离逐渐变大，就会形成螺旋效果
for i in range(120):
    turtle.color(colors[i % len(colors)])
    turtle.forward(i * 2)
    turtle.right(91)

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          当“前进距离逐渐变长、转角保持接近直角”时，图形就会形成很强的螺旋感。这类图形很适合帮助学生理解循环变量的视觉效果。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 分形树"
      >
        <h3>示例 7：利用递归绘制分形树</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 创建画布并设置背景颜色
screen = turtle.Screen()
screen.bgcolor("#081b29")

# 创建专门画树的海龟对象
t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.color("#7CFC00")

# 让海龟朝上，并移动到树干底部
t.left(90)
t.penup()
t.goto(0, -260)
t.pendown()

def draw_tree(branch_length):
    # 递归结束条件：树枝太短时，不再继续分叉
    if branch_length < 10:
        return

    # 先画当前树枝
    t.pensize(max(branch_length / 10, 1))
    t.forward(branch_length)

    # 画左边分支
    t.left(30)
    draw_tree(branch_length * 0.72)

    # 回到主干方向后，再画右边分支
    t.right(60)
    draw_tree(branch_length * 0.72)

    # 恢复方向并退回当前分支起点
    t.left(30)
    t.backward(branch_length)

# 从主干开始，递归生成整棵树
draw_tree(90)

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一页要把递归真正看成图形过程：一段树枝画完后，会在更短的长度上继续画左分支和右分支，直到长度小到可以停止。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 交互输入"
      >
        <h3>交互方式 1：让用户输入边数，再决定画什么</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 创建画布对象，用来弹出输入框
screen = turtle.Screen()
# 让用户输入多边形边数
sides = screen.numinput("边数输入", "请输入一个 3 到 12 之间的整数：", default=5, minval=3, maxval=12)

if sides is not None:
    # 根据边数自动计算转角
    turn_angle = 360 / sides
    turtle.pensize(3)
    turtle.color("darkorange")

    # 画出对应边数的正多边形
    for _ in range(int(sides)):
        turtle.forward(90)
        turtle.right(turn_angle)

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>numinput()</code> 适合做数值输入。这样一来，程序不再固定画五边形，而是可以根据用户输入画不同的多边形。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 键盘交互"
      >
        <h3>交互方式 2：用键盘控制海龟移动</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 创建画布和海龟对象
screen = turtle.Screen()
t = turtle.Turtle()
t.shape("turtle")
t.pensize(3)

# 定义按键对应的动作函数
def move_forward():
    t.forward(30)

def turn_left():
    t.left(30)

def turn_right():
    t.right(30)

# 开始监听键盘事件，并绑定按键
screen.listen()
screen.onkey(move_forward, "Up")
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一页要理解事件驱动：程序不是一启动就把所有动作做完，而是“等用户按键，再执行对应函数”。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 鼠标交互"
      >
        <h3>交互方式 3：点击画布，在点击处生成彩色圆点</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle
import random

# 创建画布和专门负责画点的海龟
screen = turtle.Screen()
t = turtle.Turtle()
t.hideturtle()
t.speed(0)

# 预先准备几种颜色
colors = ["red", "blue", "green", "purple", "orange"]

# 点击任意位置时，在点击坐标处画一个彩色圆点
def draw_dot(x, y):
    t.penup()
    t.goto(x, y)
    t.dot(24, random.choice(colors))

# 绑定鼠标点击事件
screen.onclick(draw_dot)
screen.listen()

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>onclick()</code> 会把鼠标点击位置自动传给函数，所以回调函数要写成 <code>draw_dot(x, y)</code> 这种形式。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 练习"
      >
        <h3>练习：绘制可输入花瓣数量的彩色太阳花</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>任务要求</h3>
            <p>
              用 <code>turtle</code> 编写一个小程序：先弹出输入框，让用户输入花瓣数量；再通过循环和圆弧绘制出一朵彩色太阳花；
              每画完一片花瓣，就旋转固定角度继续画下一片。最终图形要有明显的对称感和颜色变化。
            </p>
          </article>
          <article class="command-card">
            <h3>建议操作顺序</h3>
            <ol>
              <li>先创建 <code>screen = turtle.Screen()</code>，并用 <code>numinput()</code> 获取花瓣数量。</li>
              <li>定义一个画单片花瓣的函数，函数内部可以用两段圆弧组成花瓣。</li>
              <li>准备一个颜色列表，让不同花瓣轮流使用不同颜色。</li>
              <li>在循环中调用画花瓣函数，并使用 <code>left(360 / petal_count)</code> 旋转到下一片花瓣位置。</li>
              <li>最后调用 <code>turtle.done()</code> 保持窗口。</li>
            </ol>
          </article>
          <article class="command-card">
            <h3>关键提示</h3>
            <p>
              这一题的核心不在于把圆弧参数记死，而在于看懂：<code>circle(radius, extent)</code> 可以画圆弧，
              多次重复“画花瓣 + 旋转”后，就能形成完整的放射状图案。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="turtle 练习答案"
      >
        <h3>turtle 练习参考答案：可输入花瓣数量的彩色太阳花</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import turtle

# 创建画布对象，并弹出输入框
screen = turtle.Screen()
petal_count = screen.numinput(
    "花瓣数量输入",
    "请输入一个 6 到 24 之间的整数：",
    default=12,
    minval=6,
    maxval=24
)

# 如果用户没有取消输入，就继续画图
if petal_count is not None:
    turtle.speed(0)
    turtle.bgcolor("#fffaf0")
    turtle.pensize(2)

    # 准备循环使用的颜色
    colors = ["#ff6b6b", "#ffd93d", "#6bcB77", "#4d96ff", "#b983ff"]

    # 定义一片花瓣：由两段圆弧拼接而成
    def draw_petal(radius, color):
        turtle.color(color)
        turtle.begin_fill()
        turtle.circle(radius, 60)
        turtle.left(120)
        turtle.circle(radius, 60)
        turtle.left(120)
        turtle.end_fill()

    # 按照花瓣数量循环绘制
    for i in range(int(petal_count)):
        draw_petal(100, colors[i % len(colors)])
        turtle.left(360 / petal_count)

# 保持窗口不关闭
turtle.done()</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="外置模块"
      >
        <div class="section-head">
          <p class="kicker">THIRD-PARTY MODULES</p>
          <h2>常用外置模块：程序开始真正借助生态工作</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>内置模块解决通用问题，外置模块解决专门问题。</strong>
          当任务涉及中文分词、词云绘图、虚拟数据生成时，自己从零写不现实，直接使用成熟模块才是正确做法。
        </p>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>faker</h3>
            <p>快速生成姓名、地址、电话、公司等模拟数据，适合做测试样本。</p>
          </article>
          <article class="command-card">
            <h3>jieba</h3>
            <p>负责中文分词，把整段中文文本切成适合统计与分析的词语列表。</p>
          </article>
          <article class="command-card">
            <h3>wordcloud</h3>
            <p>根据词频生成可视化词云，常和文件操作、jieba 分词一起使用。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="安装外置模块"
      >
        <h3>安装外置模块：先把环境准备好</h3>
        <pre><code class="bash">python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple faker jieba wordcloud</code></pre>
        <p class="section-note">
          这条命令把本章三个外置模块一起装好，并且只在这一次安装时临时使用清华源，不会修改 pip 的全局配置。之后就可以像导入内置模块一样导入它们，只是首次使用前必须先安装。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="faker 模块"
      >
        <div class="section-head">
          <p class="kicker">FAKER</p>
          <h2><code>faker</code>：先造数据，再调程序</h2>
        </div>
        <p class="chapter-six-cue">
          <strong><code>faker</code> 不只是“随机几个名字”。</strong>
          它真正的价值是：当真实数据还没准备好时，先生成一批结构合理、格式像真的测试数据，
          让文件读写、统计分析、界面展示这些流程先跑通。学这一部分时，要把它看成“给程序准备练习材料”的工具。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>学生资料</h3>
            <p>生成姓名、电话、地址、邮箱，适合做名单、通讯录、注册表。</p>
          </article>
          <article class="concept-card">
            <h3>批量样本</h3>
            <p>把单次方法调用放进循环后，就能快速得到一整批测试数据。</p>
          </article>
          <article class="concept-card">
            <h3>配合 random</h3>
            <p>用 <code>faker</code> 造基本资料，用 <code>random</code> 补充分数、课程、等级等字段。</p>
          </article>
          <article class="concept-card">
            <h3>保存到文件</h3>
            <p>把生成结果写入文本文件后，后面就能继续练习读取、统计和分析。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="faker 应用场景"
      >
        <h3>先分清 <code>faker</code> 最常见的 4 类应用场景</h3>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>场景 1：真实名单还没有</h3>
            <p>程序已经要测试输入输出，但班级名单、用户资料、订单信息还没整理好，就先用假数据顶上。</p>
          </article>
          <article class="concept-card">
            <h3>场景 2：真实数据不方便公开</h3>
            <p>姓名、电话、地址这类信息涉及隐私，课堂演示和作业示例更适合使用模拟数据。</p>
          </article>
          <article class="concept-card">
            <h3>场景 3：需要批量样本</h3>
            <p>手敲 50 条数据太慢，也容易出错；用循环配合 <code>faker</code> 可以几秒钟生成一大批样本。</p>
          </article>
          <article class="concept-card">
            <h3>场景 4：先调流程再换真数据</h3>
            <p>先把“生成数据 → 写入文件 → 读取分析”这条链路调通，后续再替换成真实数据会更稳。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="faker 创建对象"
      >
        <h3>第一步：先创建 <code>Faker</code> 对象，再从对象身上取数据</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">from faker import Faker

fake = Faker("zh_CN")

print(fake.name())
print(fake.phone_number())
print(fake.address())
print(fake.company())</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>Faker("zh_CN")</code> 表示优先生成中文环境下更常见的姓名、电话和地址格式。
          这里最关键的不是把方法名背下来，而是看懂“先创建对象，再用 <code>对象.方法()</code> 取值”的调用方式。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="faker 常用方法"
      >
        <h3>常用方法：先记住“个人资料”和“扩展资料”两大类</h3>
        <div class="command-layout chapter-six-code-grid">
          <article class="command-card chapter-six-code-card">
            <h3>个人资料类</h3>
            <pre><code class="python">print(fake.name())
print(fake.phone_number())
print(fake.address())
print(fake.email())</code></pre>
          </article>
          <article class="command-card chapter-six-code-card">
            <h3>扩展资料类</h3>
            <pre><code class="python">print(fake.company())
print(fake.job())
print(fake.city())
print(fake.date())</code></pre>
          </article>
        </div>
        <p class="section-note">
          课堂上不需要一次把所有方法全背下来。先记住：想生成什么类型的数据，就去找对应的方法；
          例如姓名用 <code>name()</code>，电话用 <code>phone_number()</code>，公司用 <code>company()</code>。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="faker 批量生成"
      >
        <h3>示例 1：把方法调用放进循环，快速生成一批学生资料</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">from faker import Faker

fake = Faker("zh_CN")

for i in range(1, 6):
    print(
        f"学号：202500{i:02d} "
        f"姓名：{fake.name()} "
        f"电话：{fake.phone_number()}"
    )</code></pre>
          </article>
        </div>
        <p class="section-note">
          这页最重要的是看懂：<code>faker</code> 本身只负责“生成一条资料”，而循环负责“重复生成很多条资料”。
          两者组合后，才真正有了批量造测试数据的能力。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="faker 配合 random"
      >
        <h3><code>faker</code> 和 <code>random</code> 怎么分工</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3><code>faker</code> 负责什么</h3>
            <p>更适合生成“像真的”资料字段，例如姓名、电话、地址、邮箱、公司、日期。</p>
          </article>
          <article class="command-card">
            <h3><code>random</code> 负责什么</h3>
            <p>更适合补充规则简单的随机值，例如成绩、课程编号、是否通过、奖项等级。</p>
          </article>
          <article class="command-card">
            <h3>课堂记忆法</h3>
            <p><code>faker</code> 负责“造资料”，<code>random</code> 负责“补字段”。前者更像素材生成器，后者更像规则随机器。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="faker 写入文件"
      >
        <h3>示例 2：生成成绩名单，并写入文本文件</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">from faker import Faker
import random

fake = Faker("zh_CN")

with open("score_list.txt", "w", encoding="utf-8") as file:
    file.write("姓名，Python成绩，电话\\n")

    for _ in range(10):
        name = fake.name()
        score = random.randint(60, 100)
        phone = fake.phone_number()
        file.write(f"{name}，{score}，{phone}\\n")</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一页把本章主线连起来了：先生成测试数据，再写入文件。等文件准备好以后，后面就可以继续练习读取、统计、分析和可视化。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="faker 综合案例"
      >
        <h3>示例 3：模拟课程报名记录</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">from faker import Faker
import random

fake = Faker("zh_CN")
courses = ["Python 程序设计", "数据分析基础", "Web 前端入门"]

for i in range(1, 6):
    record = {
        "报名编号": f"BM2025{i:03d}",
        "姓名": fake.name(),
        "课程": random.choice(courses),
        "报名日期": fake.date(),
        "联系方式": fake.phone_number()
    }
    print(record)</code></pre>
          </article>
        </div>
        <p class="section-note">
          这类案例更接近真实项目：一条数据往往不是只有姓名，而是由编号、姓名、课程、日期、联系方式等多个字段共同组成。
          <code>faker</code> 适合用来快速补全这些资料字段。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="faker 练习"
      >
        <h3>练习：生成 8 条班级通讯录数据</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>任务要求</h3>
            <p>
              用 <code>faker</code> 编写一个小程序：生成 8 条班级通讯录数据，每条至少包含姓名、电话和城市，
              再把结果写入 <code>contacts.txt</code> 文件。要求每行保存一条记录，方便后续读取查看。
            </p>
          </article>
          <article class="command-card">
            <h3>建议操作顺序</h3>
            <ol>
              <li>先导入 <code>Faker</code>，并创建 <code>fake = Faker("zh_CN")</code>。</li>
              <li>使用 <code>for</code> 循环重复生成 8 条资料。</li>
              <li>在循环中调用 <code>fake.name()</code>、<code>fake.phone_number()</code>、<code>fake.city()</code>。</li>
              <li>使用 <code>with open(...)</code> 把每条记录写入文件。</li>
              <li>写完后打开文件，检查是否真的生成了 8 行内容。</li>
            </ol>
          </article>
          <article class="command-card">
            <h3>关键提示</h3>
            <p>
              这题的重点不在于字段越多越好，而在于看懂完整流程：
              “创建对象 → 调用方法生成资料 → 用循环批量处理 → 写入文件保存”。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="faker 练习答案"
      >
        <h3><code>faker</code> 练习参考答案：生成班级通讯录</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">from faker import Faker

fake = Faker("zh_CN")

with open("contacts.txt", "w", encoding="utf-8") as file:
    for i in range(1, 9):
        name = fake.name()
        phone = fake.phone_number()
        city = fake.city()
        file.write(f"{i}. {name}，{phone}，{city}\\n")</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="jieba 模块"
      >
        <div class="section-head">
          <p class="kicker">JIEBA</p>
          <h2><code>jieba</code>：先把中文切开，再谈统计分析</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>中文文本和英文文本有一个很大的不同。</strong>
          英文单词之间通常有空格，程序比较容易识别边界；中文句子往往是连在一起的，
          如果不先分词，程序就很难知道哪里是“一个完整的词”。所以做中文词频、关键词提取、搜索和词云之前，
          常常都要先经过 <code>jieba</code> 这一步。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>先切词</h3>
            <p>把整段中文拆成一个个更适合处理的词语列表，这是后续统计分析的入口。</p>
          </article>
          <article class="concept-card">
            <h3>再统计</h3>
            <p>分词之后，才能进一步做词频、关键词、搜索命中和文本可视化。</p>
          </article>
          <article class="concept-card">
            <h3>注意歧义</h3>
            <p>同样一串汉字，边界不同，含义就可能完全不同，这正是中文分词的难点。</p>
          </article>
          <article class="concept-card">
            <h3>可自定义</h3>
            <p>遇到人名、地名、课程名、网络梗时，可以手动加入自定义词，让结果更贴近真实语义。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 为什么要分词"
      >
        <h3>先理解一个根本问题：中文为什么需要分词</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>英文常有空格</h3>
            <p><code>I love Python</code> 里，程序看到空格，比较容易判断 <code>I</code>、<code>love</code>、<code>Python</code> 是三个词。</p>
          </article>
          <article class="command-card">
            <h3>中文通常连写</h3>
            <p><code>我喜欢Python课程</code> 里没有天然空格，程序必须自己判断到底该切成哪些词。</p>
          </article>
          <article class="command-card">
            <h3>理解重点</h3>
            <p>中文分词就是在连续汉字里找边界。边界找对了，后面的统计才有意义；边界找错了，后面的分析就会偏掉。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 基础分词"
      >
        <h3>基础示例：先用 <code>jieba.lcut()</code> 把一句话切开</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba

# 准备一段中文文本
text = "人工智能课程项目训练非常重要"
# lcut() 会直接返回一个列表
words = jieba.lcut(text)
# 打印分词结果
print(words)</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>lcut()</code> 返回的是列表，适合入门阶段使用，因为结果能直接看到、直接打印、直接参与后续循环和统计。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba cut 和 lcut"
      >
        <h3><code>cut()</code> 和 <code>lcut()</code> 的区别要先分清</h3>
        <div class="command-layout chapter-six-code-grid">
          <article class="command-card chapter-six-code-card">
            <h3><code>cut()</code></h3>
            <pre><code class="python">import jieba

text = "中文文本分析很有趣"
# cut() 返回的是一个可迭代对象
result = jieba.cut(text)

print(result)
# 转成列表后更容易观察结果
print(list(result))</code></pre>
          </article>
          <article class="command-card chapter-six-code-card">
            <h3><code>lcut()</code></h3>
            <pre><code class="python">import jieba

text = "中文文本分析很有趣"
# lcut() 直接返回列表
result = jieba.lcut(text)

print(result)</code></pre>
          </article>
        </div>
        <p class="section-note">
          简单记忆就行：<code>cut()</code> 更像“边切边给”，<code>lcut()</code> 直接给出完整列表。做课堂演示和初学练习时，通常优先用 <code>lcut()</code>。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 梗图原图"
      >
        <h3>先看原图：连续汉字一旦换一种切法，意思就会变</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-meme-card">
            <img
              class="chapter-six-meme chapter-six-meme--large"
              :src="jiebaMemeSrc"
              alt="用于说明中文分词歧义的但丁丁真梗图"
            />
            <p class="chapter-six-meme-caption">
              连续出现“但丁”“丁真”“真是”这类片段时，词语边界一旦变化，整句话的理解方向就会跟着变化。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 梗图案例"
      >
        <h3>案例：把梗图文字交给 <code>jieba</code>，观察它是怎么切词的</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba

# 让代码里的文本和梗图保持一样的换行顺序
text = """你记住
但丁是意大利人
但丁真是中国人
但丁真去过地狱
但丁真没去过地狱
但丁真是妈妈生的
但丁真也是妈妈生的
但但丁丁真真是三个人
但但丁丁真真是两个人"""

# 观察默认分词结果
words = jieba.lcut(text)
print(words)</code></pre>
          </article>
        </div>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>为什么这个梗适合讲分词</h3>
            <p>因为这里连续出现了 <code>但丁</code>、<code>丁真</code>、<code>真是</code> 这几类容易“重新切边界”的片段，同一串字换一种切法，意思就会变。</p>
          </article>
          <article class="command-card">
            <h3>观察重点</h3>
            <p>从这个例子里可以直接看到：中文不是天然按一个字一个字去理解，而是要尽量切成更合理的词。程序也在做这件事，但它不一定总能一次切对。</p>
          </article>
          <article class="command-card">
            <h3>理解提示</h3>
            <p>这一页不必把梗完全解释清楚，更重要的是记住“分词本质上是在判断边界，边界不同，语义就不同”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 自定义词"
      >
        <h3>遇到人名、专有名词和网络梗时，可以手动加词</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba

text = """但丁真是中国人
但丁真去过地狱"""

# 先看默认分词结果
print("默认分词：", jieba.lcut(text))

# 把希望优先识别的词加入词典
jieba.add_word("但丁")
jieba.add_word("丁真")

# 再次分词，比较前后差异
print("加入词语后：", jieba.lcut(text))</code></pre>
          </article>
        </div>
        <p class="section-note">
          当默认词典不能很好识别课堂里的专有词、人名、地名或课程术语时，<code>add_word()</code> 很有用。
          这也是把“通用工具”调成“更贴合当前任务工具”的常见做法。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 搜索模式"
      >
        <h3>普通模式和搜索模式：切词颗粒度并不一样</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba

text = "人工智能课程项目训练"

# 普通模式：更适合一般阅读和统计
print("普通模式：", jieba.lcut(text))
# 搜索模式：会切得更细一些
print("搜索模式：", jieba.lcut_for_search(text))</code></pre>
          </article>
        </div>
        <p class="section-note">
          搜索模式会给出更细的切分结果，适合搜索命中、检索提示这类场景。课堂里先知道“不同模式会产生不同粒度的词”就够了。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 词频统计"
      >
        <h3>示例 1：分词之后统计词频</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba

text = "数据分析很重要，文本分析也很重要，词频统计尤其重要"
# 先分词，得到词语列表
words = jieba.lcut(text)

# 用字典统计每个词出现的次数
counts = {}
for word in words:
    # 只统计长度大于 1 的词
    if len(word) &gt; 1:
        counts[word] = counts.get(word, 0) + 1

print(counts)</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一页要看懂顺序：先分词，再循环，再计数。词频统计不是直接对整段句子做的，而是对“分好词后的列表”做的。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 过滤词语"
      >
        <h3>示例 2：过滤掉太短或价值不大的词</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba

text = "这门课程很有趣，这门课程的案例也很有趣"
words = jieba.lcut(text)

# 准备一个新列表，保存筛选后的词
result = []
for word in words:
    # 过滤掉太短的词，以及不想保留的词
    if len(word) &gt; 1 and word not in ["这门", "也很"]:
        result.append(word)

print(result)</code></pre>
          </article>
        </div>
        <p class="section-note">
          不是所有分出来的词都值得保留。为了让统计结果更聚焦，常常要去掉无意义或信息量太低的词，这一步叫做过滤。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 文件分词"
      >
        <h3>示例 3：读取文本文件，再做分词</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba

# 先读取文件中的中文文本
with open("comments.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 再对读取到的内容做分词
words = jieba.lcut(text)
# 只打印前 20 个词，便于观察
print(words[:20])</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一步和本章前面的文件操作直接连上了。真实任务里，文本通常不是写死在变量里，而是从文件中读取出来后再分词处理。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 练习"
      >
        <h3>练习：分析“但丁 / 丁真”梗图文本的分词结果</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>任务要求</h3>
            <p>
              对下面这段文本先用 <code>jieba.lcut()</code> 做默认分词，
              再使用 <code>jieba.add_word()</code> 加入至少两个自定义词，比较前后结果有什么变化。
            </p>
            <pre><code class="text">你记住
但丁是意大利人
但丁真是中国人
但丁真去过地狱
但丁真没去过地狱
但丁真是妈妈生的
但丁真也是妈妈生的
但但丁丁真真是三个人
但但丁丁真真是两个人</code></pre>
          </article>
          <article class="command-card">
            <h3>建议操作顺序</h3>
            <ol>
              <li>先把题目里给出的文本复制到字符串变量 <code>text</code> 中。</li>
              <li>调用 <code>jieba.lcut(text)</code>，打印默认分词结果。</li>
              <li>加入 <code>但丁</code>、<code>丁真</code> 这类自定义词。</li>
              <li>再次分词，并观察前后差异。</li>
              <li>最后用自己的话解释：为什么这个例子适合说明中文分词的难点。</li>
            </ol>
          </article>
          <article class="command-card">
            <h3>关键提示</h3>
            <p>
              这题不要求得到唯一“标准答案”，更重要的是看懂：
              分词结果会受到上下文和词典影响，必要时需要人工补充词语。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="jieba 练习答案"
      >
        <h3><code>jieba</code> 练习参考答案：比较默认分词和加词后的结果</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba

text = """你记住
但丁是意大利人
但丁真是中国人
但丁真去过地狱
但丁真没去过地狱
但丁真是妈妈生的
但丁真也是妈妈生的
但但丁丁真真是三个人
但但丁丁真真是两个人"""

# 先看默认分词
print("默认分词：")
print(jieba.lcut(text))

# 加入希望优先识别的词语
jieba.add_word("但丁")
jieba.add_word("丁真")

# 再比较加词后的结果
print("加词后：")
print(jieba.lcut(text))</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="wordcloud 模块"
      >
        <div class="section-head">
          <p class="kicker">WORDCLOUD</p>
          <h2><code>wordcloud</code>：把高频词变成一张真正能看的图</h2>
        </div>
        <p class="chapter-six-cue">
          <strong>词云不是把文字随便堆在一起。</strong>
          它背后先要有文本，再要有分词、过滤、统计，最后才是可视化。
          这一部分特别适合用来展示“哪些词最常出现、哪些主题最值得关注”。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>先有文本</h3>
            <p>文本可以来自课程反馈、梗图句子、校园活动总结、阅读笔记或调查问卷。</p>
          </article>
          <article class="concept-card">
            <h3>再做分词</h3>
            <p>中文通常要先用 <code>jieba</code> 切词，否则整段中文不能直接拿来做高质量词云。</p>
          </article>
          <article class="concept-card">
            <h3>然后调样式</h3>
            <p>尺寸、颜色、背景、轮廓、最大词数、遮罩图形都会直接影响最后的视觉效果。</p>
          </article>
          <article class="concept-card">
            <h3>最后导出图片</h3>
            <p>生成后的词云可以保存为 PNG，用于报告、课件、海报或数据展示。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud 基础示例"
      >
        <h3>基础示例：先看最简单的词云是怎么生成的</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">from wordcloud import WordCloud

# 准备一段已经用空格分开的文本
text = "Python Python data analysis file module module wordcloud"

# 创建词云对象
wc = WordCloud(
    width=800,
    height=400,
    background_color="white"
)

# 根据文本生成词云
wc.generate(text)
# 保存为图片
wc.to_file("wordcloud_basic.png")</code></pre>
          </article>
        </div>
        <p class="section-note">
          这一页先看最基础的生成流程：准备文本，创建 <code>WordCloud</code> 对象，调用 <code>generate()</code>，最后用 <code>to_file()</code> 输出图片。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud 中文处理"
      >
        <h3>中文词云通常要先分词，再指定中文字体</h3>
        <div class="command-layout chapter-six-code-grid">
          <article class="command-card chapter-six-code-card">
            <h3>不分词时</h3>
            <pre><code class="python">from wordcloud import WordCloud

text = "人工智能课程项目训练非常重要"

wc = WordCloud(font_path="msyh.ttc", background_color="white")
wc.generate(text)
wc.to_file("cn_no_cut.png")</code></pre>
          </article>
          <article class="command-card chapter-six-code-card">
            <h3>分词后</h3>
            <pre><code class="python">import jieba
from wordcloud import WordCloud

text = "人工智能课程项目训练非常重要"
words = jieba.lcut(text)
result = " ".join(words)

wc = WordCloud(font_path="msyh.ttc", background_color="white")
wc.generate(result)
wc.to_file("cn_cut.png")</code></pre>
          </article>
        </div>
        <p class="section-note">
          中文词云通常要先分词，再用空格连接成字符串。除此之外，还要指定 <code>font_path</code>，否则很多系统里会出现中文显示不出来的问题。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud 常用参数"
      >
        <h3>常用参数：先看懂大小、背景、轮廓和词数上限</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3><code>width</code> / <code>height</code></h3>
            <p>决定图片画布大小。画布越大，词云越清晰，适合导出到报告或海报。</p>
          </article>
          <article class="command-card">
            <h3><code>background_color</code></h3>
            <p>决定背景颜色。最常见的是白底，也可以换成浅色背景配合不同主题。</p>
          </article>
          <article class="command-card">
            <h3><code>max_words</code> / <code>contour_width</code></h3>
            <p>前者控制最多显示多少个词，后者控制图形轮廓线粗细，适合配合 <code>mask</code> 一起使用。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud mask 用法"
      >
        <h3><code>mask</code> 的作用：让词云长成指定图形</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# 读取中文文本
with open("text_course_feedback.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 先分词，再拼接成词云需要的字符串
words = jieba.lcut(text)
result = " ".join(word for word in words if len(word) &gt; 1)

# 读取 mask 图像，白色区域不会绘制词云
mask = np.array(Image.open("mask_cloud.png"))

# 生成带图形轮廓的词云
wc = WordCloud(
    font_path="C:/Windows/Fonts/msyh.ttc",
    width=900,
    height=900,
    background_color="white",
    mask=mask,
    contour_width=3,
    contour_color="#0d7be8"
)
wc.generate(result)
wc.to_file("wordcloud_mask_demo.png")</code></pre>
          </article>
        </div>
        <p class="section-note">
          <code>mask</code> 本质上是在告诉程序“哪些位置可以放词，哪些位置不能放词”。这样一来，词云就不再只是一个矩形，而会长成云朵、星形、叶片、书本等轮廓。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud mask 下载"
      >
        <h3>下载区：4 张可直接使用的 <code>mask</code> 图</h3>
        <div class="command-layout chapter-six-download-grid">
          <article
            v-for="item in wordcloudMaskCards"
            :key="item.downloadHref"
            class="command-card chapter-six-resource-card"
          >
            <h3>{{ item.title }}</h3>
            <img class="chapter-six-preview chapter-six-preview--mask" :src="item.imageSrc" :alt="item.title" />
            <p>{{ item.desc }}</p>
            <a class="chapter-six-link" :href="item.downloadHref" download>下载这张 mask</a>
          </article>
        </div>
        <p class="section-note">
          这几张图都已经处理成适合 <code>wordcloud mask</code> 使用的 PNG 格式，可以直接下载后放进示例代码里。
          来源说明文件也可以一起下载查看。
          <a class="chapter-six-link" :href="wordcloudMaskSourcesHref" download>下载来源说明</a>
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud 文本下载"
      >
        <h3>下载区：5 份适合先分词再做词云的中文文本</h3>
        <div class="command-layout chapter-six-download-grid">
          <article
            v-for="item in wordcloudTextCards"
            :key="item.downloadHref"
            class="command-card chapter-six-resource-card"
          >
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
            <a class="chapter-six-link" :href="item.downloadHref" download>下载文本</a>
          </article>
        </div>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>停用词表</h3>
            <p>去掉“的、了、是、在”这类高频但信息量不大的词，词云会更聚焦。</p>
            <a class="chapter-six-link" :href="wordcloudStopwordsHref" download>下载停用词表</a>
          </article>
          <article class="command-card">
            <h3>示例脚本</h3>
            <p>把“读取文本、分词、过滤、读取 mask、生成词云”这条流程完整串起来。</p>
            <a class="chapter-six-link" :href="wordcloudMaskDemoHref" download>下载示例脚本</a>
          </article>
          <article class="command-card">
            <h3>使用顺序</h3>
            <p>先下载文本，再下载一张 mask 图，然后把两者一起放进代码里，就能练习完整的中文词云流程。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud 效果预览"
      >
        <h3>效果预览：同样是词云，换一张 <code>mask</code> 图，感觉会完全不同</h3>
        <div class="command-layout chapter-six-download-grid">
          <article
            v-for="item in wordcloudDemoCards"
            :key="item.downloadHref"
            class="command-card chapter-six-resource-card"
          >
            <h3>{{ item.title }}</h3>
            <img class="chapter-six-preview chapter-six-preview--cloud" :src="item.imageSrc" :alt="item.title" />
            <a class="chapter-six-link" :href="item.downloadHref" download>下载示例图</a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud 过滤文本"
      >
        <h3>不要急着直接生成，先过滤掉信息量太低的词</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba

with open("text_course_feedback.txt", "r", encoding="utf-8") as file:
    text = file.read()

with open("stopwords_basic.txt", "r", encoding="utf-8") as file:
    stopwords = {line.strip() for line in file if line.strip()}

words = []
for word in jieba.lcut(text):
    word = word.strip()
    # 过滤掉长度太短或停用词表中的词
    if len(word) &gt; 1 and word not in stopwords:
        words.append(word)

result = " ".join(words)
print(result)</code></pre>
          </article>
        </div>
        <p class="section-note">
          如果不过滤，词云里往往会出现很多“的、是、在、了”这类高频词。过滤之后，真正有信息量的词才能更突出。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud 综合示例"
      >
        <h3>综合示例：读取文本、分词、过滤、套用 mask，一次完成</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# 读取课程反馈文本
with open("text_course_feedback.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 读取停用词表
with open("stopwords_basic.txt", "r", encoding="utf-8") as file:
    stopwords = {line.strip() for line in file if line.strip()}

# 分词并过滤
words = []
for word in jieba.lcut(text):
    word = word.strip()
    if len(word) &gt; 1 and word not in stopwords:
        words.append(word)
result = " ".join(words)

# 读取云朵 mask
mask = np.array(Image.open("mask_cloud.png"))

# 生成词云
wc = WordCloud(
    font_path="C:/Windows/Fonts/msyh.ttc",
    width=900,
    height=900,
    background_color="white",
    mask=mask,
    contour_width=3,
    contour_color="#0d7be8",
    max_words=120
)
wc.generate(result)
wc.to_file("course_feedback_cloud.png")</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud 练习"
      >
        <h3>练习：下载一份文本和一张 <code>mask</code>，做出自己的主题词云</h3>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>任务要求</h3>
            <p>
              从下载区任选 1 份文本和 1 张 <code>mask</code> 图，先完成中文分词和停用词过滤，
              再生成一张带图形轮廓的词云图片。词云图片至少要体现：中文字体、图形轮廓、较清晰的高频词。
            </p>
          </article>
          <article class="command-card">
            <h3>建议操作顺序</h3>
            <ol>
              <li>先下载一份文本，例如 <code>text_campus_life.txt</code>。</li>
              <li>再下载一张 mask 图，例如 <code>mask_leaf.png</code>。</li>
              <li>用 <code>jieba.lcut()</code> 完成分词，并结合停用词表做过滤。</li>
              <li>用 <code>Image.open()</code> 和 <code>np.array()</code> 读取 mask。</li>
              <li>创建 <code>WordCloud</code> 对象，补上 <code>font_path</code>、<code>mask</code>、<code>contour_width</code> 等参数。</li>
              <li>调用 <code>generate()</code> 后再用 <code>to_file()</code> 导出图片。</li>
            </ol>
          </article>
          <article class="command-card">
            <h3>关键提示</h3>
            <p>
              这一题不是只比谁颜色好看，更重要的是把“文本处理”和“图形展示”连起来。
              词云效果好不好，往往先取决于分词和过滤，再取决于颜色和轮廓。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="wordcloud 练习答案"
      >
        <h3><code>wordcloud</code> 练习参考答案：叶片形校园生活词云</h3>
        <div class="command-layout chapter-six-single-code">
          <article class="command-card chapter-six-code-card">
            <pre><code class="python">import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# 读取校园生活文本
with open("text_campus_life.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 读取停用词表
with open("stopwords_basic.txt", "r", encoding="utf-8") as file:
    stopwords = {line.strip() for line in file if line.strip()}

# 分词并过滤
words = []
for word in jieba.lcut(text):
    word = word.strip()
    if len(word) &gt; 1 and word not in stopwords:
        words.append(word)
result = " ".join(words)

# 读取叶片 mask
mask = np.array(Image.open("mask_leaf.png"))

# 生成词云
wc = WordCloud(
    font_path="C:/Windows/Fonts/msyh.ttc",
    width=900,
    height=900,
    background_color="white",
    mask=mask,
    contour_width=3,
    contour_color="#2d8a4b",
    max_words=100
)
wc.generate(result)
wc.to_file("campus_life_leaf_cloud.png")</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="实验3"
      >
        <div class="section-head">
          <p class="kicker">EXPERIMENT 03</p>
          <h2>实验3：词云展示 2022 年政府工作报告关键词</h2>
        </div>
        <p class="chapter-six-cue">
          这个实验直接对应实验报告 3 和实验指导书中的实验项目三。
          需要读取《2022年政府工作报告》文本，使用 <code>jieba</code> 做中文分词与关键词统计，
          再用 <code>wordcloud</code> 生成词云图片，最后把实验目的、过程、结果和分析整理到实验报告中。
        </p>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>实验目的</h3>
            <p>练习文本读取、字典统计、中文分词和词云生成，把文件操作与外置模块真正串起来使用。</p>
          </article>
          <article class="concept-card">
            <h3>文本主题</h3>
            <p>通过关键词统计观察政府工作报告的主题词，理解高频词怎样反映经济、发展、就业、创新、民生等重点内容。</p>
          </article>
          <article class="concept-card">
            <h3>实验要求</h3>
            <p>正确读取给定文本，正确使用 <code>jieba</code> 和 <code>wordcloud</code>，并能输出词云图片。</p>
          </article>
          <article class="concept-card">
            <h3>交付内容</h3>
            <p>至少准备 3 项结果：实验源代码、词云图片 <code>government_report_cloud.png</code>、实验报告。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验3原理与流程"
      >
        <h3>实验3原理与流程</h3>
        <div class="concept-grid chapter-six-quad-grid">
          <article class="concept-card">
            <h3>步骤 1：读取文本</h3>
            <p>使用 <code>open()</code> 和 <code>read()</code> 读取《2022年政府工作报告.txt》，让长文本先进入程序。</p>
          </article>
          <article class="concept-card">
            <h3>步骤 2：精确分词</h3>
            <p>使用 <code>jieba.lcut()</code> 进行精确模式分词，把连续中文文本拆成一个个词语。</p>
          </article>
          <article class="concept-card">
            <h3>步骤 3：统计词频</h3>
            <p>创建字典，使用 <code>counts[word] = counts.get(word, 0) + 1</code> 统计关键词出现次数，并结合停用词表过滤无意义词语。</p>
          </article>
          <article class="concept-card">
            <h3>步骤 4：生成词云</h3>
            <p>创建 <code>WordCloud</code> 对象，使用 <code>generate_from_frequencies()</code> 按词频生成词云，再保存为图片。</p>
          </article>
        </div>
        <p class="section-note">
          先观察前 20 个高频词，再生成词云。这样可以先判断分词和过滤是否合理，避免词云图做出来了，
          关键词却不准确。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验3代码骨架"
      >
        <h3>实验3代码骨架：政府工作报告关键词词云</h3>
        <pre><code class="python">import jieba
from wordcloud import WordCloud

# 读取政府工作报告文本
with open("2022年政府工作报告.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 读取停用词表
with open("stopwords_basic.txt", "r", encoding="utf-8") as file:
    stopwords = {line.strip() for line in file if line.strip()}

# 使用精确模式分词
words = jieba.lcut(text)

# 创建字典，统计每个关键词出现的次数
counts = {}
for word in words:
    # 单字词通常信息量较小，先跳过
    if len(word) == 1:
        continue
    # 停用词不参与统计
    if word in stopwords:
        continue
    counts[word] = counts.get(word, 0) + 1

# 按出现次数从高到低排序，方便先观察结果
items = list(counts.items())
items.sort(key=lambda item: item[1], reverse=True)

print("出现次数最多的前 20 个关键词：")
for word, count in items[:20]:
    print(word, count)

# 创建词云对象
wc = WordCloud(
    font_path="msyh.ttc",
    width=1000,
    height=600,
    max_words=150,
    background_color="white",
)

# 按词频生成词云，并保存图片
wc.generate_from_frequencies(dict(items[:150]))
wc.to_file("government_report_cloud.png")</code></pre>
        <p class="section-note">
          这段代码和实验指导书的主线一致：读取文本、精确分词、字典计数、排序观察、按词频生成词云。
          如果脚本和素材文件不在同一个文件夹中，就需要把文件路径改成自己的实际路径。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验3素材下载"
      >
        <h3>实验3素材下载</h3>
        <div class="command-layout chapter-six-download-grid">
          <article class="command-card chapter-six-highlight-card chapter-six-resource-card">
            <h3>政府工作报告文本</h3>
            <p>先下载实验用原始文本，再把它和 Python 脚本放在同一个文件夹里，方便直接读取。</p>
            <a class="chapter-six-link" :href="exp3TextHref" download>下载《2022年政府工作报告.txt》</a>
          </article>
          <article class="command-card chapter-six-resource-card">
            <h3>停用词表</h3>
            <p>停用词表可以去掉“的、了、是、在”等高频虚词，让词云更聚焦于真正有信息量的关键词。</p>
            <a class="chapter-six-link" :href="wordcloudStopwordsHref" download>下载停用词表</a>
          </article>
          <article class="command-card chapter-six-resource-card">
            <h3>文件摆放建议</h3>
            <p>建议把 <code>2022年政府工作报告.txt</code>、<code>stopwords_basic.txt</code> 和实验代码文件放在同一目录，这样代码里的文件名可以直接使用。</p>
          </article>
          <article class="command-card chapter-six-resource-card">
            <h3>输出文件建议</h3>
            <p>建议生成并保留 <code>government_report_cloud.png</code>，后续写实验报告时可以直接插入运行结果截图。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验3报告与提交"
      >
        <h3>实验报告下载与提交</h3>
        <div class="command-layout chapter-six-download-grid">
          <article class="command-card chapter-six-highlight-card chapter-six-resource-card">
            <h3>实验报告 3</h3>
            <p>按实验要求完成代码、保存词云结果，并在实验报告中整理实验目的、实验过程、运行结果和分析结论。</p>
            <a class="chapter-six-link" :href="exp3ReportHref" download>
              下载实验报告3：词云展示2022年政府工作报告关键词
            </a>
          </article>
          <article class="command-card chapter-six-resource-card">
            <h3>实验过程怎么写</h3>
            <p>可以按“读取文本 -> 分词 -> 过滤停用词 -> 统计词频 -> 生成词云 -> 保存图片”的顺序描述，不要只贴代码，不写过程说明。</p>
          </article>
          <article class="command-card chapter-six-resource-card">
            <h3>实验结果怎么分析</h3>
            <p>重点不在于颜色是否花哨，而在于关键词是否准确、主题是否清晰，以及高频词能不能反映报告的核心内容。</p>
          </article>
          <article class="command-card chapter-six-resource-card">
            <h3>实验报告提交</h3>
            <p>完成代码、词云图片和实验分析后，将实验报告提交到 WPS 收集表。提交前先检查报告中的代码、运行结果截图和分析是否完整。</p>
            <a
              class="chapter-six-link"
              :href="exp3SubmitHref"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ exp3SubmitHref }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章总结"
      >
        <h2>本章总结：程序开始真正具备“保存、拆分、扩展”的能力</h2>
        <div class="command-layout chapter-six-2plus1">
          <article class="command-card">
            <h3>文件操作</h3>
            <p>解决的是“数据如何进出程序”。会读、会写、会追加、会处理编码，程序才不只是一次性演示。</p>
          </article>
          <article class="command-card">
            <h3>模块</h3>
            <p>解决的是“代码如何组织”。会拆模块，程序结构才会越来越清楚，而不是越来越乱。</p>
          </article>
          <article class="command-card">
            <h3>模块库</h3>
            <p>解决的是“功能如何快速扩展”。从标准库到外置库，真正的开发不是一切都自己从零造轮子。</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课堂关键词：把结果保存进文件，把功能拆进模块，把常用问题交给成熟工具库。</p>
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
.page.is-slide-deck .chapter-six-rhythm {
  margin-top: 14px;
  display: grid;
  gap: 10px;
}

.page.is-slide-deck .chapter-six-rhythm--four {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.page.is-slide-deck .chapter-six-rhythm span {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(13, 123, 232, 0.18);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.95), rgba(245, 251, 255, 0.98));
  color: #0b4f88;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
}

.page.is-slide-deck .chapter-six-cue {
  margin: 10px 0 0;
  padding: 10px 12px;
  border-left: 4px solid rgba(13, 123, 232, 0.45);
  border-radius: 10px;
  background: rgba(13, 123, 232, 0.06);
  color: var(--text-main);
  font-size: 0.94rem;
  line-height: 1.65;
}

.page.is-slide-deck .chapter-six-cue strong {
  color: #0a5eaf;
}

.page.is-slide-deck .command-layout.chapter-six-2plus1 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .command-layout.chapter-six-2plus1 > :last-child {
  grid-column: 1 / -1;
}

.page.is-slide-deck .command-layout.chapter-six-math-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  align-items: start;
}

.page.is-slide-deck .concept-grid.chapter-six-quad-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .concept-grid.chapter-six-quad-grid > .concept-card {
  grid-column: span 1;
}

.page.is-slide-deck .command-layout.chapter-six-code-grid {
  grid-template-columns: 1fr;
  align-items: start;
}

.page.is-slide-deck .command-layout.chapter-six-download-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: start;
}

.page.is-slide-deck .command-layout.chapter-six-single-code {
  grid-template-columns: 1fr;
}

.page.is-slide-deck .command-layout.chapter-six-practice-grid {
  grid-template-columns: 1fr;
  align-items: start;
}

.page.is-slide-deck .chapter-six-task-card,
.page.is-slide-deck .chapter-six-code-card {
  height: 100%;
}

.page.is-slide-deck .chapter-six-resource-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
}

.page.is-slide-deck .chapter-six-resource-card p {
  margin: 0;
  line-height: 1.7;
}

.page.is-slide-deck .chapter-six-meme-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.page.is-slide-deck .chapter-six-preview {
  width: 100%;
  align-self: center;
  border-radius: 18px;
  border: 1px solid rgba(13, 123, 232, 0.14);
  background: #fff;
  object-fit: contain;
}

.page.is-slide-deck .chapter-six-preview--mask {
  max-width: 180px;
  max-height: 150px;
  padding: 8px;
}

.page.is-slide-deck .chapter-six-preview--cloud {
  max-width: 320px;
  max-height: 220px;
}

.page.is-slide-deck .chapter-six-meme {
  width: min(100%, 420px);
  align-self: center;
  border-radius: 18px;
  border: 1px solid rgba(13, 123, 232, 0.16);
  box-shadow: 0 16px 40px rgba(10, 40, 90, 0.12);
  background: #000;
  object-fit: contain;
}

.page.is-slide-deck .chapter-six-meme--large {
  width: min(100%, 360px);
  max-height: 62vh;
}

.page.is-slide-deck .chapter-six-meme-caption {
  margin: 0;
  color: var(--text-main);
  line-height: 1.7;
  text-align: center;
}

.page.is-slide-deck .chapter-six-task-card ol {
  margin: 0;
  padding-left: 20px;
}

.page.is-slide-deck .chapter-six-code-card pre,
.page.is-slide-deck .chapter-six-code-card .fragment {
  margin-top: 0;
}

.page.is-slide-deck .chapter-six-code-card code {
  font-size: 0.84rem;
}

.page.is-slide-deck .chapter-six-link {
  display: inline-flex;
  align-items: center;
  min-height: 36px;
  margin-top: 10px;
  color: #0a5eaf;
  font-weight: 700;
  text-decoration: underline;
  word-break: break-all;
}

.page.is-slide-deck .chapter-six-highlight-card {
  border-color: rgba(13, 123, 232, 0.28);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.94), rgba(255, 255, 255, 0.98));
}

.page.is-slide-deck .chapter-six-figure-card {
  height: 100%;
}

.page.is-slide-deck .chapter-six-figure {
  width: 100%;
  height: 170px;
  margin: 6px 0 10px;
}

.page.is-slide-deck .chapter-six-figure line,
.page.is-slide-deck .chapter-six-figure circle,
.page.is-slide-deck .chapter-six-figure rect {
  stroke: #0a5eaf;
  stroke-width: 3;
  fill: none;
}

.page.is-slide-deck .chapter-six-figure text {
  fill: #0b4f88;
  font-size: 14px;
  font-weight: 700;
}

@media (max-width: 900px) {
  .page.is-slide-deck .chapter-six-rhythm--four,
  .page.is-slide-deck .command-layout.chapter-six-2plus1,
  .page.is-slide-deck .command-layout.chapter-six-math-grid,
  .page.is-slide-deck .concept-grid.chapter-six-quad-grid,
  .page.is-slide-deck .command-layout.chapter-six-code-grid,
  .page.is-slide-deck .command-layout.chapter-six-download-grid,
  .page.is-slide-deck .command-layout.chapter-six-practice-grid {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .command-layout.chapter-six-2plus1 > :last-child,
  .page.is-slide-deck .concept-grid.chapter-six-quad-grid > .concept-card {
    grid-column: span 1;
  }
}
</style>
