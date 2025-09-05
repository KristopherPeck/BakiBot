import os
import discord
import asyncio
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord import app_commands
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
client = commands.Bot(command_prefix='!', intents = intents)
client.remove_command('help')
DiscordGame = discord.Game("!help or !dmhelp")

#We have a environment variable for the Bot Administrator so only they can run certain commands.
def ownercheck(ctx):
        return ctx.message.author.id == int(ownerID)

@client.event
async def on_ready():
    #Set discord presence
    try:
        await client.tree.sync()
    except Exception as e:
        print("Failed to Sync")
    await client.change_presence(activity=discord.Game(name="!help or !dmhelp"))

@client.tree.command(name="test2")
async def test2(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)

@client.event
async def on_command_error(ctx, error):
    #Configure some error messages so we get some idea what something is broken
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command does not exist. Please check !help for the current commands")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing something.")
    else:
        await ctx.send(error)

@client.command()
@commands.check(ownercheck)
async def load(ctx, extension):
    #Load an unloaded cog
    commands.is_owner()
    await client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded Cog")

@client.command()
@commands.check(ownercheck)
async def shutdown(ctx):
    commands.is_owner()
    await ctx.send ("Shutting Down Now")
    await client.close()

@client.command()
@commands.check(ownercheck)
async def unload(ctx, extension):
    #unload loaded cog
    commands.is_owner()
    await client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded Cog")

@client.command()
@commands.check(ownercheck)
async def reload(ctx, extension):
    #reload loaded cog
    commands.is_owner()
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded Cog")
    
@client.command()
@commands.check(ownercheck)
async def checkcogs(ctx):
    #Check current status of all cogs and attempt to reload any unloaded cogs
    commands.is_owner()
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await client.load_extension(f'cogs.{filename[0:-3]}')
            except commands.ExtensionAlreadyLoaded:
                await ctx.send({filename[0:-3]})
                await ctx.send("is loaded")
            except commands.ExtensionNotFound:
                await ctx.send({filename[0:-3]})
                await ctx.send("is not found")
            else:
                await ctx.send({filename[0:-3]})
                await ctx.send("is unloaded")

async def main():
    async with client:
        #Load all available cogs at runtime
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await client.load_extension(f'cogs.{filename[0:-3]}')

        await client.start(TOKEN)


asyncio.run(main())