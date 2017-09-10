from discord.ext import commands
import json
import discord

class Word:
    def __init__(self):
        self.words_data = json.load(open('words','r'))

    def at_least_one(self,List_a, List_b):
        for value in List_a:
            if value in List_b:
                return True
        return False

    @commands.command(name="set_role")
    async def set_role(self,ctx):
        if str(ctx.guild.id) not in self.words_data:
            #Create guild info, master role and append it to allowed ranks array
            role_master = await ctx.guild.create_role(name='Word master')
            self.words_data[str(ctx.guild.id)] = {'allowed_ranks':[role_master.id],'forbidden_words':[]}
            with open('words','w') as wd:
                json.dump(self.words_data,wd)
            await ctx.send("Role \"Word Master\" created, please assign it to someone")
        else:
            await ctx.send("Role already created")

    @commands.command(name="ban_word")
    async def ban_word(self,ctx,*,word: str):
        if str(ctx.guild.id) not in self.words_data:
            await ctx.send("First create the role and assign it to someone")
        author_roles = ctx.author.roles
        author_roles = [i.id for i in author_roles]
        if self.at_least_one(author_roles,self.words_data[str(ctx.guild.id)]['allowed_ranks']):
            if word not in self.words_data[str(ctx.guild.id)]['forbidden_words']:
                self.words_data[str(ctx.guild.id)]['forbidden_words'].append(word)
                await ctx.send("Done")
                json.dump(self.words_data,open('words','w'))
            else:
                await ctx.send("Already banned")
        else:
            await ctx.send("You can\'t do that")

    @commands.command(name="allow_role",)
    async def allow_role(self,ctx,*,role: str):
        author_roles = ctx.author.roles
        author_roles = [i.id for i in author_roles]
        if self.at_least_one(author_roles,self.words_data[str(ctx.guild.id)]['allowed_ranks']):
            server_roles = ctx.guild.roles
            role_names = [i.name.lower() for i in server_roles]
            role_index = role_names.index(role)
            if role_index > -1:
                self.words_data[str(ctx.guild.id)]['allowed_ranks'].append(server_roles[role_index].id)
                await ctx.send("Done")
            else:
                await ctx.send("Can\'t find the role")
        else:
            await ctx.send("You can\'t do that")

    @commands.command(name="banned_words")
    async def banned_words(self,ctx):
        if str(ctx.guild.id) in self.words_data and self.words_data[str(ctx.guild.id)]['forbidden_words']:
            embed = discord.Embed(title="Banned words",colour=discord.Colour(0xFF0000))
            embed.add_field(name="Words",value="\n".join(self.words_data[str(ctx.guild.id)]['forbidden_words']))
            await ctx.send(embed=embed)
        else:
            await ctx.send("No banned words")

    @commands.command(name="see_ban_permissions")
    async def ban_permissions(self,ctx):
        if str(ctx.guild.id) in self.words_data:
            #Get server roles
            server_roles = ctx.guild.roles
            #Server roles ids
            roles_id = [i.id for i in server_roles]
            roles = []
            #Append server roles names
            for r in self.words_data[str(ctx.guild.id)]['allowed_ranks']:
                roles.append(server_roles[roles_id.index(r)].name)
            embed = discord.Embed(title="Ban word permissions")
            embed.add_field(name="Roles",value="\n".join(roles))
            await ctx.send(embed=embed)
        else:
            await ctx.send("No roles allowed to ban words")


    @commands.command(name="unban_word")
    async def unban_word(self,ctx,*,word:str):
        author_roles = ctx.author.roles
        author_roles = [i.id for i in author_roles]
        if self.at_least_one(author_roles, self.words_data[str(ctx.guild.id)]['allowed_ranks']):
            if str(ctx.guild.id) in self.words_data:
                found = False
                if word in self.words_data[str(ctx.guild.id)]['forbidden_words']:
                    found = True
                    self.words_data[str(ctx.guild.id)]['forbidden_words'].remove(word)
                    json.dump(self.words_data,open('words','w'))
                return await ctx.send("Done" if found else "That words is not banned")
        else:
            return ctx.send("You can\'t do that")