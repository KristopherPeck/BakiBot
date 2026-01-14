import discord
import sys
import random
import os
import os.path
import psycopg2
import datetime
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

database_url = os.environ['DATABASE_URL']

class NameCalling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whoisit", description="Call someone out.")
    @app_commands.checks.cooldown(1.0,3.0)
    async def whoisit(self, interaction: discord.Interaction, person: str):
        response = person
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await interaction.response.send_message(embed=discord.Embed(description=response + " is a scrub!", colour=c))
        
    @app_commands.command(name="findthem", description="Pick a random person from the server to call a scrub.")
    @app_commands.checks.cooldown(1, 3)
    async def findthem(self, interaction: discord.Interaction):
        users = [random.choice(interaction.guild.members)]       
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed = discord.Embed(description=f"{users[0].mention} is a scrub!", colour=c)

        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.datetime.now()
        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id) VALUES (%s, %s, %s, %s, %s)", ("findthem", users[0], now, interaction.user.name, interaction.user.id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()

        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(NameCalling(bot))
