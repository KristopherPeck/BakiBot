import discord
import sys
import random
import os
import os.path
import datetime
import requests
import requests_cache
import psycopg2
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

heroku_check = os.getenv('HEROKU_CHECK')
owner_id = os.getenv('DISCORD_OWNERID')
scryfall_url = "https://api.scryfall.com/"
database_url = os.environ['DATABASE_URL']
mtg_session = requests_cache.CachedSession('mtg_cache', expire_after=1800)

def GenerateCardDetails(card_type, random_card_json, random_color):
        card_name = random_card_json["name"]
        print(card_name)
        #MTG cards have some different layouts that place information in different spots in the API
        #For the most part these are pretty similar but I still split them out to make things easier. 
        card_layout = random_card_json["layout"]
        print(card_layout)
        print(card_type)
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

        elif card_layout == "adventure":
            card_name = random_card_json["name"]
            card_mana_cost = random_card_json["card_faces"][0]["mana_cost"]
            back_card_mana_cost = random_card_json["card_faces"][1]["mana_cost"]
            card_image_url = random_card_json["image_uris"]["large"]
            card_oracle_text = random_card_json["card_faces"][0]["oracle_text"]
            card_back_oracle_text =random_card_json["card_faces"][1]["oracle_text"]

        elif card_layout == "double_faced_token":
            card_name = random_card_json["name"]
            card_image_url = random_card_json["card_faces"][0]["image_uris"]["large"]
            card_oracle_text = random_card_json["card_faces"][0]["oracle_text"]
            card_back_oracle_text =random_card_json["card_faces"][1]["oracle_text"]
            card_layout = "Card"

        elif "Card" in card_type:
            card_name = random_card_json["name"]
            card_oracle_text = random_card_json["oracle_text"]
            card_image_url = random_card_json["image_uris"]["large"]
            card_layout = "Card"

        else:
            card_name = random_card_json["name"]
            card_mana_cost = random_card_json["mana_cost"]
            card_oracle_text = random_card_json["oracle_text"]
            card_image_url = random_card_json["image_uris"]["large"]
            back_card_type = "Blank"
        
        card_layout = card_layout.lower()
        card_url = random_card_json["scryfall_uri"]
        card_set_name = random_card_json["set_name"]
        print(card_set_name)
        card_set_code = random_card_json["set"].upper()
        print(card_set_code)
        back_card_type = "Blank"

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
        print(color_identity)
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
                embed = discord.Embed(title=f"{card_name}" + f" ({card_set_code})", url=f"{card_url}", color=identity_color_rgb)

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
        elif "Card" in card_type:
            pass
        elif card_layout == "double_faced_token":
            pass
        else:
            if card_layout == "adventure":
                embed.add_field(name="Mana Costs:", value=f"{card_mana_cost}" + " / " + f"{back_card_mana_cost}", inline=False)
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
        elif card_back_oracle_text != "":
            if card_layout == "adventure":
                embed.add_field(name="Adventure Text:", value=f"{card_back_oracle_text}", inline=False)      
            else:    
                embed.add_field(name="Alternate Side Oracle Text:", value=f"{card_back_oracle_text}", inline=False)      

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
        
        if "transform" in card_layout or "modal_dfc" in card_layout:
            card_type = random_card_json["card_faces"][0]["type_line"]
            back_card_type = random_card_json["card_faces"][1]["type_line"]

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

            elif "Battle" in card_type:
                try:
                    card_defense = random_card_json["defense"]
                except:
                    card_defense = random_card_json["card_faces"][0]["defense"]

                embed.add_field(name="Defense:", value=f"{card_defense}", inline=False)

        else:
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

            elif "Battle" in card_type:
                try:
                    card_defense = random_card_json["defense"]
                except:
                    card_defense = random_card_json["card_faces"][0]["defense"]

                embed.add_field(name="Defense:", value=f"{card_defense}", inline=False)   

        #Here we handle backside creatures/planeswalkers for things like the Battle cards or transform creatures
        if "Creature" in back_card_type:
            card_power = random_card_json["card_faces"][1]["power"]
            card_toughness = random_card_json["card_faces"][1]["toughness"]

            if card_power == "*":
                card_power = "[*]"

            if card_toughness == "*":
                card_toughness = "[*]"

            embed.add_field(name="Back Power/Toughness:", value=f"{card_power}/" + f"{card_toughness}", inline=False)

        elif "Planeswalker" in back_card_type:

            try:
                card_loyalty = random_card_json["loyalty"]
            except:
                card_loyalty = random_card_json["card_faces"][1]["loyalty"]

            if card_loyalty == "*":
                card_loyalty = " * "

            embed.add_field(name="Back Loyalty:", value=f"{card_loyalty}", inline=False)

        embed.add_field(name="Printing:", value=f"{card_set_name}", inline=False)

        card_price_usd = random_card_json["prices"]["usd"]
        card_price_foil = random_card_json["prices"]["usd_foil"]
        card_price_tix = random_card_json["prices"]["tix"]
        card_price_etched = random_card_json["prices"]["usd_etched"]

        print(card_price_usd)

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
        print("made it")
        embed.set_footer(text="Data provided by scryfall.com", icon_url="https://avatars.githubusercontent.com/u/22605579?s=200&v=4")

        return embed

class mtg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ownercheck(ctx):
        return ctx.message.author.id == int(owner_id)
    
    @app_commands.command(name='random-mtg', description="Pulls a random Magic the Gathering card from Scryfall.")
    @app_commands.checks.cooldown(1.0,3.0)
    async def randommtg(self, interaction: discord.Interaction):
        random_card_url = scryfall_url + "cards/random"

        random_card_response = requests.get(random_card_url)
        random_card_json = random_card_response.json()

        #If we get an art series or reversible fronts, search for the regular card version instead. 
        card_layout_check = random_card_json["layout"]
        typeline_check = random_card_json["type_line"]

        if "Card" in typeline_check:
            bad_type = True
            while bad_type == True:
                random_card_url = scryfall_url + "cards/random"
                random_card_response = requests.get(check_mtg_card_url)
                random_card_json = random_card_response.json()
                typeline_check = random_card_json["type_line"]

                if "Card" not in typeline_check:
                    bad_type == False

        if card_layout_check == "art_series":
            check_mtg_card_url = scryfall_url + "cards/named?fuzzy=" + random_card_json["name"]
            random_card_response = requests.get(check_mtg_card_url)
            random_card_json = random_card_response.json()

        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.datetime.now()
        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id) VALUES (%s, %s, %s, %s, %s)", ("random-mtg", random_card_json["name"], now, interaction.user.name, interaction.user.id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
        card_type = random_card_json["type_line"]

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed = GenerateCardDetails(card_type, random_card_json, random_color)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='random-commander', description="Pulls a random legal Commander from Scryfall.")
    @app_commands.checks.cooldown(1.0,3.0)
    async def randomcommander(self, interaction: discord.Interaction):

        random_card_url = scryfall_url + "cards/random?q=is%3Acommander"
        random_card_response = requests.get(random_card_url)
        random_card_json = random_card_response.json()
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

        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.datetime.now()
        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id) VALUES (%s, %s, %s, %s, %s)", ("random-commander", random_card_json["name"], now, interaction.user.name, interaction.user.id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()

        embed = GenerateCardDetails(card_type, random_card_json, random_color)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='momir', description="Pulls a random monster with the selected mana value from Scryfall.")
    @app_commands.checks.cooldown(1.0,3.0)
    async def momir(self, interaction: discord.Interaction, manavalue: str):

        try:  
                arg1 = str(manavalue)
                momir_card_url = scryfall_url + "cards/random?q=t%3Acreature+mv%3A" + arg1 + " not:funny"
                momir_card_response = requests.get(momir_card_url)
                momir_card_json = momir_card_response.json()
                card_type = momir_card_json["type_line"]
        except:
                await interaction.response.send_message("It looks like there wasn't any card with that mana value. Please try another one.")
                return

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.datetime.now()
        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id) VALUES (%s, %s, %s, %s, %s)", ("momir", momir_card_json["name"], now, interaction.user.name, interaction.user.id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()

        embed = GenerateCardDetails(card_type, momir_card_json, random_color)
                
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='jhoira', description="Pulls three random instant or sorcery cards from Scryfall. Requires you to type Sorcery or Instant")
    @app_commands.checks.cooldown(1.0,3.0)
    @app_commands.describe(cardtype="Select your requested card type")
    @app_commands.choices(
        cardtype=[
            app_commands.Choice(name="Instant", value="Instant"),
            app_commands.Choice(name="Sorcery", value="Sorcery")
        ]
    )
    async def jhoira(self, interaction: discord.Interaction, cardtype: str):

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        arg1 = str(cardtype)

        try:  
                jhoira_card_url_1 = scryfall_url + "cards/random?q=t%3A" + arg1 + " -t:enchantment -t:creature -t:artifact -t:planeswalker (game:paper) not:funny"
                jhoira_card_url_2 = scryfall_url + "cards/random?q=t%3A" + arg1 + " -t:enchantment -t:creature -t:artifact -t:planeswalker (game:paper) not:funny"
                jhoira_card_url_3 = scryfall_url + "cards/random?q=t%3A" + arg1 + " -t:enchantment -t:creature -t:artifact -t:planeswalker (game:paper) not:funny"
                jhoira_card_response_1 = requests.get(jhoira_card_url_1)
                jhoira_card_response_2 = requests.get(jhoira_card_url_2)
                jhoira_card_response_3 = requests.get(jhoira_card_url_3)
                jhoira_card_json_1 = jhoira_card_response_1.json()
                jhoira_card_json_2 = jhoira_card_response_2.json()
                jhoira_card_json_3 = jhoira_card_response_3.json()
                card_type_1 = jhoira_card_json_1["type_line"]
                card_type_2 = jhoira_card_json_2["type_line"]
                card_type_3 = jhoira_card_json_3["type_line"]
        except:
                await interaction.response.send_message("It looks like there was an issue. Please contact the administrator if you continue to have issues.")
                return
        
        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.datetime.now()
        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id) VALUES (%s, %s, %s, %s, %s)", ("jhoira", jhoira_card_json_1["name"] + " and " + jhoira_card_json_2["name"] + " and " + jhoira_card_json_3["name"], now, interaction.user.name, interaction.user.id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()

        embed1 = GenerateCardDetails(card_type_1, jhoira_card_json_1, random_color)      
        embed2 = GenerateCardDetails(card_type_2, jhoira_card_json_2, random_color) 
        embed3 = GenerateCardDetails(card_type_3, jhoira_card_json_3, random_color)

        embeds = []
        embeds.append(embed1)
        embeds.append(embed2)
        embeds.append(embed3)
        await interaction.response.send_message(embeds=embeds)


    @app_commands.command(name='post-mojhosto', description="Posts a description of the MoJhoSto format.")
    @app_commands.checks.cooldown(1.0,3.0)
    async def postmojhosto(self, interaction: discord.Interaction):

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        momir_card_url = scryfall_url + "f5ed5ad3-b970-4720-b23b-308a25f42887"
        jhoira_card_url = scryfall_url + "cd1c87eb-4974-4160-91bd-681e0a75a98e"
        stonehewer_card_url = scryfall_url + "d5cdf535-56fb-4f92-abf0-237aa6e081b0"
        print(momir_card_url)
        print(jhoira_card_url)
        print(stonehewer_card_url)

        momir_card_response = requests.get(momir_card_url)
        momir_card_json = momir_card_response.json()
        print("Got momir")
        print(momir_card_response)
        print(momir_card_json)

        jhoira_card_response = requests.get(jhoira_card_url)
        jhoira_card_json = jhoira_card_response.json()
        print("got jhoira")

        stonehewer_card_response = requests.get(stonehewer_card_url)
        stonehewer_card_json = stonehewer_card_response.json()
        print("got stonehewer")

        card_type = momir_card_json["type_line"]
        print(card_type)

        db_conn = psycopg2.connect(database_url, sslmode='require')
        db_cursor = db_conn.cursor()
        now = datetime.datetime.now()
        db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id) VALUES (%s, %s, %s, %s, %s)", ("post-mojhosto", "posted mojhosto", now, interaction.user.name, interaction.user.id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()

        #explanation_string = discord.Embed(title="MoJhoSto Explanation", description="MoJhoSto is a format of Magic the Gathering that originated on Magic Online. Using the Vanguard cards for Momir Vig, Simic Visionary, Jhoira of the Ghitu, and Stonehewer Giant and a deck of 60 basic lands to play with 20 life for each player. The players play the game by utilizing the abilities of the Vanguard cards to create creatures, cast spells, and make equipment. You do not play with the life total/hand size changes listed on the cards. There is also the alternative and more well known format of Momir Basic which is played using only the Momir Vig Vanguard ability but is otherwise identical.", color=random_color)
        embed_momir = GenerateCardDetails(card_type, momir_card_json, random_color)
        #embed_jhoira = GenerateCardDetails(card_type, jhoira_card_json, random_color)
        #embed_stonehewer = GenerateCardDetails(card_type, stonehewer_card_json, random_color)

        embeds = []
        #embeds.append(explanation_string)
        embeds.append(embed_momir)
        #embeds.append(embed_jhoira)
        #embeds.append(embed_stonehewer)

        await interaction.response.send_message(embeds=embeds)

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
        card_response = mtg_session.get(mtg_card_url)

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
