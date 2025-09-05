import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ownerID = os.getenv('DISCORD_OWNERID')

# Custom Bot class with setup_hook
class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.owner_id = int(ownerID)

    async def setup_hook(self):
        # Load all available cogs at startup
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')

        # Sync all slash commands
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} application command(s).")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")

# Configure intents and bot
intents = discord.Intents.all()
client = MyBot(command_prefix='!', intents=intents)
client.remove_command('help')

# Simple owner check for prefix commands
def ownercheck(ctx):
    return ctx.author.id == client.owner_id

# Events
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="!help or !dmhelp"))
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command does not exist. Please check !help for the current commands")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing something.")
    else:
        await ctx.send(f"⚠️ {error}")

@client.event
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"⏳ That command is on cooldown! Try again in {error.retry_after:.1f} seconds.",
            ephemeral=True
        )
    else:
        print(f"[SlashCommandError] {interaction.command} | {type(error).__name__}: {error}")
        try:
            await interaction.response.send_message(
                "⚠️ An unexpected error occurred.",
                ephemeral=True
            )
        except discord.InteractionResponded:
            await interaction.followup.send(
                "⚠️ An unexpected error occurred.",
                ephemeral=True
            )

# Example global slash command (for testing)
@client.tree.command(name="test2")
async def test2(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)

# Prefix admin commands for managing cogs
@client.command()
@commands.check(ownercheck)
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')
    await ctx.send("✅ Loaded Cog")

@client.command()
@commands.check(ownercheck)
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await ctx.send("✅ Unloaded Cog")

@client.command()
@commands.check(ownercheck)
async def reload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')
    await ctx.send("🔄 Reloaded Cog")

@client.command()
@commands.check(ownercheck)
async def shutdown(ctx):
    await ctx.send("👋 Shutting down...")
    await client.close()

# Main entrypoint
async def main():
    async with client:
        await client.start(TOKEN)

asyncio.run(main())