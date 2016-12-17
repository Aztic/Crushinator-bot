import bot
import os
BOT_TOKEN = os.getenv('CRUSHINATOR_BOT_TOKEN')
Crushinator = bot.Bot(BOT_TOKEN)


@Crushinator.event
async def on_ready():
	print('Logged in as')
	print(Crushinator.d_client.user.name)
	print(Crushinator.d_client.user.id)
	print('------')
	Crushinator.d_client.change_presence(game=bot.discord.Game(name='$help'))


@Crushinator.event
async def on_message(message):
	await Crushinator.process_message(message)

Crushinator.run_bot()