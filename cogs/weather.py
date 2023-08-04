import discord
import sys
import random
import requests
import os
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

load_dotenv()
owner_id = os.getenv('DISCORD_OWNERID')
weather_api = os.getenv('WEATHERAPI')
weather_current_forcast_url= "https://api.openweathermap.org/data/2.5/weather?"
weather_icon_url = "https://openweathermap.org/img/wn/"

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def ownercheck(ctx):
        return ctx.message.author.id == int(owner_id)
    
    @commands.command(name='weather')
    @commands.cooldown(1.0,3.0)
    async def weather(self, ctx, *args):
        list_to_str = ' '.join([str(elem) for elem in args])
        city_name = list_to_str
        city_name = city_name.title()
        complete_url = weather_current_forcast_url + "appid=" + weather_api + "&q=" + city_name
        response = requests.get(complete_url)
        api_response = response.json()
        channel = ctx.message.channel
        
        if api_response["cod"] != "404":
            async with channel.typing():
                api_selector_main = api_response["main"]
                current_temperature = api_selector_main["temp"]
                current_temperature_fahrenheit = str(round(current_temperature * 1.8 - 459.67))
                feels_like_temperature = api_selector_main["feels_like"]
                feels_like_temperature_fahrenheit = str(round(feels_like_temperature * 1.8 - 459.67))
                current_humidity = api_selector_main["humidity"]
                
                api_selector_weather = api_response["weather"]
                wind_info = api_response["wind"]
                wind_speed = wind_info["speed"]
                wind_speed = str(round(wind_speed * 2.2369))
                weather_description = api_selector_weather[0]["description"]
                weather_description = weather_description.title()
                weather_icon = api_selector_weather[0]["icon"]
                weather_icon = weather_icon_url + weather_icon + "@2x.png"
                c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                embed = discord.Embed(title=f"Weather in {city_name}",
                              color=c,
                              timestamp=ctx.message.created_at,)
                embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
                embed.add_field(name="Temperature (F)", value=f"**{current_temperature_fahrenheit}°F**", inline=False)
                embed.add_field(name="Feels Like (F)", value=f"**{feels_like_temperature_fahrenheit}°F**", inline=False)
                embed.add_field(name="Wind Speed (mph)", value=f"**{wind_speed}mph**", inline=False)
                embed.add_field(name="Humidity (%)", value=f"**{current_humidity}%**", inline=False)
                embed.set_thumbnail(url=weather_icon)
                embed.set_footer(text=f"Requested by {ctx.author.name}")
                await channel.send(embed=embed)
        else:
            await channel.send("City not found.")

async def setup(bot):
    await bot.add_cog(Weather(bot))
