# -*- coding: utf-8 -*- 
from bottle import route, request,response ,run,post,get
import requests 
import os
import json
import time
from defusedxml import ElementTree as ET

app_id = os.environ['WECHAT_APPID']
app_secret=os.environ['WECHAT_APPSECRET']
access_token_url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+app_id+'&secret='+app_secret
print(access_token_url)
access_token = ''
access_token_expire_time=0




@get('/weixin')
def hello():
	print('signature : ' ,request.query.signature)
	print('signature : ' ,request.query.timestamp)
	print('nonce :', request.query.nonce)
	print('echostr' , request.query.echostr);
	return request.query.echostr


@post('/weixin')
def receive_msg():
	try:
		req_data = request.body.read().decode(encoding='utf8')
		msg_data = get_msg_data(req_data)
		print('msg_data is ' ,msg_data)
		return "success"

	except:
		return "success"

def get_msg_data(request_data):
	result={}
	try:
		root = ET.fromstring(req_data)
		result['FromUserName'] = root.findall('FromUserName')[0].text
		result['ToUserName'] = root.findall('ToUserName')[0].text
		result['CreateTime'] = root.findall('CreateTime')[0].text
		result['MsgType'] = root.findall('MsgType')[0].text
		result['Content'] = root.findall('Content')[0].text
		result['MsgId'] = root.findall('MsgId')[0].text
		result['success'] = True
		return result
	except Exception as e:
		print('fail to get msg :',str(e))
		result['success'] = False
		result['reason']='fail to process the wechat Msg,please check if this request comes from wechat'
		return result










def get_access_token():
	try : 
		global access_token 
		global access_token_expire_time
		if access_token=='' or int(time.time()) > access_token_expire_time : 
			print('start to request access_token')
			response = requests.get(access_token_url)
			print('access_token response : ' , response)
			res_json = json.loads(response.text)
			access_token = res_json['access_token']
			access_token_expire_time = int(time.time()) + res_json['expires_in']
		return access_token
	except BaseException as e:
		print('Error , fail to get access_token.' ,e )

def create_menu(access_token):
	button_json='{"button":[{"type":"view","name":"give me some news","url":"http://www.yangsh.info/weixin/news"}]}'
	create_menu_url='https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+access_token
	resp = requests.post(create_menu_url,data=button_json,verify=False)
	resp_json = json.loads(resp.text)
	if resp_json['errcode'] == '0':
		print('create menu successfully')
	else:
		print('fail to create menu' , resp_json['errmsg'])




if __name__ == '__main__':
	access_token = get_access_token
	#since my accont is unauthorized accont , don't have permission to call this method
	# create_menu(access_token)
	run(host='localhost',port=8080,debug=True)


