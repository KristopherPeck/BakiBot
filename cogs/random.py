import discord
import sys
import random
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context
        
bakiQuotes = [
            "You'd do or say anything to save your skin... probably even lick my ass when nobody was looking. -Sikorsky",
            "Now that you've got no more urine left in you... How are you going to get out of this tetrahedron? -Mouth",
            "It seems that in this fight... I won't be able to win this without pissing on myself just a little bit. -Baki Hanma",
            "I started to wish I didn't have any fingers.. because then I could punch all out. My dream just came true. -Doppo 'Tiger Slayer' Orochi",
            "His tuxedo is still there...!! Just like a lesson in shedding your skin!! -bystander from the fight between Biscuit Oliva and Jun Guevara",
            "What's futile is not realizing the reality of your own futility. One hundred cowards are the same as one. -Yujiro 'The Ogre' Hanma"
        ]

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.command(name='randombaki')
    async def randombaki(self, ctx):
        response = random.choice(bakiQuotes)
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description=response, colour=c))
        
    @commands.command(name="choose", description="Choose from a list", usage="choose <item1 item2 item3 ... >")
    async def choose(self, ctx, *args):
        response = random.choice(args)
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="Eeny, meeny, miny, moe. I choose: " + response, colour=c))
        
    @commands.command(name="diceroll")
    async def diceroll(self, ctx, arg1):
        arg1 = int(arg1)
        result = random.randint(1, arg1)
        result = str(result)
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="Show me the money!: " + result, colour=c))
        
    @commands.command(name="color")
    async def colour(self, ctx):
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(
            embed=discord.Embed(
                title="Color Codes",
                description=f"6 digit Hexadecimal: ``{c.__str__()}``\n" f"RGB Values: ``{c.to_rgb()}``",
                color=c,
            )
        )
        
    @commands.command(name="8ball", description="classic 8ball", aliases=["eightball"])
    async def eightball(self, ctx, question: str):
        li = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Very doubtful.",
        ]
        c = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description=":8ball: " + random.choice(li), colour=c))

async def setup(bot):
    await bot.add_cog(Random(bot))