import discord
import sys
import random
import requests
import requests_cache
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

def GenerateTriviaDetails(mode_selection, random_color, trivia_db_json):

    print (mode_selection)

    trivia_difficulty = trivia_db_json["results"][0]["difficulty"]
    print (trivia_difficulty)
    trivia_category = trivia_db_json["results"][0]["category"]
    print (trivia_category)
    trivia_question = trivia_db_json["results"][0]["question"]
    print (trivia_question)
    trivia_answer = trivia_db_json["results"][0]["correct_answer"]
    print (trivia_answer)

    embed = discord.Embed(title=f"Trivia Time!", color=random_color)
    embed.add_field(name="Trivia Category:", value=f"{trivia_category}", inline=False)
    embed.add_field(name="Trivia Difficulty:", value=f"{trivia_difficulty}", inline=False)
    embed.add_field(name="Question!", value=f"{trivia_question}", inline=False)

    if mode_selection == 0:
        random_increment = random.randint(0, 3)
        trivia_incorrect_question_one = trivia_db_json["results"][0]["incorrect_answers"][0]
        print (trivia_incorrect_question_one)
        trivia_incorrect_question_two = trivia_db_json["results"][0]["incorrect_answers"][1]
        print (trivia_incorrect_question_two)
        trivia_incorrect_question_three = trivia_db_json["results"][0]["incorrect_answers"][2]
        print (trivia_incorrect_question_three)
    
        if random_increment == 0:
            embed.add_field(name="A:", value=f"{trivia_answer}", inline=False)
            embed.add_field(name="B:", value=f"{trivia_incorrect_question_one}", inline=False)
            embed.add_field(name="C:", value=f"{trivia_incorrect_question_two}", inline=False)
            embed.add_field(name="D:", value=f"{trivia_incorrect_question_three}", inline=False)
        elif random_increment == 1:
            embed.add_field(name="A:", value=f"{trivia_incorrect_question_one}", inline=False)
            embed.add_field(name="B:", value=f"{trivia_answer}", inline=False)
            embed.add_field(name="C:", value=f"{trivia_incorrect_question_two}", inline=False)
            embed.add_field(name="D:", value=f"{trivia_incorrect_question_three}", inline=False)
        elif random_increment == 2:
            embed.add_field(name="A:", value=f"{trivia_incorrect_question_one}", inline=False)
            embed.add_field(name="B:", value=f"{trivia_incorrect_question_two}", inline=False)
            embed.add_field(name="C:", value=f"{trivia_answer}", inline=False)
            embed.add_field(name="D:", value=f"{trivia_incorrect_question_three}", inline=False)
        elif random_increment == 3:
            embed.add_field(name="A:", value=f"{trivia_incorrect_question_one}", inline=False)
            embed.add_field(name="B:", value=f"{trivia_incorrect_question_two}", inline=False)
            embed.add_field(name="C:", value=f"{trivia_incorrect_question_three}", inline=False)
            embed.add_field(name="D:", value=f"{trivia_answer}", inline=False)

    elif mode_selection == 1:
        trivia_incorrect_question_one = trivia_db_json["results"][0]["incorrect_answers"][0]
        print (trivia_incorrect_question_one)

    embed.add_field(name="Correct Answer:", value=f"||{trivia_answer}||", inline=False)
    print ("Add answer Worked")
    embed.set_footer(text= "Data provided by opentdb.com", icon_url="https://opentdb.com/images/logo.png")
    print ("set Footer worked")

    return embed

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.command(name='randombaki')
    @commands.cooldown(1.0,3.0)
    async def randombaki(self, ctx):
        baki_quotes = [
            "You'd do or say anything to save your skin... probably even lick my ass when nobody was looking. -Sikorsky",
            "Now that you've got no more urine left in you... How are you going to get out of this tetrahedron? -Mouth",
            "It seems that in this fight... I won't be able to win this without pissing on myself just a little bit. -Baki Hanma",
            "I started to wish I didn't have any fingers.. because then I could punch all out. My dream just came true. -Doppo 'Tiger Slayer' Orochi",
            "His tuxedo is still there...!! Just like a lesson in shedding your skin!! -bystander from the fight between Biscuit Oliva and Jun Guevara",
            "What's futile is not realizing the reality of your own futility. One hundred cowards are the same as one. -Yujiro 'The Ogre' Hanma",
            "You’re challenging me? Surely stupidity of this magnitude can’t possibly exist. -Yujiro 'The Ogre' Hanma"
        ]
        response = random.choice(baki_quotes)
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description=response, colour=random_color))
        
    @commands.command(name="choose", description="Choose from a list", usage="choose <item1 item2 item3 ... >")
    @commands.cooldown(1.0,3.0)
    async def choose(self, ctx, *args):
        response = random.choice(args)
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="Eeny, meeny, miny, moe. I choose: " + response, colour=random_color))
        
    @commands.command(name="dieroll")
    @commands.cooldown(1.0,3.0)
    async def dieroll(self, ctx, arg1):
        arg1 = int(arg1)
        result = random.randint(1, arg1)
        result = str(result)
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="Show me the money!: " + result, colour=random_color))

    @commands.command(name="roll")
    @commands.cooldown(1.0,3.0)
    async def roll(self, ctx, dice:str):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Please use the proper format of NdT!')
            return
        
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        roll_results = []
        for roll in range(rolls): 
            roll = random.randint(1, limit)
            roll_results.append(roll)

        roll_total = sum(roll_results)

        all_rolls = ""
        for item in roll_results:
            all_rolls = all_rolls + str(item) + ", "
        all_rolls = all_rolls[:-2]

        await ctx.send(embed=discord.Embed(description="Your individual rolls were " + all_rolls + "! The total is " + str(roll_total) + "!", colour=random_color))

    @commands.command(name="flip")
    @commands.cooldown(1.0,3.0)
    async def flip(self, ctx):
        choices = ["Heads", "Tails"]
        result = random.choice(choices)
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="You got  " + result + "!", colour=random_color))
        
    @commands.command(name="color")
    @commands.cooldown(1.0,3.0)
    async def colour(self, ctx):
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(
            embed=discord.Embed(
                title="Color Codes",
                description=f"6 digit Hexadecimal: ``{random_color.__str__()}``\n" f"RGB Values: ``{random_color.to_rgb()}``",
                color=random_color,
            )
        )
        
    @commands.command(name="8ball", description="classic 8ball", aliases=["eightball"])
    @commands.cooldown(1.0,3.0)
    async def eightball(self, ctx, question: str):
        eightball_responses = [
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
        await ctx.send(embed=discord.Embed(description=":8ball: " + random.choice(eightball_responses), colour=c))

    @commands.command(name="lunchtime")
    @commands.cooldown(1.0,3.0)
    async def lunchtime(self, ctx):
        restaurant_choices = [
            "Penn Station", "Sakura", "Kumo Hibachi", "Z&W Chinese Cuisine", "Two Fellas Grill", "Red Robin", "Five Guys", "Buffalo Wild Wings", "Olgas", "Logans", "Applebees",
            "Kelvin and Co", "City BBQ", "Bob Evans", "Taco Bell", "Berries", "Firehouse Subs", "Long John Silvers", "Red Lobster", "Chilis", "Jersey Mikes", "Chinese Buffet", "Lees",
            "Mcallisters", "Burger King", "Arbys", "McDonalds", "Wendys", "Angelos", "Chipotle", "Qdoba", "Los Amigos", "Olive Garden", "Culvers", "Main Street Pub", "Monellis"
        ]
        response = random.choice(restaurant_choices)
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(embed=discord.Embed(description="It's time for " + response + "!", colour=random_color))

    @commands.command(name="trivia")
    @commands.cooldown(1.0,3.0)
    async def trivia(self, ctx):
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        mode_selection = random.randint(0, 1)

        if mode_selection == 0:
            trivia_db_url = "https://opentdb.com/api.php?amount=1&type=boolean"
        if mode_selection == 1:
            trivia_db_url = "https://opentdb.com/api.php?amount=1&type=multiple"
        
        trivia_db_response = requests.get(trivia_db_url)
        trivia_db_json = trivia_db_response.json()

        channel = ctx.message.channel
        async with channel.typing():
            embed = GenerateTriviaDetails(mode_selection, random_color, trivia_db_json)

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Random(bot))