import json
import discord
from discord.ext import commands
import modules
import time
import os

nyoko = commands.Bot(command_prefix='$',pm_help=True)
CONFIG = json.load(open('config','r'))
LOG_PATH = os.path.join(os.getcwd(), 'Logs')
modules.add_modules(nyoko)
if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

@nyoko.event
async def on_ready():
    print("logged in as")
    print(nyoko.user.name)
    print(nyoko.user.id)
    await nyoko.change_presence(game=discord.Game(name="$help"))

@nyoko.event
async def on_command(ctx):
    #Make log of every command so a user does not make anything "illegal"
    today = time.strftime('%y-%m-%d')
    t_file = os.path.join(LOG_PATH,today)
    command = ctx.command.name

    with open(t_file,'a' if os.path.isfile(t_file) else 'w+',encoding="utf-8") as f:
        f.write(f'{ctx.author.name}({ctx.author.id}) requested {command}'
                f' in {ctx.guild.name}({ctx.guild.id})'
                f' at {time.strftime("%H:%M:%S")}\n\n')


@nyoko.event
async def on_message(message):
    #Banned words management
    fw = nyoko.get_cog('Word').words_data[str(message.guild.id)]['forbidden_words']
    for w in message.content.split():
        if w in fw and message.author.id != message.guild.owner_id:
            return await message.delete()

    await nyoko.process_commands(message)


nyoko.run(CONFIG['tokens']['NYOKO_BOT_TOKEN'])
