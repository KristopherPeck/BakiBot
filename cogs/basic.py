import discord
import sys
import random
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="help")
    async def DM(self, ctx):
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed=discord.Embed(
            title="Command List",
            color=c)
        embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
        embed.add_field(name="**color**", value="Pick a random color", inline=False)
        embed.add_field(name="**diceroll**", value="Rolls a die of your choosing. Just like this: !diceroll 20", inline=False)
        embed.add_field(name="**eightball or 8ball**", value="Ask the magic 8 Ball a question. Just like this: !eightball Am I going to die tomorrow?", inline=False)
        embed.add_field(name="**gamelist**", value="Shows the current game list", inline=False)
        embed.add_field(name="**randombaki**", value="Posts a random quote from Baki", inline=False)
        embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games we own", inline=False)
        embed.add_field(name="**tts**", value="Have Baki tell everyone what you are really thinking. Just like this: !tts Chicken Butt", inline=False)
        embed.add_field(name="**whoisabitch**", value="Determine who is a bitch from a list of names", inline=False)
        await ctx.author.send(embed=embed)
        
    @commands.command(name="tts")
    async def join(self, ctx, *args):
            await ctx.send("Psst! Someone wanted me to tell you: ") 
            await ctx.send(' '.join(args), tts=True)
        
def setup(bot):
    bot.add_cog(Util(bot))