# -*- coding: utf-8 -*-

from Anilist import next_anime, anime_search, character_search
from Documentation import documents
from Weather import weather_client
import commands
from riot_client import Riot
from random import choice
from functions import Function
from Html_libs import html_content
import discord
import requests
import time
import urllib.request
import json
import asyncio
import os

TOKENS = json.load(open('tokens','r'))

RIOT_KEY = TOKENS['RIOT_API_KEY']
BOT_TOKEN = TOKENS['CRUSHINATOR_BOT_TOKEN']
CLIENT_ID = TOKENS['ANILIST_CLIENT_ID']
CLIENT_SECRET = TOKENS['ANILIST_CLIENT_SECRET']
P_ID = TOKENS['DISCORD_ID']
API_KEY = TOKENS['OPENWEATHER_API_KEY']
TAG_PATH = os.path.join(os.getcwd(),"Images/Tags/")
ANIME_PATH = os.path.join(os.getcwd(),"Images/Anime command/")
CHARACTER_PATH = os.path.join(os.getcwd(),"Images/Characters/")
LOG_PATH = os.path.join(os.getcwd(),'Logs')
supported_formats = ['jpg', 'jpeg', 'gif', 'png', 'bmp']
nya_url = 'https://nya.is/upload.php?output=json'


greetings_base = ['Qué pasó', 'Qué lo qué', 'Qué dice', 'Ládrame',
				'Háblame']
greetings_complement = ['Mano', 'Manubrio', 'Manaure', 'Manao',
						'Manivela','Manufactura','Manicura',
						'Manopla', 'Manifiesto', 'Manantial',
						'Manatí','Maniobra','Manaplás','Manaure',
						]




def kelvin_to_celsius(kelvin):
	return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
	return kelvin * 9/5 - 459.67

def at_least_one(List_a, List_b):
	for value in List_a:
		if value in List_b:
			return True
	return False


class Bot:
	def __init__(self,Token=None):

		if Token is None or not isinstance(Token,str):
			raise('You must pass client')


		#os.system('gnome-terminal')
		#temp = os.listdir('/dev/pts/')[0]
		#self.terminal_log = '/dev/pts/' + temp
		#Clients
		self.token = Token
		self.d_client = discord.Client()
		self.r_client = Riot(RIOT_KEY)
		self.op_client = weather_client.Weather(API_KEY)
		self.al_client = next_anime.client

		self.message = ''
		self.message_author = ''
		self.message_author_id = ''
		self.author_server_permissions = []
		self.message_server_id = ''
		self.message_channel = ''
		self.server_roles = []
		self.server_roles_permissions = []

		#data load
		self.words_data = json.load(open('words'))
		self.weather_data = json.load(open('weathers'))
		self.tag_data = json.load(open('tags'))

		self.optional_data_f = ['$ban word','$allow ban', '$unban word ', '$banned words'
								'$see ban permissions', '$delete ban permissions ', '$tyranny ']
		self.bot_functions = {
			'$next ':self.next_episode,
			'$anime ':self.anime,
			'$free week':self.free_week,
			'$mastery ':self.mastery,
			'$sumDivision ':self.sum_division,
			'$current game ':self.current_game,
			'$weather save ':self.weather_save,
			'$weather_only':self.weather_only,
			'$weather ':self.load_weather,
			'$restart':self.restart_bot,
			'$help_only':self.help_only,
			'$help ':self.help_command,
			'&':self.tag_send,
			'$tag save ':self.tag_save,
			'$tag list':self.tag_list,
			'$choose ':self.choose_options,
			'$der ':self.function_der,
			'$tyranny ':self.tyranny,
			'$see ban permissions':self.ban_permissions,
			'$delete ban permissions ':self.del_ban_permissions,
			'$ban word ':self.ban_word,
			'$allow ban ':self.allow_ban_word,
			'$unban word ':self.unban_word,
			'$banned words':self.banned_words,
			'$say ':self.bot_say,
			'$change game ':self.change_game,
			'$manga ':self.anime,
			'$ud ':self.urban_dictionary,
			'$to_kanji ':self.jisho,
			'$to_def ': self.jisho,
			"$purge ":self.purge,
			'$clean channel':self.purge_all,
			'$character ':self.character_search,
		}

	def __repr__(self):
		return 'Bot {}'.format(self.name)

	def event(self, *args, **kwargs):
		return self.d_client.event(*args, **kwargs)

	def _create_log(self,content,content2):
		today = time.strftime('%d-%m-%y')
		t_file = os.path.join(LOG_PATH, today)
		#os.system("echo '{}' > {}\n".format(content2,self.terminal_log))
		if not os.path.isfile(t_file):
			f = open(t_file,'w+',encoding="utf-8")
			f.write(content+'\n')
			f.close()
		else:
			f = open(t_file,'a',encoding="utf-8")
			f.write(content + ' \n')
			f.close()



	async def process_message(self,message):
		f = None
		need_to = False
		if message.author == self.d_client.user:
			return
		if self.d_client.user in message.mentions:
			await self.d_client.send_message(message.channel,'{} {}'.format(choice(greetings_base),choice(greetings_complement)))
		content = message.content.split(' &&do ')
		self.message = message
		self.message_author = message.author
		self.message_author_id = message.author.id
		try:
			s_roles = message.server.roles
			self.message_server_id = message.server.id
			author_roles = message.author.roles
			self.server_roles = [i.name.lower() for i in s_roles]
			self.server_roles_permissions = [i.id for i in s_roles]
			self.author_server_permissions = [i.id for i in author_roles]
		except:
			pass
		self.message_channel = message.channel
		if self.message.server != None and self.message.server.id in self.words_data and await self.clean_message(message.content.split()):
			return
		if '┻━┻' in self.message.content and '>(' not in self.message.content:
			await self.d_client.send_message(self.message_channel,'(ヘಠ益ಠ)ヘ┳━┳')
		for i in content:
		#special case
			if i == '$weather':
				await self.weather_only()
				need_to = True
			elif i == '$help':
				await self.help_only()
				need_to = True
			else:
				for index in self.bot_functions:
					if i.startswith(index):
						f = index
						break
			if f:
				need_to = True
				await self.bot_functions[f](message.content.split(f).pop())
			if need_to:
				content = '{}({}) requested {} from {} at {}'.format(message.author,message.author.id,message.content,message.server,time.strftime("%H:%M:%S"))
				without = '{} requested {} from {} at {}'.format(message.author,message.content,message.server,time.strftime("%H:%M:%S"))
				self._create_log(content, without)
		self._clean_vars()

	def _clean_vars(self):
		self.message = ''
		self.message_author = ''
		self.message_author_id = ''
		self.author_server_permissions = []
		self.message_server_id = ''
		self.message_channel = ''
		self.server_roles == []
		self.server_roles_permissions = []

	def run_bot(self,intervals=None):
		if not intervals:
			intervals = 3600
		while True:
			self.d_client.run(self.token)
			time.sleep(intervals)


	async def next_episode(self,content):
		split_search = [word.lower() for word in content.split()]
		#Api request URL
		path = 'anime/search/' + content.lower()
		try:
			an_id = next_anime.search_thing(content.lower(),path,self.al_client)
			if an_id is None:
				an_id = next_anime.splitted_search(split_search,path,self.al_client)
			if an_id == -1:
				await self.d_client.send_message(self.message.channel,'{} is not airing'.format(content))
			elif not an_id:
				await self.d_client.send_message(self.message.channel,'Not found')
			else:
				episode_data = next_anime.search_with_id(an_id,self.al_client)
				secs = episode_data[0]
				the_dict = next_anime.date_things(secs,0,content,1)
				order = ['day', 'hour', 'minute', 'second']
				the_string = ''
				for i in order:
					if the_dict[i] != '0':
						the_string += the_dict[i] + ' ' + i
						if int(the_dict[i]) > 1:
							the_string += 's' + ' '
						else:
							the_string += ' '
				await self.d_client.send_message(self.message_channel, the_string + 'until episode {}'.format(episode_data[1]))
		except:
			await self.d_client.send_message(self.message_channel, "Not found")
			print('ERROR with $next')

	async def anime(self,content):
		split_search = [i.lower() for i in content.split()]
		if 'anime' in self.message.content:
			path = 'anime/search/' + content.lower()
		else:
			path = 'manga/search/' + content.lower()
		try:
			url = anime_search.search_thing(content.lower(),path,self.al_client)
			if not url:
				url = anime_search.splitted_search(split_search,path,self.al_client)
		except:
			url = ''
		if not url:
			await self.d_client.send_message(self.message_channel, 'Not found')
		else:
			#Get id from url
			#an_id = url.split('/')[4]
			#response = self.al_client.get('anime/',an_id,'/page')['image_url_lge']
			#filename = ANIME_PATH + response.split('/')[-1]
			#if the file is not saved
			#if response.split('/')[-1] not in os.listdir(ANIME_PATH):
				#print('Not in path')
				#file = urllib.request.urlopen(urllib.request.Request(response, headers={'User-Agent':'next_anime/0.0.0'}))
				#output = open(filename, 'wb')
				#output.write(file.read())
				#output.close()
			await self.d_client.send_message(self.message.channel,url)
			#image = await self.d_client.send_file(self.message_channel, filename)
			#await self.d_client.edit_message(image, url)

	async def character_search(self,content):
		result = character_search.search_character(content,self.al_client)
		if not result:
			await self.d_client.send_message(self.message_channel,"Not found")
			return
		if len(result) > 1:
			all_c = ['{} {}'.format(i['name_first'],i['name_last']) if i['name_last'] else i['name_first'] for i in result]
			characters = ''
			for i,value in enumerate(all_c):
				characters += '{}: {}\n'.format(i+1,value)
			await self.d_client.send_message(self.message_channel,"Which {}?\n{}".format(content,characters))
			
			#await self.d_client.send_message(self.message_channel,characters)
			ch = self.message.channel
			option = await self.d_client.wait_for_message(timeout=60.0,author=self.message_author)
			if not option:
				await self.d_client.send_message(ch,"You took too long")
				return
			if int(option.content)-1 not in range(len(all_c)):
				await self.d_client.send_message(ch,"Invalid option")
				return
			else:
				character = result[int(option.content)-1]
				self.message_channel = ch
		else:
			character = result[0]
		filename = CHARACTER_PATH + character['image_url_lge'].split('/')[-1]
		if character['image_url_lge'].split('/')[-1] not in os.listdir(CHARACTER_PATH):
			print('{} Not in path'.format(content))
			file = urllib.request.urlopen(urllib.request.Request(character['image_url_lge'], headers={'User-Agent':'characters/0.0.0'}))
			output = open(filename, 'wb')
			output.write(file.read())
			output.close()
		image = await self.d_client.send_file(self.message_channel, filename)
		try:
			await self.d_client.edit_message(image, '{}'.format(character_search.display_info(character)))
		except:
			await self.d_client.edit_message(image, '{}'.format(character_search.simple_display(character)))





	async def free_week(self,*Nothing):
		content = ', '.join(commands.free_week(self.r_client))
		await self.d_client.send_message(self.message_channel,content)

	async def mastery(self,content):
		info = content.split()
		region = info[0]
		champ = info[1]
		summoner = ''.join(info[2:len(info)])
		data = commands.mastery_level(champ,region,summoner,self.r_client)
		if data == -1:
			await self.d_client.send_message(self.message_channel, 'Not found')
		else:
			await self.d_client.send_message(self.message_channel,'{} has lvl {} with {} and has {} points with it'.format(summoner,data['championLevel'],champ,data['championPoints']))

	async def sum_division(self,content):
		info = content.split()
		region = info[0]
		summoner = ''.join(info[1:len(info)])
		data = commands.get_division(region,summoner,self.r_client)
		if data == -1:
			await self.d_client.send_message(self.message_channel, 'Not Found')
		else:
			await self.d_client.send_message(self.message_channel, data)

	async def current_game(self,content):
		info = content.split()
		summoner = ''.join(info[1:len(info)])
		information = commands.game_information(region,summoner,self.r_client)
		s_t_p = ''
		for i in information:
			s_t_p += '**Team**' + str(int(int(i)/100)) + '\n'
			for j in information[i]:
				s_t_p += '**{}**: '.format(j)
				if information[i][j] is -1:
					s_t_p += 'Unranked\n'
				else:
					s_t_p += information[i][j] + '\n'
			s_t_p += '\n'
		await self.d_client.send_message(self.message_channel,s_t_p)

	async def weather_save(self,content):
		self.weather_data[self.message_author_id] = content
		json.dump(self.weather_data,open('weathers','w'))
		await self.d_client.send_message(self.message_channel,'Saved Successfully')

	async def weather_only(self,*nothing):
		if self.message_author_id not in self.weather_data:
			await self.d_client.send_message(self.message_channel, 'Please, first save some location')
		else:
			location = self.weather_data[self.message_author_id]
			await self.load_weather(location)

	async def load_weather(self,content):
		try:
			a_content = self.op_client.get(content)
			c_temp = '{:.2f}'.format(kelvin_to_celsius(a_content['main']['temp']))
			f_temp = '{:.2f}'.format(kelvin_to_fahrenheit(a_content['main']['temp']))
			to_print = '**{}** \n {} C {} F\n {} \n Wind: {} m/s'.format(content,c_temp,f_temp,a_content['weather'][0]['description'],a_content['wind']['speed'])	
			await self.d_client.send_message(self.message_channel, to_print)
		except:
			await self.d_client.send_message(self.message_channel, 'Can\'t find the location')

	async def restart_bot(self,*nothing):
		if self.message_author_id == P_ID:
			os.system('clear && python3 Crushinator_bot.py')

	async def help_only(self,*nothing):
		await self.d_client.send_message(self.message.author, documents.help_command)
		await self.d_client.send_message(self.message.channel, "I'm Nyoko, I'm helping Nya~")

	async def help_command(self,content):
		search = content.split()
		for i in search:
			if i in documents.help_a:
				await self.d_client.send_message(self.message.author,'**{}**\n{}'.format(i,documents.help_a[i]))
			else:
				await self.d_client.send_message(self.message.author, 'I can\'t help you with that')

	async def tag_send(self,content):
		if content in self.tag_data[self.message.server.id] and self.message.server.id in self.tag_data:
			await self.d_client.send_message(self.message_channel,self.tag_data[self.message.server.id][content])
		else:
			await self.d_client.send_message(self.message_channel,"Unknown tag")

	async def tag_list(self,*nothing):
		if self.message.server.id in self.tag_data and self.tag_data[self.message.server.id]:
			await self.d_client.send_message(self.message_channel,'```{}```'.format(', '.join(list(self.tag_data[self.message.server.id]))))
		else:
			await self.d_client.send_message(self.message_channel,"Empty")

	async def tag_save(self,content):
		splitted = content.split()
		attachments = self.message.attachments
		if attachments:
			url = attachments[0]['url']
		else:
			url = splitted[-1]
		extension = url.split('.')[-1].lower()
		if attachments:
			name = content + '.' + extension
			name1 = content
		else:
			name = ' '.join(splitted[0:len(splitted)-1]) + '.' + extension
			name1 = ' '.join(splitted[0:len(splitted)-1])
		if extension not in supported_formats:
			t_m_p = await self.d_client.send_message(self.message_channel, 'Saving...')
			if self.message.server.id not in self.tag_data:
				self.tag_data[self.message.server.id] = {}
			self.tag_data[self.message.server.id][name1] = url
			await self.d_client.edit_message(t_m_p,'Saved successfully')
			json.dump(self.tag_data,open('tags','w'))
			return
		try:
			t_m_p = await self.d_client.send_message(self.message_channel,'Uploading...')
			file = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'image_save/0.0.0'}))
			files = {'files[]':(name,file)}
			r = requests.post(nya_url,files=files)
			if r.json()['success']:
				if self.message.server.id not in self.tag_data:
					self.tag_data[self.message.server.id] = {}
				self.tag_data[self.message.server.id][name1] = r.json()['files'][0]['url']
			else:
				await self.d_client.send_message(self.message_channel,'Error, can\'t upload')
				return
			json.dump(self.tag_data,open('tags','w'))
			await self.d_client.edit_message(t_m_p,'Saved successfully')
		except:
			await self.d_client.send_message(self.message_channel, 'Error')

	async def ban_word(self,content):
		if self.message_server_id not in self.words_data:
			role_master = await self.d_client.create_role(self.message.server,name='Word master')
			#if max(self.author_server_permissions) == max(self.server_roles_permissions):
			self.words_data[self.message_server_id] = {'allowed_ranks':[], 'forbidden_words':[]}
			self.words_data[self.message_server_id]['allowed_ranks'].append(role_master.id)
			#self.words_data[self.message_server_id]['forbidden_words'].append(content)
			await self.d_client.send_message(self.message_channel, 'Please, give to someone the "Word master" role')
			#else:
				#self.d_client.send_message(self.message_channel, 'You are not allowed to do that')
				#return
		elif at_least_one(self.author_server_permissions,self.words_data[self.message_server_id]['allowed_ranks']):
			if content not in self.words_data:
				self.words_data[self.message_server_id]['forbidden_words'].append(content)
				await self.d_client.send_message(self.message_channel, 'Done')
			else:
				await self.d_client.send_message(self.message_channel, 'Already banned')
		else:
			await self.d_client.send_message(self.message_channel, 'You can\'t do that')
		json.dump(self.words_data,open('words','w'))

	async def allow_ban_word(self,content):
		if self.message_server_id not in self.words_data:
			await self.d_client.send_message(self.message_channel, 'Please ban any word first')
		elif content not in self.server_roles:
			await self.d_client.send_message(self.message_channel,'Can\t find that role')
		elif max(self.author_server_permissions) != max(self.server_roles_permissions):
			await self.d_client.send_message(self.message_channel,'You can\'t do that')
		else:
			self.words_data[self.message_server_id]['allowed_ranks'].append(self.server_roles_permissions[self.server_roles.index(content)])
			json.dump(self.words_data,open('words','w'))

	async def unban_word(self,content):
		if self.message_server_id not in self.words_data:
			await self.d_client.send_message(self.message_channel,'No banned words')
		elif at_least_one(self.author_server_permissions,self.words_data[self.message_server_id]['allowed_ranks']):
			if content not in self.words_data[self.message_server_id]['forbidden_words']:
				await self.d_client.send_mesage(self.message_channel,'That word is not banned')
			else:
				self.words_data[self.message_server_id]['forbidden_words'].remove(content)
				json.dump(self.words_data,open('words','w'))
				await self.d_client.send_message(self.message_channel,'Done')
		else:
			await self.d_client.send_message(self.message_channel,'You can\'t do that')

	async def banned_words(self,*nothing):
		if self.message_server_id not in self.words_data:
			await self.d_client.send_message(self.message_channel, 'No banned words')
		else:
			await self.d_client.send_message(self.message_channel,'**Banned words**\n{}'.format(', '.join(self.words_data[self.message_server_id]['forbidden_words'])))

	async def ban_permissions(self,*nothing):
		roles = []
		if self.message_server_id not in self.words_data:
			await self.d_client.send_message(self.message_channel,'Please, first ban any word')
			return
		#Has the "word master" role
		if self.words_data[self.message.server.id]['allowed_ranks'][0] in self.author_server_permissions:
			for i in self.words_data[self.message_server_id]['allowed_ranks']:
				roles.append(self.server_roles[self.server_roles_permissions.index(i)])
			await self.d_client.send_message(self.message_channel,', '.join(roles))
		else:
			self.d_client.send_message(self.message_channel,'You can\'t do that')

	async def del_ban_permissions(self,content):
		if self.words[self.message.server.id][allowed_ranks][0] not in self.author_server_permissions:
			await self.d_client.send_message(self.message_channel, "you cant do that")
			return
		role_id = self.server_roles_permissions[self.server_roles.index(content)]
		if self.message_server_id not in self.words_data:
			await self.d_client.send_message(self.message_channel,'Please, first ban any word')
			return
		if role_id not in self.words_data[self.message_server_id]['allowed_ranks']:
			await self.d_client.send_message(self.message_channel,'That role can\'t ban already')
		else:
			self.words_data[self.message_server_id]['allowed_ranks'].remove(role_id)
			await self.d_client.send_message(self.message_channel,'Done')

	async def tyranny(self,*nothing):
		if max(self.author_server_permissions) == max(self.server_roles_permissions):
			content = self.message.mentions
			if not content:
				await self.d_client.send_message(self.message_channel, 'You must mention someone')
			else:
				for person in content:
					try:
						await self.d_client.kick(person)
						await self.d_client.send_message(self.message_channel,'{0.mention} used tyranny and kicked {1.mention}'.format(self.message.author, person))
					except:
						await self.d_client.send_message(self.message_channel,'Bot Privilege is too low')
		else:
			await self.d_client.send_message(self.message_channel,'You can\'t do that')

	async def function_der(self,content):
		f = Function(content)
		await self.d_client.send_message(self.message_channel,'Disabled')
		return
		try:
			await self.d_client.send_message(self.message_channel, f.der)
		except:
			await self.d_client.send_message(self.message_channel,'Error')

	async def choose_options(self,content):
		things = content.split(', ')
		try:
			if things:
				await self.d_client.send_message(self.message_channel, choice(things))
			else:
				await self.d_client.send_message(self.message_channel, 'No options')
		except:
			await self.d_client.send_message(self.message_channel, 'Empty')

	async def bot_say(self,content):
		await self.d_client.send_message(self.message_channel,content)
		await self.d_client.delete_message(self.message)

	async def clean_message(self,content):
		if at_least_one(self.author_server_permissions,self.words_data[self.message_server_id]['allowed_ranks']) and self.message.content.startswith('$unban word '):
			return False
		for word in content:
			if word in self.words_data[self.message_server_id]['forbidden_words']:
				await self.d_client.delete_message(self.message)
				return True
		return False

	async def change_game(self,content=None):
		if content is None:
			content = '$help'
		elif self.message.author.id != P_ID:
			return
		await self.d_client.change_presence(game=discord.Game(name=content))

	async def urban_dictionary(self,content):
		try:
			text = html_content.process_ud(content)
			await self.d_client.send_message(self.message_channel,'**{}**\n{}'.format(content,text))
		except:
			await self.d_client.send_message(self.message_channel, 'Not found')

	async def jisho(self,content):
		try:
			r = html_content.process_js(content)
			if 'to_kanji' in self.message.content:
				await self.d_client.send_message(self.message_channel, list(r)[0])
			else:
				value = ''
				for i in r:
					for x in r[i]:
						value += x
				await self.d_client.send_message(self.message_channel, value)
		except:
			await self.d_client.send_message(self.message_channel,'Not found')

	async def purge(self,content):
		content = int(content)
		try:
			if content > 100:
				times, extra = divmod(content,100)
				for i in range(times):
					await self.d_client.purge_from(self.message_channel)
				await self.d_client.purge_from(self.message_channel,limit=extra)
			else:
				await self.d_client.purge_from(self.message_channel,limit=content)
		except:
			print("Error with purge")

	async def purge_all(self,*nothing):
		counter = 0
		all_messages = self.d_client.messages
		target_channel = self.message_channel
		for message_step in all_messages:
			if message_step.channel == target_channel:
				self.d_client.delete_message(message_step)



