from discord.ext import commands
import json
from modules.weather import weather_client

class Weather:
    def __init__(self):
        self.weather_data = json.load(open('weathers','r'))
        self.token = json.load(open('config','r'))['tokens']['OPENWEATHER_API_KEY']
        self.client = weather_client.Weather(self.token)

    def kelvin_to_celsius(self,kelvin):
        return kelvin - 273.15

    def kelvin_to_fahrenheit(self,kelvin):
        return kelvin * 9 / 5 - 459.67

    def load_weather(self,location):
        try:
            req = self.client.get(location)
            celcius = f"{self.kelvin_to_celsius(req['main']['temp']):.2f}"
            fahrenheit = f"{self.kelvin_to_fahrenheit(req['main']['temp']):.2f}"
            desc = req['weather'][0]['description']
            wind = req['wind']['speed']
            to_print = f"**{location}** \n {celcius} C {fahrenheit} F\n {desc} \n Wind: {wind} m/s"
            return to_print
        except:
            return "Can\'t find the location"

    @commands.group(name="weather")
    async def weather(self,ctx,*,place: str):
        #Check if is user has some weather saved
        if ctx.invoked_subcommand is None:
            if ctx.author.id not in self.weather_data and place is None:
                await ctx.send("Please, first save any weather")
            else:
                if place is None:
                    place = self.weather_data[ctx.author.id]
                await ctx.send(self.load_weather(place))


    @weather.command(name="save")
    async def save_weather(self,ctx,*,location: str):
        self.weather_data[ctx.author.id] = location
        json.dump(self.weather_data, open('weathers', 'w'))
        await ctx.send('Saved Successfully')
