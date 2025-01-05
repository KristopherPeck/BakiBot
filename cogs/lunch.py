import discord
import sys
import random
import html
import requests
import requests_cache
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

restaurant_choices = [
            "Penn Station", "Sakura", "Kumo Hibachi", "Z&W Chinese Cuisine", "Two Fellas Grill", "Red Robin", "Five Guys", "Buffalo Wild Wings", "Olgas", "Logans", "Applebees",
            "Kelvin and Co", "City BBQ", "Bob Evans", "Taco Bell", "Berries", "Firehouse Subs", "Long John Silvers", "Red Lobster", "Chilis", "Jersey Mikes", "Chinese Buffet", "Lees",
            "Mcallisters", "Burger King", "Arbys", "McDonalds", "Wendys", "Angelos", "Chipotle", "Qdoba", "Los Amigos", "Olive Garden", "Culvers", "Main Street Pub", "Monellis", "Steak n Shake",
            "Lake Tavern", "East Egg", "Mike's Diner", "IHOP"
        ]

class Random(commands.Cog):
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
        temporary_restaurant_choices = restaurant_choices

        response1 = random.choice(restaurant_choices)
        temporary_restaurant_choices.remove(response1)

        response2 = random.choice(restaurant_choices)
        temporary_restaurant_choices.remove(response2)
        
        response3 = random.choice(restaurant_choices)
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="Your choices for lunch are " + response1 + ", " + response2 + " or " + response3 + "!", colour=random_color))

async def setup(bot):
    await bot.add_cog(Random(bot))
