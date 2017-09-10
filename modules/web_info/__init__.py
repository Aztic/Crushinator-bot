from discord.ext import commands
import discord
from modules.web_info import html_content


class Web_info:

    @commands.command(name="jisho",description="interact with jisho webpage")
    async def jisho(self,ctx,*,word: str):
        try:
            content = html_content.process_js(word)
            kanji = list(content)[0]

            embed = discord.Embed(title="Jisho info", colour=discord.Colour(0xe49fe))
            embed.add_field(name="Kanji",value=kanji)
            embed.add_field(name="Furigana", value=content['furigana'])
            embed.add_field(name="Meaning",value=content[kanji])
            await ctx.send(embed=embed)
        except:
            await ctx.send("Not found")

    @commands.command(name="ud",description="Searchs in Urban Dictionary")
    async def urban_dictionary(self,ctx,*,word:str):
        content = html_content.process_ud(word)
        embed = discord.Embed(title="Urban Dictionary info",colour=discord.Colour(0xc0ffee))
        embed.add_field(name="Word",value=word)
        embed.add_field(name="meaning",value=content)
        await ctx.send(embed=embed)

    @commands.command(name="stando",description="Seachs the stando in jojo wikia")
    async def stand_search(self,ctx,*,stand:str):
        try:
            content = html_content.process_stand(stand)
        except:
            return await ctx.send("Not found")
        if content:
            stats = ''
            for k in content['parameters']:
                stats += f"**{k}: {content['parameters'][k]}**\n"
            embed = discord.Embed(title=stand.title(),colour=discord.Colour(0xe49fe),
                                  description=f"{content['user']}\'s stand")
            embed.set_thumbnail(url=content['thumbnail'])
            if content['appearance'] is not None:
                embed.add_field(name="Appearance",value=content['appearance'])
            embed.add_field(name="Stats",value=stats)
            embed.set_footer(text=content['kanji'])
            await ctx.send(embed=embed)
        else:
            await ctx.send('Not found')
