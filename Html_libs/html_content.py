# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

user_agent = 'Discord bot (https://github.com/Aztic/Nyoko-bot)'
base_url_ud = 'https://www.urbandictionary.com/define.php?term='
base_url_jisho = 'http://jisho.org/search/'

def convert_string(content):
	return '+'.join(content.split())

def get(command, content):
	if not content:
		return None	
	if command == 'ud':
		content = convert_string(content)
		url = base_url_ud + content
	elif command == 'js':
		content = urllib.parse.quote(content)
		url = base_url_jisho + content
	req = urllib.request.Request(url, headers={'User-Agent':user_agent})
	body = b''
	with urllib.request.urlopen(req) as resp:
		while True:
			buf = resp.read()
			if not buf:
				break
			body += buf

	soup = BeautifulSoup(body, 'html5lib')
	return soup

def process_ud(content):
	code = get('ud', content)
	return code.find('div',{'class':'meaning'}).get_text()

def process_js(content):
	code = get('js',content)
	kanji = code.find('div', {'class':'concept_light-wrapper columns zero-padding'}).find('span',{'class':'text'}).get_text()
	meaning = code.find('span', {'class':'meaning-meaning'}).get_text()
	info = {kanji:meaning}
	return info



