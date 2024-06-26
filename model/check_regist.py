from templates.config import conn

cur = conn.cursor()

def add_user(username, password):
    # sql commands
    sql = "INSERT INTO user(username, password) VALUES ('%s','%s')" %(username, password)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()

def add_vipuser(vipname, vippassword):
    # SQL 查询
    sql = "INSERT INTO vipuser(vipname, vippassword) VALUES (%s, %s)"
    # 执行查询
    cur.execute(sql, (vipname, vippassword))
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()
