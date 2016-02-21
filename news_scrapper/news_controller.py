import base_scaper
from apscheduler.schedulers.background import BackgroundScheduler
import time

class news(object):
	def __init__(self,title,description,picurl,url):
		self.title = title
		self.description =description
		self.picurl = picurl
		self.url = url

	def __repr__(self):
		return "title:" + self.title + ",description:" + self.description + ",picurl:" + picurl + ',url:' + url


def schedule():
	scheduler = BackgroundScheduler(timezone='UTC')
	scheduler.add_job(base_scaper.scape, 'interval', minutes=30)
	scheduler.start()

def get_news(command):
	news_list = []
	news_list.append(news('test title','This is a test title' , 'http://yangsh.info/media/images/hacker.jpg' ,'http://yangsh.info/blog/2016/start_with_spring_boot'))
	return news_list




if __name__ == '__main__':
	scheduler = BackgroundScheduler()
	scheduler.add_job(base_scaper.scape, 'interval', minutes=3)
	scheduler.start()
	try:
		while True:
			time.sleep(2)
	except:
		scheduler.shutdown()






