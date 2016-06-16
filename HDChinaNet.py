# -*- coding:utf-8 -*-
	# __Author__:August1996
	# 广东海洋大学一键登录宽带
	
	# 工具:
		# tesseract OCR工具
		# pyocr库
		# requests库
		# PIL库或者Image库


import urllib
import urllib2
import cookielib
import requests

# def imgTostring(path):
# 	validPage = "http://www.free-ocr.com"
# 	response = requests.post(validPage, files={'userfile' : open(path, 'rb')})
# 	fileId = response.text.split("result.php?name=")[1].split("\'")[0]

# 	textCodePage = "http://www.free-ocr.com/FW/result.php?name=" + fileId
# 	text = requests.post(textCodePage).text
# 	if(text.find(">") != -1):
# 		text = text.split(">")[1]

# 	if(text.find("<") != -1):
# 		code = text.split("<")[0].strip()
# 		return code
# 	else:
# 		return -1
#	使用在线识别验证码,作废的原因你懂的...


def imgTostring(path):
	from pyocr import pyocr
	from PIL import Image

	tools = pyocr.get_available_tools()[:]
	#寻找可用的OCR工具
	if len(tools)== 0:
		print "No OCR tool found"
		return -1
	else:
		code = tools[0].image_to_string(Image.open('code.jpg'))
		return code
		#返回识别出来的验证码

def main(username,password):
	testPage = "http://www.baidu.com/"
	# testPage = "http://enet.10000.gd.cn:10001/qs/index.jsp?wlanacip=61.146.26.191&wlanuserip=10.8.204.191"
	response = requests.post(testPage)
	testText = response.text
	if(testText.find("bd_logo1") != -1):
		print "嘿嘿,你已经可以上网了哇!!!^_^"
		return True
	testUrl = response.url
	#判断是否会跳转,不会跳转则网络正常

	wlanacip = testUrl.split("wlanacip=")[1].split("&")[0]
	wlanuserip = testUrl.split("wlanuserip=")[1]
	#若跳转,则取到wlanuserip和wlanacip的值

	# wlanacip = "61.146.26.191"
	# wlanuserip = "10.8.204.191"
	# username = "xxx"
	# password = "xxx"
	# code = ""

	loginPage = "http://enet.10000.gd.cn:10001/qs/index.jsp?wlanacip=" +wlanacip + "&wlanuserip=" + wlanuserip
	postPage = "http://enet.10000.gd.cn:10001/ajax/login"
	codePage = "http://enet.10000.gd.cn:10001/common/image_code.jsp"

	cookie = cookielib.MozillaCookieJar()
	processor= urllib2.HTTPCookieProcessor(cookie)
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(processor,handler)
	urllib2.install_opener(opener)
	#初始化

	response = urllib2.urlopen(loginPage)

	response = urllib2.urlopen(codePage)
	remotePic= response.read()
	path = "code.jpg"

	localPic = open(path,"wb")
	localPic.write(remotePic)
	localPic.close()
	#获取图片验证码并保存

	code = imgTostring(path)
	while(code == -1):
		code = imgTostring(path)
	#提取验证码

	postData = {
		"wlanacip"	:	wlanacip,
		"wlanuserip"	:	wlanuserip,
		"username"	:	username,
		"password"	:	password,
		"code"	:	code
	}


	data = urllib.urlencode(postData)

	request = urllib2.Request(postPage,data)
	response = urllib2.urlopen(request)
	#模拟登陆

	postText = response.read();
	if(postText.find("resultCode\":\"0\"") != -1):
		return True
	#判断返回状态


accounts = {
	"1"	:	{"username"	:	"xxxx","password"	:	"xxxx"},
	"2"	:	{"username"	:	"xxxx","password"	:	"xxxx"}
}
#这是我自己的两个账户

for key in accounts:
	print key + "\t" + accounts[key]['username']

account_number = raw_input("你要选择哪一个用户:");
while (account_number not in accounts):
	for key in accounts:
		print key + "\t" + accounts[key]['username']
	account_number = raw_input("请输入正确地用户编号:");

print "神经彬:正在登陆..."
while(not main(accounts[account_number]['username'],accounts[key]['password'])):
	pass