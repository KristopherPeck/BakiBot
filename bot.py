# bot.py
import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
#create a .env file and place these variables in it
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

from discord.ext import commands
from discord.ext.commands import bot

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

gameList = [
    'Battlefield V',
    'American Truck Simulator',
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
    'Zombie Army Trilogy',
    "Tom Clancy's Rainbox Six Siege",
    "Tom Clancy's The Division 2",
    ]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!help"))

@bot.command(name='randomgame', help='Randomly picks a game from the server side game list')
async def on_message(ctx):
    response = random.choice(gameList)
    await ctx.send(response)

@bot.command(name="choose", description="Choose from a list", usage="choose <item1 item2 item3 ... >")
async def choose(ctx, *args):
    response = random.choice(args)
    await ctx.send(response)

@bot.command(name="gamelist", description="Shows the current game list")
async def on_message(ctx):
    newList = ""
    for game in gameList:
        newList = newList + '\n' + game
        
    await ctx.send(newList)

@bot.command(name="help")
async def DM(ctx):
    embed=discord.Embed(
    title="Command List",
        color=discord.Color.blue())
    embed.add_field(name="**randomgame**", value="Pick a random game from the full list of games we own", inline=False)
    embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item like this: !choose Lead Salt Diesel", inline=False)
    embed.add_field(name="**gamelist**", value="Shows the current game list", inline=False)

    await ctx.author.send(embed=embed)


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)
