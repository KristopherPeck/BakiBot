import discord
import sys
import random
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="help")
    async def DM(self, ctx):
        #This help command sends a direct message to the user who requested it.
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed=discord.Embed(
            title="General Command List",
            color=c)
        embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
        embed.add_field(name="**color**", value="Pick a random color", inline=False)
        embed.add_field(name="**diceroll**", value="Rolls a die of your choosing. Just like this: !diceroll 20", inline=False)
        embed.add_field(name="**eightball or 8ball**", value="Ask the magic 8 Ball a question. Just like this: !eightball Am I going to die tomorrow?", inline=False)
        embed.add_field(name="**gamelist**", value="Shows the current game list for this server. Contact the administrator about updating it.", inline=False)
        embed.add_field(name="**help**", value="Baki will message you the current help commands", inline=False)
        embed.add_field(name="**pickapokemon**", value="Highlight a specific Pokemon. This can be either the pokedex number or their name. Just like this: !pickapokemon Mewtwo or !pickapokemon 150", inline=False)
        embed.add_field(name="**posthelp**", value="Baki will post the current commands in the current channel", inline=False)
        embed.add_field(name="**randombaki**", value="Posts a random quote from Baki", inline=False)
        embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games for this server", inline=False)
        embed.add_field(name="**randompokemon**", value="Showcase a random Pokemon. Can be from any generation", inline=False)
        embed.add_field(name="**weather**", value="Get the current weather for a city of your choosing. Just like this: !weather Portage", inline=False)
        await ctx.author.send(embed=embed)
        
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed=discord.Embed(
            title="Audio Command List",
            color=c)
        embed.add_field(name="**join**", value="Baki will join the voice channel you select. Just like this: !join General", inline=False)
        embed.add_field(name="**stop**", value="Stop current Baki stream", inline=False)
        embed.add_field(name="**stream**", value="UNSTABLE: Baki will play you the audio of a youtube video. You have to use !join first. You stream just like this: !stream https://www.youtube.com/watch?v=dQw4w9WgXcQ", inline=False)
        embed.add_field(name="**tts**", value="Have Baki tell everyone what you are really thinking. Just like this: !tts Chicken Butt", inline=False)
        embed.add_field(name="**volume**", value="Set Baki's volume like this: !volume 50", inline=False)
        await ctx.author.send(embed=embed)
        
    @commands.command(name="posthelp")
    async def post(self, ctx):
        #This help command posts directly to the current channel
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed=discord.Embed(
            title="General Command List",
            color=c)
        embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
        embed.add_field(name="**color**", value="Pick a random color", inline=False)
        embed.add_field(name="**diceroll**", value="Rolls a die of your choosing. Just like this: !diceroll 20", inline=False)
        embed.add_field(name="**eightball or 8ball**", value="Ask the magic 8 Ball a question. Just like this: !eightball Am I going to die tomorrow?", inline=False)
        embed.add_field(name="**gamelist**", value="Shows the current game list for this server. Contact the administrator about updating it.", inline=False)
        embed.add_field(name="**help**", value="Baki will message you the current help commands", inline=False)
        embed.add_field(name="**pickapokemon**", value="Highlight a specific Pokemon. This can be either the pokedex number or their name. Just like this: !pickapokemon Mewtwo or !pickapokemon 150", inline=False)
        embed.add_field(name="**posthelp**", value="Baki will post the current commands in the current channel", inline=False)
        embed.add_field(name="**randombaki**", value="Posts a random quote from Baki", inline=False)
        embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games for this server", inline=False)
        embed.add_field(name="**randompokemon**", value="Showcase a random Pokemon. Can be from any generation", inline=False)
        embed.add_field(name="**weather**", value="Get the current weather for a city of your choosing. Just like this: !weather Portage", inline=False)
        await ctx.send(embed=embed)
        
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed=discord.Embed(
            title="Audio Command List",
            color=c)
        embed.add_field(name="**join**", value="Baki will join the voice channel you select. Just like this: !join General", inline=False)
        embed.add_field(name="**stop**", value="Stop current Baki stream", inline=False)
        embed.add_field(name="**stream**", value="UNSTABLE: Baki will play you the audio of a youtube video. You have to use !join first. You stream just like this: !stream https://www.youtube.com/watch?v=dQw4w9WgXcQ", inline=False)
        embed.add_field(name="**tts**", value="Have Baki tell everyone what you are really thinking. Just like this: !tts Chicken Butt", inline=False)
        embed.add_field(name="**volume**", value="Set Baki's volume like this: !volume 50", inline=False)
        await ctx.send(embed=embed)   
        
async def setup(bot):
    await bot.add_cog(Basic(bot))
