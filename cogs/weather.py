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
database_url = os.environ['DATABASE_URL']

# Open-Meteo API endpoints (no API key required)
geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
weather_url = "https://api.open-meteo.com/v1/forecast"

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
    # Allow letters, spaces, hyphens, apostrophes, and commas
    if not all(c.isalpha() or c in " -'," for c in city):
        return False
    return True

def get_city_coordinates(city_input: str) -> dict:
    """Get latitude and longitude for a city using Open-Meteo Geocoding API.
    
    Supports formats like:
    - "Portland"
    - "Portland, Oregon"
    - "Portland, Oregon, USA"
    """
    try:
        # Parse input to separate city, state, country
        parts = [p.strip() for p in city_input.split(',')]
        
        params = {
            'name': parts[0],  # City name (required)
            'count': 5,  # Get top 5 results to pick the best match
            'language': 'en',
            'format': 'json'
        }
        
        # Add state if provided
        if len(parts) > 1:
            params['state'] = parts[1]
        
        # Add country if provided
        if len(parts) > 2:
            params['country'] = parts[2]
        
        response = requests.get(geocoding_url, params=params, timeout=request_timeout, verify=True)
        response.raise_for_status()
        data = response.json()
        
        if 'results' not in data or len(data['results']) == 0:
            return None
        
        # If user specified state/country, try to find exact match
        result = data['results'][0]
        if len(parts) > 1:
            # Look for a result that matches the state
            for r in data['results']:
                if r.get('admin1') and parts[1].lower() in r.get('admin1', '').lower():
                    result = r
                    break
        
        return {
            'latitude': result['latitude'],
            'longitude': result['longitude'],
            'name': result['name'],
            'country': result.get('country', ''),
            'admin1': result.get('admin1', '')
        }
    except requests.exceptions.Timeout:
        logger.error(f"Geocoding API timeout for city: {city_input}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding API error: {e}")
        return None
    except (KeyError, ValueError, IndexError) as e:
        logger.error(f"Invalid geocoding response: {e}")
        return None

def get_weather(latitude: float, longitude: float) -> dict:
    """Get current weather data using Open-Meteo Weather API."""
    try:
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,cloud_cover',
            'temperature_unit': 'fahrenheit',
            'wind_speed_unit': 'mph',
            'timezone': 'auto'
        }
        response = requests.get(weather_url, params=params, timeout=request_timeout, verify=True)
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

def get_weather_description(code: int) -> str:
    """Convert WMO weather code to human-readable description."""
    wmo_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return wmo_codes.get(code, "Unknown conditions")

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def ownercheck(ctx):
        return ctx.message.author.id == int(owner_id)
    
    @app_commands.command(name='weather', description="Find out the weather at a specified location")
    @app_commands.checks.cooldown(1.0, 3.0)
    @app_commands.describe(city="Input the city you wish to get the weather of")
    async def weather(self, interaction: discord.Interaction, city: str):
        if not validate_city_input(city):
            await interaction.response.send_message("Invalid city name. Please use only letters, spaces, hyphens, and apostrophes (max 100 characters).")
            return
        
        # Get coordinates for the city
        city_coords = get_city_coordinates(city)
        if not city_coords:
            await interaction.response.send_message("City not found. Please try another location.")
            DatabaseLogging("weather", city, interaction.user.name, interaction.user.id, interaction.guild_id)
            return
        
        # Get weather data
        weather_data = get_weather(city_coords['latitude'], city_coords['longitude'])
        if not weather_data:
            await interaction.response.send_message("Unable to fetch weather data. Please try again later.")
            DatabaseLogging("weather", city, interaction.user.name, interaction.user.id, interaction.guild_id)
            return
        
        try:
            current = weather_data['current']
            temperature = current['temperature_2m']
            humidity = current['relative_humidity_2m']
            wind_speed = current['wind_speed_10m']
            cloud_cover = current['cloud_cover']
            weather_code = current['weather_code']
            weather_description = get_weather_description(weather_code)
            
            # Build location string
            location = city_coords['name']
            if city_coords.get('admin1'):
                location += f", {city_coords['admin1']}"
            if city_coords.get('country'):
                location += f", {city_coords['country']}"
            
            # Create embed
            c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            embed = discord.Embed(title=f"Weather in {location}", color=c)
            embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature (°F)", value=f"**{temperature}°F**", inline=False)
            embed.add_field(name="Humidity (%)", value=f"**{humidity}%**", inline=False)
            embed.add_field(name="Wind Speed (mph)", value=f"**{wind_speed} mph**", inline=False)
            embed.add_field(name="Cloud Cover (%)", value=f"**{cloud_cover}%**", inline=False)
            embed.set_footer(text="Data provided by Open-Meteo.com")
            
            DatabaseLogging("weather", location, interaction.user.name, interaction.user.id, interaction.guild_id)
            await interaction.response.send_message(embed=embed)
            
        except (KeyError, TypeError) as e:
            logger.error(f"Error parsing weather response: {e}")
            await interaction.response.send_message("Error processing weather data. Please try again.")
        except Exception as e:
            logger.error(f"Unexpected error in weather command: {e}")
            await interaction.response.send_message("An unexpected error occurred.")

async def setup(bot):
    await bot.add_cog(Weather(bot))