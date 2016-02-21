# -*- coding: utf-8 -*- 
from bottle import route, request,response ,run,post,get
import requests 
import os
import json
import time
import news_controller
from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring



app_id = os.environ['WECHAT_APPID']
app_secret=os.environ['WECHAT_APPSECRET']
access_token_url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+app_id+'&secret='+app_secret
print(access_token_url)
access_token = ''
access_token_expire_time=0
wechat_server_ip=[]
all_command_str={'tdy':'for todays news','yda':'for yesterdays news','new':'for latest news'}


@get('/weixin')
def hello():
	print('signature : ' ,request.query.signature)
	print('signature : ' ,request.query.timestamp)
	print('nonce :', request.query.nonce)
	print('echostr' , request.query.echostr);
	return request.query.echostr


@post('/weixin')
def receive_msg():
	global all_command_str
	try:
		if verify_ip(requests.environ.get('REMOTE_ADDR')):
			return "Error! Are you sure you are wechat server?"
		req_data = request.body.read().decode(encoding='utf8')
		msg_data = get_msg_data(req_data)

		if msg_data['Content'] not in all_command_str:
			resp_content = 'invalid command.valid usages:\n'
			for command in all_command_str:
				resp_content += command
				resp_content += ':'
				resp_content += all_command_str[command]
				resp_content += '\n'
			return generate_text_messages(msg_data,resp_content)

		news_list = news_controller.get_news(msg_data['Content'])
		return generate_news_messsage(msg_data,news_list)
	except:
		return generate_text_messages(msg_data,'system busy,please try again.');



def generate_text_messages(msg_data,text):
	text_msg = '<xml><ToUserName><![CDATA[' + msg_data['ToUserName'] + ']]></ToUserName><FromUserName><![CDATA[' + msg_data['FromUserName']\
			+ ']]></FromUserName><CreateTime>' + str(int(time.time())) + '</CreateTime><MsgType><![CDATA[text]]</MsgType><Content><![CDATA[' +\
			text + ']]></Content></xml>'
	return text_msg


def generate_news_messsage(msg_data,news_list):
	if news_list is None or len(news_list) == 0 :
		return generate_text_messages(msg_data,'Not have any news yet.');

	resp_text = '<xml></ToUserName><![CDATA[' + msg_data['ToUserName'] +']]></ToUserName><<FromUserName><![CDATA['+ msg_data['FromUserName']\
				+']]></FromUserName><CreateTime>'  + str(int(time.time())) + '</CreateTime><MsgType><![CDATA[news]]</MsgType><Content><![CDATA['\
				+'<ArticleCount>' + len(news_list) + '</ArticleCount></Articles>'
	
	for news in news_list:
		resp_text = resp_text +  '<item><Title><![CDATA[' + news.title + '</Title><Description><![CDATA[' + news.description + ']]></Description>'\
					+'<PicUrl><![CDATA[' + news.picurl + ']]></PicUrl><Url><![CDATA['  + news.url + ']]></Url></item>'
	
	resp_text+=resp_text+'</Articles></xml>'
	return resp_text



def verify_ip(ip):
	if ip in wechat_server_ip:
		return True
	print('invalid ip :' , ip)
	return False



def get_msg_data(request_data):
	result={}
	try:
		root = ET.fromstring(request_data)
		result['FromUserName'] = root.findall('FromUserName')[0].text
		result['ToUserName'] = root.findall('ToUserName')[0].text
		result['CreateTime'] = root.findall('CreateTime')[0].text
		result['MsgType'] = root.findall('MsgType')[0].text
		result['Content'] = root.findall('Content')[0].text
		result['MsgId'] = root.findall('MsgId')[0].text
		if Content:
			pass
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
		print('the access token is ' ,access_token)
		return access_token
	except BaseException as e:
		print('Error , fail to get access_token.' ,e )

def create_menu(access_token):
	#turn out I don't have this permission
	button_json='{"button":[{"type":"view","name":"give me some news","url":"http://www.yangsh.info/weixin/news"}]}'
	create_menu_url='https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+access_token
	resp = requests.post(create_menu_url,data=button_json,verify=False)
	resp_json = json.loads(resp.text)
	if resp_json['errcode'] == '0':
		print('create menu successfully')
	else:
		print('fail to create menu' , resp_json['errmsg'])


def get_wechat_ip(access_token):
	global wechat_server_ip
	if len(wechat_server_ip) != 0 :
		return wechat_server_ip
	get_ip_url='https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=' + access_token
	print('get ip url is ' ,get_ip_url)
	resp = requests.get(get_ip_url,verify=False)
	print('the get_ip response : ' , resp.text);
	resp_json = json.loads(resp.text)
	if resp_json['ip_list'] is not None:
		wechat_server_ip = resp_json['ip_list']
		print('wechat_server_ip is ',wechat_server_ip , 'and have ',len(wechat_server_ip),'servers')
	else:
		print('fail to get wechat server ip',resp_json)

if __name__ == '__main__':
	access_token = get_access_token()
	wechat_server_ip=get_wechat_ip(access_token)
	print('wechat server ip list ' , wechat_server_ip)
	news_controller.schedule()
	#since my accont is unauthorized accont , don't have permission to call this method
	# create_menu(access_token)
	run(host='localhost',port=8080,debug=True)


