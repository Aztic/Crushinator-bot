from discord.ext import commands
from modules.anilist import anime_search
from modules.anilist import character_search
from modules.anilist import next_anime
from anilist import AniList
import urllib.request
import os
import json
import discord


with open('config','r') as config:
    configf = json.load(config)
    CLIENT_ID = configf['tokens']['ANILIST_CLIENT_ID']
    CLIENT_SECRET = configf['tokens']['ANILIST_CLIENT_SECRET']

class Anilist:
    def __init__(self,bot):
        self.client = AniList(client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
        self.character_path = os.path.join(os.getcwd(), "Images/Characters/")
        self.bot = bot


    @commands.group(name="anilist")
    async def anilist(self,ctx):
        pass

    @anilist.command(name="next_episode",description="search the next episode of selected anime")
    async def next_episode(self,ctx,*,anime:str):
        path = "anime/search/" + anime.lower()
        try:
            an_id = next_anime.search_thing(anime.lower(), path, self.client)
            if an_id is None:
                # Split the anime name in separated words
                split_search = [i.lower() for i in anime.split()]
                an_id = next_anime.splitted_search(split_search, path, self.client)
            if an_id == -1:
                await ctx.send(f"{anime} is not airing")
            elif not an_id:
                await ctx.send("Not found")
            else:
                print("doing time things")
                episode_data = next_anime.search_with_id(an_id,self.client)
                secs = episode_data[0]
                data = next_anime.date_things(secs,False,anime,True)
                order = ['day', 'hour', 'minute', 'second']
                output = ''
                for ord in order:
                    if data[ord] != '0':
                        output += f'{data[ord]} {ord}'
                        output += 's ' if int(data[ord]) > 1 else ' '
                await ctx.send(f"{output}until episode {episode_data[1]}")
        except:
            await ctx.send("Not found")

    @anilist.command(name="anime")
    async def anime(self,ctx,*,name:str):
        path = 'anime/search/'+name.lower()
        url = self.find_url(path, name.lower())
        await ctx.send(url if url else "Not found")

    @anilist.command(name="manga")
    async def manga(self,ctx,*,name:str):
        path = 'manga/search/'+name.lower()
        url = self.find_url(path,name.lower())
        await ctx.send(url if url else 'Not found')

    def find_url(self,path,name):
        try:
            url = anime_search.search_thing(name,path,self.client)
            if not url:
                url = anime_search.splitted_search([i.lower() for i in name.split()],path,self.client)
        except:
            url = ''

        return url

    @anilist.command(name="character")
    async def character_search(self,ctx,*,name:str):
        result = character_search.search_character(name.lower(),self.client)
        if not result:
            return await ctx.send("Not found")

        #Select the character
        if len(result) > 1:
            all_c = ['{} {}'.format(i['name_first'], i['name_last']) if i['name_last'] else i['name_first'] for i in
                     result]
            characters = ''
            for i, value in enumerate(all_c):
                characters += '{}: {}\n'.format(i + 1, value)
            await ctx.send("Which {}?\n{}".format(name, characters))
            author = ctx.author
            channel = ctx.message.channel

            def check(m):
                return m.author == author and m.channel == channel

            option = await self.bot.wait_for('message',check=check,timeout=60.0)
            if not option:
                return await ctx.send("Timeout")
            if int(option.content) - 1 not in range(len(all_c)):
                return await ctx.send("Invalid option")
            else:
                character = result[int(option.content) - 1]
        else:
            character = result[0]
        file = urllib.request.urlopen(
            urllib.request.Request(character['image_url_lge'], headers={'User-Agent': 'characters/0.0.0'})).read()
        extension = character['image_url_lge'].split('.')[-1]
        try:
            await ctx.send(f'{character_search.display_info(character)}',
                           file=discord.File(file,f'{name}.{extension}'))
        except:
            await ctx.send(f'{character_search.simple_display(character)}',
                                       file=discord.File(file, f'{name}.{extension}'))
