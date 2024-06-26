import requests, time, re  # 发送请求，接收JSON数据，正则解析
from prettytable import PrettyTable  # 美化展示
from fake_useragent import UserAgent  # 随机请求头
from lxml import etree  # 进行xpath解析
from urllib import parse  # 将中文转换为url编码
from wordcloud import WordCloud  # 导入词云库生成词云
import jieba  # 导入jieba库分词
from templates.config import conn
cur = conn.cursor()
search_url = "https://s.weibo.com/weibo?q=%s"  # 搜索要使用的url
base_url = "https://weibo.com/ajax/statuses/buildComments"  # 获取评论需要使用的url
from selenium import webdriver
import time


option = webdriver.ChromeOptions()
 
#添加保持登录的数据路径：安装目录一般在C:\Users\****\AppData\Local\Google\Chrome\User Data
option.add_argument(r"user-data-dir=C:\Users\ts\AppData\Local\Google\Chrome\User Data")
requests.packages.urllib3.disable_warnings()
response = requests.get('https://s.weibo.com', verify=True)
browser = webdriver.Chrome(options=option)
browser.get("https://s.weibo.com/weibo?q=%s")
browser.maximize_window()
url = "https://s.weibo.com/weibo?q=%s"
# browser = webdriver.Chrome()
# browser.get(url)  # 访问微博官网
# time.sleep(30)  #用户自己登录账号
# 5.获取Cookie
cookies = browser.get_cookies()

# 6.Cookie数据处理
cookie_dict = {}
for item in cookies:
    cookie_dict[item['name']] = item['value']

# 微博有cookie反爬，如果要使用其搜索功能的话，最好添加cookie
headers = {
    'authority': 's.weibo.com',
    'method': 'GET',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    # 'cookie': 'SUB=_2AkMSAnp7f8NxqwFRmfoXzGjgb41xyAHEieKkXougJRMxHRl-yT8XqkcHtRB6OYJUlIRhLuKQYZq7jivaR3zD-cdMOKV3; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W56Gf3VI0hTPYlhLcwZxu62; _s_tentry=passport.weibo.com; Apache=7528099756271.912.1700721998452; SINAGLOBAL=7528099756271.912.1700721998452; ULV=1700721998663:1:1:1:7528099756271.912.1700721998452:',
    'pragma': 'no-cache',
    'referer': 'https://weibo.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': UserAgent().random,
}

commit_data = []  # 存储获取到的数据
index = 0  # 记录爬取评论页数，打印日志

def getkw(keyword):
    sql = "INSERT INTO kw(searchkeyword) VALUES ('%s')" %(keyword)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()


def get_id_uid(keyword,post_id):
    """传入要搜索的内容"""
    keyword = parse.quote(keyword)
    info = []  # 这里面存放uid和mid形成的元组
    table = PrettyTable(["序号", "发布人", "发布时间", "发布主题"])
    headers.update({
        'path': f'/weibo?q={keyword}',
        "user-agent": UserAgent().random
    })  # 防止反爬
    resp = requests.get(search_url % keyword, headers=headers,cookies=cookie_dict,verify = False)  # 发送请求
    resp.encoding = resp.apparent_encoding  # 设置编码
    html = etree.HTML(resp.text)  # 提交给xpath解析
    divs = html.xpath('//*[@id="pl_feedlist_index"]/div[2]/div')  # 获取到存储内容的div
    info = []  # 这里面存放uid和mid形成的元组
    table = PrettyTable(["序号", "发布时间", "作者", "主题"])  # 进行美化输出
    index = 0
    for index, div in enumerate(divs):
        try:
            mid = div.xpath("./@mid")[0]  # 获取mid
            # print(mid)
            u_url = div.xpath("./div[@class='card']/div[1]/div/a/@href")[0]  # 先获取链接，再解析数据
            uid = re.search("weibo.com/(?P<uid>\d+)\?refer", u_url).group("uid")  # 解析出uid
            # print(uid)
            info.append((mid, uid))  # 添加到列表中
            time_ = div.xpath("./div[@class='card']/div[1]/div[2]/p[1]/a/text()")[0]  # 发布时间
            time_ = time_.strip()
            time_ = time_.split()[0]
            # print(time_)
            author = div.xpath("./div[@class='card']/div[1]/div[2]/p[2]/@nick-name")[0]  # 发布人
            author = author.strip()
            # print(author)
            title = div.xpath("./div[@class='card']/div[1]/div[2]/p[2]/a/text()")[0]  # 发布主题
            title = title.strip()
            # print(title)
            if not (title.startswith("#") and title.endswith("#")):
                # 一般来说，微博里面的主题都是以#开头结尾的，如果不是，说明有点问题，直接抛弃数据
                raise AttributeError
            if not title or not author:
                # 如果数据缺失，直接抛弃数据
                raise AttributeError
            table.add_row([index + 1, time_, author, title])
        except IndexError:
            continue
        except AttributeError:
            index -= 1
            continue    
        try:
            i = post_id
            if not (0 < i <= index+1):  # 如果输入的数据不符合要求，报错
                raise AttributeError
            return info[i - 1]  # 返回对应的mid和uid
        except Exception as e:
            print("请按照要求输入哦！")
        return None

def get_table(keyword):
    """传入要搜索的内容"""
    table1 = []
    keyword = parse.quote(keyword)
    info = []  # 这里面存放uid和mid形成的元组
    table = PrettyTable(["序号", "发布人", "发布时间", "发布主题"])
    headers.update({
        'path': f'/weibo?q={keyword}',
        "user-agent": UserAgent().random
    })  # 防止反爬
    resp = requests.get(search_url % keyword, headers=headers,cookies=cookie_dict,verify = False)  # 发送请求
    resp.encoding = resp.apparent_encoding  # 设置编码
    html = etree.HTML(resp.text)  # 提交给xpath解析
    divs = html.xpath('//*[@id="pl_feedlist_index"]/div[2]/div')  # 获取到存储内容的div
    info = []  # 这里面存放uid和mid形成的元组
    table = PrettyTable(["序号", "发布时间", "作者", "主题"])  # 进行美化输出
    index = 0
    for index, div in enumerate(divs):
        try:
            mid = div.xpath("./@mid")[0]  # 获取mid
            # print(mid)
            u_url = div.xpath("./div[@class='card']/div[1]/div/a/@href")[0]  # 先获取链接，再解析数据
            uid = re.search("weibo.com/(?P<uid>\d+)\?refer", u_url).group("uid")  # 解析出uid
            # print(uid)
            info.append((mid, uid))  # 添加到列表中
            time_ = div.xpath("./div[@class='card']/div[1]/div[2]/p[1]/a/text()")[0]  # 发布时间
            time_ = time_.strip()
            time_ = time_.split()[0]
            # print(time_)
            author = div.xpath("./div[@class='card']/div[1]/div[2]/p[2]/@nick-name")[0]  # 发布人
            author = author.strip()
            # print(author)
            title = div.xpath("./div[@class='card']/div[1]/div[2]/p[2]/a/text()")[0]  # 发布主题
            title = title.strip()
            # print(title)
            if not (title.startswith("#") and title.endswith("#")):
                # 一般来说，微博里面的主题都是以#开头结尾的，如果不是，说明有点问题，直接抛弃数据
                raise AttributeError
            if not title or not author:
                # 如果数据缺失，直接抛弃数据
                raise AttributeError
            table.add_row([index + 1, time_, author, title])
            table1.append([index + 1, time_, author, title])
        except IndexError:
            continue
        except AttributeError:
            index -= 1
            continue
    return table1,index
    



def get_first_commit(arg):  # 传入文章id和作者id所组成的元组
    global index
    global commit_data
    params_ = {
        'is_reload': 1,  # 是否重新加载数据到页面
        'id': arg[0],  # 微博文章的id，可以在搜索页面中获得
        'is_show_bulletin': 2,
        'is_mix': 0,
        'count': 10,  # 推测是获取每页评论条数
        'uid': arg[1],  # 发布这篇微博的用户id
    }
    # print(params_)
    resp = requests.get(url=base_url, params=params_, headers=headers,cookies=cookie_dict,verify = False)
    data = resp.json()
    max_id = data["max_id"]
    for i in data["data"]:
        text = i["text"]
        text = re.sub("<.*?>", "", text)
        text = text.strip()
        if text:
            commit_data.append(text)
            print(text)
    # print("-----------------------------------------------------")
    # print("max_id", max_id)
    # print(f"爬取完{index}第页评论，休息4秒钟")
    # print("------------------------------------------------------")
    index += 1
    time.sleep(4)

    return max_id  # 返回max_id

def add_pinglun(pinglun):
    # sql commands
    sql = "INSERT INTO pinglun(pinglun) VALUES ('%s')" %(pinglun)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()

def get_other_commit(arg, max_id):
    global index
    global commit_data
    if max_id == 0:
        return "大部分内容获取完成！"
    params = {
        'flow': 0,  # 根据什么获取，0为热度，1为发布时间
        'is_reload': 1,  # 是否重新加载数据到页面
        'id': arg[0],  # 微博文章的id
        'is_show_bulletin': 2,
        'is_mix': 0,
        'max_id': max_id,  # 用来控制页数的，这个可以在上一个数据包的响应的max_id
        'count': 20,  # 推测是获取每页评论条数
        'uid': arg[1],  # 发布这篇微博的用户id
    }
    resp = requests.get(url=base_url, params=params, headers=headers,cookies=cookie_dict,verify = False)
    data = resp.json()
    max_id = data["max_id"]
    commit = data["data"]
    if commit:
        for i in commit:
            text = i["text"]
            text = re.sub("<.*?>", "", text)
            text = text.strip()
            if text:
                commit_data.append(text)
                print(text)
        index += 1
        time.sleep(4)
        return get_other_commit(arg, max_id)
    return "大部分内容获取完成！"


def get_img():
    data = open("C:/Users/ts/Desktop/毕设/flask_app/commit1.txt", "r", encoding="utf-8").read()  # 获取我们刚才获取到的数据
    # print(jieba.cut(data))  # 对数据进行分词，得到一个生成器
    stop_word = set(open("C:/Users/ts/Desktop/毕设/flask_app/stoplist.txt", encoding='utf-8').read().split())  # 导入停词表，进行数据的清洗，这个可以直接在百度上搜索下载
    # print(stop_word)
    word_list = [w for w in jieba.cut(data)]
    # print(word_list)
    font = "C:/Users/ts/Desktop/毕设/flask_app/font.ttf"  # 导入字体
    wc = WordCloud(font_path=font,
                   width=1000, 
                   height=700,
                   background_color='white',
                   max_words=100,
                   stopwords=stop_word,  # 加载停用词
                   ).generate(" ".join(word_list))  # 加载词云文本
    wc.to_file("C:/Users/ts/Desktop/毕设/flask_app/ret.png")


def add_commit1(arg):  # 传入文章id和作者id所组成的元组
    global index
    params_ = {
        'is_reload': 1,  # 是否重新加载数据到页面
        'id': arg[0],  # 微博文章的id，可以在搜索页面中获得
        'is_show_bulletin': 2,
        'is_mix': 0,
        'count': 10,  # 推测是获取每页评论条数
        'uid': arg[1],  # 发布这篇微博的用户id
    }
    # print(params_)
    resp = requests.get(url=base_url, params=params_, headers=headers,cookies=cookie_dict,verify = False)
    data = resp.json()
    max_id = data["max_id"]
    for i in data["data"]:
        text = i["text"]
        text = re.sub("<.*?>", "", text)
        text = text.strip()
        if text:
            sql = "INSERT INTO pinglun(pinglun) VALUES ('%s')" %(text)
            # execute(sql)
            cur.execute(sql)
            # commit
            conn.commit()  # 对数据库内容有改变，需要commit()
            conn.close()
            commit_data.append(text)
            print(text)
    index += 1
    time.sleep(4)

    return max_id  # 返回max_id

def add_commit2(arg, max_id):
    global index
    if max_id == 0:
        return "大部分内容获取完成！"
    params = {
        'flow': 0,  # 根据什么获取，0为热度，1为发布时间
        'is_reload': 1,  # 是否重新加载数据到页面
        'id': arg[0],  # 微博文章的id
        'is_show_bulletin': 2,
        'is_mix': 0,
        'max_id': max_id,  # 用来控制页数的，这个可以在上一个数据包的响应的max_id
        'count': 20,  # 推测是获取每页评论条数
        'uid': arg[1],  # 发布这篇微博的用户id
    }
    resp = requests.get(url=base_url, params=params, headers=headers,cookies=cookie_dict,verify = False)
    data = resp.json()
    max_id = data["max_id"]
    commit = data["data"]
    if commit:
        for i in commit:
            text = i["text"]
            text = re.sub("<.*?>", "", text)
            text = text.strip()
            if text:
                sql = "INSERT INTO pinglun(pinglun) VALUES ('%s')" %(text)
                # execute(sql)
                cur.execute(sql)
                # commit
                conn.commit()  # 对数据库内容有改变，需要commit()
                conn.close()
                commit_data.append(text)
        index += 1
        time.sleep(4)
        return get_other_commit(arg, max_id)
    return "评论已写入数据库！"