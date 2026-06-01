export const chapter08Docs = [
  {
    title: "pandas 官方文档",
    text: "本章只用到读写 CSV、字段处理、分组统计和保存结果，遇到参数问题优先查这里。",
    href: "https://pandas.pydata.org/docs/",
  },
  {
    title: "pandas 入门教程",
    text: "适合课后继续练习 DataFrame、Series、筛选和分组统计。",
    href: "https://pandas.pydata.org/docs/getting_started/intro_tutorials/",
  },
  {
    title: "NumPy 官方文档",
    text: "本章只用少量 NumPy 做向量化分类，不把 NumPy 当作单独方法清单展开。",
    href: "https://numpy.org/doc/stable/",
  },
];

export const chapter08ConceptCards = [
  {
    title: "一行交易",
    text: "食堂消费流水中，每一行代表一次刷卡、支付码消费或账户相关操作。",
  },
  {
    title: "一个字段",
    text: "学工号、记账日期、交易时间、终端名称、交易金额等列共同描述一笔交易。",
  },
  {
    title: "先清洗再统计",
    text: "日期、时间、金额、非消费交易和异常余额都要先检查，否则统计结果会被污染。",
  },
  {
    title: "结论要可复查",
    text: "报告里的判断必须能回到清洗后 CSV 或统计表核对，不能只写主观感受。",
  },
];

export const chapter08Resources = [
  {
    title: "食堂消费数据",
    text: "本章唯一核心数据源，包含 17313 条学生食堂消费与账户流水记录。",
    href: "/courses/python/ch08/食堂消费数据.csv",
    download: "食堂消费数据.csv",
  },
];

export const chapter08MaterialSteps = [
  {
    no: "01",
    title: "下载数据",
    text: "下载食堂消费数据.csv，保持文件名不变。",
  },
  {
    no: "02",
    title: "放到目录",
    text: "把 CSV 放到 public/courses/python/ch08/ 目录，和代码中的 DATA_DIR 保持一致。",
  },
  {
    no: "03",
    title: "按 gb18030 读取",
    text: "这份 CSV 不是 UTF-8 编码，读取时要写 encoding='gb18030'，否则中文会乱码。",
  },
  {
    no: "04",
    title: "输出报告材料",
    text: "最后生成清洗后数据和多张统计表，用它们填写实验报告 5。",
  },
];

export const chapter08Pitfalls = [
  {
    title: "中文乱码",
    problem: "表头显示成问号或乱码，多半是按 UTF-8 读取了 GB 编码 CSV。",
    fix: "读取时使用 pd.read_csv(path, encoding='gb18030')，保存结果时使用 encoding='utf-8-sig'。",
  },
  {
    title: "时间少了前导 0",
    problem: "交易时间 95718 实际表示 09:57:18，直接按整数处理会丢掉前面的 0。",
    fix: "先转字符串并用 str.zfill(6) 补齐，再切出小时、分钟和秒。",
  },
  {
    title: "把非消费交易算进消费额",
    problem: "卡挂失、卡补办、换卡成本费和现金充值不是普通食堂消费。",
    fix: "统计消费行为时先筛选交易名称包含“消费”且交易金额大于 0 的记录。",
  },
  {
    title: "余额差异没检查",
    problem: "交易前余额减交易金额不等于交易后余额，可能是记录需要复核。",
    fix: "计算余额差额，绝对值大于 0.01 的记录单独列出，不直接删除。",
  },
  {
    title: "公开个人排名",
    problem: "学生消费数据涉及个人信息，直接展示姓名和学号排名不合适。",
    fix: "学生层面只做汇总和脱敏展示，用 Student001 这类编号替代姓名学号。",
  },
  {
    title: "报告没有证据",
    problem: "只写“中午很多”“支付码更多”，没有引用表格和数值。",
    fix: "每条结论至少说明来自哪张统计表，并写出具体人数、笔数、金额或占比。",
  },
];

export const chapter08Units = [
  {
    no: "01",
    label: "任务导入",
    title: "1 情境引入：食堂消费流水能回答什么问题",
    lead: "这一章不从方法清单开始，而是从一份真实 CSV 开始：怎样把原始消费流水整理成可复查的分析报告。",
    code: String.raw`analysis_questions = [
    "原始流水一共有多少条记录、多少名学生？",
    "学生主要在哪些时间段消费？",
    "支付码消费和 IC 卡消费分别占多少？",
    "哪些食堂楼层或 POS 终端更常用？",
    "哪些 0 元、非消费或余额不一致记录需要解释？",
]

for no, question in enumerate(analysis_questions, start=1):
    print(no, question)`,
    explain: "先把分析问题写清楚，再决定要读哪些字段、清洗哪些问题、生成哪些统计表。",
    why: "数据分析不是把所有 pandas 方法都试一遍，而是围绕问题选择必要操作。",
    points: ["一行是一笔交易。", "一列是一个字段。", "本章最终要交付清洗后数据、统计表和文字结论。"],
    terms: [
      { title: "交易流水", text: "按时间记录的一笔笔消费或账户操作。" },
      { title: "字段", text: "描述交易的列，例如交易金额、终端名称、交易时间。" },
      { title: "可复查", text: "别人能用同一份数据重新得到你的结果。" },
    ],
  },
  {
    no: "02",
    label: "读取数据",
    title: "2 读取数据：用正确编码打开中文 CSV",
    lead: "本章只有一个核心数据源：食堂消费数据.csv。读取时必须指定 gb18030 编码。",
    code: String.raw`from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path("public/courses/python/ch08")
data_path = DATA_DIR / "食堂消费数据.csv"

raw_df = pd.read_csv(data_path, encoding="gb18030")

print(raw_df.shape)
print(raw_df.columns.tolist())
print(raw_df.head())`,
    explain: "Path 负责定位文件，pd.read_csv 读取 CSV，encoding='gb18030' 用来正确识别中文内容。",
    why: "如果第一步读取就乱码，后面的字段选择、统计和报告都会出错。",
    points: ["不要改文件名。", "先看 shape 和 columns。", "确认中文字段能正常显示后再继续。"],
    terms: [
      { title: "encoding", text: "文件字符编码，决定中文能否正确读出。" },
      { title: "DataFrame", text: "pandas 中最常用的二维表结构。" },
      { title: "head", text: "查看前几行，确认数据读入是否正常。" },
    ],
  },
  {
    no: "03",
    label: "认识字段",
    title: "3 认识字段：先看规模、类型和金额分布",
    lead: "正式清洗前，先回答这份表有多大、有哪些字段、金额列是否像数字。",
    code: String.raw`print("记录数和字段数:", raw_df.shape)
print("学生人数:", raw_df["学工号"].nunique())
print("日期范围:", raw_df["记账日期"].min(), raw_df["记账日期"].max())

print(raw_df.info())
print(raw_df["交易金额"].describe())`,
    explain: "shape 看整体规模，nunique 看学生数量，info 看字段类型，describe 看金额列的统计摘要。",
    why: "先认识数据结构，可以避免一上来就 groupby，最后却不知道统计对象是否可靠。",
    points: ["本数据有 17313 条记录。", "学工号可用于学生去重。", "交易金额是后续统计的核心数值列。"],
    terms: [
      { title: "nunique", text: "统计不同值的数量。" },
      { title: "info", text: "查看字段类型和非空数量。" },
      { title: "describe", text: "查看数值列的均值、分位数、最大最小值。" },
    ],
  },
  {
    no: "04",
    label: "质量检查",
    title: "4 数据质量检查：缺失、重复、状态和非消费交易",
    lead: "清洗不是直接删除数据，而是先列出问题：哪些字段缺失、哪些记录重复、哪些交易不属于普通消费。",
    code: String.raw`print("缺失值数量:")
print(raw_df.isna().sum())

print("完全重复行数量:", raw_df.duplicated().sum())

print("交易状态:")
print(raw_df["状态"].value_counts())

print("交易名称:")
print(raw_df["交易名称"].value_counts())`,
    explain: "isna 检查缺失，duplicated 检查完全重复，value_counts 查看类别字段的分布。",
    why: "这一步决定后面哪些记录保留、哪些记录标注、哪些记录不进入普通消费统计。",
    points: ["先检查再处理。", "非消费交易要单独解释。", "状态字段可以帮助判断交易是否成功。"],
    terms: [
      { title: "isna", text: "判断缺失值。" },
      { title: "duplicated", text: "判断重复行。" },
      { title: "value_counts", text: "统计每个类别出现多少次。" },
    ],
  },
  {
    no: "05",
    label: "字段转换",
    title: "5 字段转换：把日期、时间和金额变成可分析格式",
    lead: "原始日期和时间是整数形式。分析消费高峰前，要先把它们转换成日期、时间和小时。",
    code: String.raw`df = raw_df.copy()
df.columns = df.columns.str.strip()

money_cols = ["可用余额（交易前）", "交易金额", "可用余额（交易后）"]
for col in money_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["交易日期"] = pd.to_datetime(df["记账日期"].astype(str), format="%Y%m%d", errors="coerce")
df["交易时间文本"] = df["交易时间"].astype(str).str.zfill(6)
df["交易小时"] = df["交易时间文本"].str[:2].astype(int)
df["交易时刻"] = pd.to_datetime(
    df["记账日期"].astype(str) + df["交易时间文本"],
    format="%Y%m%d%H%M%S",
    errors="coerce",
)

print(df[["记账日期", "交易时间", "交易日期", "交易小时", "交易时刻"]].head())`,
    explain: "to_numeric 统一金额类型，to_datetime 转换日期时间，zfill(6) 保留 09:57:18 这类前导 0。",
    why: "只有字段类型正确，后面才能按日期、小时、金额做可靠统计。",
    points: ["交易时间必须补齐 6 位。", "日期转换失败会得到 NaT。", "金额转换失败会得到 NaN。"],
    terms: [
      { title: "to_numeric", text: "把字段转成数值。" },
      { title: "to_datetime", text: "把文本或数字转成日期时间。" },
      { title: "zfill", text: "在字符串左侧补 0 到指定长度。" },
    ],
  },
  {
    no: "06",
    label: "筛选清洗",
    title: "6 清洗原始流水：筛选消费交易并保留复核线索",
    lead: "普通消费分析只统计真实消费记录，但异常线索不能悄悄删掉，要先标注出来。",
    code: String.raw`df["余额差额"] = (
    df["可用余额（交易前）"] - df["交易金额"] - df["可用余额（交易后）"]
).round(2)
df["余额是否异常"] = df["余额差额"].abs() > 0.01

review_rows = df[
    (df["交易金额"] <= 0)
    | (~df["交易名称"].str.contains("消费", na=False))
    | (df["余额是否异常"])
]

consume_df = df[
    df["交易名称"].str.contains("消费", na=False)
    & (df["交易金额"] > 0)
    & df["交易日期"].notna()
].copy()

print("需要复核的记录数:", len(review_rows))
print("进入消费分析的记录数:", len(consume_df))
print(review_rows[["学工号", "交易名称", "交易金额", "余额差额"]].head())`,
    explain: "先计算余额差额，再把 0 元、非消费和余额异常记录列为复核对象；普通消费分析只使用消费且金额大于 0 的记录。",
    why: "清洗的重点不是让问题消失，而是让分析口径清楚、异常记录有解释。",
    points: ["非消费交易不进入普通消费额。", "余额异常要保留复核表。", "筛选结果要报告行数。"],
    terms: [
      { title: "分析口径", text: "本次统计到底包含哪些记录。" },
      { title: "复核记录", text: "不直接用于常规统计，但需要在报告中说明的记录。" },
      { title: "copy", text: "复制筛选后的数据，避免后续赋值警告。" },
    ],
  },
  {
    no: "07",
    label: "分析字段",
    title: "7 生成分析字段：餐段、楼层、支付方式和金额等级",
    lead: "原始字段不一定直接回答问题。要把时间、终端和金额转换成更适合分析的字段。",
    code: String.raw`consume_df["餐段"] = pd.cut(
    consume_df["交易小时"],
    bins=[0, 10, 14, 17, 20, 24],
    labels=["早间", "午餐", "下午", "晚餐", "夜间"],
    right=False,
)

floor_match = consume_df["终端名称"].str.extract(r"食堂(\d)层|食堂(\d)F")
floor_no = floor_match.bfill(axis=1).iloc[:, 0]
consume_df["食堂楼层"] = np.where(floor_no.notna(), floor_no + "层", "非食堂终端")

consume_df["支付方式"] = np.where(
    consume_df["交易名称"].str.contains("支付码", na=False),
    "支付码",
    "IC卡",
)

amount_99 = consume_df["交易金额"].quantile(0.99)
consume_df["是否异常金额"] = np.where(
    consume_df["交易金额"] > amount_99,
    "高金额复核",
    "常规金额",
)

print(consume_df[["交易小时", "餐段", "终端名称", "食堂楼层", "支付方式", "是否异常金额"]].head())`,
    explain: "pd.cut 把小时切成餐段，正则表达式从终端名称中提取楼层，np.where 根据条件批量生成分类字段。",
    why: "这些派生字段把原始流水变成可分析对象，后面的 groupby 才能直接回答业务问题。",
    points: ["NumPy 在这里用于向量化分类。", "pd.cut 适合把连续数值分箱。", "正则提取要兼容不同终端命名。"],
    terms: [
      { title: "派生字段", text: "根据原字段计算出的新字段。" },
      { title: "pd.cut", text: "把连续数值切成区间类别。" },
      { title: "np.where", text: "按条件批量生成结果。" },
    ],
  },
  {
    no: "08",
    label: "时间分析",
    title: "8 时间分析：每日消费和餐段高峰",
    lead: "消费流水最自然的问题是时间：哪天消费多，哪个餐段最集中。",
    code: String.raw`daily_summary = (
    consume_df.groupby("交易日期")
    .agg(
        交易笔数=("交易金额", "count"),
        消费总额=("交易金额", "sum"),
        人均单笔金额=("交易金额", "mean"),
    )
    .round(2)
    .sort_index()
)

hour_summary = (
    consume_df.groupby(["交易小时", "餐段"], observed=True)
    .agg(交易笔数=("交易金额", "count"), 消费总额=("交易金额", "sum"))
    .round(2)
    .reset_index()
    .sort_values("交易小时")
)

print(daily_summary.head())
print(hour_summary.head(10))`,
    explain: "按交易日期和交易小时分组，分别统计交易笔数、消费总额和平均单笔金额。",
    why: "时间统计能支撑报告里关于消费节奏和高峰时段的结论。",
    points: ["每日统计适合看趋势。", "小时统计适合找高峰。", "平均值要和笔数一起解释。"],
    terms: [
      { title: "groupby", text: "按类别或时间分组。" },
      { title: "agg", text: "一次生成多个统计指标。" },
      { title: "observed", text: "分组时只保留真实出现过的分类组合。" },
    ],
  },
  {
    no: "09",
    label: "方式终端",
    title: "9 支付方式与终端分析：看消费发生在哪里",
    lead: "除了时间，还要看支付方式、食堂楼层和 POS 终端，这些结果更接近管理和服务问题。",
    code: String.raw`payment_summary = (
    consume_df.groupby("支付方式")
    .agg(交易笔数=("交易金额", "count"), 消费总额=("交易金额", "sum"))
    .round(2)
    .sort_values("交易笔数", ascending=False)
)
payment_summary["笔数占比"] = (
    payment_summary["交易笔数"] / payment_summary["交易笔数"].sum()
).round(4)

floor_summary = (
    consume_df.groupby("食堂楼层")
    .agg(交易笔数=("交易金额", "count"), 消费总额=("交易金额", "sum"))
    .round(2)
    .sort_values("交易笔数", ascending=False)
)

pos_summary = consume_df["终端名称"].value_counts().head(10)

print(payment_summary)
print(floor_summary)
print(pos_summary)`,
    explain: "按支付方式和楼层分组统计，再用 value_counts 找出最常出现的 POS 终端。",
    why: "这些统计表能回答支付习惯和食堂终端使用情况，而不需要介绍 pandas 的所有方法。",
    points: ["占比比单纯数量更容易解释。", "POS 热度用前 10 名即可。", "楼层提取失败的记录要保留为非食堂终端。"],
    terms: [
      { title: "占比", text: "某类记录数除以总记录数。" },
      { title: "POS 终端", text: "食堂刷卡或支付设备。" },
      { title: "排序", text: "把重点对象排到前面，方便解释。" },
    ],
  },
  {
    no: "10",
    label: "脱敏汇总",
    title: "10 学生汇总：只做脱敏展示，不公开姓名学号",
    lead: "学生消费数据涉及个人信息。课堂和报告可以统计学生层面，但展示时要脱敏。",
    code: String.raw`student_summary = (
    consume_df.groupby(["学工号", "姓名"])
    .agg(
        消费笔数=("交易金额", "count"),
        消费总额=("交易金额", "sum"),
        平均单笔金额=("交易金额", "mean"),
        首次消费=("交易日期", "min"),
        最后消费=("交易日期", "max"),
    )
    .round(2)
    .reset_index()
    .sort_values("消费总额", ascending=False)
    .reset_index(drop=True)
)

student_summary.insert(
    0,
    "学生编号",
    [f"Student{i:03d}" for i in range(1, len(student_summary) + 1)],
)
student_summary_anonymized = student_summary.drop(columns=["学工号", "姓名"])

print(student_summary_anonymized.head())`,
    explain: "先按学工号和姓名汇总，再生成 Student001 这类编号，并删除姓名和学号。",
    why: "分析要尊重数据边界。个人信息可以参与计算，但不应作为公开展示重点。",
    points: ["学生层面只交脱敏结果。", "保留消费笔数、总额、均值和日期范围。", "报告不展示原始姓名学号排名。"],
    terms: [
      { title: "脱敏", text: "去掉能直接识别个人身份的信息。" },
      { title: "reset_index", text: "把分组索引还原成普通列。" },
      { title: "平均单笔金额", text: "总消费额除以消费笔数。" },
    ],
  },
  {
    no: "11",
    label: "保存结果",
    title: "11 保存结果：把报告需要的 CSV 全部写出来",
    lead: "只在屏幕上 print 不够。实验报告需要可提交、可复查的结果文件。",
    code: String.raw`OUTPUT_DIR = DATA_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

consume_df.to_csv(
    OUTPUT_DIR / "clean_canteen_transactions.csv",
    index=False,
    encoding="utf-8-sig",
)
daily_summary.to_csv(OUTPUT_DIR / "daily_summary.csv", encoding="utf-8-sig")
hour_summary.to_csv(OUTPUT_DIR / "hour_summary.csv", index=False, encoding="utf-8-sig")
payment_summary.to_csv(OUTPUT_DIR / "payment_summary.csv", encoding="utf-8-sig")
student_summary_anonymized.to_csv(
    OUTPUT_DIR / "student_summary_anonymized.csv",
    index=False,
    encoding="utf-8-sig",
)

print("已输出报告材料:")
for path in sorted(OUTPUT_DIR.glob("*.csv")):
    print(path.name)`,
    explain: "把清洗后明细、每日统计、小时统计、支付方式统计和脱敏学生汇总分别保存成 CSV。",
    why: "报告结论必须能回到文件核对，CSV 文件就是本章的主要产出。",
    points: ["保存中文 CSV 用 utf-8-sig。", "明细表不要丢掉派生字段。", "学生汇总只保存脱敏版本。"],
    terms: [
      { title: "to_csv", text: "把 DataFrame 保存为 CSV。" },
      { title: "index=False", text: "保存时不额外写入行索引。" },
      { title: "报告材料", text: "实验报告中引用的结果表。" },
    ],
  },
  {
    no: "12",
    label: "完整流程",
    title: "12 完整流程：从原始 CSV 到五张报告结果表",
    lead: "最后把读取、清洗、分析和保存合成一个可独立运行的函数。",
    code: String.raw`def run_canteen_analysis():
    df = pd.read_csv(DATA_DIR / "食堂消费数据.csv", encoding="gb18030")
    df.columns = df.columns.str.strip()

    money_cols = ["可用余额（交易前）", "交易金额", "可用余额（交易后）"]
    for col in money_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["交易日期"] = pd.to_datetime(df["记账日期"].astype(str), format="%Y%m%d", errors="coerce")
    df["交易时间文本"] = df["交易时间"].astype(str).str.zfill(6)
    df["交易小时"] = df["交易时间文本"].str[:2].astype(int)
    df["交易时刻"] = pd.to_datetime(
        df["记账日期"].astype(str) + df["交易时间文本"],
        format="%Y%m%d%H%M%S",
        errors="coerce",
    )
    df["余额差额"] = (
        df["可用余额（交易前）"] - df["交易金额"] - df["可用余额（交易后）"]
    ).round(2)
    df["余额是否异常"] = df["余额差额"].abs() > 0.01

    clean = df[
        df["交易名称"].str.contains("消费", na=False)
        & (df["交易金额"] > 0)
        & df["交易日期"].notna()
    ].copy()
    clean["餐段"] = pd.cut(
        clean["交易小时"],
        bins=[0, 10, 14, 17, 20, 24],
        labels=["早间", "午餐", "下午", "晚餐", "夜间"],
        right=False,
    )
    floor_match = clean["终端名称"].str.extract(r"食堂(\d)层|食堂(\d)F")
    floor_no = floor_match.bfill(axis=1).iloc[:, 0]
    clean["食堂楼层"] = np.where(floor_no.notna(), floor_no + "层", "非食堂终端")
    clean["支付方式"] = np.where(clean["交易名称"].str.contains("支付码", na=False), "支付码", "IC卡")
    clean["是否异常金额"] = np.where(
        clean["交易金额"] > clean["交易金额"].quantile(0.99),
        "高金额复核",
        "常规金额",
    )

    daily = clean.groupby("交易日期").agg(
        交易笔数=("交易金额", "count"),
        消费总额=("交易金额", "sum"),
        人均单笔金额=("交易金额", "mean"),
    ).round(2)
    hour = clean.groupby(["交易小时", "餐段"], observed=True).agg(
        交易笔数=("交易金额", "count"),
        消费总额=("交易金额", "sum"),
    ).round(2).reset_index()
    payment = clean.groupby("支付方式").agg(
        交易笔数=("交易金额", "count"),
        消费总额=("交易金额", "sum"),
    ).round(2)
    payment["笔数占比"] = (payment["交易笔数"] / payment["交易笔数"].sum()).round(4)
    student = clean.groupby(["学工号", "姓名"]).agg(
        消费笔数=("交易金额", "count"),
        消费总额=("交易金额", "sum"),
        平均单笔金额=("交易金额", "mean"),
        首次消费=("交易日期", "min"),
        最后消费=("交易日期", "max"),
    ).round(2).reset_index().sort_values("消费总额", ascending=False).reset_index(drop=True)
    student.insert(0, "学生编号", [f"Student{i:03d}" for i in range(1, len(student) + 1)])
    student_public = student.drop(columns=["学工号", "姓名"])

    output_dir = DATA_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    clean.to_csv(output_dir / "clean_canteen_transactions.csv", index=False, encoding="utf-8-sig")
    daily.to_csv(output_dir / "daily_summary.csv", encoding="utf-8-sig")
    hour.to_csv(output_dir / "hour_summary.csv", index=False, encoding="utf-8-sig")
    payment.to_csv(output_dir / "payment_summary.csv", encoding="utf-8-sig")
    student_public.to_csv(output_dir / "student_summary_anonymized.csv", index=False, encoding="utf-8-sig")

    print("原始记录数:", len(df))
    print("消费分析记录数:", len(clean))
    print("学生人数:", clean["学工号"].nunique())
    print("输出目录:", output_dir)


run_canteen_analysis()`,
    explain: "完整函数重复了前面每一步，并把五张报告表写入 output 目录。",
    why: "课堂上逐段理解，实验提交前运行完整流程，能保证结果可复现。",
    points: ["完整流程不能依赖手工中间变量。", "输出文件名要和实验要求一致。", "报告文字要引用这些输出表。"],
    terms: [
      { title: "可复现", text: "重新运行仍能得到同样处理逻辑和结果。" },
      { title: "完整流程", text: "读取、清洗、分析、保存串成一个函数。" },
      { title: "输出目录", text: "集中存放实验结果文件的位置。" },
    ],
  },
];

export const chapter08AssessmentCards = [
  { title: "基础达标", text: "能正确读取 GB 编码 CSV，并说明记录数、字段数、学生人数和日期范围。" },
  { title: "核心达标", text: "能完成日期时间转换、消费交易筛选、余额差异检查和派生字段生成。" },
  { title: "分析达标", text: "能生成每日、小时、支付方式、终端楼层和脱敏学生汇总结果。" },
  { title: "提交材料", text: "提交代码、五张输出 CSV、实验报告 5，并在结论中引用具体表格和数值。" },
];
