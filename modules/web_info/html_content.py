# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

user_agent = 'Discord bot (https://github.com/Aztic/Nyoko-bot)'
base_url_ud = 'https://www.urbandictionary.com/define.php?term='
base_url_jisho = 'http://jisho.org/search/'
base_url_jojo = 'http://jojo.wikia.com/wiki/'


def convert_string(content):
    return '+'.join(content.split())


def get(command, content=None):
    url = ''
    if command == 'ud':
        content = convert_string(content)
        url = base_url_ud + content
    elif command == 'js':
        content = urllib.parse.quote(content)
        url = base_url_jisho + content
    elif command == 'stand_list':
        url = base_url_jojo + "List_of_Stands"
    elif command == 'stand_page':
        url = base_url_jojo + content

    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
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
    return code.find('div', {'class': 'meaning'}).get_text()


def process_js(content):
    code = get('js', content)
    kanji = code.find('div', {'class': 'concept_light-wrapper columns zero-padding'}).find('span',
                                                                                           {'class': 'text'}).get_text()
    meaning = code.find('span', {'class': 'meaning-meaning'}).get_text()
    furigana = code.find('span',{'class':'furigana'}).find_all('span',{'class':'kanji-2-up kanji'})
    furigana = ''.join([i.get_text() for i in furigana])

    info = {kanji: meaning,'furigana':furigana}
    return info

def process_stand(content):
    #print("Content is " + content)
    code = get(command='stand_list')
    stand = code.find('a',{'title':content.title()})
    #not found m8
    if stand is None:
        return stand
    #stand thumbnail
    code = get('stand_page',stand.get('href').split('/')[-1])
    info = code.find_all('div', {'class': ['pi-data-value', 'pi-font']})
    user = info[1].find('a').get('title') if info[1].find('a') is not None else info[2].find('a').get('title')
    #Check if it have the "appareance" tag
    appearance = code.find('span',{'id':'Appearance'})

    if not code:
        return None
    #Stand info
    parameters = code.find('a',{'title':'Stand Parameters'})\
        .find_all_next('div',{'class':['pi-item','pi-data','pi-item-spacing','pi-border-color']},limit=6)
    return {'thumbnail':stand.find_all('img')[-1].get('src'),
            'appearance':appearance.find_next('p').get_text() if appearance else None,
            'user':user,
            'kanji':info[0].get_text(),
            'parameters': {i.find('h3').get_text():i.find('h3').find_next('div').get_text() for i in parameters}
            }

