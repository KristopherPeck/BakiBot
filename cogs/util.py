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

bakiQuotes = [
            "You'd do or say anything to save your skin... probably even lick my ass when nobody was looking. -Sikorsky",
            "Now that you've got no more urine left in you... How are you going to get out of this tetrahedron? -Mouth",
            "It seems that in this fight... I won't be able to win this without pissing on myself just a little bit. -Baki Hanma",
            "I started to wish I didn't have any fingers.. because then I could punch all out. My dream just came true. -Doppo 'Tiger Slayer' Orochi",
            "His tuxedo is still there...!! Just like a lesson in shedding your skin!!",
            "What's futile is not realizing the reality of your own futility. One hundred cowards are the same as one. -Yujiro 'The Ogre' Hanma"
        ]

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="help")
    async def DM(self, ctx):
        embed=discord.Embed(
            title="Command List",
            color=discord.Color.blue())
        embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
        embed.add_field(name="**diceroll**", value="Rolls a die of your choosing. Just like this: !diceroll 20", inline=False)
        embed.add_field(name="**gamelist**", value="Shows the current game list", inline=False)
        embed.add_field(name="**randombaki**", value="Posts a random quote from Baki", inline=False)
        embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games we own", inline=False)
        await ctx.author.send(embed=embed)
        
    @commands.command(name='randomgame', help='Randomly picks a game from the server side game list')
    async def randomgame(self, ctx):
        guild = ctx.guild
        if (guild.name == ""):
            response = random.choice(gameList)
            await ctx.send("You should play: " + response)
        elif (guild.name == ""):
            response = random.choice(gameList2)
            await ctx.send("You should play: " + response)
        else:
            await ctx.send("No list found for this server")
        
    @commands.command(name='randombaki')
    async def randombaki(self, ctx):
        response = random.choice(bakiQuotes)
        await ctx.send(response)
        
    @commands.command(name="choose", description="Choose from a list", usage="choose <item1 item2 item3 ... >")
    async def choose(self, ctx, *args):
        response = random.choice(args)
        await ctx.send("Eeny, meeny, miny, moe. I choose: " + response)

    @commands.command(name="gamelist", description="Shows the current game list")
    async def on_message(self, ctx):
        newList = '**Current Game list**' + '\n'
        guild = ctx.guild
        if (guild.name == ""):
            for game in gameList:
                newList = newList + '\n' + game
            await ctx.send(newList)
        elif (guild.name == ""):
            for game in gameList2:
                newList = newList + '\n' + game
            await ctx.send(newList)
        else:
            await ctx.send("No list found for this server")
        
    @commands.command(name="diceroll")
    async def diceroll(self, ctx, arg1):
        arg1 = int(arg1)
        result = random.randint(1, arg1)
        result = str(result)
        await ctx.send("Show me the money!: " + result)
    
def setup(bot):
    bot.add_cog(Util(bot))
