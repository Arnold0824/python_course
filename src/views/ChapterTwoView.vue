<script setup>
import { ref } from 'vue'
import LessonOutlineSidebar from '../components/LessonOutlineSidebar.vue'
import { useLessonDeck } from '../composables/useLessonDeck'

const rootRef = ref(null)
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef)
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
        <span class="brand-tag">Chapter 2</span>
        <strong>Python 基础知识</strong>
      </a>
      <nav class="nav-links" aria-label="页面目录">
        <a href="#card-001">Python 基础：项目实战</a>
        <a href="#card-032">5.1 创建与访问</a>
        <a href="#card-064">任务完成！</a>
      </nav>
    </header>

    <main id="top" class="page is-slide-deck">
      <section
        id="card-001"
        class="hero reveal"
        data-outline-level="1"
        data-outline-label="Python 基础：项目实战"
      >
        <h1>Python 基础：项目实战</h1>
        <h3>构建“英雄档案管理系统”</h3>
        <p class="hero-lead">从零开始打造你的 RPG 游戏角色</p>
        <ul class="hero-checklist">
          <li>学会输入输出、变量、数值运算、字符串与常见容器类型。</li>
          <li>完成 9 个任务与 9 次实战演练，形成完整代码思维。</li>
          <li>最终独立整合并运行 <code>Genesis</code> 英雄档案系统。</li>
        </ul>
        <p class="hero-chapter-mark">第 2 章：语法与数据类型</p>
      </section>
      <section
        id="card-002"
        class="section reveal"
        data-outline-level="1"
        data-outline-label='🚀 任务简报：代号 "Genesis"'
      >
        <h2>🚀 任务简报：代号 "Genesis"</h2>
        <p style="text-align: left; margin-top: 30px">
          你好，新晋工程师。<br />
          欢迎加入 <strong>Neo-Tech 游戏开发部</strong>。
        </p>
        <p style="text-align: left">
          你的第一个任务是为我们的旗舰 RPG 游戏开发核心模块——<br />
          <span class="important">“英雄档案系统” (Hero Profile System)</span>。
        </p>
      </section>
      <section
        id="card-003"
        class="section reveal core-goals-focus"
        data-outline-level="2"
        data-outline-label="核心目标"
      >
        <h3>核心目标</h3>
        <p class="core-goal-intro">
          这一页是本章的能力总览。学完后你不仅要会写语法，还要能把语法拼成一个可运行的小系统。
        </p>
        <div class="core-goal-pillars" aria-label="核心能力框架">
          <article>
            <h4>输入与整理</h4>
            <p>能正确接收玩家输入，并完成基础清洗与格式规范。</p>
          </article>
          <article>
            <h4>计算与状态</h4>
            <p>能处理数值逻辑，维护角色状态并完成过程判断。</p>
          </article>
          <article>
            <h4>建模与输出</h4>
            <p>能用容器组织数据，并输出结构化角色档案。</p>
          </article>
        </div>
        <p class="core-goal-subtitle">你将逐步完成以下 6 类能力拼图：</p>
        <ul>
          <li class="fragment fade-up">🔗 <strong>交互</strong>：与玩家终端通信 (I/O)</li>
          <li class="fragment fade-up">🧾 <strong>存储</strong>：记录玩家 ID 与状态 (Variables)</li>
          <li class="fragment fade-up">🧮 <strong>计算</strong>：处理数值与逻辑判断 (Numbers)</li>
          <li class="fragment fade-up">🎒 <strong>装备</strong>：管理战利品与背包 (Lists)</li>
          <li class="fragment fade-up">📍 <strong>档案</strong>：保存固定信息与坐标 (Tuples)</li>
          <li class="fragment fade-up">🗂️ <strong>整合</strong>：生成完整角色数据卡 (Dicts)</li>
        </ul>
        <p class="core-goal-check fragment">
          达成标准：你可以独立解释“为什么这里用这种数据结构”，并写出可运行的最小示例。
        </p>
        <p style="margin-top: 20px; color: var(--neon-yellow)" class="fragment">准备好接受挑战了吗？</p>
      </section>
      <section
        id="card-004"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="开发任务清单"
      >
        <h2>开发任务清单</h2>
        <div class="two-col">
          <div class="col">
            <ol>
              <li><strong>交互界面</strong>：输入输出</li>
              <li><strong>角色命名</strong>：变量规范</li>
              <li><strong>基础属性</strong>：数值类型</li>
              <li><strong>战斗口号</strong>：字符串处理</li>
              <li><strong>背包系统</strong>：列表操作</li>
            </ol>
          </div>
          <div class="col">
            <ol start="6">
              <li><strong>出生档案</strong>：元组特性</li>
              <li><strong>技能树</strong>：集合去重</li>
              <li><strong>完整档案</strong>：字典映射</li>
              <li><strong>代码规范</strong>：注释与缩进</li>
            </ol>
          </div>
        </div>
      </section>
      <section
        id="card-005"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 1：交互界面 (I/O)"
      >
        <h2>任务 1：交互界面 (I/O)</h2>
        <p>构建游戏控制台：输入指令与系统反馈</p>
        <p class="note">涉及知识点：print, input, 参数控制</p>
      </section>
      <section
        id="card-006"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="print() 系统输出"
      >
        <h3>print() 系统输出</h3>
        <p>向控制台发送信号的基础语法</p>
        <ul>
          <li><strong>基本用法</strong>：<code>print("内容")</code></li>
          <li><strong>多参数</strong>：用逗号分隔，默认输出时会有空格</li>
        </ul>
        <pre><code class="python">
print("系统启动中...")
print("版本:", "1.0", "服务器:", "一区")
# 输出: 版本: 1.0 服务器: 一区</code></pre>
      </section>
      <section
        id="card-007"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="进阶控制：sep 与 end"
      >
        <h3>进阶控制：sep 与 end</h3>
        <p>定制输出格式，制作加载条或特定格式文本</p>
        <ul>
          <li><span class="important">sep</span> (Separator)：多参数之间的分隔符（默认是空格）</li>
          <li>
            <span class="important">end</span>：输出结束后的字符（默认是换行 <code>\n</code>）
          </li>
        </ul>
        <pre><code class="python">
# 1. 自定义分隔符
print("2025", "05", "20", sep="-")
# 输出: 2025-05-20

# 2. 不换行输出 (制作加载效果)
print("加载中", end="...")
print("完成！")
# 输出: 加载中...完成！</code></pre>
      </section>
      <section
        id="card-008"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="input() 玩家指令"
      >
        <h3>input() 玩家指令</h3>
        <p>获取用户键盘输入</p>
        <ul>
          <li>程序运行到此处会<strong>暂停</strong>，等待回车</li>
          <li>
            <span class="important">核心陷阱</span>：无论输入什么，返回值永远是
            <strong>字符串 (str)</strong>
          </li>
        </ul>
        <pre><code class="python">
name = input("请输入角色名: ")
print("欢迎，", name, sep="")

# 类型陷阱演示
age = input("请输入年龄: ")  # 假设输入 18
# age 的值是 "18" (文本)，不是数字 18
# print(age + 1)  ❌ 报错！文本不能加数字</code></pre>
      </section>
      <section
        id="card-009"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 实战演练：身份登记"
      >
        <h3>🛠️ 实战演练：身份登记</h3>
        <p><strong>任务目标</strong>：修复并完善下面的登记脚本。</p>
        <ol>
          <li>读取姓名和职业。</li>
          <li>使用 <code>sep</code> 输出登记结果。</li>
          <li>使用 <code>end</code> 输出欢迎语。</li>
        </ol>
        <pre><code class="python">
name = input("请输入姓名：")
job = input("请输入职业：")

print("登记成功：", name, jobs, sep="-")
print("欢迎加入 创世系统", end)</code></pre>
        <div class="fragment">
          <p style="color: var(--neon-pink)">错误解析：</p>
          <ul>
            <li>f-string 使用了未定义变量 <code>jobs</code>，应改为 <code>job</code>。</li>
            <li><code>end</code> 后面需要提供一个字符串值，例如 <code>end=""</code>。</li>
            <li>本题目标是练习 <code>print</code> 参数控制，不需要提前引入其他语法。</li>
          </ul>
          <p style="color: var(--neon-yellow); margin-top: 12px">参考修正：</p>
          <pre><code class="python">
name = input("请输入姓名：")
job = input("请输入职业：")

print("登记成功：", name, job, sep="-")
print("欢迎加入 创世系统", end="")</code></pre>
        </div>
      </section>
      <section
        id="card-010"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 2：变量与存储"
      >
        <h2>任务 2：变量与存储</h2>
        <p>给数据贴上标签，以便后续引用</p>
        <div class="var-attach-scene">
          <div class="var-tag" aria-hidden="true">
            <svg viewBox="0 0 170 76" role="img" aria-label="变量标签图标">
              <path
                d="M6 38 L36 8 H162 V68 H36 Z"
                fill="#e0f2fe"
                stroke="#0284c7"
                stroke-width="2"
              />
              <circle cx="30" cy="38" r="6.5" fill="#93c5fd" stroke="#0284c7" stroke-width="2" />
            </svg>
            <span class="var-tag-label">hero_name</span>
          </div>
          <div class="var-slot" aria-hidden="true">
            <svg viewBox="0 0 320 128" role="img" aria-label="储物格图标">
              <rect
                x="18"
                y="18"
                width="284"
                height="94"
                rx="16"
                fill="#f8fafc"
                stroke="#64748b"
                stroke-width="3"
              />
              <rect
                x="34"
                y="34"
                width="252"
                height="60"
                rx="10"
                fill="#fef3c7"
                stroke="#ca8a04"
                stroke-width="2.5"
              />
              <rect x="146" y="52" width="28" height="24" rx="6" fill="#f59e0b" />
            </svg>
            <span class="var-slot-value">"亚瑟"</span>
          </div>
        </div>
        <p class="list-visual-note">变量像“有名字的储物格”：名字用于引用，值才是实际内容。</p>
      </section>
      <section
        id="card-011"
        class="section reveal naming-focus"
        data-outline-level="2"
        data-outline-label="&#21464;&#37327;&#21629;&#21517;&#27861;&#21017;"
      >
        <h3>&#21464;&#37327;&#21629;&#21517;&#27861;&#21017;</h3>
        <p class="section-note naming-lead">
          变量名不是“随手起个名”就行。命名清晰，代码可读性会大幅提升，排错速度也会更快。
        </p>
        <div class="naming-contrast" aria-label="命名对照示例">
          <article class="bad">
            <h5>不推荐</h5>
            <p><code>a1</code>、<code>tmp2</code>、<code>x_data</code></p>
          </article>
          <article class="good">
            <h5>推荐</h5>
            <p><code>player_level</code>、<code>current_hp</code>、<code>skill_points</code></p>
          </article>
        </div>
        <p class="naming-formula">
          命名口诀：<strong>对象 + 含义 + 可维护</strong>，例如 <code>player_level</code>、
          <code>hero_name</code>。
        </p>
        <ul>
          <li>
            <strong>硬性规则</strong>：
            <ul>
              <li>只能包含字母、数字、下划线</li>
              <li><span class="important">不能以数字开头</span></li>
              <li>
                不能使用 Python <strong>关键字</strong> (如 <code>if</code>, <code>class</code>)
              </li>
            </ul>
          </li>
          <li><strong>软性规范</strong>：推荐 <code>snake_case</code> (小写_下划线)</li>
        </ul>
        <pre><code class="python">
# ✅ 合法且推荐
hero_name = "亚瑟"
player_level = 1
hp_current = 100

# ❌ 非法变量名
# 2nd_player = "阿勇"   (数字开头)
# my-score = 100       (减号被视为减法运算)
# class = "法师"       (关键字冲突)</code></pre>
      </section>
      <section
        id="card-012"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="关键字 (Keywords)"
      >
        <h3>关键字 (Keywords)</h3>
        <p>Python 的“保留地”，绝对不能占用</p>
        <ul>
          <li>
            常见关键字：<code>if</code>, <code>else</code>, <code>for</code>, <code>while</code>,
            <code>def</code>, <code>class</code>, <code>return</code>, <code>import</code>
          </li>
          <li><strong>技巧</strong>：在编辑器中，关键字通常会变色（如变橙色或紫色）。</li>
        </ul>
        <pre><code class="python">
# 这些名字不能作为变量名
# if = 1
# class = "法师"
# return = "完成"</code></pre>
      </section>
      <section
        id="card-013"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="变量的特性"
      >
        <h3>变量的特性</h3>
        <ul>
          <li><strong>动态类型</strong>：不需要声明类型，赋值即定义。</li>
          <li><strong>覆盖</strong>：重新赋值会覆盖旧值。</li>
        </ul>
        <pre><code class="python">
score = 0
print(score)  # 0

score = 100   # 重新赋值
print(score)  # 100

score = "优秀"  # 甚至可以改变类型 (不推荐但合法)</code></pre>
      </section>
      <section
        id="card-014"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 实战演练：变量纠错"
      >
        <h3>🛠️ 实战演练：变量纠错</h3>
        <p><strong>任务目标</strong>：修复命名错误并完成一次属性汇总输出。</p>
        <ol>
          <li>修复非法变量名（数字开头、减号、关键字）。</li>
          <li>统一为 <code>snake_case</code> 命名风格。</li>
          <li>计算总战力并输出角色摘要。</li>
        </ol>
        <pre><code class="python">
1st_player = "就绪"
my-score = 99
class = "战士"
base_hp = 120
atk = 35
totalPower = base_hp + attack + my_score
print(f"{class}-{1st_player}: {totalPower}")</code></pre>
        <div class="fragment">
          <p style="color: var(--neon-pink)">错误解析：</p>
          <ul>
            <li><code>1st_player</code> 不能以数字开头。</li>
            <li><code>my-score</code> 中的 <code>-</code> 会被当成减法。</li>
            <li><code>class</code> 是关键字，不能作为变量名。</li>
            <li><code>attack</code> 未定义，且 <code>totalPower</code> 不符合蛇形命名规范。</li>
          </ul>
          <p style="color: var(--neon-yellow)">参考修正：</p>
          <pre><code class="python">
first_player = "就绪"
my_score = 99
hero_class = "战士"
base_hp = 120
attack = 35

total_power = base_hp + attack + my_score
print(f"{hero_class}-{first_player}: {total_power}")</code></pre>
        </div>
      </section>
      <section
        id="card-015"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 3：数值系统"
      >
        <h2>任务 3：数值系统</h2>
        <p>构建游戏的数学基石：int, float, bool</p>
        <div class="task-intro-scene task3-scene" aria-hidden="true">
          <span class="intro-tag">数值引擎</span>
          <span class="chip c1">10</span>
          <span class="chip c2">1.5</span>
          <span class="chip c3">True</span>
          <div class="track"></div>
          <span class="formula">攻击 × 1.5 = 暴击</span>
        </div>
      </section>
      <section
        id="card-016"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="三大基础类型"
      >
        <h3>三大基础类型</h3>
        <ul>
          <li>
            <strong>int (整型)</strong>：没有小数点的数字 (如等级 <code>1</code>, 经验
            <code>100</code>)
          </li>
          <li><strong>float (浮点型)</strong>：带小数点的数字 (如攻击速度 <code>1.5</code>)</li>
          <li><strong>bool (布尔型)</strong>：逻辑真假 (<code>True</code> / <code>False</code>)</li>
        </ul>
        <pre><code class="python">
level = 10          # int
atk_speed = 0.8     # float
is_alive = True     # bool

# 查看类型
print(type(level))  # &lt;class 'int'&gt;</code></pre>
      </section>
      <section
        id="card-017"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="核心运算符"
      >
        <h3>核心运算符</h3>
        <div class="table-wrap">
          <table class="ops-table">
            <thead>
              <tr>
                <th>符号</th>
                <th>说明</th>
                <th>示例</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="ops-symbol"><code>+</code> <code>-</code> <code>*</code></td>
                <td><strong>加、减、乘</strong></td>
                <td><code>10+5</code> → <code>15</code></td>
              </tr>
              <tr>
                <td class="ops-symbol"><code>/</code></td>
                <td><strong>真除法</strong>（结果为 float）</td>
                <td><code>10 / 2</code> → <code>5.0</code></td>
              </tr>
              <tr>
                <td class="ops-symbol"><code>//</code></td>
                <td><strong>地板除</strong>（向下取整）</td>
                <td><code>10 // 3</code> → <code>3</code></td>
              </tr>
              <tr>
                <td class="ops-symbol"><code>%</code></td>
                <td><strong>取余</strong>（循环 / 奇偶判断）</td>
                <td><code>10 % 3</code> → <code>1</code></td>
              </tr>
              <tr>
                <td class="ops-symbol"><code>**</code></td>
                <td><strong>幂运算</strong>（次方）</td>
                <td><code>2 ** 3</code> → <code>8</code></td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="tip">
          口诀：<code>/</code> 看小数，<code>//</code> 向下取整，<code>%</code> 看余数。
        </p>
      </section>
      <section
        id="card-018"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="运算符实战"
      >
        <h3>运算符实战</h3>
        <p>用一组战斗数据快速跑通常用运算符，重点看“输出为什么是这个结果”。</p>
        <pre><code class="python">
# 一组数据演示 6 类运算符
atk, defense, hits = 36, 14, 5
hp, max_hp, mana = 45, 100, 18

# 1) 算术 + 优先级
base = atk - defense
total = base * hits + 20
print("算术:", total / hits, total // hits, total % hits, 2 ** 3)
print("优先级:", atk + defense * 2, (atk + defense) * 2)

# 2) 比较 + 逻辑
print("低血量:", hp < 30)
print("可治疗:", (hp < max_hp) and (mana >= 10))
print("仍存活:", not (hp <= 0))

# 3) 赋值
coins = 100
coins += 25
coins //= 3
coins %= 10
print("金币:", coins)

# 4) 复合判断
energy = 12
print("可以连招:", (hits >= 3) and (energy >= 10))
print("需要补给:", (mana < 10) or (hp < 20))</code></pre>
        <p class="tip">教学提示：同学最易混淆的是 <code>/</code> 与 <code>//</code>、<code>==</code> 与 <code>!=</code>。</p>
      </section>
      <section
        id="card-019"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="比较与逻辑运算"
      >
        <h3>比较与逻辑运算</h3>
        <p>让系统学会判断</p>
        <ul>
          <li>
            <strong>比较</strong>：<code>></code>, <code>&lt;</code>, <code>==</code> (等于),
            <code>!=</code> (不等于)
          </li>
          <li>
            <strong>逻辑</strong>：<code>and</code> (且), <code>or</code> (或),
            <code>not</code> (非)
          </li>
        </ul>
        <pre><code class="python">
hp = 50
max_hp = 100

is_full = (hp == max_hp)      # False
is_danger = (hp &lt; 30)         # False
can_heal = (hp &lt; max_hp) and (hp &gt; 0) # True</code></pre>
      </section>
      <section
        id="card-020"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="类型转换 (Casting)"
      >
        <h3>类型转换 (Casting)</h3>
        <p>解决 input() 带来的字符串问题</p>
        <ul>
          <li><code>int(x)</code>: 转为整数</li>
          <li><code>float(x)</code>: 转为浮点数</li>
          <li><code>str(x)</code>: 转为字符串</li>
        </ul>
        <pre><code class="python">
exp_str = input("输入获得经验: ") # 假设输入 "500"

# 必须转换才能计算！
exp = int(exp_str) 
total_exp = exp + 100
print(total_exp)</code></pre>
      </section>
      <section
        id="card-021"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="精度校准 (Float)"
      >
        <h3>精度校准 (Float)</h3>
        <p>浮点数存在微小的精度误差，需使用 <code>round()</code> 修正</p>
        <pre><code class="python">
# 浮点数陷阱
print(0.1 + 0.2)        # 0.30000000000000004

# 使用 round(数值, 小数位数)
print(round(0.1 + 0.2, 1)) # 0.3

# 科学计数法
print(1e3)  # 1000.0</code></pre>
      </section>
      <section
        id="card-022"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 实战演练：伤害计算器"
      >
        <h3>🛠️ 实战演练：伤害计算器</h3>
        <p><strong>任务目标</strong>：修复一个可运行的“暴击伤害计算器”。</p>
        <ol>
          <li>读取攻击力和暴击率（百分比）。</li>
          <li>完成类型转换，按公式 <code>atk * (1 + rate / 100)</code> 计算。</li>
          <li>输出保留 2 位小数的最终伤害。</li>
        </ol>
        <pre><code class="python">
atk_text = input("请输入攻击力：")
crit_rate_text = input("请输入暴击率(%)：")

atk = atk_text
crit_rate = crit_rate_text
final_damage = atk * 1 + crit_rate / 100

print("最终伤害：", round(final_damage, 2))</code></pre>
        <div class="fragment">
          <p style="color: var(--neon-pink)">错误解析：</p>
          <ul>
            <li>公式写错了：应是 <code>atk * (1 + crit_rate / 100)</code>。</li>
            <li><code>atk</code> 和 <code>crit_rate</code> 都还是字符串，不能直接做数值计算。</li>
            <li>暴击率常含小数，建议用 <code>float</code>。</li>
          </ul>
          <p style="color: var(--neon-yellow); margin-top: 12px">参考修正：</p>
          <pre><code class="python">
atk_str = input("请输入攻击力：")
crit_rate_str = input("请输入暴击率(%)：")

atk = int(atk_str)
crit_rate = float(crit_rate_str)
final_damage = atk * (1 + crit_rate / 100)

print("最终伤害：", round(final_damage, 2))</code></pre>
        </div>
      </section>
      <section
        id="card-023"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 4：文本处理 (String)"
      >
        <h2>任务 4：文本处理 (String)</h2>
        <p>处理对话、口号与 ID</p>
        <div class="task-intro-scene task4-scene" aria-hidden="true">
          <span class="intro-tag">文本清洗</span>
          <span class="chip raw">" 火球术 "</span>
          <span class="op">strip()</span>
          <span class="chip clean">"火球术"</span>
          <span class="caret">|</span>
          <span class="hint">输入清洗 + 格式化</span>
        </div>
      </section>
      <section
        id="card-024"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="定义与特性"
      >
        <h3>定义与特性</h3>
        <ul>
          <li>可以使用单引号 <code>'</code> 或双引号 <code>"</code></li>
          <li><strong>不可变性 (Immutable)</strong>：字符串一旦创建，无法修改其中的某个字符。</li>
        </ul>
        <pre><code class="python">
s = "你好"
# s[0] = "您"  ❌ 报错！无法修改

# 正确做法是生成新字符串
s = "您" + s[1:] </code></pre>
      </section>
      <section
        id="card-025"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="索引与切片 (Indexing)"
      >
        <h3>索引与切片 (Indexing)</h3>
        <p>精准提取文本片段</p>
        <ul>
          <li><code>[i]</code>：获取第 i 个字符 (从0开始)</li>
          <li><code>[start:end]</code>：获取子串 (左闭右开，含头不含尾)</li>
        </ul>
        <pre><code class="python">
code = "学号-9527-甲"

print(code[0])      # "学" (首字符)
print(code[-1])     # "甲" (末字符)
print(code[3:7])    # "9527" (从下标3开始，到7之前)</code></pre>
      </section>
      <section
        id="card-026"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="更多常用方法"
      >
        <h3>更多常用方法</h3>
        <ul>
          <li><code>find(sub)</code>: 查找子串位置（找不到返回 -1）</li>
          <li><code>count(sub)</code>: 统计出现次数</li>
          <li><code>startswith(prefix)</code>: 判断开头</li>
        </ul>
        <pre><code class="python">
s = "你好老师好"
print(s.find("老师"))    # 2
print(s.count("好"))     # 2
print(s.startswith("你好")) # True</code></pre>
      </section>
      <section
        id="card-027"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="文本清洗链"
      >
        <h3>文本清洗链</h3>
        <p>清洗与变换用户输入</p>
        <ul>
          <li><code>strip()</code>: 去除首尾空格</li>
          <li><code>upper() / lower()</code>: 大小写转换</li>
          <li><code>replace(old, new)</code>: 替换内容</li>
        </ul>
        <pre><code class="python">
msg = "  火球术  "
clean_msg = msg.strip()
# 结果: "火球术"

text = "我爱旧地图"
new_text = text.replace("旧", "新")
# 结果: "我爱新地图"</code></pre>
      </section>
      <section
        id="card-028"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="f-string 格式化"
      >
        <h3>f-string 格式化</h3>
        <p>Python 最强大的字符串拼接方式</p>
        <pre><code class="python">
name = "亚瑟"
hp = 80
max_hp = 100

# 在字符串前加 f，大括号内写变量
status = f"英雄 {name} 状态: {hp}/{max_hp}"

print(status)
# 输出: 英雄 亚瑟 状态: 80/100</code></pre>
      </section>
      <section
        id="card-029"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="特殊字符 (Escape)"
      >
        <h3>特殊字符 (Escape)</h3>
        <p>使用反斜杠 <code>\</code> 转义特殊符号</p>
        <ul>
          <li><code>\n</code>：换行 (New Line)</li>
          <li><code>\t</code>：制表符 (Tab)</li>
          <li><code>\"</code>：双引号本身</li>
        </ul>
        <pre><code class="python">
print("第一行\n第二行")
print("姓名:\t亚瑟")
print("他说: \"你好\"")</code></pre>
      </section>
      <section
        id="card-030"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 实战演练：公告板生成器"
      >
        <h3>🛠️ 实战演练：公告板生成器</h3>
        <p><strong>任务目标</strong>：修复公告生成脚本，让输出格式统一。</p>
        <ol>
          <li>清洗 Boss 名：去空格、空格替换为下划线。</li>
          <li>保留原始名字，方便对照。</li>
          <li>输出：<code>⚠️ [处理后名字] 已出现！原名=原始名字</code>。</li>
        </ol>
        <pre><code class="python">
boss = "  远古 巨龙  "
clean_boss = boss.strip.replace(" ", "_")
origin_name = boss

print("⚠️ [" + clean_boss + "] 已出现！原名=" + original_name)</code></pre>
        <div class="fragment">
          <p style="color: var(--neon-pink)">错误解析：</p>
          <ul>
            <li><code>boss.strip</code> 漏掉括号，应该写成 <code>boss.strip()</code>。</li>
            <li>输出时使用了未定义变量 <code>original_name</code>，应改为 <code>origin_name</code>。</li>
            <li>本题重点是字符串清洗与格式化，不需要提前引入条件判断。</li>
          </ul>
          <p style="color: var(--neon-yellow); margin-top: 12px">参考修正：</p>
          <pre><code class="python">
boss = "  远古 巨龙  "
origin_name = boss
clean_boss = boss.strip().replace(" ", "_")

print(f"⚠️ [{clean_boss}] 已出现！原名={origin_name}")</code></pre>
        </div>
      </section>
      <section
        id="card-031"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 5：背包系统 (List)"
      >
        <h2>任务 5：背包系统 (List)</h2>
        <p>有序、可变的数据容器</p>
        <div class="task-intro-scene task5-scene" aria-hidden="true">
          <span class="intro-tag">列表示意</span>
          <div class="slot s1">[0] 清水</div>
          <div class="slot s2">[1] 干粮</div>
          <div class="slot s3">[2] 木棍</div>
          <span class="chip incoming">地图</span>
          <span class="hint">insert(0, "地图")</span>
        </div>
      </section>
      <section
        id="card-032"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="创建与访问"
      >
        <h3>创建与访问</h3>
        <ul>
          <li>使用方括号 <code>[]</code></li>
          <li>支持索引和切片 (和字符串一样)</li>
          <li><code>len(列表)</code>：返回列表元素个数（长度）</li>
        </ul>
        <pre><code class="python">
bag = ["药水", "长剑", "地图"]
count = len(bag)  # 3
last_index = count - 1

print(bag[0])   # "药水"
print(count)    # 3 (物品数量)
print(last_index)      # 2
print(bag[last_index]) # "地图"</code></pre>
        <p class="tip"><code>len()</code> 是容器通用函数：字符串、列表、元组、字典、集合都可以求长度。</p>
      </section>
      <section
        id="card-033"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="增加物品 (Add)"
      >
        <h3>增加物品 (Add)</h3>
        <ul>
          <li><code>append(x)</code>: 加到末尾 (最常用)</li>
          <li><code>insert(i, x)</code>: 插到指定位置</li>
        </ul>
        <pre><code class="python">
# 捡到一个盾牌
bag.append("盾牌")
# ["药水", "长剑", "地图", "盾牌"]

# 把关键道具插到第一格
bag.insert(0, "钥匙")
# ["钥匙", "药水", "长剑", "地图", "盾牌"]</code></pre>
      </section>
      <section
        id="card-034"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="删除物品 (Remove)"
      >
        <h3>删除物品 (Remove)</h3>
        <ul>
          <li><code>pop(i)</code>: 移除并返回指定位置的元素 (默认最后一个)</li>
          <li><code>remove(x)</code>: 移除第一个值为 x 的元素</li>
        </ul>
        <pre><code class="python">
# 喝掉最后一瓶药 (弹出末尾)
used_item = bag.pop()

# 丢弃地图 (按名称删除)
bag.remove("地图")</code></pre>
      </section>
      <section
        id="card-035"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="查找、计数与切片"
      >
        <h3>查找、计数与切片</h3>
        <ul>
          <li><strong>切片</strong> <code>[start:end]</code>：提取子列表</li>
          <li><strong>成员判断</strong> <code>in</code>：检查元素是否存在</li>
          <li><strong>查找与计数</strong>：<code>index()</code> / <code>count()</code></li>
        </ul>
        <pre><code class="python">
items = ["药水", "长剑", "地图", "药水"]

# 切片
print(items[0:2])  # ["药水", "长剑"]

# 查找与计数
print(items.count("药水")) # 2
print(items.index("地图")) # 2

# 判断是否存在
print("药水" in items) # True</code></pre>
      </section>
      <section
        id="card-036"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="排序与反转"
      >
        <h3>排序与反转</h3>
        <ul>
          <li><code>sort()</code>：<strong>就地修改</strong>，改变原列表顺序</li>
          <li><code>sorted()</code>：<strong>返回新列表</strong>，原列表不变</li>
          <li><code>reverse()</code>：<strong>原地反转</strong>列表</li>
        </ul>
        <pre><code class="python">
nums = [5, 2, 9, 1]

# 1. 排序
nums.sort()          # nums 变为 [1, 2, 5, 9]
new_nums = sorted([5, 2, 1]) # 返回 [1, 2, 5]

# 2. 反转
nums.reverse()       # nums 变为 [9, 5, 2, 1]</code></pre>
      </section>
      <section
        id="card-037"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="拼接与复制"
      >
        <h3>拼接与复制</h3>
        <p>列表的组合与克隆</p>
        <ul>
          <li><code>+</code>：合并两个列表</li>
          <li><code>*</code>：重复列表元素</li>
          <li><code>copy()</code>：创建副本（互不影响）</li>
        </ul>
        <pre><code class="python">
# 合并
bag_a = ["药水"]
bag_b = ["长剑"]
total = bag_a + bag_b  # ["药水", "长剑"]

# 复制
backup = total.copy()</code></pre>
      </section>
      <section
        id="card-038"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 实战演练：物资整理"
      >
        <h3>🛠️ 实战演练：物资整理</h3>
        <p><strong>任务目标</strong>：修复列表操作脚本并输出关键状态。</p>
        <ol>
          <li>在列表最前面插入 <code>地图</code>，删除 <code>干粮</code>，再追加 <code>急救包</code>。</li>
          <li>输出首项、末项和总数量。</li>
          <li>保证脚本运行不报错。</li>
        </ol>
        <pre><code class="python">
supplies = ["清水", "干粮", "木棍"]
supplies.insert("地图", 0)
supplies.remove("粮食")
supplies.append = "急救包"

first_item = supplies[0]
last_item = supplies[len(supplies)]
print(f"首项={first_item}, 末项={last_item}, 总数={len(supplies)}")</code></pre>
        <div class="fragment">
          <p style="color: var(--neon-pink)">错误解析：</p>
          <ul>
            <li><code>insert</code> 参数顺序应为 <code>(index, item)</code>。</li>
            <li><code>"粮食"</code> 与原列表中的 <code>"干粮"</code> 名称不一致。</li>
            <li><code>append</code> 是方法，不是可直接赋值的属性。</li>
            <li><code>supplies[len(supplies)]</code> 会越界，末项索引应为 <code>-1</code>。</li>
          </ul>
          <p style="color: var(--neon-yellow); margin-top: 12px">参考修正：</p>
          <pre><code class="python">
supplies = ["清水", "干粮", "木棍"]
supplies.insert(0, "地图")
supplies.remove("干粮")
supplies.append("急救包")

first_item = supplies[0]
last_item = supplies[-1]
print(f"首项={first_item}, 末项={last_item}, 总数={len(supplies)}")</code></pre>
        </div>
      </section>
      <section
        id="card-039"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 6：固定档案 (Tuple)"
      >
        <h2>任务 6：固定档案 (Tuple)</h2>
        <p>不可变的有序列表</p>
        <div class="task-intro-scene task6-scene" aria-hidden="true">
          <span class="intro-tag">元组锁定</span>
          <span class="tuple-card">(50, 100)</span>
          <span class="lock-badge">🔒</span>
          <span class="warn">loc[0] = 0 ❌</span>
          <span class="hint">一旦创建，不可修改</span>
        </div>
      </section>
      <section
        id="card-040"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="定义与特性"
      >
        <h3>定义与特性</h3>
        <ul>
          <li>使用圆括号 <code>()</code></li>
          <li><strong>安全</strong>：数据一旦创建，禁止修改、增加或删除。</li>
          <li><strong>场景</strong>：坐标、配置参数、数据库查询结果。</li>
        </ul>
        <pre><code class="python">
# 出生点坐标
spawn_point = (100, 200)

# spawn_point[0] = 50  ❌ 报错！

# 单元素元组陷阱
single = (100,)  # 必须加逗号，否则是整数</code></pre>
      </section>
      <section
        id="card-041"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="解包 (Unpacking)"
      >
        <h3>解包 (Unpacking)</h3>
        <p>快速将元组的值赋给变量</p>
        <pre><code class="python">
pos = (100, 200)

# 自动解包
x, y = pos

print(f"横坐标: {x}")
print(f"纵坐标: {y}")</code></pre>
      </section>
      <section
        id="card-042"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="类型转换"
      >
        <h3>类型转换</h3>
        <p>元组与列表的相互转化</p>
        <ul>
          <li><code>list(t)</code>：转为可变列表（准备修改）</li>
          <li><code>tuple(l)</code>：转为不可变元组（存档）</li>
        </ul>
        <pre><code class="python">
data = (1, 2)
# data[0] = 3 ❌

# 转为列表修改
temp = list(data)
temp[0] = 3
data = tuple(temp) # (3, 2)</code></pre>
      </section>
      <section
        id="card-043"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 实战演练：坐标系统"
      >
        <h3>🛠️ 实战演练：坐标系统</h3>
        <p><strong>任务目标</strong>：修复坐标脚本，体现“元组不可变 + 解包”。</p>
        <ol>
          <li>保留原始坐标元组，创建修改后的新坐标。</li>
          <li>完成解包并计算曼哈顿距离 <code>|x| + |y|</code>。</li>
          <li>输出旧坐标、新坐标和距离。</li>
        </ol>
        <pre><code class="python">
loc = (50, 100)
loc[0] = 0

lat = loc[0]
lng = loc[2]
new_loc = tuple[list(loc)]
distance = lat + " + " + lng

print(f"旧坐标:{loc}, 新坐标:{new_loc}, 距离:{distance}")</code></pre>
        <div class="fragment">
          <p style="color: var(--neon-pink)">错误解析：</p>
          <ul>
            <li>元组不可变，<code>loc[0] = 0</code> 会报错。</li>
            <li><code>loc[2]</code> 越界，只有下标 0 和 1。</li>
            <li><code>tuple[list(loc)]</code> 写法错误，应使用 <code>tuple(list_obj)</code>。</li>
            <li>距离计算不能把数字与字符串直接拼接。</li>
          </ul>
          <p style="color: var(--neon-yellow); margin-top: 12px">参考修正：</p>
          <pre><code class="python">
loc = (50, 100)
temp = list(loc)
temp[0] = 0
new_loc = tuple(temp)

lat, lng = new_loc
distance = abs(lat) + abs(lng)
print(f"旧坐标:{loc}, 新坐标:{new_loc}, 距离:{distance}")</code></pre>
        </div>
      </section>
      <section
        id="card-044"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 7：技能池 (Set)"
      >
        <h2>任务 7：技能池 (Set)</h2>
        <p>无序、不重复的元素集</p>
        <div class="task-intro-scene task7-scene" aria-hidden="true">
          <span class="intro-tag">集合去重</span>
          <span class="orb o1">金币</span>
          <span class="orb o2">金币</span>
          <span class="orb o3">长剑</span>
          <span class="hint">set() 自动去重</span>
        </div>
      </section>
      <section
        id="card-045"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="核心特性：去重"
      >
        <h3>核心特性：去重</h3>
        <ul>
          <li>使用花括号 <code>{}</code> (注意：空集合用 <code>set()</code>)</li>
          <li>自动去除重复元素，适合管理标签、技能。</li>
        </ul>
        <pre><code class="python">
# 玩家重复点击学习
skills = {"火球术", "治疗术", "火球术"}

print(skills)
# 输出: {'火球术', '治疗术'} (自动去重)</code></pre>
      </section>
      <section
        id="card-046"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="集合操作"
      >
        <h3>集合操作</h3>
        <ul>
          <li><code>add(x)</code>: 添加</li>
          <li><code>in</code>: 极速判断是否存在 (比列表快得多)</li>
        </ul>
        <pre><code class="python">
learned = {"攻击", "防御"}
learned.add("闪避")

# 判定是否学会
print("是否学会攻击:", "攻击" in learned)</code></pre>
      </section>
      <section
        id="card-047"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="集合运算"
      >
        <h3>集合运算</h3>
        <p>处理技能与属性的关系</p>
        <ul>
          <li><code>&</code> 交集：同时拥有的</li>
          <li><code>|</code> 并集：所有的（去重）</li>
          <li><code>-</code> 差集：有的没的</li>
        </ul>
        <pre><code class="python">
warrior = {"攻击", "防御"}
mage = {"攻击", "火球术"}

# 通用技能 (交集)
common = warrior &amp; mage # {"攻击"}
# 所有技能 (并集)
all_skills = warrior | mage</code></pre>
      </section>
      <section
        id="card-048"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 实战演练：战利品去重"
      >
        <h3>🛠️ 实战演练：战利品去重</h3>
        <p><strong>任务目标</strong>：修复去重脚本，并完成集合运算输出。</p>
        <ol>
          <li>将战利品列表去重为集合。</li>
          <li>与稀有战利品做并集和交集。</li>
          <li>输出排序后的并集结果与唯一数量。</li>
        </ol>
        <pre><code class="python">
loot = ["金币", "金币", "长剑", "药水", "长剑"}
rare_loot = {"长剑", "宝石"}

unique_loot = {}
unique_loot = set(loot)
all_loot = unique_loot + rare_loot
common_loot = unique_loot and rare_loot

print("全部战利品:", sorted(all_loot))
print("重复过滤后数量:", unique_loot.len())
print("共同战利品:", common_loot)</code></pre>
        <div class="fragment">
          <p style="color: var(--neon-pink)">错误解析：</p>
          <ul>
            <li>集合不能用 <code>+</code> 合并，应使用 <code>|</code>。</li>
            <li><code>and</code> 不是交集运算，应使用 <code>&amp;</code>。</li>
            <li><code>len</code> 是函数，不是集合方法。</li>
          </ul>
          <p style="color: var(--neon-yellow); margin-top: 12px">参考修正：</p>
          <pre><code class="python">
loot = ["金币", "金币", "长剑", "药水", "长剑"}
rare_loot = {"长剑", "宝石"}

unique_loot = set(loot)
all_loot = unique_loot | rare_loot
common_loot = unique_loot &amp; rare_loot

print("全部战利品:", sorted(all_loot))
print("重复过滤后数量:", len(unique_loot))
print("共同战利品:", sorted(common_loot))</code></pre>
        </div>
      </section>
      <section
        id="card-049"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 8：角色卡片 (Dict)"
      >
        <h2>任务 8：角色卡片 (Dict)</h2>
        <p>键值对 (Key-Value) 映射系统</p>
        <div class="task-intro-scene task8-scene" aria-hidden="true">
          <span class="intro-tag">字典映射</span>
          <div class="pair p1">
            <span class="key">姓名</span><span class="arrow">→</span><span class="val">亚瑟</span>
          </div>
          <div class="pair p2">
            <span class="key">生命</span><span class="arrow">→</span><span class="val">100</span>
          </div>
          <span class="dict-shell">{ ... }</span>
          <span class="hint">键 → 值 映射</span>
        </div>
      </section>
      <section
        id="card-050"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="结构与定义"
      >
        <h3>结构与定义</h3>
        <ul>
          <li>使用 <code>{key: value}</code></li>
          <li>Key 必须唯一且不可变 (通常是字符串)</li>
          <li>Value 可以是任意类型 (列表、字典等)</li>
        </ul>
        <pre><code class="python">
hero = {
    "姓名": "亚瑟",
    "等级": 10,
    "生命": 100,
    "背包": ["长剑", "药水"]  # 嵌套列表
}

print(hero["姓名"])  # "亚瑟"</code></pre>
      </section>
      <section
        id="card-051"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="增删改查"
      >
        <h3>增删改查</h3>
        <pre><code class="python">
# 1. 修改/新增 (语法一样)
hero["生命"] = 90          # 修改已有键
hero["称号"] = "新兵"      # 新增键

# 2. 安全查询 get
# print(hero["法力"])    ❌ 报错 (KeyError)
print(hero.get("法力", 0)) # ✅ 返回默认值 0

# 3. 删除
hero.pop("称号")</code></pre>
      </section>
      <section
        id="card-052"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 实战演练：怪物图鉴"
      >
        <h3>🛠️ 实战演练：怪物图鉴</h3>
        <p><strong>任务目标</strong>：修复怪物档案脚本并输出结构化摘要。</p>
        <ol>
          <li>将生命值正确扣减并防止小于 0。</li>
          <li>新增等级信息，安全读取可选字段 <code>元素</code>。</li>
          <li>输出：名称、等级、生命、掉落、元素。</li>
        </ol>
        <pre><code class="python">
monster = {"姓名": "史莱姆", "生命": "10", "掉落": ["凝胶"]}
monster["生命"] = monster["生命"] - 3
monster["等级"] = 1
element = monster["元素"]

print(
    f"{monster['姓名']} 等级{level} 生命={monster['生命']} "
    f"掉落={monster['掉落'][0]} 元素={element}"
)</code></pre>
        <div class="fragment">
          <p style="color: var(--neon-pink)">错误解析：</p>
          <ul>
            <li><code>生命</code> 是字符串，不能直接参与减法。</li>
            <li><code>monster['元素']</code> 可能不存在，直接索引会报错。</li>
            <li>f-string 中 <code>level</code> 未定义，应该从字典中读取。</li>
          </ul>
          <p style="color: var(--neon-yellow); margin-top: 12px">参考修正：</p>
          <pre><code class="python">
monster = {"姓名": "史莱姆", "生命": 10, "掉落": ["凝胶"]}
monster["生命"] = max(0, monster["生命"] - 3)
monster["等级"] = 1
element = monster.get("元素", "无")

print(
    f"{monster['姓名']} 等级{monster['等级']} 生命={monster['生命']} "
    f"掉落={monster['掉落'][0]} 元素={element}"
)</code></pre>
        </div>
      </section>
      <section
        id="card-053"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="遍历视图"
      >
        <h3>遍历视图</h3>
        <p>获取字典的组成部分</p>
        <ul>
          <li><code>keys()</code>：所有键</li>
          <li><code>values()</code>：所有值</li>
          <li><code>items()</code>：所有键值对 (元组形式)</li>
        </ul>
        <pre><code class="python">
# 获取所有键
keys = hero.keys()

# 获取所有值
values = hero.values()

# 获取键值对
items = hero.items()</code></pre>
      </section>
      <section
        id="card-054"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="合并与更新"
      >
        <h3>合并与更新</h3>
        <p>使用 <code>update()</code> 批量修改数据</p>
        <pre><code class="python">
base = {"生命": 100, "法力": 50}
buff = {"法力": 100, "攻击": 20}

# buff 覆盖 base
base.update(buff)
# 结果: {'生命': 100, '法力': 100, '攻击': 20}</code></pre>
      </section>
      <section
        id="card-055"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务 9：代码规范"
      >
        <h2>任务 9：代码规范</h2>
        <p>写出优雅、可读的 Python 代码</p>
        <div class="task-intro-scene task9-scene" aria-hidden="true">
          <span class="intro-tag">代码风格</span>
          <div class="code-line l1"><span class="indent"></span># 角色资料</div>
          <div class="code-line l2"><span class="indent"></span>hero_name = "亚瑟"</div>
          <div class="code-line l3">
            <span class="indent"></span><span class="indent"></span>hero_job = "法师"
          </div>
          <span class="hint">统一缩进，结构清晰</span>
        </div>
      </section>
      <section
        id="card-056"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="注释 (Comments)"
      >
        <h3>注释 (Comments)</h3>
        <p>代码是写给人看的，顺便给机器运行</p>
        <ul>
          <li><strong>单行注释</strong>：使用 <code>#</code></li>
          <li><strong>注释要点</strong>：说明“为什么这样写”，而不是重复代码表面意思。</li>
        </ul>
        <pre><code class="python">
# 记录角色初始资料，后面会统一汇总
hero_name = "亚瑟"
hero_job = "法师"

# 用字典保存两个字段
profile = {
    "姓名": hero_name,
    "职业": hero_job
}</code></pre>
      </section>
      <section
        id="card-057"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="缩进 (Indentation)"
      >
        <h3>缩进 (Indentation)</h3>
        <p>Python 的灵魂：缩进即结构</p>
        <ul>
          <li>其他语言用 <code>{}</code>，Python 用<strong>缩进</strong></li>
          <li><span class="important">强制使用 4 个空格</span></li>
          <li>严禁 Tab 和空格混用！</li>
        </ul>
        <pre><code class="python">
profile = {
    "姓名": "亚瑟",
    "职业": "法师",
    "生命": 80
}

print(profile)</code></pre>
      </section>
      <section
        id="card-058"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🛠️ 实战演练：找茬"
      >
        <h3>🛠️ 实战演练：找茬</h3>
        <p><strong>任务目标</strong>：修复下面代码，让它正确运行并输出角色信息。</p>
        <ol>
          <li>找出并修复至少 <strong>4 处</strong> 问题（缩进、变量名、类型处理）。</li>
          <li>保证程序能输出两行内容：状态 + 角色摘要。</li>
          <li>可选加分：补 1 行注释，说明关键修复点。</li>
        </ol>
        <pre><code class="python">
hero_name = "亚瑟"
 hero_job = "法师"
hp_text = "80"

hp = hp_text + 0
 print("状态: 存活")
print(f"{hero_name} | {job} | 生命={hp}")</code></pre>
        <div class="fragment">
          <p style="color: var(--neon-pink)">错误解析：</p>
          <ul>
            <li><code>hero_job = "法师"</code> 前面多了空格，顶格代码不能随意缩进。</li>
            <li><code>hp = hp_text + 0</code> 把字符串和整数相加会报错，需先转 <code>int</code>。</li>
            <li><code>print("状态: 存活")</code> 前面多了空格，和其他顶格语句不在同一层。</li>
            <li>f-string 中使用了未定义变量 <code>job</code>，应改为 <code>hero_job</code>。</li>
          </ul>
          <p style="color: var(--neon-yellow); margin-top: 12px">参考修正：</p>
          <pre><code class="python">
hero_name = "亚瑟"
hero_job = "法师"
hp_text = "80"

# 先把文本转成整数，再输出摘要
hp = int(hp_text)
print("状态: 存活")
print(f"{hero_name} | {hero_job} | 生命={hp}")</code></pre>
        </div>
      </section>
      <section
        id="card-059"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="🚀 最终挑战：Genesis 系统整合"
      >
        <h2>🚀 最终挑战：Genesis 系统整合</h2>
        <p>将所有模块组装成一个完整的程序</p>
        <p class="note">目标：编写一个“角色初始化脚本”</p>
      </section>
      <section
        id="card-060"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="步骤 1：基础数据录入"
      >
        <h3>步骤 1：基础数据录入</h3>
        <p>利用 I/O、字符串处理与数值转换</p>
        <pre><code class="python">
print("--- 系统启动 ---")

# 1. 输入姓名 (String)
raw_name = input("请输入英雄代号: ")
hero_name = raw_name.strip().upper()  # 清洗数据

# 2. 输入属性 (Int)
atk_str = input("请输入初始攻击力 (1-100): ")
atk = int(atk_str)  # 类型转换
hp = 100            # 默认值</code></pre>
      </section>
      <section
        id="card-061"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="步骤 2：配置装备与技能"
      >
        <h3>步骤 2：配置装备与技能</h3>
        <p>利用列表、元组、集合</p>
        <pre><code class="python">
# 3. 初始化背包 (List - 有序可变)
bag = ["新手剑", "面包"]
bag.append("地图")  # 赠送地图

# 4. 绑定出生点 (Tuple - 固定不可变)
spawn_point = (0, 0)

# 5. 学习技能 (Set - 无序去重)
skills = {"普通攻击"}
skills.add("重击")
skills.add("普通攻击") # 重复学习无效，系统自动去重</code></pre>
      </section>
      <section
        id="card-062"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="步骤 3：生成档案卡"
      >
        <h3>步骤 3：生成档案卡</h3>
        <p>利用字典汇总数据</p>
        <pre><code class="python">
# 6. 汇总数据 (Dict)
hero_data = {
    "代号": hero_name,
    "属性": {"生命": hp, "攻击": atk}, # 字典嵌套
    "背包": bag,
    "坐标": spawn_point,
    "技能": skills
}

# 7. 最终输出 (f-string)
print(f"\n✅ 角色 {hero_data['代号']} 创建成功！")
print(f"当前位置: {hero_data['坐标']}")
print(f"携带物品: {hero_data['背包']}")</code></pre>
      </section>
      <section
        id="card-063"
        class="section reveal"
        data-outline-level="2"
        data-outline-label="🎉 完整代码预览"
      >
        <h3>🎉 完整代码预览</h3>
        <p style="font-size: 0.95rem">(点击放大查看)</p>
        <pre><code class="python" style="max-height: 600px; font-size: 0.9rem;">
# 项目名称：创世英雄档案系统
# 文件名称：genesis_hero_system.py
# 描述：这是一个综合练习，涵盖 Python 基础语法的核心知识点。

print("--- 🚀 创世系统启动 ---")

# ==========================================
# 第一阶段：基础数据录入
# ==========================================

# 1. 获取玩家输入的代号 (String)
raw_name = input("请输入英雄代号: ")
# 知识点：字符串清洗（去空格）与规范化（转大写）
hero_name = raw_name.strip().upper()

# 2. 获取初始攻击力 (Int)
atk_str = input("请输入初始攻击力 (1-100): ")
# 知识点：input 返回的是字符串，必须转换为整数才能进行计算
atk = int(atk_str)
hp = 100  # 默认生命值

# ==========================================
# 第二阶段：配置装备与技能
# ==========================================

# 3. 初始化背包 (List)
# 知识点：列表是有序的、可变的，适合存放背包物品
bag = ["新手剑", "面包"]
bag.append("地图")  # 系统赠送地图

# 4. 绑定出生点 (Tuple)
# 知识点：元组是不可变的，适合存放固定的坐标数据
spawn_point = (0, 0)

# 5. 学习技能 (Set)
# 知识点：集合是无序且不重复的，适合存放技能（防止重复学习）
skills = {"普通攻击"}
skills.add("重击")
skills.add("普通攻击") # 尝试重复添加，系统会自动去重

# ==========================================
# 第三阶段：生成档案卡
# ==========================================

# 6. 汇总数据 (Dict)
# 知识点：字典通过“键值对”存储复杂数据，支持嵌套
hero_data = {
    "代号": hero_name,
    "属性": {"生命": hp, "攻击": atk}, # 字典嵌套
    "背包": bag,                      # 字典的值可以是列表
    "坐标": spawn_point,              # 字典的值可以是元组
    "技能": skills                    # 字典的值可以是集合
}

# 7. 最终输出 (f-string)
print(f"\n✅ 角色 {hero_data['代号']} 创建成功！")
print("-" * 30)
print(f"❤️  生命值: {hero_data['属性']['生命']}")
print(f"⚔️  攻击力: {hero_data['属性']['攻击']}")
print(f"📍 出生点: {hero_data['坐标']}")
print(f"🎒 背包物品: {hero_data['背包']}")
print(f"⚡ 已学技能: {hero_data['技能']}")
print("-" * 30)
print("准备开始冒险！")</code></pre>
      </section>
      <section
        id="card-064"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="任务完成！"
      >
        <h2>任务完成！</h2>
        <p>你已经掌握了构建系统的基石：</p>
        <ul>
          <li>交互 (I/O) 与 存储 (Variables)</li>
          <li>
            四大容器的适用场景：
            <ul>
              <li><strong>List</strong>: 背包 (有序可变)</li>
              <li><strong>Tuple</strong>: 坐标 (不可变)</li>
              <li><strong>Set</strong>: 技能 (去重)</li>
              <li><strong>Dict</strong>: 档案 (键值对)</li>
            </ul>
          </li>
        </ul>
        <h3 style="margin-top: 50px">Ready for Adventure?</h3>
      </section>
    </main>

    <footer class="footer">
      <p>1</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">命令已复制</div>
  </div>
</template>
