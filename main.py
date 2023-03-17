import os
import discord
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

#load our environmental variables for later
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ownerID = os.getenv('DISCORD_OWNERID')

#configure the command prefix
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents = intents)
bot.remove_command('help')

#We have a environment variable for the Bot Administrator so only they can run certain commands.
def ownercheck(ctx):
        return ctx.message.author.id == int(ownerID)

@bot.event
async def on_ready():
    #Set discord presence
    await bot.change_presence(activity=discord.Game(name="!help or !posthelp"))

@bot.event
async def on_command_error(ctx, error):
    #Configure some error messages so we get some idea what something is broken
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command does not exist. Please check !help for the current commands")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing something.")
    else:
        await ctx.send(error)
        
@bot.command()
@commands.check(ownercheck)
async def load(ctx, extension):
    #Load an unloaded cog
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded Cog")

@bot.command()
@commands.check(ownercheck)
async def unload(ctx, extension):
    #unload loaded cog
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded Cog")

@bot.command()
@commands.check(ownercheck)
async def reload(ctx, extension):
    #reload loaded cog
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded Cog")

@bot.command()
@commands.check(ownercheck)
async def checkcogs(ctx):
    #Check current status of all cogs and attempt to reload any unloaded cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'cogs.{filename[0:-3]}')
            except commands.ExtensionAlreadyLoaded:
                await ctx.send({filename[0:-3]})
                await ctx.send("is loaded")
            except commands.ExtensionNotFound:
                await ctx.send({filename[0:-3]})
                await ctx.send("is not found")
            else:
                await ctx.send({filename[0:-3]})
                await ctx.send("is unloaded")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[0:-3]}')

bot.run(TOKEN)
