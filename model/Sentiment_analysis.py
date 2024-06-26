import matplotlib.pyplot as plt
from snownlp import SnowNLP
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
def sentiment():
    with open(r'C:\Users\ts\Desktop\毕设\flask_app\commit1.txt', 'r', encoding='utf-8') as file:
        sentences = file.readlines()
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    scores = []
    for sentence in sentences:
        s = SnowNLP(sentence)
        score = s.sentiments
        scores.append(score)
    data = {'评论': sentences, '得分': scores}
    df = pd.DataFrame(data)
    low_scores_df = df[(df['得分'] <= 0.2)]
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
    labels = ['消极', '略差', '中立', '良好', '积极']
    df['得分区间'] = pd.cut(df['得分'], bins=bins, labels=labels, include_lowest=True)
    score_counts = df['得分区间'].value_counts().sort_index()
    low_scores_comments = low_scores_df['评论'].tolist()
    # 统计每个类别评论数量
    score_counts = df['得分区间'].value_counts().reindex(labels)
    # 绘制柱状图
    plt.figure(figsize=(8, 6))
    plt.bar(score_counts.index, score_counts.values, color='skyblue')
    plt.xlabel('情感类别')
    plt.ylabel('评论数量')
    plt.title('评论情感分布统计')
    plt.show()
    # 将每条评论的得分打在每条评论后面
    comments = []
    for index, row in df.iterrows():
        comment_with_score = f"{row['评论'].strip()} (得分: {row['得分']})"
        comments.append(comment_with_score)


if __name__ == '__main__':
    sentiment()