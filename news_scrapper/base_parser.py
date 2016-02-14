# -*- coding: utf-8 -*- 
import re
import myblogParser
import hnParser
import infoqNewsParser

parse_map={'myblog':myblogParser,'HN':hnParser,'info_news':infoqNewsParser};
ignore_word=('\n')


def parse(html,website_name,website_url,keywords):
	if website_name in parse_map:
		return parse_map[website_name].parse(html,keywords,website_url)
	else :
		print('Warning! no parser configured for',website_name,',please check base_parser.parse_map')
		return None


def isContainKeyword(keywords,sentence):
	if type(keywords) is str:
		return keywords == '*' or  (re.search(keywords.lower(),sentence.lower()) is not None)
	elif type(keywords) is list or type(keywords) is tuple or type(keywords) is set: 
		if '*' in keywords :
			return True
		for keyword in keywords:
			if re.search(keyword.lower(),sentence.lower()) is not None:
				return True
		return False


def get_url(url_prefix,path,duplication_part):
	if url_prefix.endswith(duplication_part) and path.startswith(duplication_part) :
		return url_prefix[0:len(url_prefix) - len(duplication_part)] + path;
	return url_prefix + path;

def simplify_text(text):
	for word in ignore_word:
		text = text.replace(word,' ');
		text = text.strip();
	return text;
	







