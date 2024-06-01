import discord
import sys
import random
import os
import os.path
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

load_dotenv()
game_list_id = os.getenv('DISCORD_IB_ID')
game_list_id_2 = os.getenv('DISCORD_ZA_ID')

gameList = [
            'American Truck Simulator',
            'Battlefield V',
            'Command and Conquer: Red Alert 2',
            'Command and Conquer: Generals - Zero Hour',
            'Farming Simulator 19',
            'Green Hell',
            'Halo Infinite',
            'Halo: The Master Chief Collection',
            'Helldivers 2',
            'Left 4 Dead 2',
            'Parkitect',
            'Payday 2',
            'PUBG',
            'Pulsar: Lost Colony',
            'Pummel Party',
            'Raft',
            'Sniper Elite 5',
            'Stardew Valley',
            'Stick Fight: The Game',
            'theHunter: Call of the Wild',
            'Thunder Tier One',
            "Tom Clancy's Rainbox Six Siege",
            "Tom Clancy's The Division 2",
            'Zombie Army 4: Dead War',
            'Zombie Army Trilogy'
        ]
        
gameList2 = [
            'Age of Empires II: HD Edition',
            'Borderlands: The Pre-Sequel',
            'Borderlands 2',
            'Borderlands 3',
            "Don't Starve Together",
            'Halo Wars: Enhanced Edition',
            'Halo Wars 2',
            'Left 4 Dead 2',
            'Rocket League',
            "Sid Meier's Civilization VI",
            'Sins of a Solar Empire: Rebellion',
            'Sonic & All-Stars Racing Transformed',
            'Star Wars Battlefront II (Classic)',
            'Starbound',
            'Stardew Valley',
            'Supreme Commander 2',
            'Terraria',
            'Victor Vran',
            'Wargame: Red Dragon'
        ]

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='randomgame', help='Randomly picks a game from the server side game list')
    @commands.cooldown(1.0,3.0)
    async def randomgame(self, ctx):
        guild = ctx.guild
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if (guild.id == int(game_list_id)):
            response = random.choice(gameList)
            await ctx.send(embed=discord.Embed(description="You should play: " + response, colour=c))
        elif (guild.id == int(game_list_id_2)):
            response = random.choice(gameList2)
            await ctx.send(embed=discord.Embed(description="You should play: " + response, colour=c))
        else:
            await ctx.send(embed=discord.Embed(description="No list found for this server", colour=c))
        
    @commands.command(name="gamelist")
    @commands.cooldown(1.0,3.0)
    async def on_message(self, ctx):
        newList = '**Current Game list**' + '\n'
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        guild = ctx.guild

        if (guild.id == int(game_list_id)):
            for game in gameList:
                newList = newList + '\n' + game
            await ctx.send(embed=discord.Embed(description=newList, colour=c))
        elif (guild.id == int(game_list_id_2)):
            for game in gameList2:
                newList = newList + '\n' + game
            await ctx.send(embed=discord.Embed(description=newList, colour=c))
        else:
            await ctx.send(embed=discord.Embed(description="No list found for this server", colour=c)) 
        
async def setup(bot):
    await bot.add_cog(Games(bot))
