import os
from anilist import AniList

Client_ID = os.getenv('ANILIST_CLIENT_ID')
Client_Secret = os.getenv('ANILIST_CLIENT_SECRET')
client = AniList(client_id=Client_ID, client_secret=Client_Secret)


def search_character(character, the_client):
    try:
        options = the_client.get('character/search/', character)
        if isinstance(options, dict):
            return None
        else:
            return options
    except:
        print("Error with search_character")
        return None


def display_info(character):
    info = '```\n'
    if character['name_last']:
        info += 'Name: {} {}\n'.format(character['name_first'], character['name_last'])
    else:
        info += 'Name: {}\n'.format(character['name_first'])
    info += 'Japanese name: {}\n'.format(character['name_japanese'])
    info += 'Alt names: {}\n'.format(character['name_alt'])
    info += 'Info : {}\n'.format(character['info'])
    info += '```\n{}'.format('http://anilist.co/character/' + str(character['id']))

    return info


def simple_display(character):
    info = '```\n'
    if character['name_last']:
        info += 'Name: {} {}\n'.format(character['name_first'], character['name_last'])
    else:
        info += 'Name: {}\n'.format(character['name_first'])
    info += 'Japanese name: {}\n'.format(character['name_japanese'])
    info += 'Alt names: {}\n'.format(character['name_alt'])
    info += '```\n{}'.format('http://anilist.co/character/' + str(character['id']))
    return info
