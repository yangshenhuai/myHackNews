import base_scaper
from apscheduler.schedulers.background import BackgroundScheduler
import time
import redis_operation

class news(object):
	def __init__(self,title,url):
		self.title = title
		self.url = url
	def __repr__(self):
		return "(title:" + self.title + ',url:' + self.url + ')'


def schedule():
	scheduler = BackgroundScheduler(timezone='UTC')
	scheduler.add_job(base_scaper.scape, 'interval', minutes=30)
	scheduler.start()

def get_news(command):
	if command == 'news':
		origin_news = redis_operation.get_tdy_news()
		news_list = []
		for news_str in origin_news:
			str_arr = news_str.split('@@')
			news_list.append(news(str_arr[0],str_arr[1]))
	if len(news_list) == 0 :
		news_list.append(news('no news captured yet.',\
		'http://yangsh.info'))
	return news_list


if __name__ == '__main__':
	# scheduler = BackgroundScheduler()
	# scheduler.add_job(base_scaper.scape, 'interval', seconds=30)
	# scheduler.start()
	# try:
	# 	while True:
	# 		time.sleep(2)
	# except:
	# 	scheduler.shutdown()
	print(get_news('news'))





