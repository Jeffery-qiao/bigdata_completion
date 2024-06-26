
from templates.config import conn
cur = conn.cursor()
def is_null(username,password):
	if(username==''or password==''):
		return True
	else:
		return False



def is_existed(username,password):
	sql="SELECT * FROM user WHERE username ='%s' and password ='%s'" %(username,password)
	conn.ping(reconnect=True)
	cur.execute(sql)
	conn.commit()
	cur.execute(sql)
	result = cur.fetchall()
	
	if (len(result) == 0):
		return False
	else:
		return True

def exist_user(username):
	sql = "SELECT * FROM user WHERE username ='%s'" % (username)
	conn.ping(reconnect=True)
	cur.execute(sql)
	conn.commit()
	cur.execute(sql)
	result = cur.fetchall()
	
	if (len(result) == 0):
		return False
	else:
		return True



def vipis_null(vipname,vippassword):
	if(vipname==''or vippassword==''):
		return True
	else:
		return False


def vipis_existed(vipname,vippassword):
	sql="SELECT * FROM vipuser WHERE vipname ='%s' and vippassword ='%s'" %(vipname,vippassword)
	conn.ping(reconnect=True)
	cur.execute(sql)
	conn.commit()
	cur.execute(sql)
	result = cur.fetchall()
	
	if (len(result) == 0):
		return False
	else:
		return True

def vipexist_user(vipname):
	sql = "SELECT * FROM vipuser WHERE vipname ='%s'" % (vipname)
	conn.ping(reconnect=True)
	cur.execute(sql)
	conn.commit()
	cur.execute(sql)
	result = cur.fetchall()
	
	if (len(result) == 0):
		return False
	else:
		return True
