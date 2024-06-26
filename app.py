from flask import Flask,render_template, session
from flask import redirect
from flask import url_for
from flask import request,jsonify
from model.spider import add_pinglun, get_first_commit, get_id_uid, get_img, get_other_commit, get_table, getkw
from model.check_login import is_existed,exist_user,is_null,vipis_existed,vipexist_user,vipis_null
from model.check_regist import add_user,add_vipuser
from model.spider import commit_data
import matplotlib
matplotlib.use('Agg')
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from wordcloud import WordCloud  # 导入词云库生成词云
import jieba  # 导入jieba库分词




app = Flask(__name__,static_folder='static')
app.secret_key = 'your_secret_key'
@app.route('/')
def index():
    return redirect(url_for('user_login'))

@app.route('/index.html')
def index_page():
    return render_template('index.html')

@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method=='POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('login.html', message=login_massage)
        elif is_existed(username, password):
            return render_template('index.html', username=username)
        elif exist_user(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_massage)
    return render_template('login.html')


@app.route('/vip_login',methods=['GET','POST'])
def vip_login():
    if request.method=='POST':  # 注册发送的请求为POST请求
        vipname = request.form['vipname']
        vippassword = request.form['vippassword']
        if vipis_null(vipname,vippassword):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('login.html', message=login_massage)
        elif vipis_existed(vipname, vippassword):
            return render_template('index.html', username=vipname)
        elif vipexist_user(vipname):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_massage)
    # 在这里编写处理会员登录页面的逻辑
    # 可以返回一个渲染后的模板或其他响应
    return render_template('viplogin.html')

@app.route("/vipregister",methods=["GET", 'POST'])
def vipregister():
    if request.method == 'POST':
        vipname = request.form['vipname']
        vippassword = request.form['vippassword']
        if vipis_null(vipname,vippassword):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('vipregister.html', message=login_massage)
        elif vipexist_user(vipname):
            login_massage = "温馨提示：用户已存在，请直接登录"
            # return redirect(url_for('user_login'))
            return render_template('vipregister.html', message=login_massage)
        else:
            add_vipuser(request.form['vipname'], request.form['vippassword'] )
            return render_template('index.html', username=vipname)
    return render_template('vipregister.html')




@app.route("/regiser",methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('register.html', message=login_massage)
        elif exist_user(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            # return redirect(url_for('user_login'))
            return render_template('register.html', message=login_massage)
        else:
            add_user(request.form['username'], request.form['password'] )
            return render_template('index.html', username=username)
    return render_template('register.html')






@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    session['keyword'] = keyword
    # getkw(keyword)
    # 调用 spider.py 中的方法，传递关键词作为参数
    # table_data = get_table(keyword)
    # print(table_data)
    # return render_template('search_results.html', table_data=table_data)
    name = keyword
    # arg = get_id_uid(name)
    table1,index = get_table(name)
    print(table1)
    # if arg:
    #     get_other_commit(arg, get_first_commit(arg))
    #     # print(commit_data)
    #     with open("C:\\Users\\ts\\Desktop\\毕设\\flask_app\\commit1.txt", "w+", encoding="utf-8") as f:
    #         string = "\n".join(commit_data)
    #         f.write(string)
        # get_img()
    # return render_template('search_results.html')
    return render_template('show0.html', table=table1)

@app.route('/get_post', methods=['POST'])
def get_post():
    keyword = session.get('keyword')
    name = keyword
    table1,index = get_table(name)
    post_id = int(request.form['post_id'])
    if not (0 < post_id <= 99):  # 如果输入的数据不符合要求
        login_massage = "温馨提示：输入的编号不符合要求"
        return render_template('index.html', message=login_massage)
    else:
        # keyword = request.form['keyword']
        # getkw(keyword)
        # 调用 spider.py 中的方法，传递关键词作为参数
        # table_data = get_table(keyword)
        # print(table_data)
        # return render_template('search_results.html', table_data=table_data)
        # name = keyword
        arg = get_id_uid(name,post_id)
        table1,index = get_table(name)
        print(table1)
        if arg:
            get_other_commit(arg, get_first_commit(arg))
            # print(commit_data)
            with open("C:\\Users\\ts\\Desktop\\毕设\\flask_app\\commit1.txt", "w+", encoding="utf-8") as f:
                string = "\n".join(commit_data)
                f.write(string)
            # get_img()
        # return render_template('search_results.html')
        return render_template('search_results.html')


@app.route('/show')
def show():
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
    
    # 将每条评论的得分打在每条评论后面
    comments = []
    for index, row in df.iterrows():
        comment_with_score = f"{row['评论'].strip()} (得分: {row['得分']})"
        comments.append(comment_with_score)
    plt.clf()
    plt.pie(score_counts.values, labels=score_counts.index, autopct='%1.1f%%')
    plt.title('评论情感得分区间分布')
    plt.savefig(r'C:\Users\ts\Desktop\毕设\flask_app\static\pie_chart.png')
    file_path = 'C:/Users/ts/Desktop/毕设/flask_app/commit1.txt'
    comments = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            comments = file.readlines()
    except FileNotFoundError:
        return '文件不存在'

    data = open(r"C:\Users\ts\Desktop\毕设\flask_app\commit1.txt", "r", encoding="utf-8").read()  # 获取我们刚才获取到的数据
    # print(jieba.cut(data))  # 对数据进行分词，得到一个生成器
    stop_word = set(open("C:\\Users\\ts\\Desktop\\毕设\\spider_\\爬虫\\微博评论\\stoplist.txt", encoding='utf-8').read().split())  # 导入停词表，进行数据的清洗，这个可以直接在百度上搜索下载
    # print(stop_word)
    word_list = [w for w in jieba.cut(data)]
    # print(word_list)
    font = "C:\\Users\\ts\\Desktop\\毕设\\flask_app\\font.ttf"  # 导入字体
    wc = WordCloud(font_path=font,
                   width=1000,
                   height=700,
                   background_color='white',
                   max_words=100,
                   stopwords=stop_word,  # 加载停用词
                   ).generate(" ".join(word_list))  # 加载词云文本
    wc.to_file("C:\\Users\\ts\\Desktop\\毕设\\flask_app\\static\\ret.png")

    return render_template('show.html', comments=comments,low_scores_comments=low_scores_comments)


if __name__=="__main__":
    app.run()


