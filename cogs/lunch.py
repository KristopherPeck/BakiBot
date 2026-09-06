import discord
import sys
import random
import os
import os.path
import html
import requests
import requests_cache
import psycopg2
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

database_url = os.environ['DATABASE_URL']

class lunch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="lunchtime", description="Picks a set of three random restuarants for lunch.")
    @app_commands.checks.cooldown(1.0,3.0)
    async def lunchtime(self, interaction: discord.Interaction):

        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.now()
        day_of_week = datetime.strftime(now, "%A")

        if "Monday" in day_of_week:
            date_check = "M"
        elif "Tuesday" in day_of_week:
            date_check = "T"
        elif "Wednesday" in day_of_week:
            date_check = "W"
        elif "Thursday" in day_of_week:
            date_check = "H"
        elif "Friday" in day_of_week:
            date_check = "F"
        elif "Saturday" in day_of_week:
            date_check = "S"
        elif "Sunday" in day_of_week:
            date_check = "U"

        select_query = """
                        select restaurant_name from bakibot.lunch_options
                        where days_open like %(date)s
                        order by RANDOM()
                        limit 3
                        """
        
        query_data = {
            'date': '%{}%'.format(date_check)
        }

        db_cursor.execute(select_query, query_data)
        temp_sql_results = db_cursor.fetchall()
        restaurants = [row[0] for row in temp_sql_results]

        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id) VALUES (%s, %s, %s, %s, %s)", ("lunchtime", restaurants, now, interaction.user.name, interaction.user.id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()

        if not restaurants:
            response_text = "I couldn't find any restaurants open today."

        elif len(restaurants) == 1:
            response_text = (
                f"Your choice for lunch is {restaurants[0]}!"
            )

        elif len(restaurants) == 2:
            response_text = (
                f"Your choices for lunch are "
                f"{restaurants[0]} or {restaurants[1]}!"
            )

        else:
            response_text = (
                f"Your choices for lunch are "
                f"{restaurants[0]}, {restaurants[1]}, or {restaurants[2]}!"
            )

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await interaction.response.send_message(embed=discord.Embed(description=response_text, colour=random_color))

async def setup(bot):
    await bot.add_cog(lunch(bot))
