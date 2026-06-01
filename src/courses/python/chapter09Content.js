export const chapter09Docs = [
  {
    title: "Matplotlib 官方教程",
    text: "需要查 figure、axes、bar、plot、scatter、hist、savefig 等参数时优先看这里。",
    href: "https://matplotlib.org/stable/tutorials/index.html",
  },
  {
    title: "Matplotlib 图表示例",
    text: "课后自主学习更多图型时，可以从官方 gallery 找相似图，再改成自己的数据。",
    href: "https://matplotlib.org/stable/gallery/index.html",
  },
  {
    title: "pandas 读写 CSV",
    text: "第九章继续使用第八章输出的 CSV，读表和字段检查仍然由 pandas 完成。",
    href: "https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html",
  },
];

export const chapter09ConceptCards = [
  {
    title: "图表不是装饰",
    text: "图表要回答一个具体问题，例如“消费高峰在几点”，不是为了让报告看起来热闹。",
  },
  {
    title: "先定问题",
    text: "先判断自己要看趋势、比较、构成、分布还是关系，再选择合适的图。",
  },
  {
    title: "再定编码",
    text: "x 轴、y 轴、颜色、标注分别承担信息，不要把所有信息都堆到一张图里。",
  },
  {
    title: "最后写结论",
    text: "图表后面必须跟可核对的解释，至少写清字段、最高值、对比对象和具体数值。",
  },
];

export const chartDecisionCards = [
  { type: "趋势", chart: "折线图", question: "某个指标是否随日期变化？", example: "每日消费总额趋势" },
  { type: "比较", chart: "柱状图 / 横向柱状图", question: "哪个类别更多、更高？", example: "小时消费高峰、终端 Top 10" },
  { type: "构成", chart: "占比柱状图 / 饼图", question: "不同类别各占多少？", example: "支付码与 IC 卡占比" },
  { type: "分布", chart: "直方图", question: "数值主要集中在哪个区间？", example: "单笔交易金额分布" },
  { type: "关系", chart: "散点图", question: "两个数值是否一起变化？", example: "消费笔数与消费总额关系" },
];

export const chapter09Resources = [
  {
    title: "第八章输出目录",
    text: "第九章直接读取第八章生成的 hour_summary、daily_summary、payment_summary、student_summary 和 clean 明细。",
    href: "/courses/python/ch08/output/hour_summary.csv",
    download: "hour_summary.csv",
  },
  {
    title: "实验报告 6 模板",
    text: "完成可视化代码、图片和图表解释后，填写此实验报告。",
    href: "/courses/python/exp_reports/实验报告6：学生食堂消费数据可视化（理实课程实验部分）-学生姓名.docx",
    download: "实验报告6：学生食堂消费数据可视化（理实课程实验部分）-学生姓名.docx",
  },
];

export const chapter09MaterialSteps = [
  {
    no: "01",
    title: "先完成第八章",
    text: "确保 public/courses/python/ch08/output/ 下已经有五张统计 CSV。",
  },
  {
    no: "02",
    title: "安装 matplotlib",
    text: "如果导入失败，先执行 python -m pip install matplotlib pandas。",
  },
  {
    no: "03",
    title: "只讲透一张图",
    text: "课堂重点是小时消费高峰图，其他图型用参考代码自主迁移。",
  },
  {
    no: "04",
    title: "图片要进报告",
    text: "每张图保存为 PNG，并在实验报告中写出图回答的问题和具体结论。",
  },
];

export const chapter09Pitfalls = [
  {
    title: "先画图后想问题",
    problem: "先套代码画出很多图，但不知道每张图要说明什么。",
    fix: "每张图先写一句问题，再写 x 轴、y 轴和结论。",
  },
  {
    title: "中文显示成方框",
    problem: "标题、坐标轴或图例中的中文无法显示。",
    fix: "在代码中设置中文字体候选列表，并关闭负号乱码：axes.unicode_minus=False。",
  },
  {
    title: "图表类型不匹配",
    problem: "用折线图画没有顺序的类别，或者用饼图展示太多类别。",
    fix: "趋势用折线，比较用柱状，分布用直方图，关系用散点。",
  },
  {
    title: "轴标签缺失",
    problem: "图片只有柱子或线条，没有标题、单位和字段说明。",
    fix: "至少保留标题、x 轴标签、y 轴标签、必要图例和数据来源说明。",
  },
  {
    title: "只评价好看",
    problem: "报告写“图像清晰、美观”，但没有数据结论。",
    fix: "用具体数值解释，例如“12 点共有 4578 笔，是全天最高峰”。",
  },
  {
    title: "公开个人信息",
    problem: "直接把学号、姓名放进图表或图片文件。",
    fix: "使用第八章的 student_summary_anonymized.csv，只展示 Student001 这类脱敏编号。",
  },
];

export const chapter09Units = [
  {
    no: "01",
    label: "为什么画图",
    title: "1 引入：为什么要把表格结果画成图",
    lead: "第八章已经生成了统计表。第九章不是重新分析数据，而是学习什么时候需要用图把结论讲清楚。",
    code: String.raw`# 这一行把“表格的优势”保存成文字，后面 print 出来让学生先理解表格适合做什么。
table_strength = "表格适合精确保存数字，例如 12 点有 4578 笔。"

# 这一行把“图表的优势”保存成文字，用来强调图表更适合看结构、趋势和差异。
chart_strength = "图表适合看结构，例如午餐和晚餐是不是全天高峰。"

# 这个列表存放本章要回答的可视化问题；以后换题目时，先改这里的问题，再决定画什么图。
questions = [
    # 这个问题适合用柱状图，因为它比较不同小时的交易笔数。
    "消费高峰集中在哪些小时？",
    # 这个问题适合用折线图，因为日期有先后顺序，折线能显示变化。
    "每日消费总额有没有明显波动？",
    # 这个问题适合用柱状图或占比图，因为支付方式是少量类别。
    "支付码和 IC 卡谁更多？",
    # 这个问题适合用散点图，因为要观察两个数值变量是否一起变化。
    "学生消费笔数和消费总额是否大致同步？",
]

# 打印表格的优势，提醒自己不要把图表当成替代表格的工具。
print(table_strength)
# 打印图表的优势，说明为什么第九章需要学习可视化。
print(chart_strength)

# 遍历每一个可视化问题；for 循环适合逐条处理列表中的内容。
for question in questions:
    # 每次循环打印一个问题，帮助学生先从“要回答什么”开始，而不是先背绘图函数。
    print("可视化问题:", question)`,
    explain: "先区分表格和图表各自适合做什么，再列出需要图表回答的问题。",
    why: "如果没有问题，图表就会变成装饰。先问问题，才能判断应该画什么图。",
    points: ["表格保存精确数字。", "图表显示趋势、比较、分布和关系。", "每张图都应该对应一个问题。"],
    terms: [
      { title: "可视化问题", text: "图表真正要回答的一句话。" },
      { title: "图表编码", text: "用位置、长度、颜色、标注表达数据。" },
      { title: "数据结论", text: "能回到数据表核对的解释。" },
    ],
  },
  {
    no: "02",
    label: "准备环境",
    title: "2 准备环境：读取第八章输出表并设置中文字体",
    lead: "第九章直接使用第八章 output 目录下的 CSV。绘图前先处理 matplotlib 中文显示和输出目录。",
    code: String.raw`# 从 pathlib 导入 Path，用它拼接路径，比手写字符串路径更稳定。
from pathlib import Path

# 导入 matplotlib 主包；下一行要先设置后端，所以这里不能只导入 pyplot。
import matplotlib
# 使用 Agg 后端，表示只把图保存成文件，不弹出窗口；适合课堂网页、服务器和 notebook 批量运行。
matplotlib.use("Agg")
# pyplot 是 matplotlib 最常用的绘图入口，后面用 plt.subplots 创建画布和坐标轴。
import matplotlib.pyplot as plt
# font_manager 可以查看电脑里有哪些字体，用来解决中文标题显示成方框的问题。
from matplotlib import font_manager
# Patch 用来手动制作图例色块，主讲图里要用颜色表示餐段。
from matplotlib.patches import Patch
# pandas 用来读取第八章输出的 CSV；matplotlib 负责画图，pandas 负责读表。
import pandas as pd


# 定义一个函数，专门处理中文字体设置；写成函数后，后面需要时可以重复调用。
def setup_chinese_font():
    # 按常见系统列出字体候选；程序会从上到下找本机存在的字体。
    candidates = [
        # macOS 常见中文字体。
        "PingFang SC",
        # macOS 旧版本常见中文字体。
        "Heiti SC",
        # 一些电脑上可用的 Unicode 字体。
        "Arial Unicode MS",
        # Windows 常见中文字体。
        "Microsoft YaHei",
        # Windows / Linux 环境中常见的黑体字体名。
        "SimHei",
        # Linux 或部分环境常见的中文字体。
        "Noto Sans CJK SC",
    ]
    # 读取当前环境中 matplotlib 能找到的字体名称，做成集合方便快速判断。
    available = {font.name for font in font_manager.fontManager.ttflist}
    # 逐个检查候选字体，找到第一个可用字体就使用它。
    for name in candidates:
        # 如果这个字体在当前电脑存在，就可以用于中文显示。
        if name in available:
            # 设置默认无衬线字体；后面的标题、坐标轴和图例都会优先使用这个字体。
            plt.rcParams["font.sans-serif"] = [name]
            # 找到一个可用字体就停止循环，避免后面的字体覆盖前面的选择。
            break
    # 防止坐标轴里的负号显示成方框；虽然本章金额多为正数，但这是绘图常用设置。
    plt.rcParams["axes.unicode_minus"] = False


# 调用刚才定义的函数，让中文字体设置真正生效。
setup_chinese_font()

# DATA_DIR 指向第八章输出表所在目录；第九章不重新清洗数据，直接读取这些结果表。
DATA_DIR = Path("public/courses/python/ch08/output")
# OUTPUT_DIR 指向第九章图片输出目录；所有 PNG 都集中保存到这里，方便插入实验报告。
OUTPUT_DIR = Path("public/courses/python/ch09/output")
# 创建输出目录；parents=True 表示父目录不存在也一起创建，exist_ok=True 表示目录已存在也不报错。
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 读取小时统计表；它包含交易小时、餐段、交易笔数和消费总额，是主讲图的数据来源。
hour_summary = pd.read_csv(DATA_DIR / "hour_summary.csv")
# 查看前几行，确认 CSV 被正确读取，字段名和数据内容都符合预期。
print(hour_summary.head())
# 打印输出目录，方便学生运行后知道图片保存到了哪里。
print("输出目录:", OUTPUT_DIR)`,
    explain: "先导入 pandas 和 matplotlib，设置中文字体候选列表，再读取 hour_summary.csv。",
    why: "真实报告不能只在屏幕上显示图，必须能稳定保存 PNG；中文标题和坐标轴也要能正常显示。",
    points: ["matplotlib.use('Agg') 适合保存图片。", "中文字体要提前设置。", "OUTPUT_DIR 用于集中保存图表。"],
    terms: [
      { title: "matplotlib", text: "Python 常用绘图库。" },
      { title: "rcParams", text: "matplotlib 的全局显示设置。" },
      { title: "savefig", text: "把图保存为图片文件。" },
    ],
  },
  {
    no: "03",
    label: "选图原则",
    title: "3 核心原则：先判断问题类型，再选择图表",
    lead: "学生常犯的错误是记住了 plot、bar、pie，却不知道什么时候用。先把问题类型分清楚。",
    code: String.raw`# 用 DataFrame 保存“问题类型 -> 适合图表 -> 食堂消费例子”的对照表。
chart_guide = pd.DataFrame([
    # 趋势问题有时间顺序，所以通常用折线图表达变化。
    {"问题类型": "趋势", "适合图表": "折线图", "例子": "每日消费总额随日期变化"},
    # 比较问题关注类别高低，所以柱状图更直观。
    {"问题类型": "比较", "适合图表": "柱状图", "例子": "每个小时的交易笔数比较"},
    # 构成问题关注占比，少量类别可用饼图，也可以用占比柱状图。
    {"问题类型": "构成", "适合图表": "占比柱状图或饼图", "例子": "支付方式占比"},
    # 分布问题关注数值集中在哪些区间，直方图最常用。
    {"问题类型": "分布", "适合图表": "直方图", "例子": "单笔金额主要集中在哪些区间"},
    # 关系问题关注两个数值是否一起变化，散点图最合适。
    {"问题类型": "关系", "适合图表": "散点图", "例子": "消费笔数和消费总额的关系"},
])

# 打印这张对照表；以后遇到新数据，先用这张表判断该选哪种图。
print(chart_guide)`,
    explain: "这段代码把图表选择原则整理成一张小表，后面所有图都按这个逻辑选择。",
    why: "掌握原则比背函数更重要。遇到新问题时，先判断问题类型，再查具体代码。",
    points: ["趋势看时间顺序。", "比较看类别高低。", "分布看数值集中区间。"],
    terms: [
      { title: "趋势", text: "一个指标随时间或顺序变化。" },
      { title: "比较", text: "多个类别之间谁多谁少。" },
      { title: "分布", text: "数值集中、离散或偏斜的情况。" },
    ],
  },
  {
    no: "04",
    label: "主讲问题",
    title: "4 主讲问题：学生一天中什么时候最集中消费",
    lead: "这张图不是为了练习柱状图，而是为了回答“消费高峰在哪些小时”。",
    code: String.raw`# 按“交易笔数”从高到低排序，并查看前 5 行，用来确认哪些小时最繁忙。
print(hour_summary.sort_values("交易笔数", ascending=False).head(5))

# idxmax 找到“交易笔数”最大值所在的行位置；loc 再按这个位置取出整行数据。
peak_row = hour_summary.loc[hour_summary["交易笔数"].idxmax()]
# 用 f-string 生成一句可直接写进报告的结论；int 用来把 12.0 这类数显示成 12。
print(
    # 这里说明最高峰发生在哪个小时。
    f"最高峰是 {int(peak_row['交易小时'])} 点，"
    # 这里说明最高峰对应多少笔交易，这是图表结论的关键证据。
    f"共有 {int(peak_row['交易笔数'])} 笔交易，"
    # 这里说明最高峰属于哪个餐段，方便解释为什么这个时段高。
    f"属于{peak_row['餐段']}。"
)`,
    explain: "画图前先从表格里找出最高峰，明确图表要突出什么。",
    why: "图表要服务结论。先知道重点，再决定是否需要颜色、标注和排序。",
    points: ["问题是消费高峰。", "数据字段是交易小时和交易笔数。", "主图选择柱状图，因为它比较不同小时。"],
    terms: [
      { title: "峰值", text: "某个指标的最高点。" },
      { title: "idxmax", text: "返回最大值所在行的位置。" },
      { title: "主讲图", text: "课堂上完整讲解思路和代码的一张图。" },
    ],
  },
  {
    no: "05",
    label: "画主图",
    title: "5 怎么画：小时消费高峰柱状图",
    lead: "这一段只讲一套最核心的 matplotlib 结构：创建画布、画柱子、设置标题坐标轴、标出峰值、保存图片。",
    code: String.raw`# 用字典规定每个餐段的颜色；颜色只辅助理解，不承担主要结论。
meal_colors = {
    # 早间使用蓝色，和午餐、晚餐区分开。
    "早间": "#4e79a7",
    # 午餐使用橙色，因为本章最高峰在午餐时段，颜色较醒目。
    "午餐": "#f28e2b",
    # 下午使用绿色，表示过渡时段。
    "下午": "#59a14f",
    # 晚餐使用红色，方便和午餐峰值比较。
    "晚餐": "#e15759",
    # 夜间使用紫色，作为较少出现的时段。
    "夜间": "#b07aa1",
}

# 按 hour_summary 中的“餐段”列去字典里查颜色；每一根柱子都会得到一个对应颜色。
bar_colors = hour_summary["餐段"].map(meal_colors).fillna("#777777")
# 找到交易笔数最高的行，后面要用它添加箭头标注。
peak_row = hour_summary.loc[hour_summary["交易笔数"].idxmax()]

# 创建画布和坐标轴；fig 是整张图，ax 是具体绘图区，figsize 控制图片宽高。
fig, ax = plt.subplots(figsize=(10, 5))
# 画柱状图；x 轴放交易小时，y 轴放交易笔数，颜色来自上面生成的 bar_colors。
ax.bar(hour_summary["交易小时"], hour_summary["交易笔数"], color=bar_colors)

# 设置图标题，让读者一眼知道这张图回答“小时高峰”问题。
ax.set_title("学生食堂消费小时高峰")
# 设置 x 轴名称，说明横轴数字代表交易小时。
ax.set_xlabel("交易小时")
# 设置 y 轴名称，说明柱子高度代表交易笔数。
ax.set_ylabel("交易笔数")
# 指定 x 轴刻度为实际出现的小时，避免 matplotlib 自动省略关键小时。
ax.set_xticks(hour_summary["交易小时"])
# 添加横向网格线，方便读者比较不同柱子的高度。
ax.grid(axis="y", linestyle="--", alpha=0.35)

# 在最高柱子旁边添加文字和箭头，让读者马上看到核心结论。
ax.annotate(
    # 标注文字分两行：第一行写小时，第二行写交易笔数。
    f"最高峰：{int(peak_row['交易小时'])} 点\\n{int(peak_row['交易笔数'])} 笔",
    # xy 是箭头指向的位置，也就是最高峰柱子的顶部。
    xy=(peak_row["交易小时"], peak_row["交易笔数"]),
    # xytext 是文字摆放的位置，向右上方移动一点，避免遮住柱子。
    xytext=(peak_row["交易小时"] + 0.8, peak_row["交易笔数"] + 350),
    # arrowprops 控制箭头样式；这里用简单箭头和深灰色。
    arrowprops={"arrowstyle": "->", "color": "#333333"},
)

# 手动制作图例，因为柱子颜色是按餐段映射得到的。
legend_items = [
    # Patch 代表一个图例色块，facecolor 是颜色，label 是图例文字。
    Patch(facecolor=color, label=meal)
    # 遍历颜色字典中的每个餐段和颜色。
    for meal, color in meal_colors.items()
    # 只把数据中真实出现过的餐段放进图例，避免出现空类别。
    if meal in set(hour_summary["餐段"])
]
# 把图例放到图中，并用“餐段”作为图例标题。
ax.legend(handles=legend_items, title="餐段")

# 自动调整边距，减少标题、坐标轴标签或图例被裁掉的风险。
plt.tight_layout()
# 保存图片；dpi=160 控制清晰度，适合插入实验报告。
fig.savefig(OUTPUT_DIR / "hour_peak.png", dpi=160)
# 关闭当前图，释放内存，避免后面继续画图时叠到同一张画布上。
plt.close(fig)

# 打印保存路径，方便学生确认图片已经生成。
print("已保存:", OUTPUT_DIR / "hour_peak.png")`,
    explain: "fig 和 ax 是 matplotlib 推荐的画图入口；bar 画柱子；annotate 标出峰值；savefig 保存图片。",
    why: "学生只要先掌握这一套结构，就可以迁移到折线图、散点图和直方图。",
    points: ["x 轴是交易小时。", "y 轴是交易笔数。", "颜色只用来辅助说明餐段，不能喧宾夺主。"],
    terms: [
      { title: "fig", text: "整张画布。" },
      { title: "ax", text: "具体绘图区。" },
      { title: "annotate", text: "在图上添加文字和箭头标注。" },
    ],
  },
  {
    no: "06",
    label: "解释主图",
    title: "6 怎么解释：从图回到可核对的结论",
    lead: "图画完不等于分析完成。报告里要写出图回答了什么问题、依据哪些字段、观察到哪些具体数值。",
    code: String.raw`# 先按交易笔数排序，再取前三名，用来写“最高峰及其次高峰”的报告结论。
top_hours = hour_summary.sort_values("交易笔数", ascending=False).head(3)

# 遍历前三个小时；iterrows 会逐行返回索引和这一行数据。
for _, row in top_hours.iterrows():
    # 把每个小时的笔数、金额和餐段打印成完整句子，方便直接改写进实验报告。
    print(
        # 输出小时，例如“12 点”。
        f"{int(row['交易小时'])} 点："
        # 输出交易笔数，这是判断高峰的核心指标。
        f"{int(row['交易笔数'])} 笔，"
        # 输出消费总额，帮助学生补充金额层面的解释。
        f"消费总额 {row['消费总额']:.2f} 元，"
        # 输出餐段，帮助解释为什么该小时交易集中。
        f"餐段为{row['餐段']}。"
    )

# 打印一条示范报告句，强调图表解释必须包含具体数值和排序对象。
print("报告写法：小时消费高峰图显示，12 点交易笔数最高，其次是 17 点和 18 点。")`,
    explain: "从图对应的数据表中取前三个小时，用具体笔数和金额写成报告语言。",
    why: "可视化的贡献是让结论更清楚，不是替代表格。关键结论仍然要能回到 CSV 核对。",
    points: ["说明图回答的问题。", "说明使用的字段。", "说明具体数值。"],
    terms: [
      { title: "图表解释", text: "把视觉模式翻译成可核对文字。" },
      { title: "Top 3", text: "排序后最靠前的三个对象。" },
      { title: "报告写法", text: "面向读者的简短结论。" },
    ],
  },
];

export const referenceCharts = [
  {
    no: "A",
    label: "趋势折线图",
    title: "参考 A：每日消费总额趋势折线图",
    question: "每日消费总额是否存在明显波动？",
    data: "daily_summary.csv",
    output: "daily_trend.png",
    why: "日期有天然顺序，折线图适合观察随时间变化的趋势。",
    code: String.raw`# 读取每日统计表；parse_dates 把“交易日期”直接解析为日期类型，方便按时间画折线。
daily_summary = pd.read_csv(DATA_DIR / "daily_summary.csv", parse_dates=["交易日期"])

# 创建一张 10 x 4.8 英寸的画布；折线图横轴日期较长，所以画布要稍微宽一些。
fig, ax = plt.subplots(figsize=(10, 4.8))
# 画折线图；x 轴是交易日期，y 轴是消费总额，linewidth 控制线条粗细。
ax.plot(daily_summary["交易日期"], daily_summary["消费总额"], color="#4e79a7", linewidth=1.8)

# 设置标题，说明这张图回答“每日消费总额是否波动”的问题。
ax.set_title("每日消费总额趋势")
# 设置 x 轴标签，告诉读者横轴表示日期。
ax.set_xlabel("交易日期")
# 设置 y 轴标签，告诉读者纵轴单位是元。
ax.set_ylabel("消费总额（元）")
# 添加横向网格线，方便比较不同日期的消费总额。
ax.grid(axis="y", linestyle="--", alpha=0.35)
# 自动旋转和调整日期标签，避免日期文字挤在一起。
fig.autofmt_xdate()

# 自动调整布局，避免坐标轴文字被裁剪。
plt.tight_layout()
# 保存趋势图，文件名固定，方便插入实验报告。
fig.savefig(OUTPUT_DIR / "daily_trend.png", dpi=160)
# 关闭画布，避免影响后续图表。
plt.close(fig)`,
  },
  {
    no: "B",
    label: "支付方式",
    title: "参考 B：支付方式对比柱状图",
    question: "支付码和 IC 卡哪种方式使用更多？",
    data: "payment_summary.csv",
    output: "payment_compare.png",
    why: "支付方式只有少量类别，柱状图能直接比较交易笔数和占比。",
    code: String.raw`# 读取支付方式统计表；它包含支付方式、交易笔数、消费总额和笔数占比。
payment_summary = pd.read_csv(DATA_DIR / "payment_summary.csv")

# 创建画布和坐标轴；支付方式只有两个类别，所以画布不需要太宽。
fig, ax = plt.subplots(figsize=(7, 4.5))
# 画柱状图；x 轴是支付方式，y 轴是交易笔数，颜色列表给不同支付方式不同颜色。
bars = ax.bar(payment_summary["支付方式"], payment_summary["交易笔数"], color=["#4e79a7", "#f28e2b"])

# 设置标题，说明这张图比较的是支付方式交易笔数。
ax.set_title("支付方式交易笔数对比")
# 设置 x 轴标签，告诉读者横轴是支付方式类别。
ax.set_xlabel("支付方式")
# 设置 y 轴标签，告诉读者柱子高度表示交易笔数。
ax.set_ylabel("交易笔数")
# 添加横向网格线，方便比较两根柱子的高度。
ax.grid(axis="y", linestyle="--", alpha=0.35)

# 同时遍历每根柱子和对应占比，把占比文字写在柱子上方。
for bar, ratio in zip(bars, payment_summary["笔数占比"]):
    # ax.text 用于在图上写文字；这里把文字放到每根柱子的顶部。
    ax.text(
        # bar.get_x() 是柱子左边界，bar.get_width()/2 用来移动到柱子中心。
        bar.get_x() + bar.get_width() / 2,
        # bar.get_height() 是柱子高度，把文字放在这个高度上方。
        bar.get_height(),
        # 把 0.6238 这类小数格式化为 62.4%。
        f"{ratio:.1%}",
        # 水平居中对齐，让百分比在柱子正上方。
        ha="center",
        # 垂直方向从文字底部对齐柱顶，避免文字压进柱子。
        va="bottom",
    )

# 自动调整边距，避免标题或标签被裁剪。
plt.tight_layout()
# 保存支付方式对比图。
fig.savefig(OUTPUT_DIR / "payment_compare.png", dpi=160)
# 关闭画布，避免影响后续图表。
plt.close(fig)`,
  },
  {
    no: "C",
    label: "关系散点图",
    title: "参考 C：消费笔数与消费总额散点图",
    question: "消费笔数越多，消费总额是否也越高？",
    data: "student_summary_anonymized.csv",
    output: "student_scatter.png",
    why: "两个数值变量之间的关系，用散点图比表格更容易观察。",
    code: String.raw`# 读取脱敏后的学生汇总表；这里没有姓名和学号，适合公开展示。
student_summary = pd.read_csv(DATA_DIR / "student_summary_anonymized.csv")

# 创建画布和坐标轴；散点图需要同时观察横向和纵向分布。
fig, ax = plt.subplots(figsize=(7.5, 5))
# 画散点图；每个点代表一个脱敏学生。
ax.scatter(
    # x 轴使用消费笔数，用来表示消费频率。
    student_summary["消费笔数"],
    # y 轴使用消费总额，用来表示消费规模。
    student_summary["消费总额"],
    # s 控制点的大小，太小看不清，太大容易重叠。
    s=60,
    # color 控制点的颜色，统一颜色可以让注意力集中在关系上。
    color="#59a14f",
    # alpha 控制透明度，点重叠时更容易看出密集区域。
    alpha=0.75,
)

# 设置标题，说明这张图观察的是两个数值之间的关系。
ax.set_title("学生消费笔数与消费总额关系")
# 设置 x 轴标签，说明横轴是消费笔数。
ax.set_xlabel("消费笔数")
# 设置 y 轴标签，说明纵轴是消费总额，单位是元。
ax.set_ylabel("消费总额（元）")
# 添加网格线，方便读者估计点的位置。
ax.grid(linestyle="--", alpha=0.3)

# 自动调整布局，避免坐标轴文字被裁剪。
plt.tight_layout()
# 保存散点图。
fig.savefig(OUTPUT_DIR / "student_scatter.png", dpi=160)
# 关闭画布，避免影响后续图表。
plt.close(fig)`,
  },
  {
    no: "D",
    label: "金额分布",
    title: "参考 D：单笔交易金额分布直方图",
    question: "单笔消费金额主要集中在哪些区间？",
    data: "clean_canteen_transactions.csv",
    output: "amount_hist.png",
    why: "金额是连续数值，直方图适合观察集中区间和长尾。",
    code: String.raw`# 读取清洗后的消费明细表；直方图需要使用每一笔交易的金额，而不是汇总表。
clean_df = pd.read_csv(DATA_DIR / "clean_canteen_transactions.csv")
# 计算交易金额的 99% 分位数，用来去除最高 1% 的极端值，让主体分布更清楚。
amount_limit = clean_df["交易金额"].quantile(0.99)

# 创建画布和坐标轴；直方图用于观察金额主要集中在哪些区间。
fig, ax = plt.subplots(figsize=(8, 5))
# 画直方图；每个柱子代表一个金额区间内的交易笔数。
ax.hist(
    # 只保留不超过 99% 分位数的金额，减少极端值拉长横轴。
    clean_df.loc[clean_df["交易金额"] <= amount_limit, "交易金额"],
    # bins 控制分成多少个区间；区间太少会粗糙，太多会零碎。
    bins=30,
    # 设置柱子填充色。
    color="#76b7b2",
    # 设置柱子边框为白色，让区间边界更清楚。
    edgecolor="white",
)

# 设置标题，说明这张图看的是单笔金额分布。
ax.set_title("单笔交易金额分布（去除最高 1% 后）")
# 设置 x 轴标签，说明横轴是交易金额。
ax.set_xlabel("交易金额（元）")
# 设置 y 轴标签，说明纵轴是对应金额区间的交易笔数。
ax.set_ylabel("交易笔数")
# 添加横向网格线，方便比较不同区间的交易笔数。
ax.grid(axis="y", linestyle="--", alpha=0.35)

# 自动调整布局，避免标题或坐标轴标签被裁剪。
plt.tight_layout()
# 保存金额分布直方图。
fig.savefig(OUTPUT_DIR / "amount_hist.png", dpi=160)
# 关闭画布，避免影响后续图表。
plt.close(fig)`,
  },
  {
    no: "E",
    label: "终端排行",
    title: "参考 E：POS 终端交易笔数 Top 10 横向柱状图",
    question: "哪些食堂终端使用最频繁？",
    data: "clean_canteen_transactions.csv",
    output: "terminal_top10.png",
    why: "终端名称较长，横向柱状图比竖向柱状图更容易读。",
    code: String.raw`# 读取清洗后的消费明细表；终端排行需要按终端名称重新分组。
clean_df = pd.read_csv(DATA_DIR / "clean_canteen_transactions.csv")
# 按终端名称分组，计算每个终端的交易笔数，并取交易最多的前 10 个。
terminal_top10 = (
    # groupby 按“终端名称”把记录分组，每组代表一个 POS 终端。
    clean_df.groupby("终端名称")
    # agg 生成统计指标；这里用交易金额 count 来统计交易笔数。
    .agg(交易笔数=("交易金额", "count"))
    # 先按交易笔数从高到低排序，方便取 Top 10。
    .sort_values("交易笔数", ascending=False)
    # 只保留前 10 个终端，避免图上类别太多读不清。
    .head(10)
    # 再按交易笔数从低到高排序，这样横向柱状图会从短到长排列。
    .sort_values("交易笔数")
)

# 创建画布和坐标轴；终端名称较长，所以画布高度稍大。
fig, ax = plt.subplots(figsize=(8, 5.2))
# 画横向柱状图；y 轴是终端名称，x 轴是交易笔数。
ax.barh(terminal_top10.index, terminal_top10["交易笔数"], color="#e15759")

# 设置标题，说明这张图展示 POS 终端交易笔数 Top 10。
ax.set_title("POS 终端交易笔数 Top 10")
# 设置 x 轴标签，说明横向长度代表交易笔数。
ax.set_xlabel("交易笔数")
# 设置 y 轴标签，说明纵轴是终端名称。
ax.set_ylabel("终端名称")
# 添加纵向网格线，方便比较横向柱子的长度。
ax.grid(axis="x", linestyle="--", alpha=0.35)

# 自动调整布局，避免较长的终端名称被裁剪。
plt.tight_layout()
# 保存终端排行横向柱状图。
fig.savefig(OUTPUT_DIR / "terminal_top10.png", dpi=160)
# 关闭画布，避免影响后续图表。
plt.close(fig)`,
  },
];

export const chapter09AssessmentCards = [
  { title: "基础达标", text: "能运行主讲代码，生成 hour_peak.png，并正确解释 x 轴、y 轴和峰值标注。" },
  { title: "核心达标", text: "能根据趋势、比较、构成、分布和关系选择合适图型。" },
  { title: "优秀表现", text: "能为至少三张图写出问题、字段和具体数值结论。" },
  { title: "提交材料", text: "提交代码、至少三张 PNG 图片、实验报告 6，并避免公开姓名学号。" },
];
