import discord
import sys
import random
import os
import os.path
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

heroku_check = os.getenv('HEROKU_CHECK')

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="dmhelp")
    @commands.cooldown(1.0,3.0)
    async def DM(self, ctx):
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if heroku_check == 'False':
            embed=discord.Embed(
                title="General Command List",
                color=c)
            embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
            embed.add_field(name="**color**", value="Pick a random color", inline=False)
            embed.add_field(name="**diceroll**", value="Rolls a die of your choosing. Just like this: !diceroll 20", inline=False)
            embed.add_field(name="**dmhelp**", value="Baki will message you the current help commands", inline=False)
            embed.add_field(name="**eightball or 8ball**", value="Ask the magic 8 Ball a question. Just like this: !eightball Am I going to die tomorrow?", inline=False)
            embed.add_field(name="**findthem**", value="Bakibot will pick someone call mean names", inline=False)
            embed.add_field(name="**gamelist**", value="Shows the current game list for this server. Contact the administrator about updating it.", inline=False)
            embed.add_field(name="**help**", value="Baki will post the current commands in the current channel", inline=False)
            embed.add_field(name="**momir**", value="Generate a random Magic the Gathering creature for use in Momir Basic. Just like this: !momir 1 or !momir 13", inline=False)
            embed.add_field(name="**pokemon**", value="Highlight a specific Pokemon. This can be either the pokedex number or their name. Just like this: !pokemon Mewtwo or !pokemon 150", inline=False)
            embed.add_field(name="**randombaki**", value="Posts a random quote from Baki", inline=False)
            embed.add_field(name="**randomcommander**", value="Pick a random EDH legal Legendary Creature", inline=False)
            embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games for this server", inline=False)
            embed.add_field(name="**randommtg**", value="Pick a random Magic the Gathering card", inline=False)
            embed.add_field(name="**randompokemon**", value="Showcase a random Pokemon. Can be from any generation", inline=False)
            embed.add_field(name="**weather**", value="Get the current weather for a city of your choosing. Just like this: !weather Portage", inline=False)
            embed.add_field(name="**whoisit**", value="Determine who should be called mean names from a list of names", inline=False)
            embed.add_field(name="**xkcd**", value="Posts a random xkcd comic", inline=False)
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

        else:
            embed=discord.Embed(
                title="General Command List",
                color=c)
            embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
            embed.add_field(name="**color**", value="Pick a random color", inline=False)
            embed.add_field(name="**diceroll**", value="Rolls a die of your choosing. Just like this: !diceroll 20", inline=False)
            embed.add_field(name="**dmhelp**", value="Baki will message you the current help commands", inline=False)
            embed.add_field(name="**eightball or 8ball**", value="Ask the magic 8 Ball a question. Just like this: !eightball Am I going to die tomorrow?", inline=False)
            embed.add_field(name="**findthem**", value="Bakibot will pick someone call mean names", inline=False)
            embed.add_field(name="**gamelist**", value="Shows the current game list for this server. Contact the administrator about updating it.", inline=False)
            embed.add_field(name="**help**", value="Baki will post the current commands in the current channel", inline=False)
            embed.add_field(name="**momir**", value="Generate a random Magic the Gathering creature for use in Momir Basic. Just like this: !momir 1 or !momir 13", inline=False)
            embed.add_field(name="**pokemon**", value="Highlight a specific Pokemon. This can be either the pokedex number or their name. Just like this: !pokemon Mewtwo or !pokemon 150", inline=False)
            embed.add_field(name="**randombaki**", value="Posts a random quote from Baki", inline=False)
            embed.add_field(name="**randomcommander**", value="Pick a random EDH legal Legendary Creature", inline=False)
            embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games for this server", inline=False)
            embed.add_field(name="**randommtg**", value="Pick a random Magic the Gathering card", inline=False)
            embed.add_field(name="**randompokemon**", value="Showcase a random Pokemon. Can be from any generation", inline=False)
            embed.add_field(name="**weather**", value="Get the current weather for a city of your choosing. Just like this: !weather Portage", inline=False)
            embed.add_field(name="**whoisit**", value="Determine who should be called mean names from a list of names", inline=False)
            await ctx.author.send(embed=embed)
            
            c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            embed=discord.Embed(
                title="Audio Command List",
                color=c)
            embed.add_field(name="**tts**", value="Have Baki tell everyone what you are really thinking. Just like this: !tts Chicken Butt", inline=False)
            await ctx.author.send(embed=embed)
        
    @commands.command(name="help")
    @commands.cooldown(1.0,3.0)
    async def post(self, ctx):
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if heroku_check == 'False':
            embed=discord.Embed(
                title="General Command List",
                color=c)
            embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
            embed.add_field(name="**color**", value="Pick a random color", inline=False)
            embed.add_field(name="**diceroll**", value="Rolls a die of your choosing. Just like this: !diceroll 20", inline=False)
            embed.add_field(name="**dmhelp**", value="Baki will message you the current help commands", inline=False)
            embed.add_field(name="**eightball or 8ball**", value="Ask the magic 8 Ball a question. Just like this: !eightball Am I going to die tomorrow?", inline=False)
            embed.add_field(name="**findthem**", value="Bakibot will pick someone call mean names", inline=False)
            embed.add_field(name="**gamelist**", value="Shows the current game list for this server. Contact the administrator about updating it.", inline=False)
            embed.add_field(name="**help**", value="Baki will post the current commands in the current channel", inline=False)
            embed.add_field(name="**momir**", value="Generate a random Magic the Gathering creature for use in Momir Basic. Just like this: !momir 1 or !momir 13", inline=False)
            embed.add_field(name="**pokemon**", value="Highlight a specific Pokemon. This can be either the pokedex number or their name. Just like this: !pokemon Mewtwo or !pokemon 150", inline=False)
            embed.add_field(name="**randombaki**", value="Posts a random quote from Baki", inline=False)
            embed.add_field(name="**randomcommander**", value="Pick a random EDH legal Legendary Creature", inline=False)
            embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games for this server", inline=False)
            embed.add_field(name="**randommtg**", value="Pick a random Magic the Gathering card", inline=False)
            embed.add_field(name="**randompokemon**", value="Showcase a random Pokemon. Can be from any generation", inline=False)
            embed.add_field(name="**weather**", value="Get the current weather for a city of your choosing. Just like this: !weather Portage", inline=False)
            embed.add_field(name="**whoisit**", value="Determine who should be called mean names from a list of names", inline=False)
            embed.add_field(name="**xkcd**", value="Posts a random xkcd comic", inline=False)
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

        else:
            embed=discord.Embed(
                title="General Command List",
                color=c)
            embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
            embed.add_field(name="**color**", value="Pick a random color", inline=False)
            embed.add_field(name="**diceroll**", value="Rolls a die of your choosing. Just like this: !diceroll 20", inline=False)
            embed.add_field(name="**dmhelp**", value="Baki will message you the current help commands", inline=False)
            embed.add_field(name="**eightball or 8ball**", value="Ask the magic 8 Ball a question. Just like this: !eightball Am I going to die tomorrow?", inline=False)
            embed.add_field(name="**findthem**", value="Bakibot will pick someone call mean names", inline=False)
            embed.add_field(name="**gamelist**", value="Shows the current game list for this server. Contact the administrator about updating it.", inline=False)
            embed.add_field(name="**help**", value="Baki will post the current commands in the current channel", inline=False)
            embed.add_field(name="**momir**", value="Generate a random Magic the Gathering creature for use in Momir Basic. Just like this: !momir 1 or !momir 13", inline=False)
            embed.add_field(name="**pokemon**", value="Highlight a specific Pokemon. This can be either the pokedex number or their name. Just like this: !pokemon Mewtwo or !pokemon 150", inline=False)
            embed.add_field(name="**randombaki**", value="Posts a random quote from Baki", inline=False)
            embed.add_field(name="**randomcommander**", value="Pick a random EDH legal Legendary Creature", inline=False)
            embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games for this server", inline=False)
            embed.add_field(name="**randommtg**", value="Pick a random Magic the Gathering card", inline=False)
            embed.add_field(name="**randompokemon**", value="Showcase a random Pokemon. Can be from any generation", inline=False)
            embed.add_field(name="**weather**", value="Get the current weather for a city of your choosing. Just like this: !weather Portage", inline=False)
            embed.add_field(name="**whoisit**", value="Determine who should be called mean names from a list of names", inline=False)
            await ctx.send(embed=embed)
            
            c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            embed=discord.Embed(
                title="Audio Command List",
                color=c)
            embed.add_field(name="**tts**", value="Have Baki tell everyone what you are really thinking. Just like this: !tts Chicken Butt", inline=False)
            await ctx.send(embed=embed)   
        
async def setup(bot):
    await bot.add_cog(Basic(bot))
