import discord
import sys
import random
import os
import os.path
import psycopg2
import datetime
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

heroku_check = os.getenv('HEROKU_CHECK')
database_url = os.environ['DATABASE_URL']

def DatabaseLogging(command_name, database_value, user_name, user_id, guild):
    db_conn = psycopg2.connect(database_url, sslmode='require')
    db_cursor = db_conn.cursor()
    now = datetime.datetime.now()
    db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id, guild_id) VALUES (%s, %s, %s, %s, %s, %s)", (command_name, database_value, now, user_name, user_id, guild))
    db_conn.commit()
    db_cursor.close()
    db_conn.close()

def genHelp():
    c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    embed=discord.Embed(
        title="Command List",
        color=c)
    embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
    embed.add_field(name="**color**", value="Pick a random color", inline=False)
    embed.add_field(name="**dmhelp**", value="Baki will message you the current help commands", inline=False)
    embed.add_field(name="**eightball**", value="Ask the magic 8 Ball a question. Just like this: /eightball Am I going to die tomorrow?", inline=False)
    embed.add_field(name="**findthem**", value="Bakibot will pick someone call mean names", inline=False)
    embed.add_field(name="**flip**", value="Flip a coin", inline=False)
    embed.add_field(name="**help**", value="Baki will post the current commands in the current channel. You can also use the following prefixes to get specific lists: audio, gen, mtg, pokemon", inline=False)
    embed.add_field(name="**lunchtime**", value="Picks 3 random restaurants from a list for lunchtime.", inline=False)
    embed.add_field(name="**random-baki**", value="Posts a random quote from Baki", inline=False)
    embed.add_field(name="**random-game**", value="Pick a random game from the full list of games for this server", inline=False)
    embed.add_field(name="**rolldice**", value="Roll a set of dice in NdT format with N being the number of dice and T being how many sides are on the dice. Just like this: /rolldice 2d4", inline=False)
    embed.add_field(name="**rolldie**", value="Rolls a die of your choosing. Just like this: /rolldie 20", inline=False)
    embed.add_field(name="**source**", value="Links BakiBots source code.", inline=False)
    embed.add_field(name="**trivia**", value="Posts a random trivia question", inline=False)
    embed.add_field(name="**weather**", value="Get the current weather for a city of your choosing. Just like this: /weather Portage", inline=False)
    embed.add_field(name="**whoisit**", value="Determine who should be called mean names from a list of names", inline=False)
    embed.add_field(name="------------------------------", value="-", inline=False)
    embed.add_field(name="**jhoira**", value="Generate three random instants or sorceries for use in MoJhoSto. Just like this: /jhoira instant or /jhoira sorcery", inline=False)
    embed.add_field(name="**mojhosto**", value="A short explanation of the MoJhoSto format", inline=False)
    embed.add_field(name="**momir**", value="Generate a random Magic the Gathering creature for use in Momir Basic or MoJhoSto. Just like this: /momir 1 or /momir 13", inline=False)
    embed.add_field(name="**mtg**", value="Search a specific Magic the Gathering card. Just like this: /mtg Jace Beleren", inline=False)
    embed.add_field(name="**random-commander**", value="Pick a random EDH legal Legendary Creature", inline=False)
    embed.add_field(name="**random-mtg**", value="Pick a random Magic the Gathering card", inline=False)
    embed.add_field(name="**stonehewer**", value="Generate a random equipment for use in MoJhoSto. Remember that Stonehewer is less than not equal to. Just like this: -stonehewer 3", inline=False)
    embed.add_field(name="------------------------------", value="-", inline=False)
    embed.add_field(name="**pokemon**", value="Highlight a specific Pokemon. This can be either the pokedex number or their name. Just like this: /pokemon Mewtwo or /pokemon 150", inline=False)
    embed.add_field(name="**random-pokemon**", value="Showcase a random Pokemon. Can be from any generation", inline=False)
    return embed

def testHelp():
    c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    embed=discord.Embed(
        title="Command List",
        color=c)
    embed.add_field(name="**color**", value="Pick a random color", inline=False)
    return embed

def AudioHelp_Heroku():
    c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    embed=discord.Embed(
        title="Audio Command List",
        color=c)
    embed.add_field(name="**tts**", value="Have Baki tell everyone what you are really thinking. Just like this: !tts Chicken Butt", inline=False)
    return embed

def AudioHelp_Other():
    c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    embed=discord.Embed(
        title="Audio Command List",
        color=c)
    embed.add_field(name="**join**", value="Baki will join the voice channel you select. Just like this: !join General", inline=False)
    embed.add_field(name="**stop**", value="Stop current Baki stream", inline=False)
    embed.add_field(name="**stream**", value="UNSTABLE: Baki will play you the audio of a youtube video. You have to use !join first. You stream just like this: !stream https://www.youtube.com/watch?v=dQw4w9WgXcQ", inline=False)
    embed.add_field(name="**tts**", value="Have Baki tell everyone what you are really thinking. Just like this: !tts Chicken Butt", inline=False)
    embed.add_field(name="**volume**", value="Set Baki's volume like this: !volume 50", inline=False)
    return embed

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="list-commands", description="Post the list of bot commands")
    @app_commands.checks.cooldown(1.0,3.0)
    async def listcommands(self, interaction: discord.Interaction):
        embed = testHelp()
        DatabaseLogging("list-command", "Listed Commands", interaction.user.name, interaction.user.id, interaction.guild_id)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="whisper-commands", description="Baki wlll whisper the list of bot commands to you")
    @app_commands.checks.cooldown(1.0,3.0)
    async def whispercommands(self, interaction: discord.Interaction):
        embed = testHelp()
        DatabaseLogging("whisper-command", "Whispered Commands", interaction.user.name, interaction.user.id, interaction.guild_id)
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="source", description="Get a link to BakiBot's Github page.")
    @app_commands.checks.cooldown(1.0,3.0)
    async def source(self, interaction: discord.Interaction):
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed = discord.Embed(title="Source Code", description="My source code is over at GitHub! Click the link above to look at it!", url=f"https://github.com/KristopherPeck/BakiBot", color=random_color)

        DatabaseLogging("source", "Posted Source", interaction.user.name, interaction.user.id, interaction.guild_id)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Basic(bot))
