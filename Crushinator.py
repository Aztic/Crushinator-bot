from Anilist import next_anime, anime_search
from Documentation import documents
from Weather import weather_client
from riot_client import commands
from random import choice
from functions import Function
import time
import urllib.request
import json
import asyncio
import discord
import os

BOT_TOKEN = os.getenv('CRUSHINATOR_BOT_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
P_ID = os.getenv('DISCORD_ID')
API_KEY = os.getenv('OPENWEATHER_API_KEY')
TAG_PATH = os.path.join(os.getcwd(),"Images/Tags/")
ANIME_PATH = os.path.join(os.getcwd(),"Images/Anime command/")
supported_formats = ['jpg', 'jpeg', 'gif', 'png', 'bmp']


op_client = weather_client.Weather(API_KEY)
al_client = next_anime.client
d_client = discord.Client()
r_client = commands.client

def kelvin_to_celsius(kelvin):
	return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
	return kelvin * 9/5 - 459.67

@d_client.event
async def on_ready():
    print('Logged in as')
    print(d_client.user.name)
    print(d_client.user.id)
    print('------')
    await d_client.change_presence(game=discord.Game(name='$help'))


@d_client.event
async def on_message(message):
	if message.author == d_client.user:
		return
	
	#Next anime command
	if message.content.startswith('$next'):
		search = message.content.split("$next ")[1]
		split_search = search.split()
		split_search = [i.lower() for i in split_search]
		#Api request URL
		path = 'anime/search/' + search.lower()
		try:
			an_id = next_anime.search_thing(search.lower(),path,al_client)
			#Do a "splitted" search
			if an_id is None:
				an_id = next_anime.splitted_search(split_search,path,al_client)
			if an_id is -1:
				await d_client.send_message(message.channel, search + ' is not airing')
			elif not an_id:
				await d_client.send_message(message.channel, 'Not found, write it properly')
			else:
				secs = next_anime.search_with_id(an_id,al_client)
				the_dict = next_anime.date_things(secs,0,search,1)
				the_string = ''
				order = ['day', 'hour', 'minute', 'second']
				for i in order:
					if the_dict[i] != '0':
						the_string += the_dict[i] + ' ' + i
						if int(the_dict[i]) > 1:
							the_string += 's' + ' '
						else:
							the_string += ' '
				print(search)
				await d_client.send_message(message.channel, the_string + 'until next episode')
		except:
			await d_client.send_message(message.channel, 'Not found')


	#Anime command
	if message.content.startswith('$anime'):
		search = message.content.split('$anime ')[1]
		split_search = search.split()
		split_search = [i.lower() for i in split_search]
		path = 'anime/search/' + search.lower()
		try:
			url = anime_search.search_thing(search.lower(),path,al_client)
			if url is None:
				url = anime_search.splitted_search(split_search,path,al_client)
		except:
			await d_client.send_message(message.channel, 'Not found')
		if url is None:
			await d_client.send_message(message.channel, 'Not found')
		else:
			#Get the id from the url
			id = url.split('/')[4]
			#Get the image url
			response = al_client.get('anime/',id,'/page')['image_url_lge']
			filename = ANIME_PATH + response.split('/')[-1]
			#If the file is not saved
			if response.split('/')[-1] not in os.listdir(ANIME_PATH):
				print('not in path')
				file = urllib.request.urlopen(urllib.request.Request(response, headers={'User-Agent':'next_anime/0.0.0'}))
				output = open(filename, 'wb')
				output.write(file.read())
				output.close()
			image = await d_client.send_file(message.channel, filename)
			await d_client.edit_message(image, url)

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

	#Saves the weather location
	if message.content.startswith('$weather save'):
		#Load the data from the file. It has this structure
		#{data}
		data = json.load(open('weathers'))
		data[str(message.author.id)] = message.content.split('$weather save ')[1]
		#Replaces or add the user configuration to the file. This saves the weather id
		#So it doesnt matter if the user changes his nickname
		json.dump(data,open('weathers', 'w'))
		await d_client.send_message(message.channel, 'Saved Successfully')
	elif message.content.startswith('$weather'):
		if message.content == '$weather':
			data = json.load(open('weathers'))
			if str(message.author.id) in data:
				search = data[str(message.author.id)]
			else:
				await d_client.send_message(message.channel, 'Please, first save some location, use $weather save <location>')
		else:
			search = message.content.split('$weather ')[1]
		if search:
			try:
				content = op_client.get(search)
				c_temp = '{:.2f}'.format(kelvin_to_celsius(content['main']['temp']))
				f_temp = '{:.2f}'.format(kelvin_to_fahrenheit(content['main']['temp']))
				to_print = '**' + search + '**' + '\n' + c_temp + ' C ' + f_temp + ' F\n' + content['weather'][0]['description'] + '\n' 'Wind: ' + str(content['wind']['speed']) + 'm/s'
				await d_client.send_message(message.channel, to_print)
			except:
				await d_client.send_message(message.channel, 'Can\'t find the location')

			

	if message.content == ('$test') and message.author.id == P_ID:
		await d_client.send_message(message.channel,message.author.roles[1])
		#f = await d_client.send_file(message.author, "weathers")
		#await d_client.edit_message(f, '40')

	if message.content == '$restart' and message.author.id == P_ID:
		os.system('cls & python Crushinator.py"')

	if message.content.startswith('$do') and message.author.id == P_ID:
		content = message.content.split('$do ')[1]
		if content == 'python':
			content = 'start cmd /k "python"'
		elif content == 'cmd':
			content = 'start cmd'
		elif content == 'clean':
			content = 'cls'
		os.system(content)

	if message.content == '$help':
		await d_client.send_message(message.channel, documents.help_command)
	elif message.content.startswith('$help'):
		content = message.content.split('$help ')[1]
		search = content.split(', ')
		for i in search:
			if i in documents.help_a:
				await d_client.send_message(message.channel, '**' + i + '**\n' + documents.help_a[i])
			else:
				await d_client.send_message(message.channel, "I can't help you with that")

	if message.content == '&':
		await d_client.send_message(message.channel,'No tag there q_q')
	elif message.content.startswith('&'):
		content = message.content.split('&')[1]
		items = json.load(open('tags'))
		if content not in items:
			await d_client.send_message(message.channel,'Unknown tag')
		else:
			file = os.path.join(TAG_PATH,items[content])
			await d_client.send_file(message.channel,file)

	if message.content.startswith('$tag save'):
		data = json.load(open('tags'))
		content = message.content.split('$tag save')[1]
		splitted = content.split()
		url = splitted[-1]
		extension = url.split('.')[-1].lower()
		name = ' '.join(splitted[0:len(splitted)-1]) + '.' + extension
		if extension not in supported_formats:
			await d_client.send_message(message.channel, 'Nope')
			return
		try:
			file = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'image_save/0.0.0'}))
			output = open(TAG_PATH + name,'wb')
			output.write(file.read())
			output.close()
			data[' '.join(splitted[0:len(splitted)-1])] = name
			json.dump(data,open('tags','w'))
			await d_client.send_message(message.channel,'Saved successfully')
		except:
			await d_client.send_message(message.channel, 'Error')

	if message.content == '$tag list':
		data = json.load(open('tags'))
		string = []
		for k,v in data.items():
			string.append(k)
		await d_client.send_message(message.channel,'```'+', '.join(string)+'```')

	if message.content.startswith('$choose'):
		try:
			content = message.content.split('$choose ')[1]
			content = content.split(', ')
			if content:
				await d_client.send_message(message.channel,choice(content))
			else:
				await d_client.send_message(message.channel, 'No options')
		except:
			await d_client.send_message(message.channel, 'Empty')

	if '┻━┻' in message.content and '>(' not in message.content:
		await d_client.send_message(message.channel,'(ヘ･_･)ヘ┳━┳')

	if message.content.startswith('$der'):
		content = message.content.split('$der ')[1]
		f = Function(content)
		try:
			await d_client.send_message(message.channel, f.der)
		except:
			await d_client.send_message(message.channel, 'Can\'t do that')


if __name__ == '__main__':
	while True:
		d_client.run(BOT_TOKEN)
		time.sleep(3600)
