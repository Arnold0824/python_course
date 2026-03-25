<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../../../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const expReportHref =
  "/courses/python/exp_reports/实验报告2：编写程序模拟士兵突击任务（理实课程实验部分）-学生姓名.docx";
const expSubmitHref = "https://f.wps.cn/g/JKZmVdtG/";
const expSubmitQrHref = "/courses/python/ch05/2023级计算机科学与技术5班-实验报告2.png";
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
        <span class="brand-tag">Chapter 5</span>
        <strong>面向对象基础</strong>
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
        <p class="kicker">CHAPTER 05 OBJECT-ORIENTED PROGRAMMING</p>
        <h1>面向对象基础：<br />让数据和行为站到一起</h1>
        <p class="hero-intro">
          前四章的主线是顺序、判断、循环和函数。到了第五章，程序开始面对另一类问题：
          一组数据和操作这些数据的行为总是一起出现时，只靠分散的变量和函数会越来越乱。
          这一章要建立新的组织方式，用类描述模板，用对象承载状态，用方法驱动行为。
        </p>
        <ul class="hero-checklist">
          <li>理解对象思维：对象不只是数据，还包含围绕这些数据的行为。</li>
          <li>掌握类、对象、属性、方法、封装、继承和多态的基本写法与作用。</li>
          <li>章节末尾直接收束到综合实践：编写程序模拟士兵突击任务。</li>
        </ul>
        <div class="goal-cards fly-in-seq">
          <article>
            <h2>能力目标 1</h2>
            <p>能独立定义一个类，并创建多个对象。</p>
          </article>
          <article>
            <h2>能力目标 2</h2>
            <p>能通过属性保存状态，通过方法组织行为。</p>
          </article>
          <article>
            <h2>能力目标 3</h2>
            <p>能用继承和多态组织一个小型程序，而不是继续复制粘贴逻辑。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章路线"
      >
        <h2>本章路线：从对象思维，走到综合实践</h2>
        <p class="section-note">
          这一章不再频繁切换案例。整章统一使用“士兵突击任务”这一条主线，让类、对象、属性、方法和三大特征从同一个程序里自然长出来。
        </p>
        <div class="chapter-five-rhythm">
          <span>先感受函数式写法开始变乱</span>
          <span>再理解对象如何组织数据和行为</span>
          <span>最后用一支突击小队完成综合实践</span>
        </div>
        <div class="concept-grid chapter-five-quad-grid">
          <article class="concept-card">
            <h3>第一部分</h3>
            <p>面向对象概念：对象、类、属性、方法。</p>
          </article>
          <article class="concept-card">
            <h3>第二部分</h3>
            <p>类与对象：定义类、创建对象、<code>__init__</code>、<code>self</code>。</p>
          </article>
          <article class="concept-card">
            <h3>第三部分</h3>
            <p>三大特征：封装、继承、多态。</p>
          </article>
          <article class="concept-card">
            <h3>第四部分</h3>
            <p>综合实践：编写程序模拟士兵突击任务。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="为什么需要对象"
      >
        <h2>为什么程序到了这里，会开始需要对象</h2>
        <p class="chapter-five-cue">
          <strong>先看问题本身：</strong>当程序里有很多“士兵”，每个士兵都有姓名、生命值、弹药、攻击力、移动和攻击行为时，
          如果继续把数据拆成很多变量，把行为拆成很多函数，结构会迅速失控。
        </p>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>数据开始成组出现</h3>
            <p>姓名、血量、弹药、攻击力，这些信息天然属于同一个士兵，不适合再被拆散写到程序各处。</p>
          </article>
          <article class="command-card">
            <h3>行为开始绑定到数据</h3>
            <p>移动、攻击、装弹、显示状态，这些行为都依赖士兵自己的属性，因此行为和数据也不该继续分离。</p>
          </article>
          <article class="command-card">
            <h3>对象就是组织方式</h3>
            <p>对象的作用不是“让语法更复杂”，而是把原本就应该放在一起的状态和行为放回到一起。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="痛苦示例"
      >
        <h3>痛苦示例：只靠变量和函数管理多名士兵</h3>
        <pre><code class="python">name1 = "一班长"
hp1 = 100
ammo1 = 30
attack1 = 25

name2 = "二班长"
hp2 = 90
ammo2 = 8
attack2 = 40

def show_status(name, hp, ammo, attack):
    print(f"{name}: HP={hp}, AMMO={ammo}, ATK={attack}")

def fire(name, ammo, attack):
    if ammo &gt; 0:
        print(f"{name} 开火，造成 {attack} 点伤害")
        ammo -= 1
    else:
        print(f"{name} 弹药不足")
    return ammo</code></pre>
        <p class="section-note">
          这段代码暂时还能运行，但问题已经出现了：士兵 1 和士兵 2 的数据被拆成多组变量，行为虽然写成了函数，却仍然需要手动把相关数据一项项传入。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="旧写法为什么会乱"
      >
        <h3>旧写法为什么会越来越乱</h3>
        <div class="concept-grid chapter-five-quad-grid">
          <article class="concept-card">
            <h3>对象一多，变量爆炸</h3>
            <p>每增加一名士兵，就要增加一套姓名、血量、弹药和攻击力变量。</p>
          </article>
          <article class="concept-card">
            <h3>函数调用越来越长</h3>
            <p>只要函数和数据没有绑定，调用时就要不断重复传参。</p>
          </article>
          <article class="concept-card">
            <h3>状态更新容易错位</h3>
            <p>如果返回值没接住，或者把别人的弹药传进来了，程序逻辑就会混乱。</p>
          </article>
          <article class="concept-card">
            <h3>程序缺少现实感</h3>
            <p>代码里并没有“士兵”这个整体对象，只有一堆零散变量，思维上不自然。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="旧写法如何翻译"
      >
        <h3>把旧写法翻译成对象写法</h3>
        <p class="chapter-five-cue">
          <strong>这一页是整章真正的转折点。</strong>
          面向对象不是凭空换一套术语，而是把原来零散写着的变量和函数，重新组合成“一个完整的士兵对象”。
        </p>
        <div class="concept-grid chapter-five-quad-grid">
          <article class="concept-card">
            <h3>旧写法中的一组变量</h3>
            <p><code>name1</code>、<code>hp1</code>、<code>ammo1</code>、<code>attack1</code> 本来就都属于同一个士兵。</p>
          </article>
          <article class="concept-card">
            <h3>翻译成对象</h3>
            <p>这一整组数据可以收进一个对象，例如 <code>soldier1</code>。</p>
          </article>
          <article class="concept-card">
            <h3>旧写法中的函数</h3>
            <p><code>show_status(name, hp, ammo, attack)</code> 和 <code>fire(name, ammo, attack)</code> 本来就在操作士兵自己的数据。</p>
          </article>
          <article class="concept-card">
            <h3>翻译成方法</h3>
            <p>这些函数可以改写成 <code>soldier.show_status()</code> 和 <code>soldier.attack()</code>，让对象自己管理自己的行为。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="面向对象概念"
      >
        <h2>面向对象概念：先把四个基本词讲清楚</h2>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>对象</h3>
            <p>对象是程序里的一个具体事物。这里的一个士兵，就是一个对象。</p>
          </article>
          <article class="command-card">
            <h3>类</h3>
            <p>类是创建对象的模板。士兵类写好以后，才能根据它创建很多具体士兵。</p>
          </article>
          <article class="command-card">
            <h3>属性与方法</h3>
            <p>属性表示对象记住的数据，方法表示对象会做的事。对象不是“只有数据”，而是“数据和行为的组合体”。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="一句话理解对象"
      >
        <h3>一句话理解对象思维</h3>
        <p class="chapter-five-cue">
          <strong>对象 = 数据 + 行为。</strong>
          一个士兵对象，不只是“姓名、血量、弹药”这些数据，还应该知道自己如何显示状态、如何移动、如何攻击和装弹。
        </p>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>旧思路</h3>
            <p>先放很多变量，再让函数来找这些变量。</p>
          </article>
          <article class="command-card">
            <h3>新思路</h3>
            <p>让对象自己保存状态，也让对象自己提供对应的方法。</p>
          </article>
          <article class="command-card">
            <h3>本章核心变化</h3>
            <p>程序不再主要围绕“函数名”展开，而开始围绕“对象”展开。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="类与对象"
      >
        <h2>类与对象：先写模板，再创建实例</h2>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <h3>最小类定义</h3>
            <pre><code class="python">class Soldier:
    pass</code></pre>
            <p>这一步只是在定义模板，还没有创建任何具体士兵。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="创建对象"
      >
        <h3>类定义好了，不等于对象已经存在</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <h3>根据类创建对象</h3>
            <pre><code class="python">class Soldier:
    pass

soldier1 = Soldier()
soldier2 = Soldier()

print(soldier1)
print(soldier2)</code></pre>
            <p>这里的 <code>soldier1</code> 和 <code>soldier2</code> 都是对象，而且是彼此独立的两个对象。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="为什么要有 __init__"
      >
        <h3>为什么要有 <code>__init__</code></h3>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>没有初始化时</h3>
            <p>对象虽然创建出来了，但一开始什么属性都没有，不适合直接使用。</p>
          </article>
          <article class="command-card">
            <h3>初始化的作用</h3>
            <p><code>__init__</code> 会在对象创建时自动执行，用来给对象准备初始状态。</p>
          </article>
          <article class="command-card">
            <h3>本章里的用途</h3>
            <p>士兵在创建时就应该拥有姓名、血量、弹药和攻击力，而不是事后再一项项补写。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="self 是谁"
      >
        <h3><code>self</code> 到底是谁</h3>
        <p class="chapter-five-cue">
          <strong><code>self</code> 指向当前对象自己。</strong>
          哪个对象在调用方法，<code>self</code> 就代表哪个对象。它不是固定名字对应某个对象，而是“调用者自己”。
        </p>
        <div class="concept-grid chapter-five-quad-grid">
          <article class="concept-card">
            <h3><code>soldier1.show_status()</code></h3>
            <p>这里方法里的 <code>self</code> 指向 <code>soldier1</code>。</p>
          </article>
          <article class="concept-card">
            <h3><code>soldier2.show_status()</code></h3>
            <p>这里方法里的 <code>self</code> 指向 <code>soldier2</code>。</p>
          </article>
          <article class="concept-card">
            <h3><code>self.name</code></h3>
            <p>表示当前对象自己的姓名属性。</p>
          </article>
          <article class="concept-card">
            <h3>不能省略</h3>
            <p>只要是对象方法，就必须写出 <code>self</code> 这个参数位置。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="self 为什么不用手传"
      >
        <h3>为什么调用方法时，不用手动传 <code>self</code></h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Soldier:
    def show_status(self):
        print(self)

soldier1 = Soldier()

soldier1.show_status()

# 上面这一句可以理解成：
Soldier.show_status(soldier1)</code></pre>
            <p>
              写成 <code>soldier1.show_status()</code> 时，Python 会自动把当前对象 <code>soldier1</code> 作为第一个参数传进去。
              所以方法定义里必须保留 <code>self</code>，但调用时不需要手动写出来。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="完整 Soldier 类"
      >
        <h3>把士兵类真正写出来</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Soldier:
    def __init__(self, name, hp, ammo, attack_power):
        self.name = name
        self.hp = hp
        self.ammo = ammo
        self.attack_power = attack_power

soldier1 = Soldier("一班长", 100, 30, 25)
soldier2 = Soldier("二班长", 90, 8, 40)

print(soldier1.name, soldier1.hp)
print(soldier2.name, soldier2.hp)</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="对象独立状态"
      >
        <h3>同一个类创建出来的对象，状态彼此独立</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">soldier1 = Soldier("一班长", 100, 30, 25)
soldier2 = Soldier("二班长", 90, 8, 40)

soldier1.ammo -= 1

print("soldier1:", soldier1.ammo)
print("soldier2:", soldier2.ammo)</code></pre>
            <p>修改 <code>soldier1</code> 的弹药，不会自动影响 <code>soldier2</code>。这就是对象实例彼此独立的意义。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="补全练习 1"
      >
        <h3>课堂补全练习：补出类定义、初始化和对象创建</h3>
        <div class="command-layout chapter-five-practice-grid">
          <article class="command-card chapter-five-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>补出 <code>Soldier</code> 类。</li>
              <li>补出初始化方法的参数和属性赋值。</li>
              <li>创建一个具体士兵对象并读取属性。</li>
            </ol>
          </article>
          <article class="command-card chapter-five-code-card">
            <pre><code class="python">class ________:
    def __init__(self, name, hp, ammo, attack_power):
        self.name = ________
        self.hp = ________
        self.ammo = ammo
        self.attack_power = attack_power

soldier = ________("新兵", 100, 20, 18)
print(soldier.________)</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">Soldier
name
hp
Soldier
name</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="属性与方法"
      >
        <h2>属性与方法：对象不只保存数据，还要能行动</h2>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>属性</h3>
            <p>属性表示对象当前保存的数据，例如姓名、血量、弹药和攻击力。</p>
          </article>
          <article class="command-card">
            <h3>方法</h3>
            <p>方法表示对象能执行的行为，例如显示状态、移动、攻击和装弹。</p>
          </article>
          <article class="command-card">
            <h3>关键变化</h3>
            <p>行为不再是散落在类外的函数，而是直接写进类里，让对象自己管理自己的行为。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="第一个方法"
      >
        <h3>第一个方法：让士兵自己显示状态</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Soldier:
    def __init__(self, name, hp, ammo, attack_power):
        self.name = name
        self.hp = hp
        self.ammo = ammo
        self.attack_power = attack_power

    def show_status(self):
        print(f"{self.name}: HP={self.hp}, AMMO={self.ammo}, ATK={self.attack_power}")

soldier = Soldier("一班长", 100, 30, 25)
soldier.show_status()</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="第二个方法"
      >
        <h3>第二个方法：攻击行为开始改变对象状态</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Soldier:
    def __init__(self, name, hp, ammo, attack_power):
        self.name = name
        self.hp = hp
        self.ammo = ammo
        self.attack_power = attack_power

    def attack(self):
        if self.ammo &gt; 0:
            self.ammo -= 1
            print(f"{self.name} 开火，造成 {self.attack_power} 点伤害")
        else:
            print(f"{self.name} 弹药不足")

soldier = Soldier("一班长", 100, 2, 25)
soldier.attack()
soldier.attack()
soldier.attack()</code></pre>
            <p>这里最重要的不是输出内容，而是方法已经能修改对象自己的状态了。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="第三个方法"
      >
        <h3>第三个方法：装弹和移动</h3>
        <div class="command-layout chapter-five-link-grid chapter-five-link-grid--balanced">
          <article class="command-card">
            <h3><code>reload(count)</code></h3>
            <p>让对象自己补充弹药，而不是在类外直接写 <code>soldier.ammo += 10</code>。</p>
          </article>
          <article class="command-card">
            <h3><code>move(position)</code></h3>
            <p>动作也由对象自己执行，程序的表达会更自然，例如“士兵向掩体前进”。</p>
          </article>
          <article class="command-card">
            <h3>方法的真正价值</h3>
            <p>方法把一段“围绕对象状态展开的行为”封装成对象自己的能力，而不是让外部反复操心细节。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="带参数的方法"
      >
        <h3>方法除了 <code>self</code>，也可以接收普通参数</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Soldier:
    def __init__(self, name, hp, ammo, attack_power):
        self.name = name
        self.hp = hp
        self.ammo = ammo
        self.attack_power = attack_power

    def reload(self, count):
        self.ammo += count
        print(f"{self.name} 补充了 {count} 发弹药")

    def move(self, position):
        print(f"{self.name} 向 {position} 前进")

soldier = Soldier("一班长", 100, 10, 25)
soldier.reload(5)
soldier.move("掩体左侧")</code></pre>
            <p>
              这里的 <code>self</code> 仍然代表当前对象，
              <code>count</code> 和 <code>position</code> 则是额外业务参数。
              这一步很重要，因为后面的 <code>attack(target)</code> 也是同样的结构。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="补全练习 2"
      >
        <h3>课堂补全练习：补出状态显示与攻击方法</h3>
        <div class="command-layout chapter-five-practice-grid">
          <article class="command-card chapter-five-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>补出显示状态的方法。</li>
              <li>补出攻击时弹药减少的逻辑。</li>
              <li>理解方法会读取并修改对象自己的属性。</li>
            </ol>
          </article>
          <article class="command-card chapter-five-code-card">
            <pre><code class="python">class Soldier:
    def __init__(self, name, hp, ammo, attack_power):
        self.name = name
        self.hp = hp
        self.ammo = ammo
        self.attack_power = attack_power

    def show_status(self):
        print(f"{self.name}: HP={self.________}, AMMO={self.________}")

    def attack(self):
        if self.ammo &gt; 0:
            self.________ -= 1
            print(f"{self.name} 开火，造成 {self.attack_power} 点伤害")
        else:
            print(f"{self.name} 弹药不足")</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">hp
ammo
ammo</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="封装性"
      >
        <h2>封装性：不要让对象状态被随意破坏</h2>
        <p class="chapter-five-cue">
          <strong>初学阶段先记住思想：</strong>封装不是为了把语法搞神秘，而是为了保护对象状态，让状态变化遵守规则。
        </p>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>为什么要保护状态</h3>
            <p>血量不能小于 0，弹药不能变成负数，这些都属于对象的约束条件。</p>
          </article>
          <article class="command-card">
            <h3>更好的做法</h3>
            <p>通过方法去修改状态，而不是在类外随意写 <code>soldier.hp = -200</code> 这种破坏性操作。</p>
          </article>
          <article class="command-card">
            <h3>这一章如何理解封装</h3>
            <p>先理解“规则控制”和“数据与行为放在一起”，不急着深挖更复杂的私有化细节。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="封装示例"
      >
        <h3>用方法保护血量和弹药</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Soldier:
    def __init__(self, name, hp, ammo, attack_power):
        self.name = name
        self.hp = hp
        self.ammo = ammo
        self.attack_power = attack_power

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp &lt; 0:
            self.hp = 0

    def reload(self, count):
        if count &gt; 0:
            self.ammo += count</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="封装为什么有价值"
      >
        <h3>封装为什么有价值</h3>
        <div class="concept-grid chapter-five-quad-grid">
          <article class="concept-card">
            <h3>规则集中</h3>
            <p>血量下限、弹药变化规则写进方法后，就不必在程序各处重复判断。</p>
          </article>
          <article class="concept-card">
            <h3>状态更安全</h3>
            <p>对象不会轻易被外部代码改成不合理状态。</p>
          </article>
          <article class="concept-card">
            <h3>修改成本更低</h3>
            <p>一旦规则变化，只改方法内部即可。</p>
          </article>
          <article class="concept-card">
            <h3>程序更像现实系统</h3>
            <p>士兵受到伤害、装弹、移动，都是通过“行为”驱动状态变化，而不是直接篡改数据。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="补全练习 3"
      >
        <h3>课堂补全练习：用方法保护状态</h3>
        <div class="command-layout chapter-five-practice-grid">
          <article class="command-card chapter-five-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>补出受伤后的血量修正。</li>
              <li>补出装弹的合法性判断。</li>
              <li>理解封装的重点是“规则保护”。</li>
            </ol>
          </article>
          <article class="command-card chapter-five-code-card">
            <pre><code class="python">def take_damage(self, damage):
    self.hp -= damage
    if self.hp &lt; ________:
        self.hp = ________

def reload(self, count):
    if count ________ 0:
        self.ammo += count</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">0
0
&gt;</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="继承性"
      >
        <h2>继承性：不同兵种的公共部分，不该重复写</h2>
        <p class="section-note">
          当程序里出现很多“相似对象”时，继承的价值就会明显出现。战士、狙击手、重装兵都有共同属性和方法，
          没必要每个类都重新写一遍。
        </p>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>父类</h3>
            <p><code>Soldier</code> 负责保存所有兵种都共有的属性和方法。</p>
          </article>
          <article class="command-card">
            <h3>子类</h3>
            <p><code>RifleSoldier</code>、<code>SniperSoldier</code>、<code>HeavySoldier</code> 继承公共结构，再扩展自己的特性。</p>
          </article>
          <article class="command-card">
            <h3>继承的意义</h3>
            <p>继承不是复制一份父类代码，而是复用父类已有能力，让子类在此基础上继续扩展。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="第一个子类"
      >
        <h3>第一个子类：步枪兵</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Soldier:
    def __init__(self, name, hp, ammo, attack_power):
        self.name = name
        self.hp = hp
        self.ammo = ammo
        self.attack_power = attack_power

class RifleSoldier(Soldier):
    def __init__(self, name, hp, ammo, attack_power, burst_size):
        super().__init__(name, hp, ammo, attack_power)
        self.burst_size = burst_size</code></pre>
            <p><code>super().__init__()</code> 用来复用父类初始化逻辑，再补充子类自己的专属属性。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="更多子类"
      >
        <h3>更多子类：狙击手与重装兵</h3>
        <div class="command-layout chapter-five-link-grid chapter-five-link-grid--balanced">
          <article class="command-card">
            <h3><code>SniperSoldier</code></h3>
            <p>可以扩展一个 <code>scope_level</code> 或 <code>critical_rate</code> 属性，用来表示更强的单发攻击能力。</p>
          </article>
          <article class="command-card">
            <h3><code>HeavySoldier</code></h3>
            <p>可以扩展更高血量、更大弹药量或火力压制能力，体现其角色差异。</p>
          </article>
          <article class="command-card">
            <h3>继承后的效果</h3>
            <p>每个子类不再从零开始写，而是在父类基础上只补充差异部分，程序结构会更清楚。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="方法重写"
      >
        <h3>子类为什么可以写和父类同名的方法：这一步叫方法重写</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Soldier:
    def attack(self):
        print("士兵执行基础攻击")

class RifleSoldier(Soldier):
    def attack(self):
        print("步枪兵使用步枪点射")

base = Soldier()
rifle = RifleSoldier()

base.attack()
rifle.attack()</code></pre>
            <p>
              当子类写出和父类同名的方法时，子类对象优先使用自己的版本。
              这一步就是多态成立的直接前提：先有“重写”，后面才会有“同样调用，不同表现”。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="补全练习 4"
      >
        <h3>课堂补全练习：补出子类和 <code>super()</code></h3>
        <div class="command-layout chapter-five-practice-grid">
          <article class="command-card chapter-five-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>补出子类名与继承关系。</li>
              <li>补出父类初始化调用。</li>
              <li>补出子类自己的新增属性。</li>
            </ol>
          </article>
          <article class="command-card chapter-five-code-card">
            <pre><code class="python">class ________(Soldier):
    def __init__(self, name, hp, ammo, attack_power, burst_size):
        ________(name, hp, ammo, attack_power)
        self.burst_size = ________</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">RifleSoldier
super().__init__
burst_size</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="多态性"
      >
        <h2>多态性：相同调用方式，不同对象表现不同</h2>
        <p class="chapter-five-cue">
          <strong>这一部分不要先背定义。</strong>
          先看现象：同样都叫 <code>attack()</code>，不同兵种执行时，输出和效果并不相同。
        </p>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>步枪兵的攻击</h3>
            <p>强调持续火力和连发特点。</p>
          </article>
          <article class="command-card">
            <h3>狙击手的攻击</h3>
            <p>强调高伤害、低射速和精确打击。</p>
          </article>
          <article class="command-card">
            <h3>多态的关键价值</h3>
            <p>程序只需要统一地调用 <code>attack()</code>，至于具体怎么打，由对象自己决定。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="多态示例"
      >
        <h3>多态示例：统一调用不同士兵的攻击方法</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class RifleSoldier(Soldier):
    def attack(self):
        print(f"{self.name} 使用步枪点射")

class SniperSoldier(Soldier):
    def attack(self):
        print(f"{self.name} 进行远距离狙击")

class HeavySoldier(Soldier):
    def attack(self):
        print(f"{self.name} 发起火力压制")

team = [
    RifleSoldier("一班长", 100, 30, 20, 3),
    SniperSoldier("狙击手", 80, 6, 50),
    HeavySoldier("火力手", 130, 60, 18),
]

for soldier in team:
    soldier.attack()</code></pre>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="多态的意义"
      >
        <h3>多态的意义不在定义，而在使用方式统一</h3>
        <div class="concept-grid chapter-five-quad-grid">
          <article class="concept-card">
            <h3>统一接口</h3>
            <p>外部代码只需要知道“调用 attack”，不必为每个兵种写一套独立流程。</p>
          </article>
          <article class="concept-card">
            <h3>差异留给对象自己</h3>
            <p>具体攻击方式不同，但差异被收在类内部，而不是散落在程序各处。</p>
          </article>
          <article class="concept-card">
            <h3>更适合扩展</h3>
            <p>以后再增加新兵种，只需要新增子类并实现自己的攻击方式。</p>
          </article>
          <article class="concept-card">
            <h3>代码更自然</h3>
            <p>“让小队所有成员执行攻击”这种需求，会变得非常直接。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="对象协作"
      >
        <h3>对象与对象也可以协作</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Target:
    def __init__(self, name, durability):
        self.name = name
        self.durability = durability

    def take_damage(self, damage):
        self.durability -= damage

class RifleSoldier(Soldier):
    def attack(self, target):
        damage = self.attack_power
        target.take_damage(damage)
        print(f"{self.name} 攻击了 {target.name}")</code></pre>
            <p>
              这里的重点不是语法，而是对象关系：
              一个士兵对象的方法可以接收另一个对象 <code>target</code>，
              再调用对方的方法。综合实践里的 <code>attack(target)</code> 就建立在这一步之上。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="对象作为属性"
      >
        <h3>对象的属性，也可以是另一个对象</h3>
        <p class="chapter-five-cue">
          <strong>这一点在实验里会直接用到。</strong>
          士兵不一定只保存字符串和数字，士兵还可以把“枪”作为自己的一个属性。这样程序的结构会更接近真实系统。
        </p>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Gun:
    def __init__(self, model, bullet_count):
        self.model = model
        self.bullet_count = bullet_count

class Soldier:
    def __init__(self, name, gun):
        self.name = name
        self.gun = gun

ak = Gun("AK47", 30)
soldier = Soldier("许三多", ak)</code></pre>
            <p>
              这里的 <code>soldier.gun</code> 不是字符串，也不是数字，而是一个真正的 <code>Gun</code> 对象。
              这类“对象里再放对象”的设计，在面向对象程序里非常常见。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="补全练习 5"
      >
        <h3>课堂补全练习：补出不同兵种的同名方法</h3>
        <div class="command-layout chapter-five-practice-grid">
          <article class="command-card chapter-five-task-card">
            <h3>练习目标</h3>
            <ol>
              <li>补出多个子类中的 <code>attack()</code> 方法。</li>
              <li>理解“同名方法，不同实现”的意义。</li>
              <li>为后面的综合实践做准备。</li>
            </ol>
          </article>
          <article class="command-card chapter-five-code-card">
            <pre><code class="python">class RifleSoldier(Soldier):
    def attack(self):
        print(f"{self.name} ________")

class SniperSoldier(Soldier):
    def attack(self):
        print(f"{self.name} ________")</code></pre>
            <div class="fragment">
              <strong>参考补全</strong>
              <pre><code class="python">使用步枪点射
进行远距离狙击</code></pre>
            </div>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="综合实践引入"
      >
        <div class="section-head">
          <p class="kicker">CAPSTONE PRACTICE</p>
          <h2>综合实践：编写程序模拟士兵突击任务</h2>
        </div>
        <p class="chapter-five-cue">
          这个实验直接对接实验报告中的完整任务，不再额外自创题目。
          它不是只有“士兵类”一个对象，而是同时涉及枪类、枪械子类和士兵类三类对象，并且体现“对象作为另一个对象的属性”。
        </p>
        <div class="concept-grid chapter-five-quad-grid">
          <article class="concept-card">
            <h3>类 1：Gun</h3>
            <p>表示枪类武器，负责型号、子弹数量、装弹和射击行为。</p>
          </article>
          <article class="concept-card">
            <h3>类 2：G95</h3>
            <p>继承自 Gun，增加夜视功能，并重写射击方法。</p>
          </article>
          <article class="concept-card">
            <h3>类 3：Soldier</h3>
            <p>士兵对象拥有姓名和武器，体现“一个对象包含另一个对象”的结构。</p>
          </article>
          <article class="concept-card">
            <h3>实验主线</h3>
            <p>先设计武器，再设计新式武器，最后让士兵装配不同武器并完成冲锋射击。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="为什么适合作为实验"
      >
        <h3>为什么“士兵突击任务”适合作为本章实验</h3>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>不只一个类</h3>
            <p>这个实验不是只有一个 <code>Soldier</code> 类，而是至少有 <code>Gun</code>、<code>G95</code>、<code>Soldier</code> 三个类，结构更完整。</p>
          </article>
          <article class="command-card">
            <h3>三大特征都能落地</h3>
            <p>封装体现在属性管理和对象内部方法，继承体现在 <code>G95(Gun)</code>，多态体现在士兵装配不同武器后调用到不同版本的 <code>shoot()</code>。</p>
          </article>
          <article class="command-card">
            <h3>更贴近实验报告</h3>
            <p>课堂讲授和实验报告采用同一套类设计，学生不会出现“课上是一套，实验又换一套”的断层。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验任务说明"
      >
        <h3>实验任务说明</h3>
        <div class="command-layout chapter-five-2plus1">
          <article class="command-card">
            <h3>任务 1</h3>
            <p>设计 <code>Gun</code> 类，包含 <code>model</code> 和 <code>bullet_count</code> 两个属性，并实现装弹、射击和字符串描述。</p>
          </article>
          <article class="command-card">
            <h3>任务 2</h3>
            <p>设计 <code>G95</code> 类继承自 <code>Gun</code>，增加夜视功能，并重写 <code>shoot()</code> 方法。</p>
          </article>
          <article class="command-card">
            <h3>任务 3</h3>
            <p>设计 <code>Soldier</code> 类，包含姓名和武器两个属性，完成装配武器与冲锋射击，并在主函数中测试不同武器的效果。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="类设计图"
      >
        <h3>综合实践类设计图</h3>
        <div class="concept-grid chapter-five-quad-grid">
          <article class="concept-card">
            <h3>Gun</h3>
            <p>属性：枪型号、子弹数量。方法：装弹、射击、生成字符串描述。</p>
          </article>
          <article class="concept-card">
            <h3>G95</h3>
            <p>Gun 的子类。增加夜视功能，并重写射击方法。</p>
          </article>
          <article class="concept-card">
            <h3>Soldier</h3>
            <p>属性：姓名、武器。方法：冲锋射击、装配武器。</p>
          </article>
          <article class="concept-card">
            <h3>main</h3>
            <p>实例化士兵，先使用默认武器，再装配 G95，观察射击行为变化。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验分任务 1"
      >
        <h3>实验分任务 1：先补全 Gun 类</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Gun:
    def __init__(self, model, bullet_count):
        self.model = model
        self.bullet_count = bullet_count

    def add_bullet(self, count):
        self.bullet_count += count

    def shoot(self):
        if self.bullet_count &lt;= 0:
            print(f"{self.model}没有子弹了")
            return
        self.bullet_count -= 1
        print(f"{self.model}射击哒哒哒... 还有子弹{self.bullet_count}发")

    def __str__(self):
        return self.model</code></pre>
            <p>这一部分负责把“武器对象”本身先立起来。枪要先是一个完整对象，后面士兵才有东西可装配。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验分任务 2"
      >
        <h3>实验分任务 2：再补全 G95 类</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class G95(Gun):
    def add_night_vision(self):
        print(f"{self.model}打开夜间瞄准装置")

    def shoot(self):
        self.add_night_vision()
        super().shoot()</code></pre>
            <p>
              这一段同时体现了两层关系：
              <code>G95</code> 继承 <code>Gun</code>，
              并且通过重写 <code>shoot()</code> 增加自己的扩展能力。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验分任务 3"
      >
        <h3>实验分任务 3：最后补全 Soldier 类与主函数</h3>
        <div class="command-layout chapter-five-single-code">
          <article class="command-card">
            <pre><code class="python">class Soldier:
    def __init__(self, name):
        self.__name = name
        self.__gun = None

    def fire(self):
        if self.__gun is None:
            print(f"{self.__name}还没有枪")
            self.__gun = Gun("56式半自动步枪", 10)
            print(f"{self.__name}自动装配枪支：{self.__gun}")
        else:
            print(f"{self.__name}装配枪支：{self.__gun}")
        print(f"{self.__name}冲啊...")
        self.__gun.shoot()

    def gunfix(self, gun):
        self.__gun = gun

def main():
    soldier = Soldier("许三多")
    soldier.fire()
    print("-" * 10)
    soldier.gunfix(G95("95式自动步枪", 30))
    soldier.fire()</code></pre>
            <p>
              这里同时用到了封装、对象作为属性、继承和多态。
              当士兵装配的武器从 <code>Gun</code> 变成 <code>G95</code> 后，
              调用的仍然是 <code>shoot()</code>，但实际执行的是子类重写后的版本。
            </p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="运行预览"
      >
        <h3>运行预览：一次完整突击任务可能看到的输出</h3>
        <pre><code class="python">许三多还没有枪
许三多自动装配枪支：56式半自动步枪
许三多冲啊...
56式半自动步枪射击哒哒哒... 还有子弹9发
----------
许三多装配枪支：95式自动步枪
许三多冲啊...
95式自动步枪打开夜间瞄准装置
95式自动步枪射击哒哒哒... 还有子弹29发</code></pre>
        <p class="section-note">
          这组输出能直接看出多态效果：士兵调用的仍然是“武器的射击行为”，
          但当武器换成 G95 后，实际执行的已经是子类重写过的 <code>shoot()</code>。
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
          <h2>本章总结：把同一组状态和行为交给对象管理</h2>
        </div>
        <div class="concept-grid chapter-five-quad-grid">
          <article class="concept-card">
            <h3>类与对象</h3>
            <p>类是模板，对象是实例。对象是程序中真正被创建和使用的具体事物。</p>
          </article>
          <article class="concept-card">
            <h3>属性与方法</h3>
            <p>属性表示状态，方法表示行为。对象思维的核心不是“换一种语法”，而是换一种组织程序的方式。</p>
          </article>
          <article class="concept-card">
            <h3>继承与多态</h3>
            <p>继承减少重复，多态统一调用。它们共同解决“对象很多、又彼此相似”的组织问题。</p>
          </article>
          <article class="concept-card">
            <h3>综合实践</h3>
            <p>士兵突击任务把 Gun、G95、Soldier 三个类组织到一起，让封装、继承、多态和对象协作真正落到了程序里。</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="综合收束"
      >
        <h3>综合收束：完整思路骨架</h3>
        <pre><code class="python">class Gun:
    def __init__(self, model, bullet_count):
        self.model = model
        self.bullet_count = bullet_count

    def add_bullet(self, count):
        pass

    def shoot(self):
        pass

    def __str__(self):
        return self.model

class G95(Gun):
    def add_night_vision(self):
        pass

    def shoot(self):
        pass

class Soldier:
    def __init__(self, name):
        self.__name = name
        self.__gun = None

    def fire(self):
        pass

    def gunfix(self, gun):
        self.__gun = gun

def main():
    soldier = Soldier("许三多")
    soldier.fire()
    soldier.gunfix(G95("95式自动步枪", 30))
    soldier.fire()</code></pre>
        <p class="section-note">
          这一段骨架和实验报告完全对齐：先有武器类，再有新式武器子类，最后让士兵对象装配不同武器并执行冲锋射击。
        </p>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="实验报告下载"
      >
        <h3>实验报告下载：编写程序模拟士兵突击任务</h3>
        <div class="command-layout chapter-five-link-grid chapter-five-report-grid">
          <article class="command-card chapter-five-highlight-card chapter-five-report-card">
            <div class="chapter-five-report-content">
              <h3>实验报告 2</h3>
              <p>按章节综合实践完成程序，并基于实验报告整理类设计、程序结构、运行结果和分析结论。</p>
            </div>
            <a class="chapter-five-link" :href="expReportHref" download>
              下载实验报告2：编写程序模拟士兵突击任务
            </a>
          </article>
          <article class="command-card">
            <h3>完成顺序建议</h3>
            <p>先完成 Gun，再完成 G95，最后完成 Soldier 和 main 测试流程。先让武器类独立工作，再让士兵对象装配武器。</p>
          </article>
          <article class="command-card">
            <h3>实验重点</h3>
            <p>不要把重点放在输出花样上，而要把 Gun、G95、Soldier 三个类的职责，以及 shoot()、gunfix()、fire() 的调用关系真正写清楚。</p>
          </article>
          <article class="command-card chapter-five-submit-card">
            <div class="chapter-five-submit-content">
              <div>
                <h3>实验报告提交</h3>
                <p>完成代码、运行结果和实验分析后，将实验报告提交到 WPS 收集表。提交前先检查报告中的类设计、运行截图和分析结论是否完整。</p>
                <a
                  class="chapter-five-link"
                  :href="expSubmitHref"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ expSubmitHref }}
                </a>
              </div>
              <img
                class="chapter-five-submit-qr"
                :src="expSubmitQrHref"
                alt="实验报告2提交二维码"
              />
            </div>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>课堂关键词：当数据和行为总是成组出现时，就让对象来管理它们。</p>
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
.page.is-slide-deck .chapter-five-rhythm {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.page.is-slide-deck .chapter-five-rhythm span {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(13, 123, 232, 0.18);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.95), rgba(245, 251, 255, 0.98));
  color: #0b4f88;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
}

.page.is-slide-deck .chapter-five-cue {
  margin: 10px 0 0;
  padding: 10px 12px;
  border-left: 4px solid rgba(13, 123, 232, 0.45);
  border-radius: 10px;
  background: rgba(13, 123, 232, 0.06);
  color: var(--text-main);
  font-size: 0.94rem;
  line-height: 1.65;
}

.page.is-slide-deck .chapter-five-cue strong {
  color: #0a5eaf;
}

.page.is-slide-deck .command-layout.chapter-five-2plus1 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .command-layout.chapter-five-2plus1 > :last-child {
  grid-column: 1 / -1;
}

.page.is-slide-deck .concept-grid.chapter-five-quad-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .concept-grid.chapter-five-quad-grid > .concept-card {
  grid-column: span 1;
}

.page.is-slide-deck .command-layout.chapter-five-practice-grid {
  grid-template-columns: minmax(0, 0.92fr) minmax(0, 1.18fr);
  align-items: start;
}

.page.is-slide-deck .chapter-five-task-card,
.page.is-slide-deck .chapter-five-code-card {
  height: 100%;
}

.page.is-slide-deck .chapter-five-task-card ol {
  margin: 0;
  padding-left: 20px;
}

.page.is-slide-deck .chapter-five-code-card pre,
.page.is-slide-deck .chapter-five-code-card .fragment {
  margin-top: 0;
}

.page.is-slide-deck .chapter-five-code-card code {
  font-size: 0.84rem;
}

.page.is-slide-deck .command-layout.chapter-five-single-code {
  grid-template-columns: 1fr;
}

.page.is-slide-deck .command-layout.chapter-five-link-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: start;
}

.page.is-slide-deck .command-layout.chapter-five-link-grid.chapter-five-report-grid > .chapter-five-report-card,
.page.is-slide-deck .chapter-five-submit-card {
  grid-column: 1 / -1;
}

.page.is-slide-deck .chapter-five-report-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 18px 24px;
  align-items: end;
}

.page.is-slide-deck .chapter-five-report-content h3,
.page.is-slide-deck .chapter-five-report-content p {
  margin-bottom: 0;
}

.page.is-slide-deck .chapter-five-report-card .chapter-five-link {
  margin-top: 0;
  justify-self: end;
  align-self: center;
}

.page.is-slide-deck .chapter-five-submit-content {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 160px;
  gap: 18px;
  align-items: center;
}

.page.is-slide-deck .chapter-five-submit-qr {
  width: 160px;
  max-width: 100%;
  justify-self: end;
  border-radius: 12px;
  border: 1px solid rgba(13, 123, 232, 0.14);
  box-shadow: 0 10px 24px rgba(13, 62, 108, 0.12);
  background: #fff;
}

.page.is-slide-deck .chapter-five-link {
  display: inline-flex;
  align-items: center;
  min-height: 36px;
  margin-top: 10px;
  color: #0a5eaf;
  font-weight: 700;
  text-decoration: underline;
  word-break: break-all;
}

.page.is-slide-deck .chapter-five-highlight-card {
  border-color: rgba(13, 123, 232, 0.28);
  background: linear-gradient(180deg, rgba(228, 243, 255, 0.94), rgba(255, 255, 255, 0.98));
}

@media (max-width: 900px) {
  .page.is-slide-deck .chapter-five-rhythm,
  .page.is-slide-deck .command-layout.chapter-five-2plus1,
  .page.is-slide-deck .concept-grid.chapter-five-quad-grid,
  .page.is-slide-deck .command-layout.chapter-five-practice-grid,
  .page.is-slide-deck .command-layout.chapter-five-link-grid {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .command-layout.chapter-five-2plus1 > :last-child,
  .page.is-slide-deck .concept-grid.chapter-five-quad-grid > .concept-card,
  .page.is-slide-deck .command-layout.chapter-five-link-grid.chapter-five-report-grid > .chapter-five-report-card,
  .page.is-slide-deck .chapter-five-submit-card {
    grid-column: span 1;
  }

  .page.is-slide-deck .chapter-five-report-card,
  .page.is-slide-deck .chapter-five-submit-content {
    grid-template-columns: 1fr;
  }

  .page.is-slide-deck .chapter-five-report-card .chapter-five-link,
  .page.is-slide-deck .chapter-five-submit-qr {
    justify-self: start;
  }
}
</style>
