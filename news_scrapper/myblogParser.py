# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup 
import base_parser


def parse(html,keywords,url_prefix):
	soup = BeautifulSoup(html,'html.parser');
	header_list = soup.find_all('header',attrs={'class':'entry-header'});
	results= {}
	for header in header_list:
		for child in header.descendants:
			if child.name=='a' and base_parser.isContainKeyword(keywords,child.text):	
				if not base_parser.isContainKeyword('tags',child['href']):
					#titles
					results[child.text] = url_prefix + child['href']		

				else:
					#tags
					results[header.find('a').text] = url_prefix + header.find('a')['href']		
	return results
			
if __name__=='__main__':
	parse(open('myblog.html'),['spring','Test'],'')