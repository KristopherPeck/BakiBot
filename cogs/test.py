import discord
import sys
import random
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
async def setup(bot):
    await bot.add_cog(Test(bot))