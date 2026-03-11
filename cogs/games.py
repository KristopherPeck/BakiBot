import discord
import sys
import random
import os
import os.path
import psycopg2
import datetime
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

database_url = os.environ['DATABASE_URL']

def DatabaseLogging(command_name, database_value, user_name, user_id, guild):
    db_conn = psycopg2.connect(database_url, sslmode='require')
    db_cursor = db_conn.cursor()
    now = datetime.datetime.now()
    db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id, guild_id) VALUES (%s, %s, %s, %s, %s, %s)", (command_name, database_value, now, user_name, user_id, guild))
    db_conn.commit()
    db_cursor.close()
    db_conn.close()

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='random-game', description='Randomly picks a game from the server side game list')
    @app_commands.checks.cooldown(1.0,3.0)
    async def randomgame(self, interaction: discord.Interaction):
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        print("test")

        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.datetime.now()
        #guild_id = interaction.guild_id
        guild_id = "potato"

        print(now)
        print(guild_id)

        select_query = """
                        select game_name from bakibot.game_options
                        where guild_id = %(guild_detail)%
                        order by RANDOM()
                        limit 1
                       """
        
        query_data = {
            'guild_detail': '%{}%'.format(guild_id)
        }

        print(query_data)

        db_cursor.execute(select_query, query_data)
        temp_sql_results = db_cursor.fetchall()
        print(temp_sql_results)
        sql_results = map(list, list(temp_sql_results))
        print(sql_results)
        sql_results = sum(sql_results, [])
        print(sql_results)

        if (sql_results == ""):
            sql_results = "No Entry in Database."
            response_text = "No Games in the Database for this Server. Please add some and try again"
            await interaction.response.send_message(embed=discord.Embed(description=response_text, colour=random_color))

        else:
            response1 = str(sql_results[0])
            await interaction.response.send_message(embed=discord.Embed(description="You should play " + response1 + "!", colour=random_color))

        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id) VALUES (%s, %s, %s, %s, %s)", ("random-game", sql_results, now, interaction.user.name, interaction.user.id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
        
async def setup(bot):
    await bot.add_cog(Games(bot))
