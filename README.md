## 大数据专业的毕业生做的一个爬虫+情感分析毕设

此项目将爬虫与情感分析制作成了一个交互网站，爬虫和情感分析使用的是Python，网站制作用的是Flask，用户登录注册用到了MySQL数据库。

－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

一. 项目内容介绍
   
　　1.model文件夹中包含了用户的登陆注册方法，情感分析模块以及爬虫模块。
   
　　　![image](https://github.com/Jeffery-qiao/-/assets/78896220/7ed01399-3c3f-4d4d-b79f-9a39650ddbd6)

　　2.static文件夹中包含了网页所用到的css文件和各种图片
   
　　　![image](https://github.com/Jeffery-qiao/-/assets/78896220/e7e49930-4a1b-4a39-92c2-e4129fd67200)

　　3.templates文件夹中包含了各个网页的html

　　　![image](https://github.com/Jeffery-qiao/-/assets/78896220/4e788f10-b9fd-45ca-8d1d-593ec21b9afd)

　　4.app.py包含了flask的路由方法，调用各文件中的方法，是项目的启动文件。

　　5.其他：停用词、字体文件等等。


二. 使用方法

  1. 连接mysql数据库（导入connections.ncx文件）
  2. 注意：浏览器版本自动更新后，可能驱动与之不匹配会报错，如下所示：
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 99
Current browser version is 102.0.5005.63 with binary path C:\Program Files\Google\Chrome\Application\chrome.exe
```
此时我们需要重新下载与浏览器对应的驱动，覆盖如下两个位置：浏览器安装目录：C:\Program Files\Google\Chrome\Application 和 python安装目录

## 爬虫模块：

  1.  在本模块的设计初期都是先登录本人的微博账号后 F12 检
测 network，复制 cookie 到爬虫脚本中的头信息中后来实现信息爬取，这样操作十分繁琐
而且每次打开网站后，都需要进行登录账号，无法实现自动获取，于是决定设计添加保持
登录的数据路径，这样在第一次登录后，就可以自动获取用户的登录信息，方便来获取用
户的 cookie 信息。并且由于微博的 cookie 具有时效性，在一定时间后会过期，所以设计
用 selenium 库来实现 cookie 的自动获取。由使用者第一次使用该系统时，登录自己的微博
账号，之后利用 selenium 库自动获取用户的账号密码实现自动化登录微博，并获取 Cookie
信息。

      需要注意的是，浏览器版本自动更新后，可能 selenium 驱动会与之不匹配并返回报
错信息，此时需要重新下载与浏览器对应的驱动，覆盖浏览器安装目录和 python 安装目录
两个位置。

      为了实现这部分模块，需要初始化浏览器并创建一个 Chrome 浏览器对象，用它来加载
微博搜索页面，同时获取页面的 Cookie 信息。selenium 自动打开微博网页并获
取用户的登录信息来实现自动登录并且获取 cookie 等 header 信息供爬虫使用处理 Cookie
数据，将获取到的 Cookie 信息整理成字典形式，方便后续使用。设计定义了一个包含必要
请求头信息的字典，来模拟浏览器发送请求，系统自动控制打开了谷歌浏览器并登录了用户的微博账号。

![image](https://github.com/Jeffery-qiao/-/assets/78896220/4357dccc-1cd3-4b78-b70a-d8879991b6fb)

## 网页交互端展示：
  1. 首先注册并登录账号，登陆注册逻辑很简单，不讲解了。
  2. 在搜索栏输入想在微博搜索的关键词。

     ![image](https://github.com/Jeffery-qiao/-/assets/78896220/2101d064-7224-440b-b8ba-9d3e7760deda)

  3. 返回搜索到的帖子，输入帖子序号后爬取帖子的评论。

     ![image](https://github.com/Jeffery-qiao/-/assets/78896220/cae419c2-1f10-4da1-bc7e-30ee4d8b4088)

  
  4.爬取到评论内容并进行可视化展示。 
  
   ![image](https://github.com/Jeffery-qiao/-/assets/78896220/b6ebf8c7-5552-4105-a482-d5265a671dc6)
  
   ![image](https://github.com/Jeffery-qiao/-/assets/78896220/c6c59c94-09e3-4928-8a3d-9a5ce4859d3c)


  
  

如有需要教学，可添加作者vx号：landlords_dog
