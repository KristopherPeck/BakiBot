import discord
import sys
import random
from discord.ext import commands
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
        await ctx.send(embed=discord.Embed(description=response + " is a bitch!", colour=c))
        
    @commands.command(name="findthem")
    @commands.cooldown(1.0,3.0)
    async def on_message(self, ctx):
        users = [random.choice(ctx.guild.members)]       
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description=f"{users[0].mention} is a bitch!", colour=c))
    
async def setup(bot):
    await bot.add_cog(NameCalling(bot))
