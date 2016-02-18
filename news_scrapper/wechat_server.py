from bottle import route, request,response ,run
import requests 
import os
import json
import time
app_id = os.environ['WECHAT_APPID']
app_secret=os.environ['WECHAT_APPSECRET']
access_token_url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+app_id+'&secret='+app_secret
print(access_token_url)
access_token = ''
access_token_expire_time=0




@route('/weixin')
def hello():
	print('signature : ' ,request.query.signature)
	print('signature : ' ,request.query.timestamp)
	print('nonce :', request.query.nonce)
	print('echostr' , request.query.echostr);
	return request.query.echostr


def get_access_token():
	try : 
		if access_token=='' or int(time.time()) > access_token_expire_time : 
			print('start to request access_token')
			response = requests.get(access_token_url)
			print('access_token response : ' , response)
			res_json = json.load(response.text)
			access_token = res_json['access_token']
			access_token_expire_time = int(time.time()) + res_json['expires_in']
		return access_token
	except BaseException as e:
		print('Error , fail to get access_token.' ,e )

def create_menu(access_token):
	button_json='{"button":[{"type":"view","name":"给我点新鲜信息","url":"http://www.yangsh.info/weixin/news"}]}'
	create_menu_url='https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+access_token
	resp = requests.post(create_menu_url,data=button_json)
	resp_json = json.load(resp.text)
	if resp_json['errcode'] == '0':
		print('create menu successfully')
	else:
		print('fail to create menu' , resp_json['errmsg'])




if __name__ == '__main__':
	access_token = get_access_token()
	create_menu(access_token)
	run(host='localhost',port=8080,debug=True)


