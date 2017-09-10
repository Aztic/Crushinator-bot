from discord.ext import commands
import urllib.request
import requests
import json
from urllib.parse import urlparse

class Tag:
    def __init__(self,bot):
        self.prefix = bot.command_prefix
        self.tag_data = json.load(open('tags','r'))
        self.supported_formats = ['jpg', 'jpeg', 'gif', 'png', 'bmp']
        self.pomf_url = "https://pomf.onigiri.com.ve/upload"

    @commands.group(name="tag",description="All aboot tags m8")
    async def tag(self,ctx):
        #send tag
        if ctx.invoked_subcommand is None:
            content = ctx.message.content.split(self.prefix + 'tag ')[-1]
            if str(ctx.guild.id) in self.tag_data and content in self.tag_data[str(ctx.guild.id)]:
                await ctx.send(self.tag_data[str(ctx.guild.id)][content])
            else:
                await ctx.send("invalid tag")


    #Save the desired tag, either a uploaded file or url/text
    @tag.command(name="save",description="Saves a tag in the server")
    async def save(self,ctx):
        #Create the server data if required
        if str(ctx.guild.id) not in self.tag_data:
            self.tag_data[str(ctx.guild.id)] = {}

        #Split the message
        splitted = ctx.message.content.split("tag save ")[-1].split("\" ")
        splitted[0] = splitted[0].replace("\"",'')

        #Attachments > url
        if not ctx.message.attachments:
            tag_name,tag = splitted
        else:
            tag_name = splitted[0]
            tag = ctx.message.attachments[0].url


        parse = urlparse(tag)
        #Check if is a valid filetype and a url
        if parse.scheme and parse.path.split('.')[-1] in self.supported_formats:
            name = parse.path.split('/')[-1]
            file = urllib.request.urlopen(urllib.request.Request(tag, headers={'User-Agent': 'image_save/0.0.0'}))
            files = {'files[]': (name, file)}
            r =requests.post(self.pomf_url,files=files)
            #If the upload was gud
            if r.json()['success']:
                self.tag_data[str(ctx.guild.id)][tag_name] = r.json()['files'][0]['url']
            else:
                await ctx.send("error, can\'t upload")
                return
        else:
            self.tag_data[str(ctx.guild.id)][tag_name] = tag

        json.dump(self.tag_data, open('tags', 'w'))
        await ctx.send("success")

    #Show all tags
    @tag.command()
    async def list(self,ctx):
        #Check if not a pm and if the guild has any tag saved
        if ctx.guild.id is not None and str(ctx.guild.id) in self.tag_data:
            await ctx.send(', '.join(list(self.tag_data[str(ctx.guild.id)])))
        else:
            await ctx.send("no tags saved")
