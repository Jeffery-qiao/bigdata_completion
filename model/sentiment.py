import matplotlib
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
with open(r'C:\Users\ts\Desktop\毕设\flask_app\commit1.txt', 'r', encoding='utf-8') as file:
    sentences = file.readlines()
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
scores = []
for sentence in sentences:
    s = SnowNLP(sentence)
    score = s.sentiments
    scores.append(score)

# for i, sentence in enumerate(sentences):
#     print(f"评论 {i+1}: {sentence.strip()}")
#     print(f"评论得分: {scores[i]}")
#     print()
data = {'评论': sentences, '得分': scores}
df = pd.DataFrame(data)

# 将得分按照指定区间划分
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
labels = ['消极', '略差', '中立', '良好', '积极']
df['得分区间'] = pd.cut(df['得分'], bins=bins, labels=labels, include_lowest=True)

# 统计得分区间的数量
score_counts = df['得分区间'].value_counts().sort_index()

# 绘制饼图展示得分区间分布
plt.pie(score_counts.values, labels=score_counts.index, autopct='%1.1f%%')
plt.title('评论情感得分区间分布')
plt.savefig('pie_chart.png')