import discord
import sys
import random
import os
import os.path
import html
import requests
import requests_cache
import psycopg2
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

database_url = os.environ['DATABASE_URL']

restaurant_choices = [
            "Penn Station (M-Su)", 
            "Sakura (M-Su)", 
            "Kumo Hibachi (M-Su)", 
            "Z&W Chinese Cuisine (Tu-Su)", 
            "Two Fellas Grill (M-Su)", 
            "Red Robin (M-Su)", 
            "Five Guys (M-Su)", 
            "Buffalo Wild Wings (M-Su)", 
            "Olgas (M-Su)", 
            "Applebees (M-Su)",
            "City BBQ (M-Su)", 
            "Bob Evans (M-Su)", 
            "Taco Bell (M-Su)", 
            "Berries (M-Su)", 
            "Firehouse Subs (M-Su)", 
            "Long John Silvers (M-Su)", 
            "Red Lobster (M-Su)", 
            "Chilis (M-Su)", 
            "Jersey Mikes (M-Su)", 
            "Chinese Buffet (M-Su)", 
            "Lees (M-Su)",
            "Mcallisters (M-Su)", 
            "Burger King (M-Su)", 
            "Arbys (M-Su)", 
            "McDonalds (M-Su)", 
            "Wendys (M-Su)", 
            "Angelos (M-F)", 
            "Chipotle (M-Su)", 
            "Qdoba (M-Su)", 
            "Los Amigos (M-Su)", 
            "Olive Garden (M-Su)", 
            "Culvers (M-Su)", 
            "Main Street Pub (M-Su)", 
            "Monellis (M-Su)", 
            "Steak n Shake (M-Su)",
            "Lake Tavern (Tu-Su)", 
            "East Egg (W-S)", 
            "Mark's Diner (M-Su)", 
            "IHOP (M-Su)", 
            "The Rooster's Call (M-Su)",
            "Root Beer Stand (M-Su Summer)",
            "Dak Good (M-Su)"
        ]

class lunch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lunchtime")
    @commands.cooldown(1.0,3.0)
    async def lunchtime(self, ctx):
        response = random.choice(restaurant_choices)
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="It's time for " + response + "!", colour=random_color))

    @commands.command(name="lunchtimex2")
    @commands.cooldown(1.0,3.0)
    async def lunchtimex2(self, ctx):
        temporary_restaurant_choices = restaurant_choices

        response1 = random.choice(temporary_restaurant_choices)
        temporary_restaurant_choices.remove(response1)

        response2 = random.choice(temporary_restaurant_choices)
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="Your choices for lunch are " + response1 + " or " + response2 + "!", colour=random_color))

    @commands.command(name="lunchtimex3")
    @commands.cooldown(1.0,3.0)
    async def lunchtimex3(self, ctx):

        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.now()
        day_of_week = str(datetime.strftime(now, "%A"))
        db_cursor.execute("select * from bakibot.lunch_options where %s != 0 order by RANDOM() limit 3", (day_of_week, ))
        sql_results = db_cursor.fetchall()
        print (sql_results)
        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp) VALUES (%s, %s, %s)", ("lunchtimex3", sql_results, now))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()

        temporary_restaurant_choices = restaurant_choices

        response1 = random.choice(restaurant_choices)
        temporary_restaurant_choices.remove(response1)

        response2 = random.choice(restaurant_choices)
        temporary_restaurant_choices.remove(response2)
        
        response3 = random.choice(restaurant_choices)
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="Your choices for lunch are " + response1 + ", " + response2 + " or " + response3 + "!", colour=random_color))

async def setup(bot):
    await bot.add_cog(lunch(bot))
