# -*- coding:utf-8 -*-
#__Author__ August1996
#只适用于广东海洋大学
import urllib
import urllib2
import cookielib
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

def Login(username,password):
	cookie = cookielib.CookieJar()
	handle = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handle)
	#创建一些必要的网络通信构件
	
	url = "http://210.38.138.10:81/IndexDo.asp"
	values = {
		"Users_LoginName":username,
		"Users_LoginPass":password,
		"Enter":"66"
	}
	data = urllib.urlencode(values)
	#构造用户登录的表单信息
	
	req = urllib2.Request(url,data)
	response = opener.open(req)
	#用前面构造的信息构造出一个request对象并且打开
	#
	text = response.read()
	if len(text) > 20:
		print("登陆失败,请重新登录")
		return False

	url = "http://210.38.138.10:81/exam.asp"
	opener.open(url)
	#打开考试地址,让系统标记你为考试状态


	url = "http://210.38.138.10:81/MainDo.asp"
	values = {
		"TimeOutDo":"0",
		"Enter":"66",
		"QuestionA139":"A",
		"Question0":",139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139",
		"Question1":"",
		"Question2":""
	}
	data = urllib.urlencode(values)
	#个人找到了一些规律,构造交卷信息

	req = urllib2.Request(url,data)
	response = opener.open(req)
	#...
	
	text = response.read()
	text = text.split("测试通过")[0]
	print text
	#...
	return True

print("输入基本信息,图书馆初始密码为学号!")
username = raw_input("请输入学号:")
password = raw_input("请输入密码:")
while not Login(username,password):
	print("输入基本信息,图书馆初始密码为学号!")
	username = raw_input("请输入学号:")
	password = raw_input("请输入密码:")
#...