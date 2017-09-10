import os
from anilist import AniList
from time import gmtime, strftime, time

# This is only necessary if you are going to use the client
Client_ID = os.getenv('ANILIST_CLIENT_ID')
Client_Secret = os.getenv('ANILIST_CLIENT_SECRET')
client = AniList(client_id=Client_ID, client_secret=Client_Secret)


# Searchs the id of the anime/manga/movie
# Return possibilities
# Path examples
# manga/search/*manga name*
# anime/search/*anime name*
#
# Return possibilities
# 0 == Not found, write it properly
# -1 == anime is not airing
# -2 == manga is not publishing
# else == Anime/manga ID
def search_thing(name, path, a_object):
    the_list = a_object.get(path)
    options = ['currently airing', 'not yet aired']
    if the_list:
        for i in the_list:
            if name == i['title_romaji'].lower() or name == i['title_english'].lower() or name == i['title_japanese']:
                if 'anime' in path and i['airing_status'] not in options:
                    return -1
                elif 'manga' in path and i['publishing_status'] != 'publishing':
                    return -2

                return i['id']
    return None


# search the anime from the content
# of a list
def splitted_search(names, path, a_object):
    the_list = a_object.get(path)
    options = ['currently airing', 'not yet aired']
    if the_list:
        for content in the_list:
            for name in names:
                if name not in content['title_romaji'].lower() and name not in \
                    content['title_english'].lower() and name not in content['title_japanese']:
                    break
                if name == names[len(names) - 1]:
                    if content['airing_status'] not in options:
                        return -1
                    return content['id']
    return None


# Returns the date of the next episode
# Anilist only supports anime atm
def search_with_id(id, a_object):
    the_list = a_object.get('anime/', id, '/airing/')
    # Search the "lowest" episode in the dictionary
    # This is because Anilist doesn't show only future
    # episodes
    lower_episode = min(the_list, key=int)
    while True:
        if the_list[lower_episode] > int(time()):
            return [int(the_list[lower_episode]), int(lower_episode)]
        lower_episode = int(lower_episode)
        lower_episode += 1
        lower_episode = str(lower_episode)


# Converts the seconds until the next episode
# to a most "readable" form
def date_things(seconds, want_to_show, anime, want_to_return):
    episode_date = strftime("%Y-%m-%d %H:%M:%S", gmtime(seconds))
    if want_to_show:
        print("The next episode of ", anime, " will be on", episode_date)
        print("That means you'll need to wait:")
    secs = seconds - int(time())
    days = int(secs / 86400)
    secs -= 86400 * days
    hours = int(secs / 3600)
    secs -= 3600 * hours
    mins = int(secs / 60)
    secs -= 60 * mins
    print(days, "days ", hours, "hours ", mins, "minutes ", secs, "seconds until next episode")
    # if you want to return the string
    if want_to_return:
        dict_to_return = {'day': str(days), 'hour': str(hours), 'minute': str(mins), 'second': str(secs)}
        return dict_to_return
