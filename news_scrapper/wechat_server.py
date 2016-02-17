from bottle import route, request,response ,run

@route('/weixin')
def hello():
	print('signature : ' ,request.query.signature)
	print('signature : ' ,request.query.timestamp)
	print('nonce :', request.query.nonce)
	print('echostr' , request.query.echostr);
	return "hello world"

run(host='localhost',port=8080,debug=True)