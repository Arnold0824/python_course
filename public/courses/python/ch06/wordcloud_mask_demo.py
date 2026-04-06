import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# 读取文本文件
with open("text_course_feedback.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 读取停用词
with open("stopwords_basic.txt", "r", encoding="utf-8") as file:
    stopwords = {line.strip() for line in file if line.strip()}

# 分词并过滤掉过短或无意义的词
words = []
for word in jieba.lcut(text):
    word = word.strip()
    if len(word) > 1 and word not in stopwords:
        words.append(word)
result = " ".join(words)

# 读取 mask 图像，白色区域不会绘制词云
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
)
wc.generate(result)
wc.to_file("wordcloud_mask_demo.png")
