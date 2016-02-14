# -*- coding: utf-8 -*- 
import requests
import redis_operation
import sys
import base_parser

the_http_prefix = "http://"


settings = redis_operation.readConfigurations()
print (settings)

all_results = {}
for setting in settings:
	website_url = the_http_prefix+setting.url
	r = requests.get(website_url,verify=False)
	result = base_parser.parse(r.text,setting.name,website_url,setting.keywords)
	if result is not None:
		all_results.update(result);

redis_operation.save_result(all_results)		

