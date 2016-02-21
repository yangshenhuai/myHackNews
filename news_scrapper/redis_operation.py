# -*- coding: utf-8 -*- 
import redis
import time
import os



r = redis.Redis(host='50.30.35.9',port=3464,db=0,password=os.environ['REDIS_PWD'])

result_table_name='result_table' 

class setting(object):
	def __init__(self,name,url,keywords):
		self.name=name
		self.url=url
		self.keywords=keywords

	def __str__(self):
		return "name:" + self.name + ",url:" + self.url + ",keywords:" + str(self.keywords)

	def __repr__(self):
		return "name:" + self.name + ",url:" + self.url + ",keywords:" + str(self.keywords)



def readConfigurations() :
	result = [];
	urls=r.lrange('urls',0,-1);
	for url in urls:
		url_str = url.decode('utf-8');
		name=url_str.split(':')[0]
		r_url=url_str.split(':')[1];
		member_key_words={ m.decode('utf-8') for m in  r.smembers(name) }
		
		result.append(setting(name,r_url,member_key_words))
	return result;

def save_result(results) :
	add_list=[]
	if results is not None and len(results) > 0:
		for result in results:
			key=gen_key(result,results)
			if r.zscore(result_table_name,key) is None :
				add_list.append(key)
				add_list.append(time.time())
		print(add_list)
		r.zadd(result_table_name,*add_list) 

def gen_key(title,results_map) :
	return title + "@@" + results_map[title]

if __name__ == "__main__":
	print("results :",readConfigurations())