import os
from anilist import AniList

CLIENT_ID = os.getenv('ANILIST_CLIENT_ID')
CLIENT_SECRET = os.getenv('ANILIST_CLIENT_SECRET')
client = AniList(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
BASE_URL = 'http://anilist.co/anime/'
special_characters = [',', ';', '.', ':', '=', '(', ')', '!','?']

def search_thing(name, path, a_object):
	the_list = a_object.get(path)
	the_dict = {'name': None, 'id': None}
	if the_list:
		for i in the_list:
			if name == i['title_romaji'].lower() or name == i['title_english'].lower() or name == i['title_japanese']:
				url = BASE_URL + str(i['id']) + '/'
				for x in special_characters:
					if x in i['title_romaji']:
						i['title_romaji'] = i['title_romaji'].replace(x,'')
				url = url + i['title_romaji'].replace(' ', '')
				return url
	return None

#search the anime from the content of a list
def splitted_search(names, path, a_object):
	the_list = a_object.get(path)
	if the_list:
		for content in the_list:
			for name in names:
				if name not in content['title_romaji'].lower() and name not in content['title_english'].lower() and name not in content['title_japanese']:
					break
				if name == names[len(names)-1]:
					url = BASE_URL + str(content['id']) + '/'
					for x in special_characters:
						if x in content['title_romaji']:
							content['title_romaji'] = content['title_romaji'].replace(x, '')
					url = url + content['title_romaji'].replace(' ', '')
					return url
	return None
