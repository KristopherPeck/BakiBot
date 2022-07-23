import discord
import sys
import random
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

gameList = [
        ]
        
gameList2 = [
        ]

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='randomgame', help='Randomly picks a game from the server side game list')
    async def randomgame(self, ctx):
        guild = ctx.guild
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if (guild.name == ""):
            response = random.choice(gameList)
            await ctx.send(embed=discord.Embed(description="You should play: " + response, colour=c))
        elif (guild.name == ""):
            response = random.choice(gameList2)
            await ctx.send(embed=discord.Embed(description="You should play: " + response, colour=c))
        else:
            await ctx.send(embed=discord.Embed(description="No list found for this server", colour=c))
        
    @commands.command(name="gamelist")
    async def on_message(self, ctx):
        newList = '**Current Game list**' + '\n'
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        guild = ctx.guild

        if (guild.name == ""):
            for game in gameList:
                newList = newList + '\n' + game
            await ctx.send(embed=discord.Embed(description=newList, colour=c))
        elif (guild.name == ""):
            for game in gameList2:
                newList = newList + '\n' + game
            await ctx.send(embed=discord.Embed(description=newList, colour=c))
        else:
            await ctx.send(embed=discord.Embed(description="No list found for this server", colour=c)) 
        
def setup(bot):
    bot.add_cog(Util(bot))