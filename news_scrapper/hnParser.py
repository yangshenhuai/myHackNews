# -*- coding: utf8 -*-
from bs4 import BeautifulSoup 
import base_parser

def parse(html,keywords,url_prefix):
	soup=BeautifulSoup(html,'html.parser')
	results= {}
	title_list = soup.find_all('td',attrs={'class':'title'})
	for title in title_list:
		a = title.find('a');
		if a is not None and base_parser.isContainKeyword(keywords,a.text) and a['href'].startswith('http'):
			results[a.text] =  a['href']

	return results




if __name__ == '__main__':
	parse(open('hn.html',encoding='utf8'),['http','js'],'http://news.ycombinator.com')
