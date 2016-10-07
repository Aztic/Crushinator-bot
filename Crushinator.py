from Anilist_date_search import next_anime
import asyncio
import discord
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

al_client = next_anime.client
d_client = discord.Client()

@d_client.event
async def on_ready():
    print('Logged in as')
    print(d_client.user.name)
    print(d_client.user.id)
    print('------')


@d_client.event
async def on_message(message):
	if message.content.startswith('$next'):
		anime = message.content.split("$next ")[1]
		path = 'anime/search/' + anime
		an_id = next_anime.search_thing(anime,path,al_client)
		if an_id == -1:
			await d_client.send_message(message.channel, anime + ' is not airing')
		elif not an_id:
			await d_client.send_message(message.channel, 'Not found, write it properly')
		else:
			secs = next_anime.search_with_id(an_id,al_client)
			the_string = next_anime.date_things(secs,0,anime,1)
			await d_client.send_message(message.channel, the_string)


d_client.run(BOT_TOKEN)