<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);
const exp1ReportHref = encodeURI(
  "/courses/python/exp_reports/实验报告1：阶梯电价计算电费（理实课程实验部分）-学生姓名.docx",
);
const exp1SubmissionQrSrc = encodeURI("/courses/python/ch03/表单QR.png");
const exp1SubmissionHref = "https://f.wps.cn/g/Nm7bHL0N/";
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
      <CourseSwitcher />
    </header>

    <main id="top" class="page is-slide-deck">
      <section
        id="cover"
        class="hero reveal"
        data-outline-level="1"
        data-outline-label="章节封面"
      >
        <p class="kicker">CHAPTER 03 FLOW LOGIC</p>
        <h1>运算符与控制流程：<br />让程序开始“会判断、会重复”</h1>
        <p class="hero-intro">
          前两章我们已经会输入、存储、计算和组织数据；这一章开始，程序不再只是从上到下执行，
          而是能够根据条件做选择、根据需求重复执行、根据规则提前停止或跳过某一步。
        </p>
        <ul class="hero-checklist">
          <li>理解运算符为什么是 <strong>if</strong> 和循环的地基，而不是孤立的符号表。</li>
          <li>学会把现实规则翻译成 <strong>if / elif / else</strong> 分支结构。</li>
          <li>掌握 <strong>while / for / 嵌套循环 / break / continue</strong> 的使用场景。</li>
        </ul>
        <div class="goal-cards fly-in-seq">
          <article>
            <h2>能力目标 1</h2>
            <p>会读表达式结果，知道什么时候得到数值，什么时候得到布尔值。</p>
          </article>
          <article>
            <h2>能力目标 2</h2>
            <p>会写分支和循环，不把代码写成只会顺序执行的“流水账”。</p>
          </article>
          <article>
            <h2>能力目标 3</h2>
            <p>会定位常见逻辑错误：条件写错、边界写错、循环停不下来。</p>
          </article>
        </div>
      </section>

      <section
        id="roadmap"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务简报：程序开始会思考"
      >
        <h2>任务简报：程序为什么要“判断”和“重复”</h2>
        <p class="section-note">
          如果程序只能顺序执行，它就很难像真实系统一样处理变化中的输入。第三章要解决的是：
          <strong>什么时候走这条路，什么时候反复做同一件事，什么时候提前停下来。</strong>
        </p>
        <div class="command-layout">
          <article class="command-card">
            <h3>顺序执行</h3>
            <p>前两章大多数程序都像清单：第 1 行做完，再做第 2 行，再做第 3 行。</p>
            <p>这类程序适合“固定流程”，但不擅长处理变化。</p>
          </article>
          <article class="command-card">
            <h3>遇到判断</h3>
            <p>例如：分数是否及格、口令是否正确、背包里是否有钥匙。</p>
            <p>这时候程序必须先算出条件，再决定接下来走哪个分支。</p>
          </article>
          <article class="command-card">
            <h3>遇到重复</h3>
            <p>例如：反复输入直到合法、统计全班成绩、打印九九乘法表。</p>
            <p>这时候程序不能只写一遍，而要把动作交给循环结构。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章能力地图"
      >
        <div class="section-head">
          <p class="kicker">LEARNING MAP</p>
          <h2>本章能力地图：先算，再判，再循环</h2>
        </div>
        <div class="concept-grid">
          <article class="concept-card">
            <h3>表达式</h3>
            <p>运算符把数据组合起来，得到数值结果或布尔结果。</p>
          </article>
          <article class="concept-card">
            <h3>条件</h3>
            <p>if 读取条件真假，让程序在不同分支之间做选择。</p>
          </article>
          <article class="concept-card">
            <h3>重复</h3>
            <p>while 盯条件，for 盯次数或数据，两者都负责“反复执行”。</p>
          </article>
          <article class="concept-card">
            <h3>控制</h3>
            <p>break 和 continue 让循环可以中途结束或跳过当前轮次。</p>
          </article>
        </div>
        <p class="section-note">
          这一章最重要的不是把语法背下来，而是形成一条固定思路：
          <strong>先看问题里有没有条件，再看有没有重复，最后选对结构。</strong>
        </p>
      </section>

      <section
        id="operators-overview"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 1：运算符与表达式"
      >
        <h2>任务 1：运算符与表达式</h2>
        <p class="section-note">
          运算符不是为了背诵而存在，它们真正的作用是把数据加工成结果，再把结果交给
          <code>if</code> 或循环结构使用。
        </p>
        <div class="chapter-three-rhythm">
          <span>先看表达式算出什么</span>
          <span>再区分数值和布尔值</span>
          <span>最后再进入条件判断</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="六类常用运算符"
      >
        <h3>六类常用运算符</h3>
        <p class="chapter-three-cue">
          <strong>先观察：</strong>这一页先记“作用”，不用急着把所有符号一次背完。后面每一类都会在
          <code>if</code> 或循环里反复出现。
        </p>
        <div class="table-wrap">
          <table class="ops-table">
            <thead>
              <tr>
                <th>类别</th>
                <th>典型符号</th>
                <th>作用</th>
                <th>课堂例子</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>算术运算符</td>
                <td class="ops-symbol"><code>+</code> <code>-</code> <code>*</code> <code>/</code> <code>//</code> <code>%</code></td>
                <td>做数值计算</td>
                <td><code>damage = atk * 2</code></td>
              </tr>
              <tr>
                <td>比较运算符</td>
                <td class="ops-symbol"><code>&gt;</code> <code>&lt;</code> <code>&gt;=</code> <code>&lt;=</code> <code>==</code> <code>!=</code></td>
                <td>比较大小或是否相等</td>
                <td><code>score &gt;= 60</code></td>
              </tr>
              <tr>
                <td>逻辑运算符</td>
                <td class="ops-symbol"><code>and</code> <code>or</code> <code>not</code></td>
                <td>组合多个条件</td>
                <td><code>age &gt;= 18 and has_id</code></td>
              </tr>
              <tr>
                <td>赋值运算符</td>
                <td class="ops-symbol"><code>=</code> <code>+=</code> <code>-=</code> <code>*=</code></td>
                <td>保存或更新变量值</td>
                <td><code>total += score</code></td>
              </tr>
              <tr>
                <td>成员运算符</td>
                <td class="ops-symbol"><code>in</code> <code>not in</code></td>
                <td>判断元素是否存在</td>
                <td><code>"钥匙" in bag</code></td>
              </tr>
              <tr>
                <td>身份运算符</td>
                <td class="ops-symbol"><code>is</code> <code>is not</code></td>
                <td>判断是不是同一个对象</td>
                <td><code>cache is None</code></td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="section-note">
          初学阶段要记住一个安全原则：<strong>比较值是否相等，用 <code>==</code>；<code>is</code> 先只和 <code>None</code> 一起使用。</strong>
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="表达式如何变成条件"
      >
        <h3>表达式如何变成条件</h3>
        <p class="chapter-three-cue">
          <strong>先预测：</strong>看三段代码最后一行会输出什么，再用“数值结果 / 布尔结果”给它们分类。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>数值结果</h3>
            <pre><code class="python">atk = 12
buff = 1.5
damage = atk * buff  # 先计算乘法
print(damage)  # 再输出结果 18.0</code></pre>
            <p>执行顺序是先算右侧表达式，再把结果保存到 <code>damage</code>。</p>
          </article>
          <article class="command-card">
            <h3>布尔结果</h3>
            <pre><code class="python">score = 82
passed = score &gt;= 60  # 比较结果是布尔值
print(passed)  # True 表示条件成立</code></pre>
            <p>比较表达式不会得到新的分数，而是得到 <code>True</code> 或 <code>False</code>。</p>
          </article>
          <article class="command-card">
            <h3>条件组合</h3>
            <pre><code class="python">score = 82
has_ticket = True
can_enter = score &gt;= 60 and has_ticket
print(can_enter)  # 两个条件都成立才为 True</code></pre>
            <p><code>and</code> 表示“并且”，只有两个条件同时满足，结果才是 <code>True</code>。</p>
          </article>
        </div>
        <p class="section-note">
          先预测结果，再运行验证。难点往往不在于输入代码，而在于
          <strong>先判断表达式到底会得到什么结果。</strong>
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="优先级、括号与链式比较"
      >
        <h3>优先级、括号与链式比较</h3>
        <p class="chapter-three-cue">
          <strong>阅读顺序：</strong>先看括号是否改变了计算顺序，再看这一行代码最终是在判断“大小”、 “区间”还是“成员关系”。
        </p>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>优先级</h3>
            <p>复杂表达式里，运算顺序会影响结果。拿不准时，优先加括号。</p>
            <pre><code class="python">result = 3 + 2 * 5     # 13
result = (3 + 2) * 5   # 25</code></pre>
            <p>第一行先算乘法，第二行因为有括号，所以先算加法。</p>
          </article>
          <article class="concept-card">
            <h3>逻辑可读性</h3>
            <p>条件一复杂，可读性比“少写几个括号”更重要。</p>
            <pre><code class="python">ok = (score &gt;= 60) and (age &gt;= 18)</code></pre>
            <p>括号把两个子条件分开后，阅读时更容易看出“及格”与“成年”是并列关系。</p>
          </article>
          <article class="concept-card">
            <h3>链式比较</h3>
            <p>Python 支持把区间判断写得更自然。</p>
            <pre><code class="python">if 60 &lt;= score &lt; 90:
    print("良好")</code></pre>
            <p>这一句等价于“<code>score &gt;= 60</code> 并且 <code>score &lt; 90</code>”。</p>
          </article>
          <article class="concept-card">
            <h3>成员判断</h3>
            <p>写菜单、口令白名单、背包检查时很常用。</p>
            <pre><code class="python">cmd = input("指令: ")
if cmd in ["1", "2", "q"]:
    print("有效输入")</code></pre>
            <p>这里不是比较某一个固定值，而是检查输入是否属于允许的那一组数据。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="三个最容易混淆的坑"
      >
        <h3>三个最容易混淆的坑</h3>
        <p class="chapter-three-cue">
          <strong>做题前先排查：</strong><code>=</code> 和 <code>==</code> 有没有混用，<code>input()</code> 的结果有没有先做类型转换。
        </p>
        <div class="pitfall-grid compact-grid">
          <article class="pitfall">
            <h3>1) <code>=</code> 和 <code>==</code></h3>
            <p class="problem">问题：把赋值和比较混为一谈。</p>
            <p class="solution">结论：<code>=</code> 是“把值放进去”，<code>==</code> 是“问它们是否相等”。</p>
          </article>
          <article class="pitfall">
            <h3>2) <code>is</code> 和 <code>==</code></h3>
            <p class="problem">问题：把“值相等”误写成“同一对象”。</p>
            <p class="solution">结论：初学阶段，判断相等用 <code>==</code>；判断空值常写 <code>value is None</code>。</p>
          </article>
          <article class="pitfall">
            <h3>3) <code>input()</code> 默认是字符串</h3>
            <p class="problem">问题：输入 <code>18</code>，以为拿到的是整数 18。</p>
            <p class="solution">结论：参与数值比较或计算前，先用 <code>int()</code> 或 <code>float()</code> 转换。</p>
          </article>
        </div>
      </section>

      <section
        id="if-structure"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 2：选择结构 if"
      >
        <h2>任务 2：选择结构 if</h2>
        <p class="section-note">
          <code>if</code> 的本质不是“语法块”，而是把现实规则写进程序。只要题目里出现
          “如果……否则……”，通常就该想到分支结构。
        </p>
        <div class="chapter-three-rhythm">
          <span>先找题目里的条件</span>
          <span>再安排分支顺序</span>
          <span>最后检查边界值</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="if 的三种基本写法"
      >
        <h3>if 的三种基本写法</h3>
        <p class="chapter-three-cue">
          <strong>先分清结构：</strong>单分支是“成立才执行”，双分支是“二选一”，多分支是“按顺序逐个判断”。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>单分支</h3>
            <pre><code class="python">if score == 100:
    print("满分")  # 只在条件成立时输出</code></pre>
            <p>如果条件为假，这一段代码会被直接跳过，程序继续往下执行。</p>
          </article>
          <article class="command-card">
            <h3>双分支</h3>
            <pre><code class="python">if score &gt;= 60:
    print("及格")  # 条件为真走这里
else:
    print("不及格")  # 条件为假走这里</code></pre>
            <p>双分支一定会执行其中一条，适合“是 / 否”这类判断。</p>
          </article>
          <article class="command-card">
            <h3>多分支</h3>
            <pre><code class="python">if score &gt;= 90:
    level = "A"      # 先判断最高档
elif score &gt;= 75:
    level = "B"      # 前面没命中再判断这里
else:
    level = "C"      # 剩余情况统一归到这里</code></pre>
            <p>多分支最关键的是顺序，范围更高、更特殊的条件要放在前面。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="把规则翻译成 if 的四步法"
      >
        <h3>把规则翻译成 if 的四步法</h3>
        <ol class="timeline">
          <li>
            <h3>1. 找条件</h3>
            <p>先把题目里的判断词圈出来，例如“大于等于”“并且”“否则”“否则如果”。</p>
          </li>
          <li>
            <h3>2. 写布尔表达式</h3>
            <p>不要急着写整段 if，先把每个条件单独翻译成比较或逻辑表达式。</p>
          </li>
          <li>
            <h3>3. 安排分支顺序</h3>
            <p>多分支题通常要从范围更严格、更特殊的情况先写，再写宽松的情况。</p>
          </li>
          <li>
            <h3>4. 检查边界</h3>
            <p>重点检查 <code>60</code>、<code>90</code> 这类边界值，看会不会掉进错误分支。</p>
          </li>
        </ol>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="分支示例：成绩评级器"
      >
        <h3>分支示例：成绩评级器</h3>
        <p class="section-note">
          这是第三章最典型的示例之一。它简单，但几乎包含了分支结构的全部关键点：
          输入、类型转换、区间判断、顺序安排、边界检查。
        </p>
        <p class="chapter-three-cue">
          <strong>带着问题看：</strong>如果成绩是 <code>92</code>、<code>78</code>、<code>60</code>、<code>59</code>，
          程序分别会走到哪一段？
        </p>
        <pre><code class="python">score = int(input("请输入成绩: "))

if score &gt;= 90:
    level = "优秀"   # 先判断最高分段
elif score &gt;= 75:
    level = "良好"   # 前面不成立，再判断这一档
elif score &gt;= 60:
    level = "及格"   # 继续往下判断
else:
    level = "不及格" # 剩余情况统一处理

print("成绩等级:", level)</code></pre>
        <p class="section-note">
          多分支按从上到下的顺序依次判断。一旦命中某个分支，后面的分支就不会再执行。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 课堂练习：补全奖学金评定"
      >
        <h3>🛠️ 课堂练习：补全奖学金评定</h3>
        <div class="command-layout chapter-three-practice-grid">
          <article class="command-card chapter-three-task-card">
            <p><strong>任务目标</strong>：补全多分支条件，完成奖学金等级评定。</p>
            <ol>
              <li>同时考虑成绩和出勤率，条件里需要使用 <code>and</code>。</li>
              <li>按“特等奖 → 一等奖 → 合格 → 待改进”的顺序补全条件。</li>
              <li>注意高标准的分支必须写在前面。</li>
            </ol>
          </article>
          <article class="command-card chapter-three-code-card">
            <pre><code class="python">score = int(input("请输入成绩: "))
attendance = int(input("请输入出勤率: "))

if ________:
    # 提示：95+ 且出勤率 98+ 
    level = "特等奖"
elif ________:
    # 提示：85+ 且出勤率 95+ 
    level = "一等奖"
elif ________:
    # 提示：成绩至少及格
    level = "合格"
else:
    level = "待改进"

print("评定结果:", level)</code></pre>
            <div class="fragment">
              <p style="color: var(--neon-yellow); margin-top: 12px">参考补全：</p>
              <pre><code class="python">score = int(input("请输入成绩: "))
attendance = int(input("请输入出勤率: "))

if score &gt;= 95 and attendance &gt;= 98:
    # 提示：95+ 且出勤率 98+
    level = "特等奖"
elif score &gt;= 85 and attendance &gt;= 95:
    # 提示：85+ 且出勤率 95+
    level = "一等奖"
elif score &gt;= 60:
    # 提示：成绩至少及格
    level = "合格"
else:
    level = "待改进"

print("评定结果:", level)</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        id="loop-roadmap"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 3：循环结构"
      >
        <h2>任务 3：循环结构</h2>
        <p class="section-note">
          循环的价值在于：同样的动作不需要写很多遍。第三章只抓两类核心循环：
          <strong>while 看条件，for 看次数或数据。</strong>
        </p>
        <div class="chapter-three-rhythm">
          <span>先问循环靠什么结束</span>
          <span>再看每轮变量怎么变化</span>
          <span>最后选择 while 或 for</span>
        </div>
      </section>

      <section
        id="while-structure"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="while：次数未知，看条件"
      >
        <h3>while：次数未知，看条件</h3>
        <p class="chapter-three-cue">
          <strong>先盯条件：</strong>读 <code>while</code> 代码时，先不要急着看循环体，先问“这一轮为什么会继续”以及“它靠什么停下来”。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>使用场景</h3>
            <p>不知道要执行多少次，但知道什么时候结束。</p>
            <p>例如：反复输入直到合法、持续重试直到成功、菜单循环直到退出。</p>
          </article>
          <article class="command-card">
            <h3>基本骨架</h3>
            <pre><code class="python">while 条件:
    要重复执行的代码
# 条件变成 False 时，循环结束</code></pre>
            <p><code>while</code> 会先判断条件，再决定这一轮代码要不要执行。</p>
          </article>
          <article class="command-card">
            <h3>输入校验示例</h3>
            <pre><code class="python">score = -1
# 先给一个非法值，确保能进入循环
while score &lt; 0 or score &gt; 100:
    score = int(input("请输入 0~100 的成绩: "))
print("录入完成:", score)</code></pre>
            <p>只要输入仍然不在 0 到 100 之间，循环就会继续要求重新输入。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="死循环通常是怎么来的"
      >
        <h3>死循环通常是怎么来的</h3>
        <p class="chapter-three-cue">
          <strong>检查顺序：</strong>先看初始值，再看条件，最后看循环体里有没有更新变量。
        </p>
        <div class="pitfall-grid compact-grid">
          <article class="pitfall">
            <h3>1) 忘记更新变量</h3>
            <p class="problem">问题：条件一直为真，循环永远停不下来。</p>
            <p class="solution">解法：检查循环体里有没有让条件发生变化的语句。</p>
          </article>
          <article class="pitfall">
            <h3>2) 初始值设置不当</h3>
            <p class="problem">问题：还没开始判断，变量就已经不合理。</p>
            <p class="solution">解法：先想“第一次进入循环时，这个值应该是什么”。</p>
          </article>
          <article class="pitfall">
            <h3>3) 条件写反了</h3>
            <p class="problem">问题：想“直到合法才停”，却写成了“合法时继续”。</p>
            <p class="solution">解法：把条件翻成中文再读一遍，确认和题意一致。</p>
          </article>
          <article class="pitfall">
            <h3>4) 字符串和数字混用</h3>
            <p class="problem">问题：输入是字符串，和整数比较时逻辑混乱。</p>
            <p class="solution">解法：在进入条件判断前先完成类型转换。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 课堂练习：补全口令验证"
      >
        <h3>🛠️ 课堂练习：补全口令验证</h3>
        <div class="command-layout chapter-three-practice-grid">
          <article class="command-card chapter-three-task-card">
            <p><strong>任务目标</strong>：补全 <code>while</code> 循环，完成最多 3 次的口令验证。</p>
            <ol>
              <li>循环条件同时考虑“次数未用完”和“尚未成功”。</li>
              <li>输入正确时修改状态，输入错误时增加次数。</li>
              <li>体会 <code>while</code> 如何依靠变量变化来结束循环。</li>
            </ol>
          </article>
          <article class="command-card chapter-three-code-card">
            <pre><code class="python">secret = "python"
attempt = 0
success = False

while ________:
    code = input("请输入口令: ")
    if ________:
        # 提示：输入正确时，更新成功状态
        success = True
    else:
        # 提示：输入错误时，次数加 1
        ________

if success:
    print("验证成功")
else:
    print("次数已用完")</code></pre>
            <div class="fragment">
              <p style="color: var(--neon-yellow); margin-top: 12px">参考补全：</p>
              <pre><code class="python">secret = "python"
attempt = 0
success = False

while attempt &lt; 3 and not success:
    code = input("请输入口令: ")
    if code == secret:
        # 提示：输入正确时，更新成功状态
        success = True
    else:
        # 提示：输入错误时，次数加 1
        attempt += 1

if success:
    print("验证成功")
else:
    print("次数已用完")</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        id="for-structure"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="for：次数已知，或要遍历数据"
      >
        <h3>for：次数已知，或要遍历数据</h3>
        <p class="chapter-three-cue">
          <strong>先看循环变量：</strong>每轮到底拿到了什么，是数字、字符串，还是列表中的一个元素。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>固定次数</h3>
            <pre><code class="python">for num in range(1, 6):
    print(num)  # num 会依次取 1 到 5</code></pre>
            <p><code>range(1, 6)</code> 的起点包含 1，终点不包含 6，所以一共循环 5 次。</p>
          </article>
          <article class="command-card">
            <h3>遍历数据</h3>
            <pre><code class="python">names = ["张三", "李四", "王五"]
for name in names:
    print(name)  # 每轮处理一个名字</code></pre>
            <p>当目标是“把列表中的每个元素都处理一遍”时，通常优先考虑 <code>for</code>。</p>
          </article>
          <article class="command-card">
            <h3>累加统计</h3>
            <pre><code class="python">scores = [80, 92, 76]
total = 0
for score in scores:
    total += score  # 把当前成绩累加进总分
print("总分:", total)  # 循环结束后再统一输出</code></pre>
            <p>这种“遍历一遍列表并持续更新结果”的写法，在统计题里非常常见。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="while 和 for 怎么选"
      >
        <h3>while 和 for 怎么选</h3>
        <p class="chapter-three-cue">
          <strong>先问题目：</strong>如果重点是“重复到满足条件为止”，优先想 <code>while</code>；如果重点是“把一组数据处理一遍”，优先想 <code>for</code>。
        </p>
        <div class="concept-grid chapter-three-quad-grid">
          <article class="concept-card">
            <h3>已知次数</h3>
            <p>比如打印 10 次、遍历 30 个学生，优先用 <code>for</code>。</p>
          </article>
          <article class="concept-card">
            <h3>已知结束条件</h3>
            <p>比如“直到输入合法”“直到用户输入 q”，优先用 <code>while</code>。</p>
          </article>
          <article class="concept-card">
            <h3>遍历容器</h3>
            <p>列表、字符串、集合、字典键值对，通常先想到 <code>for</code>。</p>
          </article>
          <article class="concept-card">
            <h3>自己维护状态</h3>
            <p>如果循环是否继续依赖某个变量的动态变化，<code>while</code> 更自然。</p>
          </article>
        </div>
        <p class="section-note">
          判断方法可以压缩成一句话：<strong>要么遍历东西，要么盯住条件；前者多半是 for，后者多半是 while。</strong>
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 课堂练习：补全成绩汇总"
      >
        <h3>🛠️ 课堂练习：补全成绩汇总</h3>
        <div class="command-layout chapter-three-practice-grid">
          <article class="command-card chapter-three-task-card">
            <p><strong>任务目标</strong>：补全 <code>for</code> 循环，同时统计平均分、及格人数和最高分。</p>
            <ol>
              <li>补全遍历方式，让循环依次读取每个成绩。</li>
              <li>补全及格条件和最高分更新条件。</li>
              <li>观察一次遍历可以完成多项统计任务。</li>
            </ol>
          </article>
          <article class="command-card chapter-three-code-card">
            <pre><code class="python">scores = [78, 92, 55, 84, 61]
total = 0
passed_count = 0
best_score = scores[0]

for ________:
    total += score
    if ________:
        passed_count += 1
    if ________:
        best_score = score

average = total / len(scores)
print("平均分:", average)
print("及格人数:", passed_count)
print("最高分:", best_score)</code></pre>
            <div class="fragment">
              <p style="color: var(--neon-yellow); margin-top: 12px">参考补全：</p>
              <pre><code class="python">scores = [78, 92, 55, 84, 61]
total = 0
passed_count = 0
best_score = scores[0]

for score in scores:
    total += score
    if score &gt;= 60:
        passed_count += 1
    if score &gt; best_score:
        best_score = score

average = total / len(scores)
print("平均分:", average)
print("及格人数:", passed_count)
print("最高分:", best_score)</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 4：嵌套循环"
      >
        <h2>任务 4：嵌套循环</h2>
        <p class="section-note">
          当“外层”和“内层”两个重复动作同时存在时，就需要嵌套循环。九九乘法表是入门案例，
          杨辉三角则更能体现“逐行生成”的结构特点。
        </p>
        <div class="chapter-three-rhythm">
          <span>先说外层循环做什么</span>
          <span>再说内层循环做什么</span>
          <span>最后再看行与行之间的关系</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="外层管行，内层管列"
      >
        <h3>外层管行，内层管列</h3>
        <p class="chapter-three-cue">
          <strong>推荐读法：</strong>先完整说出外层循环一轮代表什么，再说内层在这一轮里重复了多少次。
        </p>
        <pre><code class="python">for row in range(1, 4):
    # 先确定当前是第几行
    for col in range(1, 4):
        # 再处理这一行中的每一列
        print(f"({row},{col})", end=" ")
    print()  # 一整行结束后换行</code></pre>
        <p class="section-note">
          读这段代码时，要先盯外层：外层每走一轮，都会把内层完整执行一遍。
          如果每个位置的值还依赖上一行的数据，就会再叠加 <code>if</code> 判断和列表访问。
        </p>
      </section>

      <section
        id="nested-practice"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 课堂练习：补全杨辉三角"
      >
        <h3>🛠️ 课堂练习：补全杨辉三角</h3>
        <div class="command-layout chapter-three-practice-grid">
          <article class="command-card chapter-three-task-card">
            <p><strong>任务目标</strong>：补全嵌套循环和 <code>if</code> 判断，逐行生成前 5 行杨辉三角。</p>
            <ol>
              <li>两端位置固定为 <code>1</code>。</li>
              <li>中间位置等于上一行左上和右上的和。</li>
              <li>这道题会同时调用上一章的列表知识。</li>
            </ol>
          </article>
          <article class="command-card chapter-three-code-card">
            <pre><code class="python">triangle = []

for row in range(5):
    current_row = []
    for col in range(row + 1):
        if ________:
            # 提示：每行两端都是 1
            current_row.append(1)
        else:
            # 提示：中间值 = 左上 + 右上
            value = ________
            current_row.append(value)
    triangle.append(current_row)

for row in triangle:
    print(row)</code></pre>
            <div class="fragment">
              <p style="color: var(--neon-yellow); margin-top: 12px">参考补全：</p>
              <pre><code class="python">triangle = []

for row in range(5):
    current_row = []
    for col in range(row + 1):
        if col == 0 or col == row:
            # 提示：每行两端都是 1
            current_row.append(1)
        else:
            # 提示：中间值 = 左上 + 右上
            value = (
                triangle[row - 1][col - 1]
                + triangle[row - 1][col]
            )
            current_row.append(value)
    triangle.append(current_row)

for row in triangle:
    print(row)</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 5：循环控制"
      >
        <h2>任务 5：循环控制</h2>
        <p class="section-note">
          学会循环之后，还要学会“调节循环节奏”。有时我们不想把所有轮次都跑完，
          这时就要用到 <code>break</code> 和 <code>continue</code>。
        </p>
        <div class="chapter-three-rhythm">
          <span>先分清跳过还是结束</span>
          <span>再看它作用在哪一层循环</span>
          <span>最后放进真实数据处理中</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="break 和 continue"
      >
        <h3>break 和 continue</h3>
        <p class="chapter-three-cue">
          <strong>先比较结果：</strong><code>continue</code> 是“跳过这一轮剩余代码”，<code>break</code> 是“整层循环到此结束”。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3><code>break</code></h3>
            <pre><code class="python">for num in range(1, 10):
    if num == 5:
        # 找到目标后，整个循环结束
        break
    print(num)</code></pre>
            <p>执行到 5 时，循环直接结束，所以 5 后面的数字不会再输出。</p>
          </article>
          <article class="command-card">
            <h3><code>continue</code></h3>
            <pre><code class="python">for num in range(1, 6):
    if num == 3:
        # 这一轮不做后面的代码，直接进入下一轮
        continue
    print(num)</code></pre>
            <p>第 3 轮被跳过，但循环不会结束，4 和 5 仍然会继续执行。</p>
          </article>
          <article class="command-card">
            <h3>综合示例</h3>
            <pre><code class="python">scores = [86, -1, 91, 999, 75]
for score in scores:
    if score &lt; 0:
        # 负数视为无效数据，直接跳过
        continue
    if score == 999:
        # 999 视为停止标记，直接结束循环
        break
    print(score)</code></pre>
            <p>同一段循环里可以同时使用 <code>continue</code> 和 <code>break</code>，但作用不同。</p>
          </article>
        </div>
        <p class="section-note">
          必须强调：<strong><code>break</code> 只结束当前这一层循环。</strong>
          如果它写在嵌套循环的内层，只会跳出内层，不会自动结束外层。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 课堂练习：补全有效成绩平均分"
      >
        <h3>🛠️ 课堂练习：补全有效成绩平均分</h3>
        <div class="command-layout chapter-three-practice-grid">
          <article class="command-card chapter-three-task-card">
            <p><strong>任务目标</strong>：补全循环控制条件，统计有效成绩的平均分。</p>
            <ol>
              <li><code>-1</code> 表示缺考，应跳过，不计入总分和人数。</li>
              <li><code>999</code> 表示录入结束，应直接停止循环。</li>
              <li>有效数据才参与总分和人数统计。</li>
            </ol>
          </article>
          <article class="command-card chapter-three-code-card">
            <pre><code class="python">scores = [86, -1, 91, 999, 75, 88]
total = 0
count = 0

for score in scores:
    if ________:
        # 提示：缺考，跳过本轮
        continue
    if ________:
        # 提示：录入结束，停止循环
        break
    total += score
    count += 1

average = total / count
print("有效人数:", count)
print("平均分:", average)</code></pre>
            <div class="fragment">
              <p style="color: var(--neon-yellow); margin-top: 12px">参考补全：</p>
              <pre><code class="python">scores = [86, -1, 91, 999, 75, 88]
total = 0
count = 0

for score in scores:
    if score == -1:
        # 提示：缺考，跳过本轮
        continue
    if score == 999:
        # 提示：录入结束，停止循环
        break
    total += score
    count += 1

average = total / count
print("有效人数:", count)
print("平均分:", average)</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        id="summary"
        class="section reveal summary"
        data-outline-level="1"
        data-outline-label="课堂收束"
      >
        <div class="section-head">
          <p class="kicker">CHAPTER WRAP-UP</p>
          <h2>课堂收束：把逻辑写进程序的标准路径</h2>
        </div>
        <p class="chapter-three-cue">
          <strong>回看整章：</strong>先用运算符得到结果，再把结果交给 <code>if</code> 或循环，最后用
          <code>break</code> / <code>continue</code> 调整执行节奏。
        </p>
        <div class="flow">
          <span>运算符算出结果</span>
          <span>条件交给 if</span>
          <span>重复交给循环</span>
          <span>嵌套处理多层结构</span>
          <span>break/continue 调节节奏</span>
        </div>
        <pre class="final-snippet"><code class="python">choice = ""

while choice != "q":  # != 读作“不等于”
    choice = input("1.开始 2.帮助 q.退出: ")

    if choice == "1":
        print("进入任务")  # 输入 1，进入功能
    elif choice == "2":
        print("显示帮助")  # 输入 2，查看帮助
    elif choice == "q":
        print("程序结束")  # 输入 q，准备退出循环
    else:
        print("无效指令，请重新输入")</code></pre>
        <p class="section-note">
          <code>!=</code> 表示“不等于”。只要 <code>choice</code> 还不是 <code>"q"</code>，
          循环就会继续；当输入 <code>q</code> 后，条件变为假，循环结束。
        </p>
        <p class="section-note">
          到这里，已经具备进入章节结尾综合案例的基础：会算、会判断、会循环、会控制流程。
        </p>
      </section>

      <section
        id="experiment-1"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="实验 1：阶梯电价计算电费"
      >
        <div class="section-head">
          <p class="kicker">EXPERIMENT 01</p>
          <h2>实验 1：阶梯电价计算电费</h2>
        </div>
        <p class="section-note">
          这是第三章的综合训练。需要把输入校验、列表成员判断、嵌套选择结构、循环控制和分段计算整合在同一个程序里。
        </p>
        <div class="mirror-grid">
          <article class="mirror-card">
            <h3>实验目标</h3>
            <p>输入月份与用电量，判断季节，再按阶梯电价规则计算该月应缴纳的总电费。</p>
          </article>
          <article class="mirror-card">
            <h3>实验报告</h3>
            <p>实验完成后，需要结合程序与运行结果填写实验报告。</p>
            <a
              class="chapter-three-report-link"
              :href="exp1ReportHref"
              download
            >
              下载实验报告 1
            </a>
          </article>
        </div>
        <div class="chapter-three-rhythm">
          <span>先校验输入是否合法</span>
          <span>再按月份进入季节分支</span>
          <span>最后按档位累计总电费</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验规则：季节与档位"
      >
        <h3>实验规则：季节与档位</h3>
        <p class="chapter-three-cue">
          <strong>本实验统一使用以下规则：</strong>非夏季指 <code>1, 2, 3, 4, 11, 12</code> 月，
          夏季指 <code>5, 6, 7, 8, 9, 10</code> 月。单价在全年相同，但每个季节的分档上限不同。
        </p>
        <div class="table-wrap">
          <table class="ops-table">
            <thead>
              <tr>
                <th>季节</th>
                <th>月份</th>
                <th>第一档</th>
                <th>第二档</th>
                <th>第三档</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>非夏季</td>
                <td><code>[1, 2, 3, 4, 11, 12]</code></td>
                <td>0~200 度，<code>0.5469</code> 元/度</td>
                <td>201~400 度，<code>0.5969</code> 元/度</td>
                <td>400 度以上，<code>0.8469</code> 元/度</td>
              </tr>
              <tr>
                <td>夏季</td>
                <td><code>[5, 6, 7, 8, 9, 10]</code></td>
                <td>0~260 度，<code>0.5469</code> 元/度</td>
                <td>261~600 度，<code>0.5969</code> 元/度</td>
                <td>600 度以上，<code>0.8469</code> 元/度</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="section-note">
          这里的关键不是把电价背下来，而是学会把“分段规则”翻译成嵌套分支，并正确算出每一档的电量小计。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验拆解：输入与外层分流"
      >
        <h3>实验拆解：输入与外层分流</h3>
        <p class="chapter-three-cue">
          <strong>先处理入口：</strong>如果月份或用电量不合法，后面的阶梯计算就没有意义，所以综合题要先把输入校验放在最前面。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>步骤 1：校验月份</h3>
            <pre><code class="python">while True:
    month = int(input("请输入月份(1-12): "))
    if 1 &lt;= month &lt;= 12:
        break
    print("月份输入无效，请重新输入")</code></pre>
            <p>这里使用 <code>while True</code> 搭配 <code>break</code>，只要输入合法就立即退出循环。</p>
          </article>
          <article class="command-card">
            <h3>步骤 2：校验用电量</h3>
            <pre><code class="python">while True:
    ele_num = float(input("请输入当月用电总度数: "))
    if ele_num &gt;= 0:
        break
    print("用电量不能为负数，请重新输入")</code></pre>
            <p>负数不可能表示真实的用电量，所以也要先完成校验，再进入后面的分支计算。</p>
          </article>
          <article class="command-card">
            <h3>步骤 3：外层选择结构</h3>
            <pre><code class="python">if month in [1, 2, 3, 4, 11, 12]:
    # 非夏季分支
    ...
else:
    # 夏季分支
    ...</code></pre>
            <p>外层分支先按季节分类，内层分支再按用电量所在区间计算各档费用。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验拆解：非夏季与夏季计费"
      >
        <h3>实验拆解：非夏季与夏季计费</h3>
        <p class="chapter-three-cue">
          <strong>读题顺序：</strong>先看当前属于哪一个季节，再看总用电量落在哪个区间，最后把每一档的费用分开计算后求和。
        </p>
        <div class="command-layout chapter-three-2plus1">
          <article class="command-card">
            <h3>非夏季计费</h3>
            <pre><code class="python">if ele_num &lt;= 200:
    ele_charge = ele_num * LOW_PRICE
elif ele_num &lt;= 400:
    ele_charge = (
        200 * LOW_PRICE
        + (ele_num - 200) * MID_PRICE
    )
else:
    ele_charge = (
        200 * LOW_PRICE
        + 200 * MID_PRICE
        + (ele_num - 400) * HIGH_PRICE
    )</code></pre>
            <p>前两档用电量是固定的，只有最后一档的“超出部分”需要用减法算出来。</p>
          </article>
          <article class="command-card">
            <h3>夏季计费</h3>
            <pre><code class="python">if ele_num &lt;= 260:
    ele_charge = ele_num * LOW_PRICE
elif ele_num &lt;= 600:
    ele_charge = (
        260 * LOW_PRICE
        + (ele_num - 260) * MID_PRICE
    )
else:
    ele_charge = (
        260 * LOW_PRICE
        + 340 * MID_PRICE
        + (ele_num - 600) * HIGH_PRICE
    )</code></pre>
            <p>夏季的第一档和第二档上限更高，所以分段常量和减去的基准值也会跟着变化。</p>
          </article>
          <article class="command-card">
            <h3>输出结果</h3>
            <pre><code class="python">print(f"{month} 月电费为：{ele_charge:.2f} 元")</code></pre>
            <p>这里用 <code>:.2f</code> 保留两位小数，让电费显示更符合日常格式。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🧪 综合实验：补全主程序（上）"
      >
        <h3>🧪 综合实验：补全主程序（上）</h3>
        <div class="command-layout chapter-three-practice-grid">
          <article class="command-card chapter-three-task-card">
            <p><strong>任务目标</strong>：补全程序开头，完成常量定义、输入校验和外层季节分流。</p>
            <ol>
              <li>单价常量和总电费变量先写在程序最前面。</li>
              <li>月份和用电量都需要通过 <code>while True</code> + <code>break</code> 完成校验。</li>
              <li>外层分支用 <code>month in [...]</code> 判断非夏季。</li>
            </ol>
          </article>
          <article class="command-card chapter-three-code-card">
            <pre><code class="python">LOW_PRICE = ________
MID_PRICE = ________
HIGH_PRICE = ________
ele_charge = ________

while True:
    month = int(input("请输入月份(1-12): "))
    if ________:
        break
    print("月份输入无效，请重新输入")

while True:
    ele_num = float(input("请输入当月用电总度数: "))
    if ________:
        break
    print("用电量不能为负数，请重新输入")

if month in ________:
    # 提示：这里进入非夏季分支
    pass
else:
    # 提示：这里进入夏季分支
    pass</code></pre>
            <div class="fragment">
              <p style="color: var(--neon-yellow); margin-top: 12px">参考补全：</p>
              <pre><code class="python">LOW_PRICE = 0.5469
MID_PRICE = 0.5969
HIGH_PRICE = 0.8469
ele_charge = 0

while True:
    month = int(input("请输入月份(1-12): "))
    if 1 &lt;= month &lt;= 12:
        break
    print("月份输入无效，请重新输入")

while True:
    ele_num = float(input("请输入当月用电总度数: "))
    if ele_num &gt;= 0:
        break
    print("用电量不能为负数，请重新输入")

if month in [1, 2, 3, 4, 11, 12]:
    # 提示：这里进入非夏季分支
    pass
else:
    # 提示：这里进入夏季分支
    pass</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🧪 综合实验：补全主程序（下）"
      >
        <h3>🧪 综合实验：补全主程序（下）</h3>
        <div class="command-layout chapter-three-practice-grid">
          <article class="command-card chapter-three-task-card">
            <p><strong>任务目标</strong>：补全非夏季和夏季的内层多分支结构，算出总电费。</p>
            <ol>
              <li>非夏季按 <code>200 / 400</code> 的分档边界计算。</li>
              <li>夏季按 <code>260 / 600</code> 的分档边界计算。</li>
              <li>超过某一档时，要把前面各档的固定费用和超出部分的费用一起加起来。</li>
            </ol>
          </article>
          <article class="command-card chapter-three-code-card">
            <pre><code class="python">if month in [1, 2, 3, 4, 11, 12]:
    if ________:
        ele_charge = ________
    elif ________:
        ele_charge = (
            200 * LOW_PRICE
            + ________
        )
    else:
        ele_charge = (
            200 * LOW_PRICE
            + 200 * MID_PRICE
            + ________
        )
else:
    if ________:
        ele_charge = ________
    elif ________:
        ele_charge = (
            260 * LOW_PRICE
            + ________
        )
    else:
        ele_charge = (
            260 * LOW_PRICE
            + 340 * MID_PRICE
            + ________
        )

print(f"{month} 月电费为：{ele_charge:.2f} 元")</code></pre>
            <div class="fragment">
              <p style="color: var(--neon-yellow); margin-top: 12px">参考补全：</p>
              <pre><code class="python">if month in [1, 2, 3, 4, 11, 12]:
    if ele_num &lt;= 200:
        ele_charge = ele_num * LOW_PRICE
    elif ele_num &lt;= 400:
        ele_charge = (
            200 * LOW_PRICE
            + (ele_num - 200) * MID_PRICE
        )
    else:
        ele_charge = (
            200 * LOW_PRICE
            + 200 * MID_PRICE
            + (ele_num - 400) * HIGH_PRICE
        )
else:
    if ele_num &lt;= 260:
        ele_charge = ele_num * LOW_PRICE
    elif ele_num &lt;= 600:
        ele_charge = (
            260 * LOW_PRICE
            + (ele_num - 260) * MID_PRICE
        )
    else:
        ele_charge = (
            260 * LOW_PRICE
            + 340 * MID_PRICE
            + (ele_num - 600) * HIGH_PRICE
        )

print(f"{month} 月电费为：{ele_charge:.2f} 元")</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验报告与提交"
      >
        <h3>实验报告与提交</h3>
        <p class="chapter-three-cue">
          <strong>完成顺序：</strong>先补全代码并运行，再截图或记录测试结果，最后填写实验报告中的“实验过程与结果记录”“结果分析”“收获与思考”。
        </p>
        <div class="mirror-grid">
          <article class="mirror-card">
            <h3>建议测试数据</h3>
            <p><code>month = 3</code>，<code>ele_num = 150</code></p>
            <p><code>month = 8</code>，<code>ele_num = 350</code></p>
            <p><code>month = 12</code>，<code>ele_num = 460</code></p>
          </article>
          <article class="mirror-card">
            <h3>实验报告下载</h3>
            <p>下载后填写姓名、学号、实验过程、运行结果和分析内容。</p>
            <a
              class="chapter-three-report-link"
              :href="exp1ReportHref"
              download
            >
              下载《实验报告1：阶梯电价计算电费》
            </a>
          </article>
          <article class="mirror-card chapter-three-submit-card">
            <div class="chapter-three-qr-wrap">
              <img
                class="chapter-three-qr"
                :src="exp1SubmissionQrSrc"
                alt="实验1作业收集二维码"
              />
            </div>
            <div class="chapter-three-submit-copy">
              <h3>作业提交</h3>
              <p>扫描二维码或直接打开下方链接，提交本次实验的代码、运行结果和实验报告。</p>
              <a
                class="chapter-three-report-link"
                :href="exp1SubmissionHref"
                target="_blank"
                rel="noopener noreferrer"
              >
                打开作业收集链接
              </a>
              <p class="chapter-three-link-text">
                <a
                  :href="exp1SubmissionHref"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ exp1SubmissionHref }}
                </a>
              </p>
            </div>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课堂关键句：先算出条件，再让 if 和循环接管流程。</p>
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
.page.is-slide-deck .chapter-three-rhythm {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.page.is-slide-deck .chapter-three-rhythm span {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(13, 123, 232, 0.18);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.95), rgba(245, 251, 255, 0.98));
  color: #0b4f88;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
}

.page.is-slide-deck .chapter-three-cue {
  margin: 10px 0 0;
  padding: 10px 12px;
  border-left: 4px solid rgba(13, 123, 232, 0.45);
  border-radius: 10px;
  background: rgba(13, 123, 232, 0.06);
  color: var(--text-main);
  font-size: 0.94rem;
  line-height: 1.65;
}

.page.is-slide-deck .chapter-three-cue strong {
  color: #0a5eaf;
}

.page.is-slide-deck .chapter-three-report-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  margin-top: 8px;
  padding: 9px 14px;
  border-radius: 10px;
  border: 1px solid rgba(13, 123, 232, 0.24);
  background: linear-gradient(180deg, rgba(13, 123, 232, 0.12), rgba(13, 123, 232, 0.18));
  color: #0a5eaf;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.15s ease, border-color 0.18s ease, background 0.18s ease;
}

.page.is-slide-deck .chapter-three-report-link:hover {
  transform: translateY(-1px);
  border-color: rgba(13, 123, 232, 0.38);
  background: linear-gradient(180deg, rgba(13, 123, 232, 0.16), rgba(13, 123, 232, 0.24));
}

.page.is-slide-deck .chapter-three-submit-card {
  grid-column: 1 / -1;
  grid-template-columns: 220px minmax(0, 1fr);
  align-items: center;
  gap: 18px;
}

.page.is-slide-deck .chapter-three-qr-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
}

.page.is-slide-deck .chapter-three-qr {
  width: min(220px, 100%);
  max-width: 220px;
  border-radius: 14px;
  border: 1px solid rgba(13, 123, 232, 0.16);
  background: #fff;
  padding: 10px;
  box-shadow: 0 8px 20px rgba(13, 123, 232, 0.12);
}

.page.is-slide-deck .chapter-three-submit-copy {
  display: grid;
  gap: 10px;
}

.page.is-slide-deck .chapter-three-link-text {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.65;
  word-break: break-all;
}

.page.is-slide-deck .chapter-three-link-text a {
  color: #0a5eaf;
  text-decoration: underline;
}

.page.is-slide-deck .command-layout.chapter-three-2plus1 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .command-layout.chapter-three-2plus1 > :last-child {
  grid-column: 1 / -1;
}

.page.is-slide-deck .concept-grid.chapter-three-quad-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .concept-grid.chapter-three-quad-grid > .concept-card {
  grid-column: span 1;
}

.page.is-slide-deck .command-layout.chapter-three-practice-grid {
  grid-template-columns: minmax(0, 0.92fr) minmax(0, 1.18fr);
  align-items: start;
}

.page.is-slide-deck .chapter-three-task-card,
.page.is-slide-deck .chapter-three-code-card {
  height: 100%;
}

.page.is-slide-deck .chapter-three-task-card ol {
  margin: 0;
  padding-left: 20px;
}

.page.is-slide-deck .chapter-three-code-card pre,
.page.is-slide-deck .chapter-three-code-card .fragment {
  margin-top: 0;
}

.page.is-slide-deck .chapter-three-code-card code {
  font-size: 0.85rem;
}

@media (max-width: 900px) {
  .page.is-slide-deck .chapter-three-rhythm,
  .page.is-slide-deck .command-layout.chapter-three-2plus1,
  .page.is-slide-deck .concept-grid.chapter-three-quad-grid,
  .page.is-slide-deck .command-layout.chapter-three-practice-grid {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .command-layout.chapter-three-2plus1 > :last-child,
  .page.is-slide-deck .concept-grid.chapter-three-quad-grid > .concept-card {
    grid-column: span 1;
  }

  .page.is-slide-deck .chapter-three-submit-card {
    grid-template-columns: 1fr;
  }
}
</style>
