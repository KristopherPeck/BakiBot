import discord
import random
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

gameList = [
            'American Truck Simulator',
            'Battlefield V',
            'Halo Infinite',
            'Halo: The Master Chief Collection',
            'Left 4 Dead 2',
            'Parkitect',
            'Payday 2',
            'PUBG',
            'Pulsar: Lost Colony',
            'Raft',
            'Stardew Valley',
            'Stick Fight: The Game',
            "Tom Clancy's Rainbox Six Siege",
            "Tom Clancy's The Division 2",
            'Zombie Army Trilogy'
        ]

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        
    @commands.command(name='randomgame', help='Randomly picks a game from the server side game list')
    async def randomgame(self, ctx):
        response = random.choice(gameList)
        await ctx.send("You should play: " + response)
        
    @commands.command(name="choose", description="Choose from a list", usage="choose <item1 item2 item3 ... >")
    async def choose(self, ctx, *args):
        response = random.choice(args)
        await ctx.send("Eeny, meeny, miny, moe. I choose: " + response)

    @commands.command(name="gamelist", description="Shows the current game list")
    async def on_message(self, ctx):
        newList = '**Current Game list**'
        for game in gameList:
            newList = newList + '\n' + game
        
        await ctx.send(newList)

    @commands.command(name="help")
    async def DM(self, ctx):
        embed=discord.Embed(
        title="Command List",
            color=discord.Color.blue())
        embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games we own", inline=False)
        embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
        embed.add_field(name="**gamelist**", value="Shows the current game list", inline=False)

        await ctx.author.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Util(bot))
    
