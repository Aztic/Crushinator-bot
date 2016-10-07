import os
from anilist import AniList
from time import gmtime, strftime, time

#This is only necessary if you are going to use the client
Client_ID = os.getenv('ANILIST_CLIENT_ID')
Client_Secret = os.getenv('ANILIST_CLIENT_SECRET')
client = AniList(client_id=Client_ID, client_secret=Client_Secret)


#Searchs the id of the anime/manga/movie
#Return possibilities
#Path examples
# manga/search/*manga name*
# anime/search/*anime name*
#
#Return possibilities
#0 == Not found, write it properly
#-1 == Is not airing
#else == Anime ID
def search_thing(name, path, a_object):
	the_list = a_object.get(path)
	if len(the_list) > 1:
		for i in the_list:
			if name == i['title_romaji'] or name == i['title_english'] or name == i['title_japanese']:
				if i['airing_status'] != 'currently airing':
					return -1
				return i['id']
	return 0


#Returns the date of the next episode
def search_with_id(id, a_object):
	the_list = a_object.get('anime/',id,'/airing/')
	#Search the "lowest" episode in the dictionary
	#This is because Anilist doesn't show only future
	#episodes
	lower_episode = min(the_list, key=int)
	while True:
		if the_list[lower_episode] > int(time()):
			return int(the_list[lower_episode])
		lower_episode = int(lower_episode)
		lower_episode += 1
		lower_episode = str(lower_episode)


#Converts the seconds until the next episode
#to a most "readable" form
def date_things(seconds, want_to_show, anime, want_to_return):
	episode_date = strftime("%Y-%m-%d %H:%M:%S", gmtime(seconds))
	if want_to_show:
		print("The next episode of ",anime," will be on",episode_date)
		print("That means you'll need to wait:")
	secs = seconds - int(time())
	days = int(secs/86400)
	secs -= 86400*days
	hours = int(secs/3600)
	secs -= 3600*hours
	mins = int(secs/60)
	secs -= 60*mins
	print(days,"days ",hours,"hours ", mins,"minutes ", secs, "seconds until next episode")
	#if you want to return the string
	if want_to_return:
		string_to_return = str(days) + " days " + str(hours) + " hours " + str(mins) + " minutes " + str(secs) + " seconds until next episode"
		return string_to_return
