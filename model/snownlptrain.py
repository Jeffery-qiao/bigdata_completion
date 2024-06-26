from asyncio import log
from cmath import exp
from snownlp import sentiment
sentiment.train('neg.txt', 'pos.txt')
sentiment.save('sentiment.marshal')
import pandas as pd
import jieba
import bayes
df = pd.read_table("bosonnlp//BosonNLP_sentiment_score.txt",sep= " ",names=['key','score'])

class Sentiment(object):

    def __init__(self):
        self.classifier = Bayes()

    def save(self, fname, iszip=True):
        self.classifier.save(fname, iszip)

    def load(self, fname=data_path, iszip=True):
        self.classifier.load(fname, iszip)

    def handle(self, doc):
        words = seg.seg(doc)
        words = normal.filter_stop(words)
        return words

    def train(self, neg_docs, pos_docs):
        data = []
        for sent in neg_docs:
            data.append([self.handle(sent), 'neg'])
        for sent in pos_docs:
            data.append([self.handle(sent), 'pos'])
        self.classifier.train(data)

    def classify(self, sent):
        ret, prob = self.classifier.classify(self.handle(sent))
        if ret == 'pos':
            return prob
        return 1-prob
    
def train(self, data):
    # data 中既包含正样本，也包含负样本
    for d in data: # data中是list
        # d[0]:分词的结果，list
        # d[1]:正/负样本的标记
        c = d[1]
        if c not in self.d:
            self.d[c] = AddOneProb() # 类的初始化
        for word in d[0]: # 分词结果中的每一个词
            self.d[c].add(word, 1)
    # 返回的是正类和负类之和
    self.total = sum(map(lambda x: self.d[x].getsum(), self.d.keys())) # 取得所有的d中的sum之和

class AddOneProb():

    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 1 # 默认所有的none为1
    # 这里如果value也等于1，则当key不存在时，累加的是2
    def add(self, key, value):
        self.total += value
        # 不存在该key时，需新建key
        if not self.exists(key):
            self.d[key] = 1
            self.total += 1
        self.d[key] += value

def classify(self, x):
    tmp = {}
    for k in self.d: # 正类和负类
        tmp[k] = log(self.d[k].getsum()) - log(self.total) # 正类/负类的和的log函数-所有之和的log函数
        for word in x:
            tmp[k] += log(self.d[k].freq(word)) # 词频，不存在就为0
    ret, prob = 0, 0
    for k in self.d:
        now = 0
        try:
            for otherk in self.d:
                now += exp(tmp[otherk]-tmp[k])
            now = 1/now
        except OverflowError:
            now = 0
        if now > prob:
            ret, prob = k, now
    return (ret, prob)

key = df['key'].values.tolist()
score = df['score'].values.tolist()
def getscore(line):
    segs = jieba.lcut(line)  #分词
    score_list  = [score[key.index(x)] for x in segs if(x in key)]
    return  sum(score_list)  #计算得分

line = "今天天气很好，我很开心"
print(round(getscore(line),2))
#5.26

line = "今天下雨，心情也受到影响。"
print(round(getscore(line),2))
#-0.96