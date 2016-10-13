from Anilist_date_search import next_anime
from Documentation import documents
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
    await d_client.change_presence(game=discord.Game(name='$help'))


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

	if message.content.startswith('$sumDivision'):
		search = message.content.split("$sumDivision")[1].split()
		region = search[0]
		summoner = ''.join(search[1:len(search)])
		data = commands.get_division(region,summoner,r_client)
		if data == -1:
			await d_client.send_message(message.channel, 'Not Found')
		else:
			await d_client.send_message(message.channel, data)

	if message.content.startswith('$current game'):
		search = message.content.split('$current game')[1].split()
		region = search[0]
		summoner = ''.join(search[1:len(search)])
		information = commands.game_information(region,summoner,r_client)
		string_to_print = ''
		for i in information:
			string_to_print += '**Team** ' + str(int(int(i)/100)) + '\n'
			for j in information[i]:
				string_to_print += '**' + j + '**:' +' '
				if information[i][j] == -1:
					string_to_print += 'unranked \n'
				else:
					string_to_print += information[i][j] + '\n'
			string_to_print += '\n'
		await d_client.send_message(message.channel, string_to_print)

	if message.content == '$help':
		await d_client.send_message(message.channel, documents.help_command)



d_client.run(BOT_TOKEN)
