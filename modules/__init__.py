from modules.tags import Tag
from modules.weather import Weather
from modules.web_info import Web_info
from modules.anilist import Anilist
from modules.words import Word

def add_modules(bot):
    bot.add_cog(Tag(bot))
    bot.add_cog(Weather())
    bot.add_cog(Web_info())
    bot.add_cog(Anilist(bot))
    bot.add_cog(Word())
