import discord
import sys
import random
import yt_dlp
import os
import os.path
import asyncio
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

heroku_check = os.getenv('HEROKU_CHECK')

#yt_dlp.Voices.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn -reconnect 1   -reconnect_streamed 1 -reconnect_delay_max 5',  
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="tts")
    @commands.cooldown(1.0,3.0)
    async def join(self, ctx, *args):
            await ctx.send("Psst! Someone wanted me to tell you guys: ") 
            await ctx.send(' '.join(args), tts=True)
            
    @commands.command(name="join")
    @commands.cooldown(1.0,3.0)
    async def joinchannel(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        if heroku_check == 'False':
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)

            await channel.connect()
        else:
            await ctx.send("This command is not available on Heroku deployments.")

    @commands.command()
    @commands.cooldown(1.0,3.0)
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        if heroku_check == 'False':
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
            ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

            await ctx.send(f'Now playing: {query}')

        else:
            await ctx.send("This command is not available on Heroku deployments.")

    @commands.command()
    @commands.cooldown(1.0,3.0)
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything yt_dlp supports)"""

        if heroku_check == 'False':
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

            await ctx.send(f'Now playing: {player.title}')

        else:
            await ctx.send("This command is not available on Heroku deployments.")

    @commands.command()
    @commands.cooldown(1.0,3.0)
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        if heroku_check == 'False':
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

            await ctx.send(f'Now playing: {player.title}')

        else:
            await ctx.send("This command is not available on Heroku deployments.")
    
    @commands.command()
    @commands.cooldown(1.0,3.0)
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if heroku_check == 'False':
            if ctx.voice_client is None:
                return await ctx.send("Not connected to a voice channel.")

            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"Changed volume to {volume}%")

        else:
            await ctx.send("This command is not available on Heroku deployments.")

    @commands.command()
    @commands.cooldown(1.0,3.0)
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        if heroku_check == 'False':
            await ctx.voice_client.disconnect()

        else:
            await ctx.send("This command is not available on Heroku deployments.")

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
    
async def setup(bot):
    await bot.add_cog(Voice(bot))