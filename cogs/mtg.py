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
            card_name = random_card_json["card_faces"][0]["name"]
            card_mana_cost = random_card_json["card_faces"][0]["mana_cost"]
            card_image_url = random_card_json["card_faces"][0]["image_uris"]["large"]
            card_oracle_text = random_card_json["card_faces"][0]["oracle_text"]
            card_back_oracle_text =random_card_json["card_faces"][1]["oracle_text"]

        elif card_layout == "modal_dfc":
            card_name = random_card_json["card_faces"][0]["name"]
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

        #Currently I pick a random color for the embed like I do for other instances.
        #Eventually I would like to update it to take the color identity of the card into account. 
        embed = discord.Embed(title=f"{card_name}" + f" ({card_set_code})", url=f"{card_url}", color=random_color)
        
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
                card_power = "* "

            if card_toughness == "*":
                card_toughness = " *"

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
                momir_card_url = scryfall_url + "cards/random?q=t%3Acreature+mv%3A" + arg1
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

async def setup(bot):
    await bot.add_cog(mtg(bot))
