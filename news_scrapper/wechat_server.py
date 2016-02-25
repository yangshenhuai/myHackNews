# -*- coding: utf-8 -*- 
from bottle import route, request,response ,run,post,get,template,static_file
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
all_command_str={'news':'for tdy latest news'}


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
	response.headers['Content-Type'] = 'xml/application'
	try:
		
		req_data = request.body.read().decode(encoding='utf8')
		msg_data = get_msg_data(req_data)
		print('msg_data',msg_data)
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
	except Exception as e:
		print('fail to process coming msg' , e );
		return generate_text_messages(msg_data,'system busy,please try again.');

@route('/gen_news/<filename>')
def server_static(filename):
	return static_file(filename, root='./gen_news')


def generate_text_messages(msg_data,text):
	text_msg = '<xml><ToUserName><![CDATA[' + msg_data['FromUserName'] + ']]></ToUserName><FromUserName><![CDATA[' + msg_data['ToUserName']\
			+ ']]></FromUserName><CreateTime>' + str(int(time.time())) + '</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[' +\
			text + ']]></Content></xml>'
	print('return text_msg ',text_msg)
	return text_msg


def generate_news_messsage(msg_data,news_list):
	
	file_name = generate_html_files(news_list)
	title = str(int(time.time()))
	url = 'http://yangsh.info:8080/gen_news/' + file_name


	resp_text = '<xml><ToUserName><![CDATA[' + msg_data['FromUserName'] +']]></ToUserName><FromUserName><![CDATA['+ msg_data['ToUserName']\
				+']]></FromUserName><CreateTime>'  + str(int(time.time())) + '</CreateTime><MsgType><![CDATA[news]]></MsgType>'\
				+'<ArticleCount>1</ArticleCount><Articles>'
	resp_text = resp_text + '<item><Title><![CDATA[' + title + ']]></Title><Description><![CDATA[' + title + ' \'s news ]]></Description>'\
					+'<PicUrl><![CDATA[http://yangsh.info/media/images/hacker.jpg]]></PicUrl><Url><![CDATA['  + url + ']]></Url></item>' 
	resp_text=resp_text + '</Articles></xml>'
	print('return news msg',resp_text)
	return resp_text

def generate_html_files(news_list):
	file_content = template('news',rows=news_list)
	file_name = 'gen_news/' + str(int(time.time())) + ".html"
	if not os.path.exists('gen_news'):
		os.makedirs(directory)
	with open(file_name, "w") as html_file:
		print(file_name,file=html_file)
	return file_name


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
		result['success'] = True
		print('result' , result)
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

	news_controller.schedule()
	#since my accont is unauthorized accont , don't have permission to call this method
	# create_menu(access_token)
	run(host='localhost',port=8080,debug=True)


