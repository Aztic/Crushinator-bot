from Anilist_date_search import next_anime
import commands
import asyncio
import discord
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

al_client = next_anime.client
d_client = discord.Client()
r_client = commands.client

@d_client.event
async def on_ready():
    print('Logged in as')
    print(d_client.user.name)
    print(d_client.user.id)
    print('------')


@d_client.event
async def on_message(message):
	if message.content.startswith('$next'):
		search = message.content.split("$next ")[1]
		path = 'anime/search/' + search
		an_id = next_anime.search_thing(search,path,al_client)
		if an_id == -1:
			await d_client.send_message(message.channel, search + ' is not airing')
		elif not an_id:
			await d_client.send_message(message.channel, 'Not found, write it properly')
		else:
			secs = next_anime.search_with_id(an_id,al_client)
			the_dict = next_anime.date_things(secs,0,search,1)
			the_string = ''
			order = ['days', 'hours', 'minutes', 'seconds']
			for i in order:
				if the_dict[i] != '0':
					the_string += the_dict[i] + ' ' + i + ' '
			print(search)
			await d_client.send_message(message.channel, the_string)

	if message.content == '$free week':
		await d_client.send_message(message.channel, ', '.join(commands.free_week(r_client)))

	if message.content.startswith('$mastery'):
		search = message.content.split("$mastery")[1].split()
		region = search[0]
		champ = search[1]
		summoner = ''.join(search[2:len(search)])
		data = commands.mastery_level(champ,region,summoner,r_client)
		if data == -1:
			await d_client.send_message(message.channel, 'Not found')
		else:
			await d_client.send_message(message.channel, summoner + ' has lvl ' + str(data['championLevel']) + ' with ' + champ + ' and has ' + str(data['championPoints']) + ' points with it')


d_client.run(BOT_TOKEN)
