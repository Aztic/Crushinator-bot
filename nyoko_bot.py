import bot
import asyncio
Nyoko = bot.Bot(Command_Prefix='$',Tag_Prefix='&')


@Nyoko.event
async def on_ready():
	print('Logged in as')
	print(Nyoko.d_client.user.name)
	print(Nyoko.d_client.user.id)
	print('------')
	await Nyoko.change_game()


@Nyoko.event
async def on_message(message):
	await Nyoko.process_message(message)

Nyoko.run_bot()
