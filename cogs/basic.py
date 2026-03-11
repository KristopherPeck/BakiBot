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

def testHelp():
    c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    general_command_list_part_one = '''
                   **color**: Pick a random color\n
                   **eightball**: Ask the magic 8 Ball a question. Just like this: /eightball Am I going to die tomorrow?\n
                   **findthem**: Bakibot will pick someone call mean names\n
                   **flip**: Flip a coin\n
                   **lunchtime**: Picks 3 random restaurants from a list for lunchtime\n
                   **random-baki**: Posts a random quote from Baki\n
                   **random-game**: Pick a random game from the full list of games for this server\n
                   '''
    
    general_command_list_part_two = '''
                   **rolldice**: Roll a set of dice in NdT format with N being the number of dice and T being how many sides are on the dice. Just like this: /rolldice 2d4\n
                   **rolldie**: Rolls a die of your choosing. Just like this: /rolldie 20\n
                   **source**: Links BakiBots source code\n
                   **trivia**: Posts a random trivia question\n
                   **weather**: Get the current weather for a city of your choosing. Just like this: /weather Portage\n
                   **whoisit**: Determine who should be called mean names from a list of names\n
                   '''
    
    pokemon_command_list = '''
                           **pokemon**: Highlight a specific Pokemon. This can be either the pokedex number or their name. Just like this: /pokemon Mewtwo or /pokemon 150\n
                           **random-pokemon**: Showcase a random Pokemon. Can be from any generation\n
                           '''
    
    mtg_command_list = '''
                           **jhoira**: Generate three random instants or sorceries for use in MoJhoSto. Just like this: /jhoira instant or /jhoira sorcery\n
                           **mojhosto**: A short explanation of the MoJhoSto format\n
                           **momir**: Generate a random Magic the Gathering creature for use in Momir Basic or MoJhoSto. Just like this: /momir 1 or /momir 13\n
                           **mtg**: Search a specific Magic the Gathering card. Just like this: /mtg Jace Beleren\n
                           **random-commander**: Pick a random EDH legal Legendary Creature\n
                           **random-mtg**: Pick a random Magic the Gathering card\n
                           **stonehewer**: Generate a random equipment for use in MoJhoSto. Remember that Stonehewer is less than not equal to. Just like this: /stonehewer 3\n
                           '''
    
    embed=discord.Embed(
        title="BakiBot Command List",
        color=c)
    embed.add_field(name="**General: Part One**", value=general_command_list_part_one, inline=False)
    embed.add_field(name="**General: Part Two**", value=general_command_list_part_two, inline=False)
    embed.add_field(name="**Magic the Gathering", value=mtg_command_list, inline=False)
    embed.add_field(name="**Pokemon**", value =pokemon_command_list, inline=False)
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
