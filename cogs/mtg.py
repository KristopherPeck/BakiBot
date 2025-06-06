import discord
import sys
import random
import os
import os.path
import requests
import requests_cache
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import Context

heroku_check = os.getenv('HEROKU_CHECK')
owner_id = os.getenv('DISCORD_OWNERID')
scryfall_url = "https://api.scryfall.com/"

def GenerateCardDetails(card_type, random_card_json, random_color):
        card_name = random_card_json["name"]

        #MTG cards have some different layouts that place information in different spots in the API
        #For the most part these are pretty similar but I still split them out to make things easier. 
        card_layout = random_card_json["layout"]
        if card_layout == "transform":
            card_name = random_card_json["name"]
            card_mana_cost = random_card_json["card_faces"][0]["mana_cost"]
            card_image_url = random_card_json["card_faces"][0]["image_uris"]["large"]
            card_oracle_text = random_card_json["card_faces"][0]["oracle_text"]
            card_back_oracle_text =random_card_json["card_faces"][1]["oracle_text"]

        elif card_layout == "modal_dfc":
            card_name = random_card_json["name"]
            card_mana_cost = random_card_json["card_faces"][0]["mana_cost"]
            card_image_url = random_card_json["card_faces"][0]["image_uris"]["large"]
            card_oracle_text = random_card_json["card_faces"][0]["oracle_text"]
            card_back_oracle_text =random_card_json["card_faces"][1]["oracle_text"]
        
        elif card_layout == "split":
            card_name = random_card_json["name"]
            card_mana_cost = random_card_json["mana_cost"]
            card_image_url = random_card_json["image_uris"]["large"]
            card_oracle_text = random_card_json["card_faces"][0]["oracle_text"]
            card_back_oracle_text =random_card_json["card_faces"][1]["oracle_text"]

        elif card_layout == "flip":
            card_name = random_card_json["name"]
            card_mana_cost = random_card_json["mana_cost"]
            card_image_url = random_card_json["image_uris"]["large"]
            card_oracle_text = random_card_json["card_faces"][0]["oracle_text"]
            card_back_oracle_text =random_card_json["card_faces"][1]["oracle_text"]

        elif card_layout == "reversible_card":
            card_name = random_card_json["name"]
            card_mana_cost = random_card_json["card_faces"][0]["mana_cost"]
            card_image_url = random_card_json["image_uris"]["large"]
            card_oracle_text = random_card_json["card_faces"][0]["oracle_text"]
            card_back_oracle_text =random_card_json["card_faces"][1]["oracle_text"]

        else:
            card_name = random_card_json["name"]
            card_mana_cost = random_card_json["mana_cost"]
            card_oracle_text = random_card_json["oracle_text"]
            card_image_url = random_card_json["image_uris"]["large"]
        
        card_layout = card_layout.upper()
        card_url = random_card_json["scryfall_uri"]
        card_set_name = random_card_json["set_name"]
        card_set_code = random_card_json["set"].upper()

        #Flavor text as well as back oracle text aren't always on the cards.
        try:
            card_flavor_text = random_card_json["flavor_text"]
        except:
            card_flavor_text = ""

        try:
            card_back_flavor_text = random_card_json["card_faces"][1]["flavor_text"]
        except:
            card_back_flavor_text = ""

        try:
            card_back_oracle_text = random_card_json["card_faces"][1]["oracle_text"]
        except:
            card_back_oracle_text = ""

        #Determine color of embed box based on the color identity of the card 
        
        color_identity = random_card_json["color_identity"]
        color_identity_length = len(color_identity)

        if color_identity_length >= 2:
            identity_color_rgb = discord.Color.from_rgb(187, 165, 61)
            embed = discord.Embed(title=f"{card_name}" + f" ({card_set_code})", url=f"{card_url}", color=identity_color_rgb)

        elif color_identity_length == 0:
            identity_color_rgb = discord.Color.from_rgb(93, 93, 93)
            embed = discord.Embed(title=f"{card_name}" + f" ({card_set_code})", url=f"{card_url}", color=identity_color_rgb)
       
        else:
            color_identity_text = color_identity[0]
            if color_identity_text == "W":
                identity_color_rgb = discord.Color.from_rgb(255, 255, 255)
                mbed = discord.Embed(title=f"{card_name}" + f" ({card_set_code})", url=f"{card_url}", color=identity_color_rgb)

            elif color_identity_text == "U":
                identity_color_rgb = discord.Color.from_rgb(0, 94, 255)
                embed = discord.Embed(title=f"{card_name}" + f" ({card_set_code})", url=f"{card_url}", color=identity_color_rgb)

            elif color_identity_text == "B":
                identity_color_rgb = discord.Color.from_rgb(0, 0, 0)
                embed = discord.Embed(title=f"{card_name}" + f" ({card_set_code})", url=f"{card_url}", color=identity_color_rgb)

            elif color_identity_text == "R":
                identity_color_rgb = discord.Color.from_rgb(255, 8, 0)
                embed = discord.Embed(title=f"{card_name}" + f" ({card_set_code})", url=f"{card_url}", color=identity_color_rgb)

            elif color_identity_text == "G":
                identity_color_rgb = discord.Color.from_rgb(14, 92, 0)
                embed = discord.Embed(title=f"{card_name}" + f" ({card_set_code})", url=f"{card_url}", color=identity_color_rgb)

        #Some cards don't have a Mana Cost so we have to accomodate for that.
        if "Land" in card_type:
            pass
        elif "Vanguard" in card_type:
            pass
        else:
            embed.add_field(name="Mana Cost:", value=f"{card_mana_cost}", inline=False)

        embed.add_field(name="Card Type:", value=f"{card_type}", inline=False)

        #Technically Lands have no Oracle text. 
        if card_oracle_text == "":
            pass
        else:
            embed.add_field(name="Oracle Text:", value=f"{card_oracle_text}", inline=False)

        if card_back_oracle_text == "":
            pass
        elif card_layout == "flip":
            embed.add_field(name="Flipped Oracle Text:", value=f"{card_back_oracle_text}", inline=False)
        else:
            embed.add_field(name="Back Oracle Text:", value=f"{card_back_oracle_text}", inline=False)


        #While Vanguard may not exist anymore I still accomodate for them. 
        #Vanguard cards have some additional text on them regarding hand and life modifiers I want to display. 
        if "Vanguard" in card_type:
            card_hand_modifier = random_card_json["hand_modifier"]
            card_life_modifier = random_card_json["life_modifier"]
            embed.add_field(name="Vanguard Bonuses:", value="Hand Size: " + f"{card_hand_modifier}" + "Life Total: " + f"{card_life_modifier}", inline=False)


        if card_flavor_text == "":
            pass
        else:
            embed.add_field(name="Flavor Text:", value=f"{card_flavor_text}", inline=False)

        if card_back_flavor_text == "":
            pass
        else:
            embed.add_field(name="Back Flavor Text:", value=f"{card_back_flavor_text}", inline=False)

        #Transform and Modal DFC store the details about power/toughness/loyalty in a separate array
        #Currently we don't track what they have for those on the back side. I only care about the front face. 
        if card_layout == "transform" or card_layout == "modal_dfc":
                card_type = random_card_json["card_faces"][0]["type_line"]

        if "Creature" in card_type:
            try:
                card_power = random_card_json["power"]
            except:
                card_power = random_card_json["card_faces"][0]["power"]

            try:    
                card_toughness = random_card_json["toughness"]
            except:
                card_toughness = random_card_json["card_faces"][0]["toughness"]

            if card_power == "*":
                card_power = "[*]"

            if card_toughness == "*":
                card_toughness = "[*]"

            embed.add_field(name="Power/Toughness:", value=f"{card_power}/" + f"{card_toughness}", inline=False)

        elif "Planeswalker" in card_type:

            try:
                card_loyalty = random_card_json["loyalty"]
            except:
                card_loyalty = random_card_json["card_faces"][0]["loyalty"]

            if card_loyalty == "*":
                card_loyalty = " * "

            embed.add_field(name="Loyalty:", value=f"{card_loyalty}", inline=False)

        embed.add_field(name="Printing:", value=f"{card_set_name}", inline=False)

        card_price_usd = random_card_json["prices"]["usd"]
        card_price_foil = random_card_json["prices"]["usd_foil"]
        card_price_tix = random_card_json["prices"]["tix"]
        card_price_etched = random_card_json["prices"]["usd_etched"]

        if card_price_usd is None:
            card_price_usd = "N/A"
        
        if card_price_foil is None:
            card_price_foil = "N/A"

        if card_price_tix is None:
            card_price_tix = "N/A"

        if card_price_etched is None:
            card_price_etched = "N/A"

        #Alchemy cards and other MTG Arena cards don't have prices so we show a different result for them. 
        if card_price_usd == "N/A" and card_price_foil == "N/A" and card_price_tix == "N/A" and card_price_etched == "N/A":
            embed.add_field(name="Price:", value="No Price Information Available")
        else:
            embed.add_field(name="Price:", value="Nonfoil: $ " + f"{card_price_usd}" + " | Foil: $ " + f"{card_price_foil}" +  " | Etched: $ " + f"{card_price_etched}" + " | Tickets: " + f"{card_price_tix}")

        embed.set_thumbnail(url=card_image_url)
        embed.set_footer(text="Data provided by scryfall.com", icon_url="https://avatars.githubusercontent.com/u/22605579?s=200&v=4")

        return embed

class mtg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ownercheck(ctx):
        return ctx.message.author.id == int(owner_id)
    
    @commands.command(name='randommtg')
    @commands.cooldown(1.0,3.0)
    async def randommtg(self, ctx):
        random_card_url = scryfall_url + "cards/random"
        print ("Random MTG Card")
        random_card_response = requests.get(random_card_url)
        random_card_json = random_card_response.json()
        print (random_card_json["name"])
        card_type = random_card_json["type_line"]

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        channel = ctx.message.channel
        async with channel.typing():
            embed = GenerateCardDetails(card_type, random_card_json, random_color)
        
        await channel.send(embed=embed)

    @commands.command(name='randomcommander')
    @commands.cooldown(1.0,3.0)
    async def randomcommander(self, ctx):

        random_card_url = scryfall_url + "cards/random?q=is%3Acommander"
        print ("Random Commander")
        random_card_response = requests.get(random_card_url)
        random_card_json = random_card_response.json()
        print (random_card_json["name"])
        card_type = random_card_json["type_line"]
        card_edh_legal = random_card_json["legalities"]["commander"]

        #The Random Commander API command for some reason includes the Background cards from Baldur's Gate since they technically exist in the Command Zone.
        #However, I don't want them to show up in my iteration. So we filter out those as well as any cards that aren't legal in EDH.
        while ("Background" in card_type) and (card_edh_legal == "not_legal"):
            random_card_url = scryfall_url + "cards/random?q=is%3Acommander"
            random_card_response = requests.get(random_card_url)
            random_card_json = random_card_response.json()
            card_type = random_card_json["type_line"]
            card_edh_legal = random_card_json["legalities"]["commander"]

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        channel = ctx.message.channel
        async with channel.typing():
            embed = GenerateCardDetails(card_type, random_card_json, random_color)
        
        await channel.send(embed=embed)

    @commands.command(name='momir')
    @commands.cooldown(1.0,3.0)
    async def momir(self, ctx, arg1):

        try:  
                arg1 = str(arg1)
                momir_card_url = scryfall_url + "cards/random?q=t%3Acreature+mv%3A" + arg1 + " not:funny"
                print ("Random Momir prompt for:" + arg1)
                momir_card_response = requests.get(momir_card_url)
                momir_card_json = momir_card_response.json()
                print (momir_card_json["name"])
                card_type = momir_card_json["type_line"]
        except:
                await ctx.send("It looks like there wasn't any card with that mana value. Please try another one.")
                return

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        channel = ctx.message.channel
        async with channel.typing():
            embed = GenerateCardDetails(card_type, momir_card_json, random_color)
                
        await channel.send(embed=embed)

    @commands.command(name='jhoira')
    @commands.cooldown(1.0,3.0)
    async def jhoira(self, ctx, arg1):

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        arg1 = str(arg1)

        if arg1 not in ("Instant", "instant", "sorcery", "Sorcery"):
            await ctx.send("Jhoira of the Ghitu only works with instant or sorcery.")

        try:  
                jhoira_card_url_1 = scryfall_url + "cards/random?q=t%3A" + arg1 + " -t:enchantment -t:creature -t:artifact -t:planeswalker (game:paper) not:funny"
                jhoira_card_url_2 = scryfall_url + "cards/random?q=t%3A" + arg1 + " -t:enchantment -t:creature -t:artifact -t:planeswalker (game:paper) not:funny"
                jhoira_card_url_3 = scryfall_url + "cards/random?q=t%3A" + arg1 + " -t:enchantment -t:creature -t:artifact -t:planeswalker (game:paper) not:funny"
                print ("Random Jhoira prompt for:" + arg1)
                jhoira_card_response_1 = requests.get(jhoira_card_url_1)
                jhoira_card_response_2 = requests.get(jhoira_card_url_2)
                jhoira_card_response_3 = requests.get(jhoira_card_url_3)
                jhoira_card_json_1 = jhoira_card_response_1.json()
                jhoira_card_json_2 = jhoira_card_response_2.json()
                jhoira_card_json_3 = jhoira_card_response_3.json()
                print (jhoira_card_json_1["name"])
                print (jhoira_card_json_2["name"])
                print (jhoira_card_json_3["name"])
                card_type_1 = jhoira_card_json_1["type_line"]
                card_type_2 = jhoira_card_json_2["type_line"]
                card_type_3 = jhoira_card_json_3["type_line"]
        except:
                await ctx.send("It looks like there was an issue. Please contact the administrator if you continue to have issues.")
                return

        channel = ctx.message.channel
        async with channel.typing():
            embed = GenerateCardDetails(card_type_1, jhoira_card_json_1, random_color)
                
        await channel.send(embed=embed)

        channel = ctx.message.channel
        async with channel.typing():
            embed = GenerateCardDetails(card_type_2, jhoira_card_json_2, random_color)
                
        await channel.send(embed=embed)

        channel = ctx.message.channel
        async with channel.typing():
            embed = GenerateCardDetails(card_type_3, jhoira_card_json_3, random_color)
                
        await channel.send(embed=embed)


    @commands.command(name='mojhosto')
    @commands.cooldown(1.0,3.0)
    async def mojhosto(self, ctx):

        await ctx.send("MoJhoSto is a format of Magic the Gathering that originated on Magic Online. Using the Vanguard cards for Momir Vig, Simic Visionary, Jhoira of the Ghitu, and Stonehewer Giant and a deck of 60 basic lands to play with 20 life for each player. The players play the game by utilizing the abilities of the Vanguard cards to create creatures, cast spells, and make equipment. You do not play with the life total/hand size changes listed on the cards.")
        await ctx.send("There is also the alternative and more well known format of Momir Basic which is played using only the Momir Vig Vanguard ability but is otherwise identical.")
        await ctx.send("https://cards.scryfall.io/large/front/f/5/f5ed5ad3-b970-4720-b23b-308a25f42887.jpg?1562953277")
        await ctx.send("https://cards.scryfall.io/large/front/c/d/cd1c87eb-4974-4160-91bd-681e0a75a98e.jpg?1562943398")
        await ctx.send("https://cards.scryfall.io/large/front/d/5/d5cdf535-56fb-4f92-abf0-237aa6e081b0.jpg?1562945952")

    @commands.command(name='stonehewer')
    @commands.cooldown(1.0,3.0)
    async def stonehewer(self, ctx, arg1):

        try:  
                arg1 = str(arg1)
                stonehewer_card_url = scryfall_url + "cards/random?q=t%3Aequipment+mv%3A<" + arg1 + " not:funny"
                print ("Random Stonehewer prompt for:" + arg1)
                stonehewer_card_response = requests.get(stonehewer_card_url)
                stonehewer_card_json = stonehewer_card_response.json()
                print (stonehewer_card_json["name"])
                card_type = stonehewer_card_json["type_line"]
        except:
                await ctx.send("It looks like there wasn't any card available for that mana value. Please try another one.")
                return

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        channel = ctx.message.channel
        async with channel.typing():
            embed = GenerateCardDetails(card_type, stonehewer_card_json, random_color)
                
        await channel.send(embed=embed)

    @commands.command(name="mtg")
    @commands.cooldown(1.0,3.0)
    async def mtg(selfe, ctx, *args):
        card_name_string = ' '.join([str(elem) for elem in args])
        mtg_card_url = scryfall_url + "cards/named?fuzzy=" + card_name_string
        print ("Named MTG Card Submitted String")
        print (card_name_string)
        card_response = requests.get(mtg_card_url)

        if card_response.status_code == 404:
            card_json = card_response.json()
            print ("API Response")
            print (card_json)
            await ctx.send("Sorry, I don't recognize that card or I am finding multiple cards with that name. Please try something else.")
            return
        else:
            card_json = card_response.json()
            print (card_json["name"])
            card_type = card_json["type_line"]

            random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            channel = ctx.message.channel
            async with channel.typing():
                embed = GenerateCardDetails(card_type, card_json, random_color)

            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(mtg(bot))
