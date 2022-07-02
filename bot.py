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

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!help"))

@bot.command(name='pickfromlist', help='Randomly picks a game from the server side game list')
async def on_message(ctx):
    gameList = [
    'Battlefield V',
    'American Truck Simulator',
    'Halo Infinite',
    'The Master Chief Collection',
    'Left 4 Dead 2',
    'Parkitect',
    'Payday 2',
    'PUBG',
    'Pulsar: Lost Colony',
    'Raft',
    'Stardew Valley',
    'Stick Fight: The Game',
    'Zombie Army Trilogy',
    'Rainbox Six Siege',
    'The Division 2',
    ]
    
    response = random.choice(gameList)
    await ctx.send(response)

@bot.command(name="choose", description="Choose from a list", usage="choose <item1 item2 item3 ... >")
async def choose(ctx, *args):
    response = random.choice(args)
    await ctx.send(response)

@bot.command(name="help")
async def embed(ctx):
    #response = "Command Prefix is !. Available Commands: PickFromGameList (Selects from a list of games) choose <item1 item2 item3 ...> (Will randomly select from the items listed after it)"
    #await ctx.send(response)
    
    embed=discord.Embed(
    title="Command List",
        color=discord.Color.blue())
    embed.add_field(name="**pickfromlist**", value="Pick a random game from the full list of games we own", inline=False)
    embed.add_field(name="**choose**", value="Pick a random option from the items given. Put a space between each item", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)