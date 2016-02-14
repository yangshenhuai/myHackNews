# -*- coding: utf8 -*-

from bs4 import BeautifulSoup 
import base_parser


def parse(html,keywords,url_prefix):
	soup=BeautifulSoup(html,'html.parser')
	news_blocks = soup.find_all('div',class_='news_type_block')
	results= {}
	for block in news_blocks :
		h2_block = block.contents[1]
		title_block = h2_block.contents[1]
		if base_parser.isContainKeyword(keywords,title_block.text):
			results[base_parser.simplify_text(title_block.text)] = base_parser.get_url(url_prefix,title_block['href'],'/news')
	return results;


if __name__ == '__main__':
	parse(open('infoq_news.html',encoding='utf8'),['db','google','github'],'infoq.com/news')