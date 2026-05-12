export const chapter08Docs = [
  {
    title: "NumPy 官方文档",
    text: "数组创建、索引、统计函数和广播规则都可以在这里查。",
    href: "https://numpy.org/doc/stable/",
  },
  {
    title: "pandas 官方文档",
    text: "DataFrame、Series、读写文件、分组和透视表是本章重点。",
    href: "https://pandas.pydata.org/docs/",
  },
  {
    title: "pandas 入门教程",
    text: "适合在课后继续查阅 DataFrame 的常见操作。",
    href: "https://pandas.pydata.org/docs/getting_started/intro_tutorials/",
  },
];

export const chapter08ConceptCards = [
  {
    title: "NumPy",
    text: "面向数值数组，适合批量计算、矩阵形状、统计函数和科学计算底层能力。",
  },
  {
    title: "pandas",
    text: "面向表格数据，适合读取 CSV、选择字段、清洗缺失值、分组统计和保存结果。",
  },
  {
    title: "Series",
    text: "pandas 中的一列数据，既有值，也有索引和名称。",
  },
  {
    title: "DataFrame",
    text: "pandas 中的二维表，最接近 Excel、CSV 和数据库查询结果。",
  },
];

export const chapter08NumpyMethods = [
  { method: "np.array()", use: "把列表转换为数组", example: "np.array([80, 90, 70])" },
  { method: "np.arange()", use: "生成等间隔整数序列", example: "np.arange(1, 10, 2)" },
  { method: "np.linspace()", use: "生成指定数量的等间隔数", example: "np.linspace(0, 1, 5)" },
  { method: "np.zeros() / np.ones()", use: "生成全 0 或全 1 数组", example: "np.zeros((2, 3))" },
  { method: "np.mean() / np.sum()", use: "计算均值或总和", example: "np.mean(scores)" },
  { method: "np.nanmean()", use: "忽略 NaN 计算均值", example: "np.nanmean(scores)" },
];

export const chapter08PandasMethods = [
  { method: "pd.read_csv()", use: "读取 CSV 文件", example: "pd.read_csv('scores.csv')" },
  { method: "head() / info()", use: "快速查看数据", example: "df.head()" },
  { method: "loc[] / iloc[]", use: "按标签或位置选择行列", example: "df.loc[df['python'] >= 85]" },
  { method: "isna() / fillna()", use: "检查和处理缺失值", example: "df['english'].fillna(0)" },
  { method: "groupby()", use: "按类别分组统计", example: "df.groupby('major').mean()" },
  { method: "pivot_table()", use: "生成交叉统计表", example: "pd.pivot_table(df, index='性质')" },
  { method: "merge() / concat()", use: "合并或拼接表格", example: "pd.merge(left, right)" },
  { method: "to_csv()", use: "保存分析结果", example: "df.to_csv('result.csv')" },
];

export const chapter08Resources = [
  {
    title: "成绩练习数据",
    text: "用于 NumPy 与 pandas 基础操作的小型 CSV。",
    href: "/courses/python/ch08/scores.csv",
    download: "scores.csv",
  },
  {
    title: "课表示例数据",
    text: "字段结构与第七章最终课表 CSV 保持一致。",
    href: "/courses/python/ch08/course_schedule_sample.csv",
    download: "course_schedule_sample.csv",
  },
];

export const chapter08MaterialSteps = [
  {
    no: "01",
    title: "下载成绩练习数据",
    text: "下载 scores.csv，用于前半章练习 NumPy 与 pandas 的基础操作。",
  },
  {
    no: "02",
    title: "下载课表示例数据",
    text: "下载 course_schedule_sample.csv，用于后半章完成课表清洗、统计和结论分析。",
  },
  {
    no: "03",
    title: "放到指定目录",
    text: "把两个 CSV 都放到 public/courses/python/ch08/ 目录下，和第 2 个代码段中的 DATA_DIR 保持一致。",
  },
  {
    no: "04",
    title: "再开始运行",
    text: "先运行环境检查和准备数据两段代码，确认能读到 scores.csv，再继续后面的分析。",
  },
];

export const chapter08Pitfalls = [
  {
    title: "路径找不到",
    problem: "报错里出现 FileNotFoundError，通常是当前 notebook 工作目录和代码里的相对路径不一致。",
    fix: "先运行 Path.cwd() 看当前位置，再确认 public/courses/python/ch08 目录是否能从当前位置访问。",
  },
  {
    title: "列名写错",
    problem: "报错里出现 KeyError，多半是字段名和 CSV 里的真实列名不一致，中文列名尤其要注意空格和换行。",
    fix: "先打印 df.columns.tolist()，必要时使用 df.columns.str.replace('\\n', '').str.strip() 清理列名。",
  },
  {
    title: "axis 混乱",
    problem: "均分结果数量不对，经常是 axis=0 和 axis=1 用反了。",
    fix: "axis=0 常用于按列汇总，axis=1 常用于按行计算；学生均分通常使用 axis=1。",
  },
  {
    title: "数字列变成文字",
    problem: "学分求和或平均值结果异常，可能是 CSV 读取后把数字当成了字符串。",
    fix: "用 pd.to_numeric(df['学分'], errors='coerce') 转成数值，再检查是否产生缺失值。",
  },
  {
    title: "中文 CSV 乱码",
    problem: "CSV 用 Excel 打开后中文显示异常，通常是编码不匹配。",
    fix: "保存中文 CSV 时使用 encoding='utf-8-sig'，这样更适合直接交给 Excel 查看。",
  },
  {
    title: "结论没有证据",
    problem: "报告只写“比较多”“比较集中”，但没有引用具体统计表和数值。",
    fix: "每条结论都至少写清楚统计表名称、排名对象和具体数值。",
  },
];

export const chapter08Units = [
  {
    no: "01",
    label: "环境检查",
    title: "1 环境检查：确认 NumPy 与 pandas 可以导入",
    lead: "第八章先不急着分析数据。第一步是确认库已经安装，并形成统一的导入别名。",
    code: String.raw`import numpy as np
import pandas as pd

print("NumPy version:", np.__version__)
print("pandas version:", pd.__version__)`,
    explain: "这段代码导入 NumPy 和 pandas，并打印版本号。后面统一使用 np 和 pd 作为别名。",
    why: "数据分析代码通常从导入库开始。统一别名能减少代码长度，也方便阅读官方文档和他人代码。",
    points: ["NumPy 常写作 np。", "pandas 常写作 pd。", "如果导入失败，先回到第一章复习 pip 或 conda 安装。"],
    terms: [
      { title: "import", text: "导入第三方库。" },
      { title: "alias", text: "别名，np 和 pd 都是行业惯例。" },
      { title: "__version__", text: "查看当前库版本。" },
    ],
  },
  {
    no: "02",
    label: "准备数据",
    title: "2 准备数据：先从一张小成绩表开始",
    lead: "正式分析课表前，先用一张 12 行成绩表练习基础操作。小数据更适合理解概念。",
    code: String.raw`from pathlib import Path

DATA_DIR = Path("public/courses/python/ch08")
scores_path = DATA_DIR / "scores.csv"

scores_df = pd.read_csv(scores_path)
print(scores_df.head())`,
    explain: "这段代码用 Path 定位示例数据目录，再用 pd.read_csv 读取成绩表。",
    why: "真实项目经常从文件开始。先把路径、读取和预览写清楚，后面的分析才有对象。",
    points: ["Path 负责拼接路径。", "pd.read_csv 读取 CSV。", "head 默认查看前 5 行。"],
    terms: [
      { title: "CSV", text: "用逗号分隔字段的文本表格。" },
      { title: "DataFrame", text: "pandas 的二维表。" },
      { title: "head", text: "查看表格前几行。" },
    ],
  },
  {
    no: "03",
    label: "NumPy 数组",
    title: "3 NumPy 数组：从 Python 列表进入批量计算",
    lead: "NumPy 的核心是数组。数组看起来像列表，但它更适合做整列、整块数据的批量计算。",
    code: String.raw`python_scores = np.array([92, 95, 80, 70, 98, 66])

print(python_scores)
print("维度:", python_scores.ndim)
print("形状:", python_scores.shape)
print("类型:", python_scores.dtype)`,
    explain: "np.array 把普通列表转换成数组，ndim、shape 和 dtype 分别查看维度、形状和元素类型。",
    why: "后面理解 DataFrame 数值列、矩阵和统计函数时，都绕不开数组形状。",
    points: ["一维数组像一列数据。", "shape 是理解数组结构的入口。", "dtype 决定数组能做什么类型的计算。"],
    terms: [
      { title: "ndim", text: "数组维度数量。" },
      { title: "shape", text: "数组每个维度的长度。" },
      { title: "dtype", text: "数组元素类型。" },
    ],
  },
  {
    no: "04",
    label: "数组创建",
    title: "4 数组创建：不用手写每一个数字",
    lead: "除了从列表创建数组，NumPy 还能快速生成等差序列、全 0、全 1 和随机数组。",
    code: String.raw`print(np.arange(1, 10, 2))
print(np.linspace(0, 1, 5))
print(np.zeros((2, 3)))
print(np.ones((2, 3)))

rng = np.random.default_rng(42)
print(rng.integers(60, 101, size=(3, 4)))`,
    explain: "arange、linspace、zeros、ones 和随机数生成器都用于快速创建数组。",
    why: "学习数据分析时，经常需要构造测试数据、模拟数据或初始化计算结果。",
    points: ["arange 更像 range。", "linspace 控制生成数量。", "default_rng 是推荐的随机数入口。"],
    terms: [
      { title: "size", text: "随机数组形状。" },
      { title: "zeros", text: "生成全 0 数组。" },
      { title: "ones", text: "生成全 1 数组。" },
    ],
  },
  {
    no: "05",
    label: "索引筛选",
    title: "5 索引、切片与布尔筛选",
    lead: "数组不只是能存数据，还能快速取出一部分数据。布尔筛选是数据分析中最常用的思想之一。",
    code: String.raw`scores = np.array([86, 91, 72, 65, 95, 58, 77, 88])

print("第 1 个成绩:", scores[0])
print("前 3 个成绩:", scores[:3])
print("及格成绩:", scores[scores >= 60])
print("优秀成绩:", scores[scores >= 85])`,
    explain: "索引用位置取单个值，切片取连续片段，布尔表达式筛选满足条件的数据。",
    why: "pandas 中的条件筛选本质上也会用到类似的布尔判断。",
    points: ["Python 索引从 0 开始。", "scores >= 60 会得到布尔数组。", "把布尔数组放回中括号就能筛选。"],
    terms: [
      { title: "索引", text: "按位置取值。" },
      { title: "切片", text: "按范围取值。" },
      { title: "布尔筛选", text: "按 True / False 选择数据。" },
    ],
  },
  {
    no: "06",
    label: "向量化",
    title: "6 向量化计算：整列数据一起算",
    lead: "NumPy 的优势不是少写几行代码，而是把对每个元素的重复计算变成整体计算。",
    code: String.raw`raw_scores = np.array([58, 69, 80, 92, 100])
bonus_scores = raw_scores + 5
bonus_scores = np.minimum(bonus_scores, 100)

print("原始成绩:", raw_scores)
print("加分后:", bonus_scores)
print("是否及格:", bonus_scores >= 60)`,
    explain: "数组可以直接和数字相加，np.minimum 用于限制最高值不超过 100。",
    why: "向量化能让代码更接近数学表达，也更适合大规模数据。",
    points: ["数组和数字运算会作用到每个元素。", "np.minimum 可以逐元素取较小值。", "避免一开始就写复杂 for 循环。"],
    terms: [
      { title: "向量化", text: "整组数据一次性计算。" },
      { title: "逐元素", text: "数组中每个元素分别参与计算。" },
      { title: "广播", text: "不同形状数据自动扩展后计算的机制。" },
    ],
  },
  {
    no: "07",
    label: "统计与 axis",
    title: "7 统计函数与 axis：按列算还是按行算",
    lead: "二维数组里，axis 是最容易混淆的概念。本节用成绩矩阵理解按列和按行统计。",
    code: String.raw`score_matrix = np.array([
    [86, 78, 92],
    [91, 85, 95],
    [72, 69, 80],
])

print("每门课均分:", score_matrix.mean(axis=0))
print("每个学生均分:", score_matrix.mean(axis=1))
print("最高分位置:", np.argmax(score_matrix))`,
    explain: "axis=0 表示沿着行方向汇总，得到每一列的结果；axis=1 表示沿着列方向汇总，得到每一行的结果。",
    why: "pandas 的按行、按列计算也会遇到 axis，先在 NumPy 中理解更直观。",
    points: ["axis=0 常理解为按列统计。", "axis=1 常理解为按行统计。", "argmax 返回最大值的位置编号。"],
    terms: [
      { title: "axis", text: "统计时压缩哪一个方向。" },
      { title: "mean", text: "平均值。" },
      { title: "argmax", text: "最大值所在位置。" },
    ],
  },
  {
    no: "08",
    label: "缺失值",
    title: "8 NaN：数据缺失不能简单当作 0",
    lead: "真实数据经常缺字段。NumPy 用 NaN 表示缺失数值，统计时要选择合适的方法。",
    code: String.raw`scores = np.array([86, 91, np.nan, 72, 65])

print("普通均值:", np.mean(scores))
print("忽略缺失后的均值:", np.nanmean(scores))
print("缺失位置:", np.isnan(scores))`,
    explain: "np.nan 表示缺失值。普通 mean 遇到 NaN 会得到 NaN，nanmean 会忽略缺失值。",
    why: "把缺失值当作 0 会拉低统计结果。正确识别缺失，是数据清洗的第一步。",
    points: ["NaN 不是 0。", "np.isnan 可以判断缺失位置。", "nanmean 适合忽略缺失后计算均值。"],
    terms: [
      { title: "NaN", text: "Not a Number，常用于表示缺失数值。" },
      { title: "np.isnan", text: "判断哪些位置是 NaN。" },
      { title: "np.nanmean", text: "忽略 NaN 计算均值。" },
    ],
  },
  {
    no: "09",
    label: "Series 与 DataFrame",
    title: "9 pandas 的两种核心对象：Series 与 DataFrame",
    lead: "pandas 面向表格。Series 是一列，DataFrame 是一张表。",
    code: String.raw`python_series = scores_df["python"]
print(type(python_series))

mini_df = scores_df[["name", "major", "python"]]
print(type(mini_df))
print(mini_df.head())`,
    explain: "从 DataFrame 中取一列会得到 Series，取多列仍然是 DataFrame。",
    why: "很多 pandas 报错都来自混淆 Series 和 DataFrame。先分清对象类型，后面操作更稳。",
    points: ["单列通常是 Series。", "双中括号取多列。", "DataFrame 最接近一张二维表。"],
    terms: [
      { title: "Series", text: "带索引的一维数据。" },
      { title: "DataFrame", text: "带行索引和列名的二维表。" },
      { title: "列名", text: "DataFrame 中定位字段的名称。" },
    ],
  },
  {
    no: "10",
    label: "查看数据",
    title: "10 读取后先查看：不要直接开始算",
    lead: "数据分析的第一步不是写复杂代码，而是先看表格长什么样。",
    code: String.raw`print(scores_df.shape)
print(scores_df.columns)
print(scores_df.info())
print(scores_df.describe())`,
    explain: "shape 看行列数，columns 看字段名，info 看类型和缺失，describe 看数值列摘要。",
    why: "先查看数据结构，可以避免字段名写错、类型不对、缺失值没发现等问题。",
    points: ["shape 是整体规模。", "info 重点看非空数量和数据类型。", "describe 只对数值列做统计摘要。"],
    terms: [
      { title: "shape", text: "行数和列数。" },
      { title: "columns", text: "所有列名。" },
      { title: "describe", text: "数值列的统计摘要。" },
    ],
  },
  {
    no: "11",
    label: "行列选择",
    title: "11 选择列、选择行与条件筛选",
    lead: "pandas 最常见的操作就是取字段、取行和按条件筛选。",
    code: String.raw`print(scores_df["python"].head())
print(scores_df[["name", "major", "python"]].head())

excellent = scores_df.loc[scores_df["python"] >= 85, ["name", "python"]]
print(excellent)

print(scores_df.iloc[0:3, 0:4])`,
    explain: "中括号按列名取字段，loc 按标签和条件筛选，iloc 按位置筛选。",
    why: "后面分析课表时，要频繁筛选某个院系、某个校区、某类课程。",
    points: ["loc 更适合按条件筛选。", "iloc 更适合按位置截取。", "多列选择要用列表。"],
    terms: [
      { title: "loc", text: "按标签和条件选择数据。" },
      { title: "iloc", text: "按整数位置选择数据。" },
      { title: "条件筛选", text: "筛选满足条件的行。" },
    ],
  },
  {
    no: "12",
    label: "排序新增列",
    title: "12 排序与新增列：让原始数据更有解释力",
    lead: "分析不是只看原字段。经常要根据已有字段生成新字段，再排序观察。",
    code: String.raw`scores_df["score_mean"] = scores_df[["math", "english", "python"]].mean(axis=1)
scores_df["python_level"] = np.where(scores_df["python"] >= 85, "优秀", "继续练习")

ranked = scores_df.sort_values("score_mean", ascending=False)
print(ranked[["name", "score_mean", "python_level"]].head())`,
    explain: "mean(axis=1) 计算每个学生三门课均分，np.where 根据条件生成等级字段。",
    why: "新增列能把计算逻辑保存下来，排序能快速找到重点对象。",
    points: ["axis=1 表示按行计算。", "sort_values 用于排序。", "np.where 适合简单二分类。"],
    terms: [
      { title: "新增列", text: "把计算结果作为新字段放回表格。" },
      { title: "sort_values", text: "按某列排序。" },
      { title: "np.where", text: "按条件批量生成结果。" },
    ],
  },
  {
    no: "13",
    label: "清洗数据",
    title: "13 缺失值、重复值与异常值",
    lead: "真实数据不会天然干净。pandas 提供了一组专门处理脏数据的方法。",
    code: String.raw`print(scores_df.isna().sum())

scores_df["english"] = scores_df["english"].fillna(scores_df["english"].mean())

print("重复行数量:", scores_df.duplicated().sum())
scores_df = scores_df.drop_duplicates()

print(scores_df[["name", "english"]])`,
    explain: "isna 检查缺失，fillna 填充缺失，duplicated 和 drop_duplicates 处理重复。",
    why: "缺失和重复会直接影响均值、计数和排行榜，必须在分析前处理。",
    points: ["先检查，再决定怎么处理。", "均值填充适合数值列的简单练习。", "去重前要确认重复的定义。"],
    terms: [
      { title: "isna", text: "判断缺失值。" },
      { title: "fillna", text: "填充缺失值。" },
      { title: "drop_duplicates", text: "删除重复行。" },
    ],
  },
  {
    no: "14",
    label: "字符串处理",
    title: "14 字符串处理：清理字段中的文字",
    lead: "课表数据里很多字段是文字，例如课程名称、时间地点、校区。字符串方法很重要。",
    code: String.raw`course_path = DATA_DIR / "course_schedule_sample.csv"
course_df = pd.read_csv(course_path)

course_df.columns = course_df.columns.str.strip()
course_df["课程名称"] = course_df["课程名称"].str.strip()
python_courses = course_df[course_df["课程名称"].str.contains("数据|Python", na=False)]

print(python_courses[["课程名称", "教师", "时间地点"]])`,
    explain: "str.strip 清理前后空格，str.contains 按关键词筛选文本字段。",
    why: "网页和 CSV 中的文字经常带空格、换行或混合信息。字符串处理能让字段更规范。",
    points: ["字符串列使用 .str 访问字符串方法。", "contains 支持关键词筛选。", "na=False 避免缺失值导致筛选报错。"],
    terms: [
      { title: ".str", text: "pandas 字符串方法入口。" },
      { title: "contains", text: "判断是否包含关键词。" },
      { title: "strip", text: "去掉前后空白字符。" },
    ],
  },
  {
    no: "15",
    label: "分组统计",
    title: "15 groupby：按类别统计",
    lead: "groupby 是 pandas 数据分析的核心。它能回答“每个类别分别怎么样”。",
    code: String.raw`department_summary = (
    course_df.groupby("开课院系")
    .agg(
        课程数=("课程名称", "count"),
        总学分=("学分", "sum"),
        平均学分=("学分", "mean"),
    )
    .round(2)
    .sort_values("课程数", ascending=False)
)

print(department_summary)`,
    explain: "按开课院系分组，再统计课程数、总学分和平均学分。",
    why: "分组统计能把明细数据变成可解释的汇总结果，是实验报告最常用的分析方法。",
    points: ["groupby 后通常接 agg。", "count 统计数量。", "sum 和 mean 用于数值列。"],
    terms: [
      { title: "groupby", text: "按类别分组。" },
      { title: "agg", text: "一次计算多个统计指标。" },
      { title: "sort_values", text: "让结果按重点指标排序。" },
    ],
  },
  {
    no: "16",
    label: "透视表",
    title: "16 pivot_table：做二维交叉统计",
    lead: "当问题变成“某类课程在不同校区分别有多少”时，透视表比普通分组更直观。",
    code: String.raw`nature_by_campus = pd.pivot_table(
    course_df,
    index="性质",
    columns="校区",
    values="课程名称",
    aggfunc="count",
    fill_value=0,
)

print(nature_by_campus)`,
    explain: "index 指定行分类，columns 指定列分类，values 指定被统计字段，aggfunc 指定统计方式。",
    why: "透视表适合观察两个分类变量之间的关系，和 Excel 数据透视表思路一致。",
    points: ["index 是行。", "columns 是列。", "fill_value=0 可以把空组合填成 0。"],
    terms: [
      { title: "pivot_table", text: "数据透视表。" },
      { title: "aggfunc", text: "聚合函数。" },
      { title: "交叉统计", text: "两个类别维度共同统计。" },
    ],
  },
  {
    no: "17",
    label: "合并拼接",
    title: "17 concat 与 merge：把多张表连接起来",
    lead: "真实分析常常不止一张表。concat 适合上下拼接，merge 适合按共同字段横向合并。",
    code: String.raw`department_info = pd.DataFrame({
    "开课院系": ["计算机学院", "人工智能学院", "数据科学学院"],
    "院系类别": ["工科", "工科", "工科"],
})

course_with_info = pd.merge(course_df, department_info, on="开课院系", how="left")
print(course_with_info[["课程名称", "开课院系", "院系类别"]].head())

double_rows = pd.concat([course_df.head(2), course_df.tail(2)])
print(double_rows[["课程名称", "教师"]])`,
    explain: "merge 按开课院系补充院系类别，concat 把两段表格上下拼接。",
    why: "合并数据能把孤立字段连成更完整的分析对象。",
    points: ["merge 需要共同字段。", "how='left' 保留左表所有行。", "concat 默认上下拼接。"],
    terms: [
      { title: "merge", text: "按键合并表格。" },
      { title: "concat", text: "拼接表格。" },
      { title: "left join", text: "保留左表全部记录的合并方式。" },
    ],
  },
  {
    no: "18",
    label: "保存结果",
    title: "18 保存结果：分析必须能复查",
    lead: "只在屏幕上 print 不够。分析结果要保存为文件，便于提交、复查和继续处理。",
    code: String.raw`OUTPUT_DIR = DATA_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

department_summary.to_csv(
    OUTPUT_DIR / "department_summary.csv",
    encoding="utf-8-sig",
)
nature_by_campus.to_csv(
    OUTPUT_DIR / "nature_by_campus.csv",
    encoding="utf-8-sig",
)

print("已保存到:", OUTPUT_DIR)`,
    explain: "创建 output 目录，并把两个统计结果保存成 CSV。",
    why: "实验报告需要结果文件。utf-8-sig 能让 Excel 更稳定地打开中文 CSV。",
    points: ["mkdir 创建输出目录。", "to_csv 保存表格。", "encoding='utf-8-sig' 适合中文 CSV。"],
    terms: [
      { title: "to_csv", text: "保存为 CSV 文件。" },
      { title: "encoding", text: "文件编码。" },
      { title: "output", text: "建议统一放分析结果。" },
    ],
  },
  {
    no: "19",
    label: "NumPy 配合 pandas",
    title: "19 NumPy 与 pandas 配合：标准分示例",
    lead: "pandas 负责字段和表格，NumPy 负责数值计算。两者经常一起使用。",
    code: String.raw`python_array = scores_df["python"].to_numpy()
python_zscore = (python_array - np.nanmean(python_array)) / np.nanstd(python_array)

scores_df["python_zscore"] = python_zscore.round(2)
print(scores_df[["name", "python", "python_zscore"]].head())`,
    explain: "把 pandas 列转成 NumPy 数组，计算标准分，再放回 DataFrame。",
    why: "复杂数值计算用 NumPy 更自然，结果放回 pandas 后更方便继续按字段分析。",
    points: ["to_numpy 把列转为数组。", "标准分描述距离均值几个标准差。", "计算结果可以作为新列保存。"],
    terms: [
      { title: "to_numpy", text: "从 pandas 转到 NumPy。" },
      { title: "z-score", text: "标准分。" },
      { title: "nanstd", text: "忽略 NaN 的标准差。" },
    ],
  },
  {
    no: "20",
    label: "读取课表",
    title: "20 综合实战：读取课表数据",
    lead: "从这里开始进入第七章的延续任务：分析课表 CSV。",
    code: String.raw`course_path = DATA_DIR / "course_schedule_sample.csv"
courses = pd.read_csv(course_path)

print(courses.shape)
print(courses.columns.tolist())
print(courses.head(3))`,
    explain: "读取课表示例数据，查看行列规模、字段名和前三行。",
    why: "正式分析前必须先确认字段是否符合预期。第七章最终 CSV 也可以替换成同样字段的数据。",
    points: ["先看 shape。", "再看 columns。", "最后抽样看内容。"],
    terms: [
      { title: "课表明细", text: "每一行代表一个教学班或选课记录。" },
      { title: "字段", text: "课程名称、教师、院系、学分等列。" },
      { title: "抽样查看", text: "先看几行，避免盲目处理。" },
    ],
  },
  {
    no: "21",
    label: "清洗课表",
    title: "21 综合实战：清洗课表数据",
    lead: "课表字段来自网页，可能有换行、空格、重复记录和学分类型问题。",
    code: String.raw`courses.columns = courses.columns.str.replace("\n", "").str.strip()
courses = courses.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
courses["学分"] = pd.to_numeric(courses["学分"], errors="coerce")

courses = courses.drop_duplicates(subset=["选课编号", "课程代码", "教学班号"])
courses["是否高学分"] = np.where(courses["学分"] >= 3, "高学分", "普通学分")
courses["是否专业课"] = np.where(courses["性质"].str.contains("专业", na=False), "专业课", "公共课")

print(courses[["课程名称", "学分", "是否高学分", "是否专业课"]].head())`,
    explain: "清理列名和文本空格，把学分转成数值，按关键字段去重，并新增两个分析字段。",
    why: "清洗后的数据才适合统计。新增字段能把后续分析问题表达得更清楚。",
    points: ["字段名要统一。", "学分必须是数值才能求和求均值。", "drop_duplicates 要指定判断重复的字段。"],
    terms: [
      { title: "to_numeric", text: "把文本转成数值。" },
      { title: "subset", text: "指定去重依据字段。" },
      { title: "派生字段", text: "根据已有字段计算的新字段。" },
    ],
  },
  {
    no: "22",
    label: "课表统计",
    title: "22 综合实战：统计院系、教师、校区和学分",
    lead: "清洗完成后，开始把明细数据转成统计表。",
    code: String.raw`department_count = (
    courses.groupby("开课院系")
    .agg(课程数=("课程名称", "count"), 总学分=("学分", "sum"))
    .sort_values("课程数", ascending=False)
)

teacher_count = (
    courses.groupby("教师")
    .agg(授课门数=("课程名称", "count"), 学分合计=("学分", "sum"))
    .sort_values(["授课门数", "学分合计"], ascending=False)
)

campus_count = courses["校区"].value_counts()
credit_count = courses["学分"].value_counts().sort_index()

print(department_count)
print(teacher_count.head(10))
print(campus_count)
print(credit_count)`,
    explain: "分别统计院系课程数、教师授课量、校区分布和学分分布。",
    why: "这些统计表能直接支撑实验报告中的数据分析结论。",
    points: ["不同问题对应不同分组字段。", "value_counts 适合单列计数。", "排行榜要排序后再解释。"],
    terms: [
      { title: "课程数", text: "明细记录数量。" },
      { title: "授课门数", text: "教师对应的课程记录数。" },
      { title: "学分分布", text: "不同学分课程各有多少。" },
    ],
  },
  {
    no: "23",
    label: "解释结论",
    title: "23 写出分析结论：把统计表翻译成人话",
    lead: "数据分析的最后一步不是表格，而是基于数据写出可核对的结论。",
    code: String.raw`top_department = department_count.index[0]
top_teacher = teacher_count.index[0]
top_campus = campus_count.index[0]

print(f"开课数量最多的院系是：{top_department}")
print(f"授课门数最多的教师是：{top_teacher}")
print(f"课程数量最多的校区是：{top_campus}")
print("写报告时，要同时引用表格名称和具体数值。")`,
    explain: "从统计结果中取出排名第一的类别，并生成简短文字结论。",
    why: "实验报告不能只贴代码和表格。结论要说明从哪个统计结果得出，最好带具体数值。",
    points: ["结论必须能回到数据表核对。", "不要只写主观感受。", "排名、数量、比例都可以成为结论依据。"],
    terms: [
      { title: "分析结论", text: "从统计结果中得到的文字解释。" },
      { title: "可核对", text: "读者能回到数据文件验证。" },
      { title: "具体数值", text: "比笼统形容更可靠。" },
    ],
  },
  {
    no: "24",
    label: "完整流程",
    title: "24 完整流程：读取、清洗、分析、保存",
    lead: "最后把本章主线串起来，形成一份可以独立运行的分析脚本。",
    code: String.raw`def run_course_analysis():
    courses = pd.read_csv(DATA_DIR / "course_schedule_sample.csv")
    courses.columns = courses.columns.str.replace("\n", "").str.strip()
    courses = courses.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
    courses["学分"] = pd.to_numeric(courses["学分"], errors="coerce")
    courses = courses.drop_duplicates(subset=["选课编号", "课程代码", "教学班号"])

    department_count = courses.groupby("开课院系").agg(
        课程数=("课程名称", "count"),
        总学分=("学分", "sum"),
        平均学分=("学分", "mean"),
    ).round(2)
    teacher_count = courses.groupby("教师").agg(
        授课门数=("课程名称", "count"),
        学分合计=("学分", "sum"),
    )

    output_dir = DATA_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    courses.to_csv(output_dir / "course_schedule_clean.csv", index=False, encoding="utf-8-sig")
    department_count.to_csv(output_dir / "department_count.csv", encoding="utf-8-sig")
    teacher_count.to_csv(output_dir / "teacher_count.csv", encoding="utf-8-sig")
    print("分析完成，结果已保存。")


run_course_analysis()`,
    explain: "这段代码把读取、清洗、分组统计和保存结果串成一个函数，并在函数内部创建输出目录。",
    why: "完整流程能让分析过程可复现。课堂练习时逐段理解，最后再把步骤整理成函数。",
    points: ["函数封装让主流程更清楚。", "函数内部创建输出目录，减少对前面代码段的依赖。", "不要直接跳到最后一段，前面的代码用于理解每一步的意义。"],
    terms: [
      { title: "可复现", text: "再次运行能得到同样的处理流程和结果。" },
      { title: "清洗后数据", text: "已经规范字段和类型的数据。" },
      { title: "统计结果", text: "用于报告分析的汇总表。" },
    ],
  },
];

export const chapter08AssessmentCards = [
  { title: "基础达标", text: "能读取 CSV，查看数据结构，完成筛选、排序和保存。" },
  { title: "核心达标", text: "能用 groupby 和 pivot_table 生成统计表。" },
  { title: "优秀表现", text: "能发现缺失、重复或异常，并用具体数据写出结论。" },
  { title: "提交材料", text: "代码、清洗后 CSV、统计结果 CSV 和分析说明。" },
];
