<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";

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
        <span class="brand-tag">Chapter 4</span>
        <strong>函数与异常处理</strong>
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
        <p class="kicker">CHAPTER 04 FUNCTIONS</p>
        <h1>函数与异常处理：<br />把长程序拆成可复用模块</h1>
        <p class="hero-intro">
          第三章让程序学会了判断和循环，第四章要解决另一个关键问题：代码越来越长以后，
          怎样把重复逻辑收起来，怎样让错误输入不至于直接把程序打断。
        </p>
        <ul class="hero-checklist">
          <li>理解函数为什么能减少重复、降低修改成本、提升程序可维护性。</li>
          <li>掌握函数定义、调用、参数、返回值、变量作用域与递归函数。</li>
          <li>学会用异常处理保护输入过程，让程序从“会报错”升级到“能恢复”。</li>
        </ul>
        <div class="goal-cards fly-in-seq">
          <article>
            <h2>能力目标 1</h2>
            <p>会把一段重复逻辑抽成函数，而不是继续复制粘贴。</p>
          </article>
          <article>
            <h2>能力目标 2</h2>
            <p>会用参数和 <code>return</code> 组织数据流，而不是依赖混乱的全局变量。</p>
          </article>
          <article>
            <h2>能力目标 3</h2>
            <p>会在真实程序里使用递归和异常处理，而不只是记住语法形式。</p>
          </article>
        </div>
      </section>

      <section
        id="why-functions"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务简报：为什么需要函数"
      >
        <h2>任务简报：为什么需要函数</h2>
        <p class="section-note">
          先不急着写 <code>def</code>。先观察没有函数时的程序形态，再判断函数到底解决了什么问题。
        </p>
        <div class="chapter-four-rhythm">
          <span>先感受重复代码的痛苦</span>
          <span>再理解函数的价值</span>
          <span>最后学会自己拆函数</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="为什么初学者会先复制代码"
      >
        <h3>为什么初学者会先复制代码</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>第一步：先把 1 个任务做出来</h3>
            <p>刚开始只处理 1 个学生时，直接写一段判断和输出代码就够用了，代码也不长。</p>
          </article>
          <article class="command-card">
            <h3>第二步：任务突然扩展</h3>
            <p>当题目变成 3 个学生、10 个学生、全班学生时，最直接的做法往往就是复制上一段代码，再改变量名。</p>
          </article>
          <article class="command-card">
            <h3>复制不是错，但代价很高</h3>
            <p>复制代码在最开始看起来省事，因为它能立刻跑起来；问题出在后面，一旦规则修改，所有副本都要一起改。</p>
          </article>
        </div>
        <p class="section-note">
          函数不是为了否定“先复制再改”的本能，而是为了把这件事升级成更可维护的写法：<strong>同一段规则只保留一份。</strong>
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="痛苦示例：复制三遍的成绩报告"
      >
        <h3>痛苦示例：复制三遍的成绩报告</h3>
        <p class="chapter-four-cue">
          <strong>先感受：</strong>这段程序可以运行，但相同逻辑被复制了三遍。人数一多，代码会迅速膨胀。
        </p>
        <pre><code class="python">name1 = "张三"
score1 = 92
if score1 &gt;= 90:
    level1 = "优秀"
elif score1 &gt;= 60:
    level1 = "及格"
else:
    level1 = "不及格"
print(f"{name1} - {score1} - {level1}")

name2 = "李四"
score2 = 76
if score2 &gt;= 90:
    level2 = "优秀"
elif score2 &gt;= 60:
    level2 = "及格"
else:
    level2 = "不及格"
print(f"{name2} - {score2} - {level2}")

name3 = "王五"
score3 = 58
if score3 &gt;= 90:
    level3 = "优秀"
elif score3 &gt;= 60:
    level3 = "及格"
else:
    level3 = "不及格"
print(f"{name3} - {score3} - {level3}")</code></pre>
        <p class="section-note">
          问题不在于它不能运行，而在于它把同一套规则写了三次。重复越多，出错风险越高。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="需求一变，修改立刻变痛苦"
      >
        <h3>需求一变，修改立刻变痛苦</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>变化 1：及格线改成 70</h3>
            <p>原来只改一条规则，现在却要把三段代码里的判断条件全部改一遍。</p>
            <p>只要漏改一处，不同学生就会按不同标准评级。</p>
          </article>
          <article class="command-card">
            <h3>变化 2：新增“良好”档</h3>
            <p>原来只有两个分段，现在要加一层 <code>elif</code>。</p>
            <p>复制代码的数量越多，修改就越容易出错。</p>
          </article>
          <article class="command-card">
            <h3>变化 3：统一输出格式</h3>
            <pre><code class="python">print(
    f"{name} | 成绩={score} | 等级={level}"
)</code></pre>
            <p>如果输出格式要改，也必须在每一段重复逻辑里同步修改。</p>
          </article>
        </div>
        <p class="section-note">
          函数存在的核心原因只有一个：<strong>把会重复、会变化、会反复调用的逻辑收起来。</strong>
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章能力地图"
      >
        <div class="section-head">
          <p class="kicker">LEARNING MAP</p>
          <h2>本章能力地图：先封装，再传参，再保护程序</h2>
        </div>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card">
            <h3>函数基础</h3>
            <p>会定义函数、调用函数、使用 <code>return</code> 返回结果。</p>
          </article>
          <article class="concept-card">
            <h3>参数设计</h3>
            <p>会用位置参数、默认参数、关键字参数与可变参数组织函数输入。</p>
          </article>
          <article class="concept-card">
            <h3>变量作用域</h3>
            <p>分清局部变量、全局变量，以及可变对象参数的影响。</p>
          </article>
          <article class="concept-card">
            <h3>递归与异常</h3>
            <p>会写有结束条件的递归函数，也会用 <code>try/except</code> 处理输入错误。</p>
          </article>
        </div>
      </section>

      <section
        id="task-function-basics"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 1：函数基础"
      >
        <h2>任务 1：函数基础</h2>
        <p class="section-note">
          学函数的第一步不是背 <code>def</code> 语法，而是建立一个认识：函数就是一段有名字、能重复调用的功能。
        </p>
        <div class="chapter-four-rhythm">
          <span>先分清定义和调用</span>
          <span>再理解 return 的作用</span>
          <span>最后学会组织主流程</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="内置函数与自定义函数"
      >
        <h3>内置函数与自定义函数</h3>
        <p class="chapter-four-cue">
          <strong>先建立认识：</strong><code>print()</code>、<code>len()</code>、<code>int()</code> 本来就是函数。
          第四章只是从“使用函数”升级到“自己定义函数”。
        </p>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>内置函数</h3>
            <pre><code class="python">name = "Python"
print(name)
print(len(name))
print(int("18"))</code></pre>
            <p>这些函数已经由 Python 提前准备好，可以直接调用。</p>
          </article>
          <article class="command-card">
            <h3>自定义函数</h3>
            <pre><code class="python">def say_hello():
    print("你好，欢迎来到第四章")

say_hello()</code></pre>
            <p>自定义函数是把一段逻辑包起来，并给它起一个名字。</p>
          </article>
          <article class="command-card">
            <h3>核心结论</h3>
            <p>函数不是新对象，而是程序世界里最常见的组织方式。</p>
            <p>会写函数，程序才能从“能跑”升级到“能复用、能维护、能扩展”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="定义函数的基本骨架"
      >
        <h3>定义函数的基本骨架</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>骨架结构</h3>
            <pre><code class="python">def 函数名():
    函数体</code></pre>
            <p><code>def</code> 表示“定义一个函数”，冒号后面必须是缩进代码块。</p>
          </article>
          <article class="command-card">
            <h3>最小示例</h3>
            <pre><code class="python">def show_title():
    print("学生成绩系统")

show_title()</code></pre>
            <p>函数定义好以后，要通过函数名加括号来调用。</p>
          </article>
          <article class="command-card">
            <h3>阅读顺序</h3>
            <p>先看函数名，再看函数体在做什么，最后看程序在什么位置调用了它。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="定义和调用不是一回事"
      >
        <h3>定义和调用不是一回事</h3>
        <p class="chapter-four-cue">
          <strong>高频误区：</strong>定义函数不会让函数自动执行。程序只是“记住了这段功能”，真正运行要靠调用。
        </p>
        <pre><code class="python">def show_tip():
    print("函数体正在执行")

print("程序开始")
show_tip()
print("程序结束")</code></pre>
        <p class="section-note">
          先定义函数，再执行普通语句，碰到调用时才进入函数体。定义和调用必须分开理解。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="print 和 return 的区别"
      >
        <h3>print 和 return 的区别</h3>
        <p class="chapter-four-cue">
          <strong>先分工：</strong><code>print()</code> 负责显示给人看，<code>return</code> 负责把结果交还给调用者。
        </p>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>只打印，不返回</h3>
            <pre><code class="python">def show_square(x):
    print(x * x)

result = show_square(4)
print(result)  # None</code></pre>
            <p>函数把结果打印出来了，但没有真正“交回去”，变量里拿到的是 <code>None</code>。</p>
          </article>
          <article class="command-card">
            <h3>返回结果</h3>
            <pre><code class="python">def get_square(x):
    return x * x

result = get_square(4)
print(result)  # 16</code></pre>
            <p>返回值可以继续参与计算、比较或赋值，这才是函数真正强大的地方。</p>
          </article>
          <article class="command-card">
            <h3>结论</h3>
            <p>如果只是给人看，<code>print()</code> 足够；如果结果还要继续被程序使用，就应该 <code>return</code>。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="没有 return 时会发生什么"
      >
        <h3>没有 return 时会发生什么</h3>
        <pre><code class="python">def say_ok():
    print("执行完成")

value = say_ok()
print(value)  # None</code></pre>
        <p class="section-note">
          函数如果没有写 <code>return</code>，默认返回 <code>None</code>。这是理解函数行为时必须掌握的一条规则。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="用 main 组织主流程"
      >
        <h3>用 <code>main()</code> 组织主流程</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>直接写在一起</h3>
            <pre><code class="python">print("学生成绩系统")
print("1. 录入成绩")
print("2. 查询成绩")
print("3. 退出")</code></pre>
            <p>程序一长，主流程和细节会混在一起，阅读成本很高。</p>
          </article>
          <article class="command-card">
            <h3>拆成函数后</h3>
            <pre><code class="python">def show_title():
    print("学生成绩系统")

def show_menu():
    print("1. 录入成绩")
    print("2. 查询成绩")
    print("3. 退出")

def main():
    show_title()
    show_menu()

main()</code></pre>
            <p><code>main()</code> 负责描述“程序按什么顺序做事”，细节交给其他函数。</p>
          </article>
          <article class="command-card">
            <h3>设计习惯</h3>
            <p>函数名要清楚，一个函数尽量只做一件事，主流程尽量从上到下读得通顺。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="课堂练习：补全矩形面积函数"
      >
        <h3>🛠️ 课堂练习：补全矩形面积函数</h3>
        <div class="command-layout chapter-four-practice-grid">
          <article class="command-card chapter-four-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>写出函数头，让函数接收长和宽两个输入。</li>
              <li>使用 <code>return</code> 返回面积，而不是只打印结果。</li>
              <li>调用函数，并把结果保存到变量里。</li>
            </ol>
          </article>
          <article class="command-card chapter-four-code-card">
            <pre><code class="python">def calc_rectangle_area(length, width):
    # 返回矩形面积
    ________

area = ________(6, 4)
print("面积:", area)</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">return length * width

calc_rectangle_area</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        id="task-params"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 2：函数参数"
      >
        <h2>任务 2：函数参数</h2>
        <p class="section-note">
          如果一个函数只能处理固定数据，它的复用价值就很低。参数的作用，就是把函数做成带输入接口的工具。
        </p>
        <div class="chapter-four-rhythm">
          <span>先理解形参与实参</span>
          <span>再掌握默认参数、关键字参数和可变参数</span>
          <span>最后学会函数之间传递数据</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="一个参数与多个参数"
      >
        <h3>一个参数与多个参数</h3>
        <p class="chapter-four-cue">
          <strong>先问一个问题：</strong>如果函数内部把 <code>score = 88</code> 写死，它就只能服务这一次。参数的意义，就是让函数不再依赖写死的数据。
        </p>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>一个参数</h3>
            <pre><code class="python">def calc_grade(score):
    if score &gt;= 90:
        return "优秀"
    elif score &gt;= 60:
        return "及格"
    return "不及格"

print(calc_grade(88))</code></pre>
            <p>函数头里的 <code>score</code> 是形参，调用时传入的 <code>88</code> 是实参。</p>
          </article>
          <article class="command-card">
            <h3>多个参数</h3>
            <pre><code class="python">def calc_total(price, count):
    return price * count

print(calc_total(12.5, 3))</code></pre>
            <p>参数让同一段逻辑可以处理不同数据，而不是只能服务一组固定值。</p>
          </article>
          <article class="command-card">
            <h3>阅读方法</h3>
            <p>先看函数需要哪些输入，再看调用时传入了什么，最后看返回值是什么。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="默认参数与关键字参数"
      >
        <h3>默认参数与关键字参数</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>默认参数</h3>
            <pre><code class="python">def print_line(char="-", count=20):
    print(char * count)

print_line()
print_line("*", 8)</code></pre>
            <p>如果调用时没有提供某个参数，就使用默认值。</p>
          </article>
          <article class="command-card">
            <h3>关键字参数</h3>
            <pre><code class="python">def make_title(text, width=18):
    print(text.center(width, "="))

make_title("函数")
make_title("异常处理", width=24)</code></pre>
            <p>关键字参数能明确说明“这个值是给谁的”，可读性更好。</p>
          </article>
          <article class="command-card">
            <h3>注意点</h3>
            <p>默认参数应放在普通参数后面。关键字参数能让调用更清晰，但参数名必须写对。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="可变位置参数 *args"
      >
        <h3>可变位置参数 <code>*args</code></h3>
        <p class="chapter-four-cue">
          <strong>什么时候会需要它：</strong>当函数要接收的位置参数个数不固定时，普通参数就不够用了，这时可以用 <code>*args</code> 接住多出来的值。
        </p>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>基本写法</h3>
            <pre><code class="python">def calc_sum(*args):
    total = 0
    for num in args:
        total += num
    return total

print(calc_sum(10, 20, 30))</code></pre>
            <p><code>args</code> 会把传进来的多个位置参数收成一个元组。</p>
          </article>
          <article class="command-card">
            <h3>为什么有用</h3>
            <p>如果实参个数每次都不一样，提前写死 2 个、3 个、4 个参数会非常僵硬。</p>
          </article>
          <article class="command-card">
            <h3>阅读重点</h3>
            <p>看到 <code>*args</code> 时，先想到“这里会收到一组位置参数”，再把它当作元组去遍历。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="可变关键字参数 **kwargs"
      >
        <h3>可变关键字参数 <code>**kwargs</code></h3>
        <p class="chapter-four-cue">
          <strong>它解决的不是“数量不固定”，而是“字段名和数量都可能变化”。</strong> 这类参数最适合接收一组带名字的数据。
        </p>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>基本写法</h3>
            <pre><code class="python">def show_profile(**kwargs):
    for key, value in kwargs.items():
        print(key, "=", value)

show_profile(
    name="小林",
    age=19,
    major="计算机",
)</code></pre>
            <p><code>kwargs</code> 会把传进来的关键字参数收成一个字典。</p>
          </article>
          <article class="command-card">
            <h3>为什么有用</h3>
            <p>有些信息字段并不固定，例如个人资料、商品属性、筛选条件，这时用字典式接收更灵活。</p>
          </article>
          <article class="command-card">
            <h3>阅读重点</h3>
            <p>看到 <code>**kwargs</code> 时，先想到“这里会收到一组键值对”，再按字典方式访问。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="普通参数、*args、**kwargs 怎么选"
      >
        <h3>普通参数、<code>*args</code>、<code>**kwargs</code> 怎么选</h3>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card">
            <h3>普通参数</h3>
            <p>输入项明确、数量固定时，优先使用普通参数，最清晰。</p>
          </article>
          <article class="concept-card">
            <h3><code>*args</code></h3>
            <p>适合接收数量不固定的一组位置数据，例如多个分数、多个数字。</p>
          </article>
          <article class="concept-card">
            <h3><code>**kwargs</code></h3>
            <p>适合接收数量和字段名都可能变化的一组关键字数据。</p>
          </article>
          <article class="concept-card">
            <h3>教学建议</h3>
            <p>普通参数是主线，<code>*args</code> 和 <code>**kwargs</code> 先做到会读、会写基础用法即可。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="函数也可以返回多个结果"
      >
        <h3>函数也可以返回多个结果</h3>
        <p class="chapter-four-cue">
          <strong>补充能力：</strong>有时一个函数需要同时交回两个结果，Python 可以一次返回多个值。
        </p>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>返回最小值和最大值</h3>
            <pre><code class="python">def get_min_max(a, b, c):
    return min(a, b, c), max(a, b, c)

small, big = get_min_max(15, 8, 21)
print(small, big)</code></pre>
            <p>本质上是返回一个元组，只是接收时可以拆开。</p>
          </article>
          <article class="command-card">
            <h3>为什么有用</h3>
            <p>当一个任务天然会产生多个结果时，可以一次返回，避免反复重复计算。</p>
          </article>
          <article class="command-card">
            <h3>阅读方法</h3>
            <p>先看函数返回了几个值，再看左边有几个变量在接收，数量要对应。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="函数也可以调用函数"
      >
        <h3>函数也可以调用函数</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>先定义小功能</h3>
            <pre><code class="python">def calc_grade(score):
    if score &gt;= 90:
        return "优秀"
    elif score &gt;= 60:
        return "及格"
    return "不及格"</code></pre>
            <p>先把单一职责的小函数写清楚。</p>
          </article>
          <article class="command-card">
            <h3>再让大函数组合它</h3>
            <pre><code class="python">def print_report(name, score):
    level = calc_grade(score)
    print(f"{name} 的等级是 {level}")

print_report("小林", 83)</code></pre>
            <p>一个函数可以先调用另一个函数拿结果，再继续完成更大的任务。</p>
          </article>
          <article class="command-card">
            <h3>设计意义</h3>
            <p>大问题不是一口气写完，而是拆成多个小函数，再由主函数负责组合。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="参数匹配常见问题"
      >
        <h3>参数匹配常见问题</h3>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card">
            <h3>参数个数不对</h3>
            <p>函数要求两个参数，却只传了一个，程序会直接报错。</p>
          </article>
          <article class="concept-card">
            <h3>参数顺序传错</h3>
            <p>位置参数按顺序匹配，顺序错了，含义也会跟着错。</p>
          </article>
          <article class="concept-card">
            <h3>关键字写错</h3>
            <p>关键字参数提高了可读性，但参数名必须与函数定义一致。</p>
          </article>
          <article class="concept-card">
            <h3>默认值被忽略</h3>
            <p>只要显式传值，就会覆盖默认值。默认值不会自动“合并”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="课堂练习：补全运费计算函数"
      >
        <h3>🛠️ 课堂练习：补全运费计算函数</h3>
        <div class="command-layout chapter-four-practice-grid">
          <article class="command-card chapter-four-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>函数接收重量、单价和附加费。</li>
              <li>附加费使用默认参数，默认值为 0。</li>
              <li>返回总运费，并用关键字参数完成第二次调用。</li>
            </ol>
          </article>
          <article class="command-card chapter-four-code-card">
            <pre><code class="python">def calc_shipping(weight, unit_price, extra_fee=0):
    total = ________
    return total

fee1 = calc_shipping(3, 12)
fee2 = calc_shipping(
    5,
    unit_price=10,
    ________=8,
)
print(fee1, fee2)</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">weight * unit_price + extra_fee
extra_fee</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        id="task-scope"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 3：函数中的变量"
      >
        <h2>任务 3：函数中的变量</h2>
        <p class="section-note">
          函数不只是“把代码包起来”，还会形成自己的作用范围。很多报错都来自对变量作用域判断不清。
        </p>
        <div class="chapter-four-rhythm">
          <span>先理解局部变量</span>
          <span>再认识全局变量的边界</span>
          <span>最后掌握更稳的传值方式</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="局部变量与参数变量"
      >
        <h3>局部变量与参数变量</h3>
        <p class="chapter-four-cue">
          <strong>先看一个常见困惑：</strong>为什么函数里可以打印 <code>name</code> 或 <code>score</code>，函数外面却会报错？答案就在作用域。
        </p>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>局部变量</h3>
            <pre><code class="python">def show_student():
    name = "小林"
    print(name)

show_student()
print(name)  # NameError</code></pre>
            <p>在函数内部创建的变量，默认只在函数内部有效。</p>
          </article>
          <article class="command-card">
            <h3>参数也是局部变量</h3>
            <pre><code class="python">def show_score(score):
    print("当前成绩:", score)

show_score(88)
print(score)  # NameError</code></pre>
            <p>参数进入函数以后，本质上也是函数内部可用的局部变量。</p>
          </article>
          <article class="command-card">
            <h3>核心规则</h3>
            <p>函数内部的名字，默认不会自动带到函数外面。作用域是理解函数行为的关键。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="全局变量可以用，但不要乱用"
      >
        <h3>全局变量可以用，但不要乱用</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>读取全局变量</h3>
            <pre><code class="python">school = "启程班"

def show_school():
    print(school)

show_school()</code></pre>
            <p>函数内部可以读取外部已经存在的全局变量。</p>
          </article>
          <article class="command-card">
            <h3>修改全局变量</h3>
            <pre><code class="python">visit_count = 0

def add_visit():
    global visit_count
    visit_count += 1</code></pre>
            <p>如果确实要修改全局变量，需要使用 <code>global</code> 明确声明。</p>
          </article>
          <article class="command-card">
            <h3>风险提醒</h3>
            <p>全局变量一多，程序状态会变得难跟踪。读起来方便，维护起来却很危险。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="为什么优先用参数和 return"
      >
        <h3>为什么优先用参数和 <code>return</code></h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>不推荐的写法</h3>
            <pre><code class="python">total = 0

def add_score(score):
    global total
    total += score</code></pre>
            <p>函数悄悄修改外部变量，主流程很难看出数据是怎么变化的。</p>
          </article>
          <article class="command-card">
            <h3>更稳的写法</h3>
            <pre><code class="python">def add_score(total, score):
    return total + score

total = add_score(80, 5)
print(total)</code></pre>
            <p>输入从参数进来，结果从返回值出去，数据流更清楚，也更容易调试。</p>
          </article>
          <article class="command-card">
            <h3>结论</h3>
            <p>优先选择“参数 + return”这种显式传值方式。全局变量只在确有必要时使用。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="可变对象参数的影响"
      >
        <h3>可变对象参数的影响</h3>
        <p class="chapter-four-cue">
          <strong>必须看清：</strong>列表这类可变对象作为参数传入函数后，在函数内部修改，外部对象也会跟着变化。
        </p>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>直接修改原列表</h3>
            <pre><code class="python">def add_bonus(scores):
    scores.append(100)

data = [78, 82]
add_bonus(data)
print(data)  # [78, 82, 100]</code></pre>
            <p>函数里的 <code>append()</code> 直接改动了原始列表。</p>
          </article>
          <article class="command-card">
            <h3>先复制再修改</h3>
            <pre><code class="python">def add_bonus_safe(scores):
    new_scores = scores.copy()
    new_scores.append(100)
    return new_scores</code></pre>
            <p>如果不希望改到原对象，可以先复制，再返回新结果。</p>
          </article>
          <article class="command-card">
            <h3>阅读关键</h3>
            <p>看到列表、字典这类可变对象时，要特别关注函数内部有没有修改操作。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="课堂练习：补全安全加分函数"
      >
        <h3>🛠️ 课堂练习：补全安全加分函数</h3>
        <div class="command-layout chapter-four-practice-grid">
          <article class="command-card chapter-four-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>不要直接修改原列表，先复制再处理。</li>
              <li>给每个成绩加 5 分，但最高不能超过 100 分。</li>
              <li>返回新列表，并观察原列表是否保持不变。</li>
            </ol>
          </article>
          <article class="command-card chapter-four-code-card">
            <pre><code class="python">def add_bonus_safe(scores, bonus):
    new_scores = ________
    for i in range(len(new_scores)):
        new_scores[i] = ________
    return ________

scores = [78, 82, 97]
better_scores = add_bonus_safe(scores, 5)
print("原列表:", scores)
print("新列表:", better_scores)</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">scores.copy()
min(100, new_scores[i] + bonus)
new_scores</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        id="task-recursion"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 4：递归函数"
      >
        <h2>任务 4：递归函数</h2>
        <p class="section-note">
          递归不是“高级魔法”，而是一种特殊的函数调用方式：函数在完成任务的过程中，再次调用自己。
        </p>
        <div class="chapter-four-rhythm">
          <span>先看它怎样停下来</span>
          <span>再看它怎样逐步推进</span>
          <span>最后把规律翻译成代码</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="递归必须满足的两个条件"
      >
        <h3>递归必须满足的两个条件</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>条件 1：有结束条件</h3>
            <p>递归不能无限继续，必须在某个时刻停下来，否则会一直调用自己。</p>
          </article>
          <article class="command-card">
            <h3>条件 2：越来越接近结束</h3>
            <p>每次递归都要让问题规模变小，例如从 <code>n</code> 变成 <code>n - 1</code>。</p>
          </article>
          <article class="command-card">
            <h3>关键句</h3>
            <p>递归是否成立，不是看“有没有自己调用自己”，而是看“能不能停、怎么逼近终点”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="递归入门：倒计时"
      >
        <h3>递归入门：倒计时</h3>
        <pre><code class="python">def countdown(n):
    # 结束条件：倒到 0 就停止
    if n == 0:
        print("开始")
        return

    print(n)
    # 递归推进：离结束条件更近一步
    countdown(n - 1)

countdown(3)</code></pre>
        <p class="section-note">
          这个例子最适合观察递归的骨架：先判断是否结束，再处理当前层，最后把更小的问题交给下一次调用。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="经典示例：阶乘函数"
      >
        <h3>经典示例：阶乘函数</h3>
        <p class="chapter-four-cue">
          <strong>先翻译规律：</strong>“求 <code>n!</code>”其实是在问“当前的 <code>n</code> 乘以前一个更小问题的结果”。把中文规律看明白，代码就不难了。
        </p>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>数学规律</h3>
            <pre><code class="python">5! = 5 * 4 * 3 * 2 * 1

n! = n * (n - 1)!</code></pre>
            <p>递归适合把这种“当前问题依赖更小的同类问题”的规律翻译成代码。</p>
          </article>
          <article class="command-card">
            <h3>递归实现</h3>
            <pre><code class="python">def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))</code></pre>
            <p>当 <code>n == 1</code> 时直接返回；否则就把问题交给 <code>factorial(n - 1)</code>。</p>
          </article>
          <article class="command-card">
            <h3>读代码的顺序</h3>
            <p>先找结束条件，再找递归调用，最后判断每次调用是否真的更接近结束条件。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="递归执行过程：factorial(4)"
      >
        <h3>递归执行过程：<code>factorial(4)</code></h3>
        <div class="chapter-four-trace">
          <article class="command-card">
            <h3>向下展开</h3>
            <pre><code class="python">factorial(4)
= 4 * factorial(3)
= 4 * 3 * factorial(2)
= 4 * 3 * 2 * factorial(1)</code></pre>
          </article>
          <article class="command-card">
            <h3>触底返回</h3>
            <pre><code class="python">factorial(1) = 1

4 * 3 * 2 * 1
= 24</code></pre>
          </article>
          <article class="command-card">
            <h3>理解重点</h3>
            <p>递归并不是“一次算完”，而是先一层层向下展开，到达结束条件后，再一层层返回结果。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="循环和递归怎么选"
      >
        <h3>循环和递归怎么选</h3>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card">
            <h3>适合循环</h3>
            <p>重复次数明确，或天然是“遍历每个元素”的问题，优先考虑 <code>for</code> 和 <code>while</code>。</p>
          </article>
          <article class="concept-card">
            <h3>适合递归</h3>
            <p>问题能自然拆成“同类的小问题”，并且很容易写出结束条件时，递归更清晰。</p>
          </article>
          <article class="concept-card">
            <h3>共同点</h3>
            <p>本质上都在处理重复，只是组织方式不同。循环靠结构，递归靠函数调用。</p>
          </article>
          <article class="concept-card">
            <h3>初学建议</h3>
            <p>先确认问题是否真的适合递归，不要为了用递归而递归。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="递归常见错误"
      >
        <h3>递归常见错误</h3>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card">
            <h3>没有结束条件</h3>
            <p>函数会无限调用自己，直到触发递归深度错误。</p>
          </article>
          <article class="concept-card">
            <h3>方向走错了</h3>
            <p>例如把 <code>n - 1</code> 写成 <code>n + 1</code>，问题会越来越远离终点。</p>
          </article>
          <article class="concept-card">
            <h3>漏掉 return</h3>
            <p>递归函数常常依赖返回值传回上一层，漏写后结果会直接断掉。</p>
          </article>
          <article class="concept-card">
            <h3>把递归当循环背模板</h3>
            <p>真正重要的不是模板，而是看清结束条件和递推关系。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="斐波那契数列：另一种递归结构"
      >
        <h3>斐波那契数列：另一种递归结构</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>规则背景</h3>
            <pre><code class="python">第 1 个月：1
第 2 个月：1
第 n 个月：前两个月之和</code></pre>
            <p>这是一个非常经典的递归模型，也常被用来描述“兔子繁殖”这类增长问题。</p>
          </article>
          <article class="command-card">
            <h3>前几项</h3>
            <pre><code class="python">1, 1, 2, 3, 5, 8, 13, ...</code></pre>
            <p>和阶乘不同，斐波那契不是只依赖前一个结果，而是依赖前两个结果。</p>
          </article>
          <article class="command-card">
            <h3>难点提醒</h3>
            <p>这一类递归会出现两次递归调用，所以更适合检验是否真正理解“结束条件 + 递推关系”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="课堂练习：补全斐波那契函数"
      >
        <h3>🛠️ 课堂练习：补全斐波那契函数</h3>
        <div class="command-layout chapter-four-practice-grid">
          <article class="command-card chapter-four-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>写出两个结束情况：第 1 项和第 2 项都等于 1。</li>
              <li>补出两次递归调用，观察它与阶乘递归的区别。</li>
              <li>思考为什么这里不能只写一次 <code>fibonacci(n - 1)</code>。</li>
            </ol>
          </article>
          <article class="command-card chapter-four-code-card">
            <pre><code class="python">def fibonacci(n):
    if ________:
        return 1
    return ________ + ________

print(fibonacci(7))</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">n == 1 or n == 2
fibonacci(n - 1)
fibonacci(n - 2)</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        id="task-exception"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 5：异常处理"
      >
        <h2>任务 5：异常处理</h2>
        <p class="section-note">
          学生输入不会总是符合预期。异常处理的意义，不是“让错误消失”，而是“让程序在出错后还能继续工作”。
        </p>
        <div class="chapter-four-rhythm">
          <span>先看程序为什么会崩</span>
          <span>再学会接住错误</span>
          <span>最后封装成安全输入函数</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="程序为什么会崩"
      >
        <h3>程序为什么会崩</h3>
        <p class="chapter-four-cue">
          <strong>先看现象：</strong>有些错误不是写代码时出现，而是运行到某一行、遇到非法输入时才出现。
        </p>
        <pre><code class="python">age = int(input("请输入年龄："))
print("明年年龄:", age + 1)</code></pre>
        <p class="section-note">
          如果输入的是 <code>18</code>，程序正常运行；如果输入的是 <code>abc</code>，就会触发
          <code>ValueError</code>。程序不是“坏了”，而是遇到了无法完成的任务。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="try 和 except 的基本结构"
      >
        <h3><code>try</code> 和 <code>except</code> 的基本结构</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>基本写法</h3>
            <pre><code class="python">try:
    age = int(input("请输入年龄："))
    print(age + 1)
except ValueError:
    print("输入错误，请输入整数")</code></pre>
            <p><code>try</code> 里放可能出错的代码，<code>except</code> 里放出错后的处理方式。</p>
          </article>
          <article class="command-card">
            <h3>执行逻辑</h3>
            <p>如果 <code>try</code> 中没有出错，就跳过 <code>except</code>。如果发生指定异常，就执行对应处理。</p>
          </article>
          <article class="command-card">
            <h3>关键认识</h3>
            <p>异常处理不是“忽略问题”，而是用明确方式告诉程序：这种错误出现时应该怎样继续。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="except、else、finally"
      >
        <h3><code>except</code>、<code>else</code>、<code>finally</code></h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>完整结构</h3>
            <pre><code class="python">try:
    n = int(input("请输入整数："))
except ValueError:
    print("输入必须是整数")
else:
    print("平方:", n * n)
finally:
    print("本次输入结束")</code></pre>
            <p><code>else</code> 在没有异常时执行，<code>finally</code> 无论是否出错都会执行。</p>
          </article>
          <article class="command-card">
            <h3>适用理解</h3>
            <p><code>except</code> 负责处理错误，<code>else</code> 负责成功后的额外逻辑，<code>finally</code> 负责收尾动作。</p>
          </article>
          <article class="command-card">
            <h3>初学重点</h3>
            <p>本章最常用的是 <code>try/except</code>。<code>else</code> 和 <code>finally</code> 先做到会读、会用简单场景即可。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="把异常处理封装成安全输入函数"
      >
        <h3>把异常处理封装成安全输入函数</h3>
        <pre><code class="python">def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value &gt; 0:
                return value
            print("请输入大于 0 的整数")
        except ValueError:
            print("输入格式错误，请重新输入")</code></pre>
        <p class="section-note">
          这就是“函数 + 循环 + 异常处理”的组合应用。主流程以后只需要调用一次
          <code>read_positive_int()</code>，就能得到安全的整数输入。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="课堂练习：补全安全输入函数"
      >
        <h3>🛠️ 课堂练习：补全安全输入函数</h3>
        <div class="command-layout chapter-four-practice-grid">
          <article class="command-card chapter-four-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>补出 <code>try</code> 中的整数转换语句。</li>
              <li>只接受大于 0 的整数，合法时直接返回。</li>
              <li>非法输入时输出提示，并继续循环。</li>
            </ol>
          </article>
          <article class="command-card chapter-four-code-card">
            <pre><code class="python">def read_positive_int(prompt):
    while True:
        try:
            value = ________
            if value &gt; 0:
                return ________
            print("请输入大于 0 的整数")
        except ________:
            print("输入格式错误，请重新输入")</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">int(input(prompt))
value
ValueError</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        id="challenge-rabbit"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="综合训练：兔子繁殖预测器"
      >
        <div class="section-head">
          <p class="kicker">INTEGRATED CHALLENGE</p>
          <h2>综合训练：兔子繁殖预测器</h2>
        </div>
        <p class="section-note">
          这个案例比汉诺塔更直观：先看懂“每个月兔子数量怎样增长”，再把这条规则翻译成函数、递归和异常处理。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="规则说明：兔子数量怎样增长"
      >
        <h3>规则说明：兔子数量怎样增长</h3>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card">
            <h3>第 1 个月</h3>
            <p>只有 1 对兔子。</p>
          </article>
          <article class="concept-card">
            <h3>第 2 个月</h3>
            <p>仍然是 1 对兔子。</p>
          </article>
          <article class="concept-card">
            <h3>第 3 个月起</h3>
            <p>当前月份的兔子对数，等于前两个月兔子对数之和。</p>
          </article>
          <article class="concept-card">
            <h3>程序任务</h3>
            <p>输入目标月份，输出该月兔子对数，并打印前 n 个月的变化序列。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="从前几个月观察规律"
      >
        <h3>从前几个月观察规律</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3>前 7 个月</h3>
            <pre><code class="python">月份: 1  2  3  4  5  6  7
数量: 1  1  2  3  5  8  13</code></pre>
            <p>只要把前两项确定下来，后面的每一项都可以由前两项推出。</p>
          </article>
          <article class="command-card">
            <h3>递推关系</h3>
            <pre><code class="python">f(1) = 1
f(2) = 1
f(n) = f(n - 1) + f(n - 2)</code></pre>
            <p>这正是斐波那契数列，也是非常典型的递归模型。</p>
          </article>
          <article class="command-card">
            <h3>为什么适合作为综合训练</h3>
            <p>规则直观，结束条件明确，同时能自然用到函数拆分、递归、异常处理和函数调用函数。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="把综合问题拆成多个函数"
      >
        <h3>把综合问题拆成多个函数</h3>
        <div class="command-layout chapter-four-2plus1">
          <article class="command-card">
            <h3><code>read_month()</code></h3>
            <p>负责安全读取月份，只接受大于 0 的整数。</p>
          </article>
          <article class="command-card">
            <h3><code>fibonacci(n)</code></h3>
            <p>负责计算第 <code>n</code> 个月的兔子对数，是核心递归函数。</p>
          </article>
          <article class="command-card">
            <h3><code>build_sequence(n)</code> 与 <code>main()</code></h3>
            <p>一个负责生成前 n 个月的序列，一个负责组织主流程并输出结果。</p>
          </article>
        </div>
        <p class="section-note">
          这样拆开以后，每个函数都只承担一件事，主流程也更容易阅读和调试。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="核心函数的参数与数据流"
      >
        <h3>核心函数的参数与数据流</h3>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card">
            <h3><code>read_month()</code></h3>
            <p>没有参数，返回一个合法月份。</p>
          </article>
          <article class="concept-card">
            <h3><code>fibonacci(n)</code></h3>
            <p>参数 <code>n</code> 表示目标月份，返回该月兔子对数。</p>
          </article>
          <article class="concept-card">
            <h3><code>build_sequence(n)</code></h3>
            <p>参数 <code>n</code> 表示需要生成几个月的数据，返回一个列表。</p>
          </article>
          <article class="concept-card">
            <h3><code>main()</code></h3>
            <p>先调用输入函数，再调用计算函数和序列函数，最后统一输出。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="综合练习：补全主流程"
      >
        <h3>🛠️ 综合练习：补全主流程</h3>
        <div class="command-layout chapter-four-practice-grid">
          <article class="command-card chapter-four-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>在异常处理中识别整数转换错误。</li>
              <li>只接受大于 0 的月份。</li>
              <li>在 <code>main()</code> 中读取月份，并调用计算函数与序列函数。</li>
            </ol>
          </article>
          <article class="command-card chapter-four-code-card">
            <pre><code class="python">def read_month():
    while True:
        try:
            month = int(input("请输入要查看的月份："))
            if month &gt; 0:
                return month
            print("月份必须大于 0")
        except ________:
            print("请输入整数")

def main():
    month = ________()
    result = fibonacci(month)
    sequence = build_sequence(month)
    print(f"第 {month} 个月:", result)
    print("前几个月:", sequence)</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">ValueError
read_month</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="综合练习：补全递归核心与序列生成"
      >
        <h3>🛠️ 综合练习：补全递归核心与序列生成</h3>
        <div class="command-layout chapter-four-practice-grid">
          <article class="command-card chapter-four-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>补出斐波那契递归的两个结束条件。</li>
              <li>补出两次递归调用，体现“前两个月之和”。</li>
              <li>在循环中不断调用函数，生成完整序列。</li>
            </ol>
          </article>
          <article class="command-card chapter-four-code-card">
            <pre><code class="python">def fibonacci(n):
    if ________:
        return 1
    return ________ + ________

def build_sequence(n):
    data = []
    for month in range(1, n + 1):
        data.append(________)
    return data</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">n == 1 or n == 2
fibonacci(n - 1)
fibonacci(n - 2)
fibonacci(month)</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="运行预览：month = 7"
      >
        <h3>运行预览：<code>month = 7</code></h3>
        <pre><code class="python">第 7 个月: 13
前几个月: [1, 1, 2, 3, 5, 8, 13]</code></pre>
        <p class="section-note">
          这组结果说明程序已经完成了两个任务：既能算出某个月的结果，也能输出从第 1 个月到目标月份的完整变化过程。
        </p>
      </section>

      <section
        id="summary"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章总结"
      >
        <div class="section-head">
          <p class="kicker">SUMMARY</p>
          <h2>本章总结：重复逻辑交给函数，输入风险交给异常处理</h2>
        </div>
        <div class="concept-grid chapter-four-quad-grid">
          <article class="concept-card">
            <h3>函数基础</h3>
            <p>定义函数是“记住功能”，调用函数才是“执行功能”。<code>return</code> 决定结果能否继续被程序使用。</p>
          </article>
          <article class="concept-card">
            <h3>参数与返回值</h3>
            <p>参数是输入接口，返回值是输出接口。普通参数是主线，<code>*args</code> 和 <code>**kwargs</code> 用来处理更灵活的输入场景。</p>
          </article>
          <article class="concept-card">
            <h3>作用域与递归</h3>
            <p>局部变量默认只在函数内部有效。递归必须有结束条件，而且每次都更接近结束条件。</p>
          </article>
          <article class="concept-card">
            <h3>异常处理</h3>
            <p>异常处理不是删除错误，而是给程序一条“出错后还能继续”的路径。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="综合收束：完整思路骨架"
      >
        <h3>综合收束：完整思路骨架</h3>
        <pre><code class="python">def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value &gt; 0:
                return value
            print("请输入大于 0 的整数")
        except ValueError:
            print("输入格式错误，请重新输入")

def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def build_sequence(n):
    data = []
    for month in range(1, n + 1):
        data.append(fibonacci(month))
    return data

def main():
    month = read_positive_int("请输入月份：")
    print(f"第 {month} 个月:", fibonacci(month))
    print("前几个月:", build_sequence(month))</code></pre>
        <p class="section-note">
          这一段骨架同时体现了本章主线：把功能拆成函数，用参数和返回值传数据，用递归解决增长规律，用异常处理保护输入。
        </p>
      </section>
    </main>

    <footer class="footer">
      <p>课堂关键句：重复逻辑交给函数，复杂规律交给拆分，输入风险交给异常处理。</p>
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
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.page.is-slide-deck .chapter-four-rhythm span {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(13, 123, 232, 0.18);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.95), rgba(245, 251, 255, 0.98));
  color: #0b4f88;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
}

.page.is-slide-deck .chapter-four-cue {
  margin: 10px 0 0;
  padding: 10px 12px;
  border-left: 4px solid rgba(13, 123, 232, 0.45);
  border-radius: 10px;
  background: rgba(13, 123, 232, 0.06);
  color: var(--text-main);
  font-size: 0.94rem;
  line-height: 1.65;
}

.page.is-slide-deck .chapter-four-cue strong {
  color: #0a5eaf;
}

.page.is-slide-deck .command-layout.chapter-four-2plus1 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .command-layout.chapter-four-2plus1 > :last-child {
  grid-column: 1 / -1;
}

.page.is-slide-deck .concept-grid.chapter-four-quad-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .concept-grid.chapter-four-quad-grid > .concept-card {
  grid-column: span 1;
}

.page.is-slide-deck .command-layout.chapter-four-practice-grid {
  grid-template-columns: minmax(0, 0.92fr) minmax(0, 1.18fr);
  align-items: start;
}

.page.is-slide-deck .chapter-four-task-card,
.page.is-slide-deck .chapter-four-code-card {
  height: 100%;
}

.page.is-slide-deck .chapter-four-task-card ol {
  margin: 0;
  padding-left: 20px;
}

.page.is-slide-deck .chapter-four-code-card pre,
.page.is-slide-deck .chapter-four-code-card .fragment {
  margin-top: 0;
}

.page.is-slide-deck .chapter-four-code-card code {
  font-size: 0.84rem;
}

.page.is-slide-deck .chapter-four-trace {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

@media (max-width: 900px) {
  .page.is-slide-deck .chapter-four-rhythm,
  .page.is-slide-deck .command-layout.chapter-four-2plus1,
  .page.is-slide-deck .concept-grid.chapter-four-quad-grid,
  .page.is-slide-deck .command-layout.chapter-four-practice-grid,
  .page.is-slide-deck .chapter-four-trace {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .command-layout.chapter-four-2plus1 > :last-child,
  .page.is-slide-deck .concept-grid.chapter-four-quad-grid > .concept-card {
    grid-column: span 1;
  }
}
</style>
