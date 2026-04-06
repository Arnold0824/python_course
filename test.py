import jieba
from wordcloud import WordCloud

text = "人工智能课程项目训练非常重要"
words = jieba.lcut(text)
result = " ".join(words)

wc = WordCloud(font_path="msyh.ttc", background_color="white")
wc.generate(result)
wc.to_file("cn_cut.png")