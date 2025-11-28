import discord
import sys
import random
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

class NameCalling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="whoisit")
    @commands.cooldown(1.0,3.0)
    async def on_message(self, ctx, *args):
        response = random.choice(args)
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description=response + " is a scrub!", colour=c))
        
    @app_commands.command(name="findthem", description="Pick a random person from the server to call a scrub.")
    @app_commands.checks.cooldown(1, 3)
    async def findthem(self, interaction: discord.Interaction):
        users = [random.choice(interaction.guild.members)]       
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed = discord.Embed(description=f"{users[0].mention} is a scrub!", colour=c)
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(NameCalling(bot))
