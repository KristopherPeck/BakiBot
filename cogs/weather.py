import discord
import sys
import random
import requests
import os
import psycopg2
import datetime
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

load_dotenv()
owner_id = os.getenv('DISCORD_OWNERID')
weather_api = os.getenv('WEATHERAPI')
weather_current_forcast_url= "https://api.openweathermap.org/data/2.5/weather?"
weather_icon_url = "https://openweathermap.org/img/wn/"
database_url = os.environ['DATABASE_URL']

def DatabaseLogging(command_name, database_value, user_name, user_id, guild):
    db_conn = psycopg2.connect(database_url, sslmode='require')
    db_cursor = db_conn.cursor()
    now = datetime.datetime.now()
    db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id, guild_id) VALUES (%s, %s, %s, %s, %s, %s)", (command_name, database_value, now, user_name, user_id, guild))
    db_conn.commit()
    db_cursor.close()
    db_conn.close()

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def ownercheck(ctx):
        return ctx.message.author.id == int(owner_id)
    
    @app_commands.command(name='weather', description="Find out the weather at a specified location")
    @app_commands.checks.cooldown(1.0,3.0)
    @app_commands.describe(city="Input the city you wish to get the weather of")
    async def weather(self, interaction: discord.Interaction, city: str):
        #list_to_str = ' '.join([str(elem) for elem in args])
        city_name = city.title()
        complete_url = weather_current_forcast_url + "appid=" + weather_api + "&q=" + city_name
        response = requests.get(complete_url)
        api_response = response.json()
        
        if api_response["cod"] != "404":
            DatabaseLogging("weather", city_name, interaction.user.name, interaction.user.id, interaction.guild_id)
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

            cloud_info = api_response["clouds"]
            cloud_cover = cloud_info["all"]

            try:
                rain_info = api_response["rain"]
                rain_volume = rain_info["1h"]
                rain_volume = str(round(rain_volume / 25.4))
            except: 
                rain_info = 0

            try:
                snow_info = api_response["snow"]
                snow_volume = snow_info["1h"]
                snow_volume = str(round(snow_volume / 25.4))
            except: 
                snow_info = 0

            visibility = api_response["visibility"]
            visibility = round(visibility * 3.280839895)
                
            if visibility > 5280:
                visibility = str(round(visibility * 0.0001893939))
                visibility_mile_indicator = 1
            else:
                visibility = str(visibility)

            weather_description = api_selector_weather[0]["description"]
            weather_description = weather_description.title()
            weather_icon = api_selector_weather[0]["icon"]
            weather_icon = weather_icon_url + weather_icon + "@2x.png"
            c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            embed = discord.Embed(title=f"Weather in {city_name}",
                              color=c)
            embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Cloud Cover", value=f"**{cloud_cover}%**", inline=False)
                                
            if visibility_mile_indicator == 1:
                embed.add_field(name="Visibility (mi)", value=f"**{visibility}mi**", inline=False)
            else:
                embed.add_field(name="Visibility (ft)", value=f"**{visibility}ft**", inline=False)

            embed.add_field(name="Temperature (F)", value=f"**{current_temperature_fahrenheit}°F**", inline=False)
            embed.add_field(name="Feels Like (F)", value=f"**{feels_like_temperature_fahrenheit}°F**", inline=False)
            embed.add_field(name="Wind Speed (mph)", value=f"**{wind_speed}mph**", inline=False)
            embed.add_field(name="Humidity (%)", value=f"**{current_humidity}%**", inline=False)
                
            if rain_info == 0:
                pass
            else:
                embed.add_field(name="Rain Volume (Past Hour - in)", value=f"**{rain_volume}in**", inline=False)

            if snow_info == 0:
                pass
            else:
                embed.add_field(name="Snow Volume (Past Hour - in)", value=f"**{snow_volume}in**", inline=False)

            embed.set_thumbnail(url=weather_icon)
            embed.set_footer(text="Data provided by openweathermap.org.", icon_url="https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png")
            await interaction.response.send_message(embed=embed)
        else:
            DatabaseLogging("weather", city_name, interaction.user.name, interaction.user.id, interaction.guild_id)
            await interaction.response.send_message("City not found.")

async def setup(bot):
    await bot.add_cog(Weather(bot))
