import discord
import sys
import random
import requests
import os
import psycopg2
import datetime
import logging
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

request_timeout = 10

owner_id = os.getenv('DISCORD_OWNERID')
weather_api = os.getenv('WEATHERAPI')
geocoding_url = "https://api.openweathermap.org/geo/1.0/direct"
weather_current_forecast_url= "https://api.openweathermap.org/data/2.5/weather"
weather_icon_url = "https://openweathermap.org/img/wn/"
database_url = os.environ['DATABASE_URL']

def DatabaseLogging(command_name, database_value, user_name, user_id, guild):
    try:
        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.datetime.now()
        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id, guild_id) VALUES (%s, %s, %s, %s, %s, %s)", (command_name, database_value, now, user_name, user_id, guild))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
    except psycopg2.Error as e:
        logger.error(f"Database logging failed: {e}")

def validate_city_input(city: str) -> bool:
    """Validate city input for length and allowed characters."""
    if not city or len(city) > 100:
        return False
    # Allow letters, spaces, hyphens, and apostrophes
    if not all(c.isalpha() or c in " -'" for c in city):
        return False
    return True

def get_city_coordinates(city_name: str) -> dict:
    """Get latitude and longitude for a city using OpenWeatherMap Geocoding API."""
    try:
        params = {
            'q': city_name,
            'limit': 1,
            'appid': weather_api
        }
        response = requests.get(geocoding_url, params=params, timeout=request_timeout, verify=True)
        response.raise_for_status()
        data = response.json()
        
        if len(data) == 0:
            return None
        
        result = data[0]
        return {
            'latitude': result['lat'],
            'longitude': result['lon'],
            'name': result['name'],
            'country': result.get('country', ''),
            'state': result.get('state', '')
        }
    except requests.exceptions.Timeout:
        logger.error(f"Geocoding API timeout for city: {city_name}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding API error: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Invalid geocoding response: {e}")
        return None

def get_weather(latitude: float, longitude: float) -> dict:
    try:
        params = {
            'lat': latitude,
            'lon': longitude,
            'units': 'imperial',
            'appid': weather_api
        }
        response = requests.get(weather_current_forecast_url, params=params, timeout=request_timeout, verify=True)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.error(f"Weather API timeout for coordinates: {latitude}, {longitude}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API error: {e}")
        return None
    except ValueError as e:
        logger.error(f"Invalid weather response: {e}")
        return None

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def ownercheck(ctx):
        return ctx.message.author.id == int(owner_id)
    
    @app_commands.command(name='weather', description="Find out the weather at a specified location")
    @app_commands.checks.cooldown(1.0,3.0)
    @app_commands.describe(city="Input the city you wish to get the weather of")
    async def weather(self, interaction: discord.Interaction, city: str):
        if not validate_city_input(city):
            await interaction.response.send_message("Invalid city name. Please use only letters, spaces, hyphens, and apostrophes (max 100 characters).")
            return
        
        try:
            city_coords = get_city_coordinates(city)
            if not city_coords:
                await interaction.response.send_message("City not found. Please try another location.")
                DatabaseLogging("weather", city, interaction.user.name, interaction.user.id, interaction.guild_id)
                return
        
            weather_data = get_weather(city_coords['latitude'], city_coords['longitude'])
            if not weather_data:
                await interaction.response.send_message("Unable to fetch weather data. Please try again later.")
                DatabaseLogging("weather", city, interaction.user.name, interaction.user.id, interaction.guild_id)
                return
            
        except requests.exceptions.Timeout:
            logger.error(f"Weather API timeout for city: {city}")
            await interaction.response.send_message("Weather service timed out. Please try again.")
            return
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {e}")
            await interaction.response.send_message("Unable to fetch weather data. Please try again later.")
            return
        except ValueError as e:
            logger.error(f"Invalid JSON response: {e}")
            await interaction.response.send_message("Weather service returned invalid data.")
            return
        
        if weather_data.get("cod") != "200":
            DatabaseLogging("weather", city, interaction.user.name, interaction.user.id, interaction.guild_id)
            await interaction.response.send_message("City not found.")
            return
        
        try: 
            api_selector_main = weather_data["main"]
            current_temperature = api_selector_main["temp"]
            feels_like_temperature = api_selector_main["feels_like"]
            current_humidity = api_selector_main["humidity"]
                
            api_selector_weather = weather_data["weather"]
            wind_info = weather_data["wind"]
            wind_speed = wind_info["speed"]

            cloud_info = weather_data["clouds"]
            cloud_cover = cloud_info["all"]

            try:
                rain_info = weather_data["rain"]
                rain_volume = rain_info["1h"]
            except (KeyError, TypeError):  
                rain_info = 0

            try:
                snow_info = weather_data["snow"]
                snow_volume = snow_info["1h"]
            except (KeyError, TypeError):  
                snow_info = 0

            try:
                visibility = weather_data["visibility"]
            except (KeyError, TypeError): 
                visibility = 0
                
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
            embed = discord.Embed(title=f"Weather in {city}", color=c)
            embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Cloud Cover", value=f"**{cloud_cover}%**", inline=False)
                                
            if visibility_mile_indicator == 1:
                embed.add_field(name="Visibility (mi)", value=f"**{visibility}mi**", inline=False)
            else:
                embed.add_field(name="Visibility (ft)", value=f"**{visibility}ft**", inline=False)

            embed.add_field(name="Temperature (F)", value=f"**{current_temperature}°F**", inline=False)
            embed.add_field(name="Feels Like (F)", value=f"**{feels_like_temperature}°F**", inline=False)
            embed.add_field(name="Wind Speed (mph)", value=f"**{wind_speed}mph**", inline=False)
            embed.add_field(name="Humidity (%)", value=f"**{current_humidity}%**", inline=False)
                
            if rain_info != 0:
                embed.add_field(name="Rain Volume (Past Hour - in)", value=f"**{rain_volume}in**", inline=False)

            if snow_info != 0:
                embed.add_field(name="Snow Volume (Past Hour - in)", value=f"**{snow_volume}in**", inline=False)

            embed.set_thumbnail(url=weather_icon)
            embed.set_footer(text="Data provided by openweathermap.org.", icon_url="https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png")

            DatabaseLogging("weather", city, interaction.user.name, interaction.user.id, interaction.guild_id)

            await interaction.response.send_message(embed=embed)
            
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error parsing weather response: {e}")
            await interaction.response.send_message("Error processing weather data. Please try again.")

        except Exception as e:
            logger.error(f"Unexpected error in weather command: {e}")
            await interaction.response.send_message("An unexpected error occurred.")

async def setup(bot):
    await bot.add_cog(Weather(bot))
