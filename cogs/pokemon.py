import discord
import sys
import random
import os
import os.path
import requests
import requests_cache
import psycopg2
import datetime
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
from discord.ext.commands import Context

load_dotenv()
owner_id = os.getenv('DISCORD_OWNERID')
#This includes everything up through Paradox.
#max_pokemon_count = 1301
pokemon_api_url = "https://pokeapi.co/api/v2/"
database_url = os.environ['DATABASE_URL']
poke_session = requests_cache.CachedSession('poke_cache', expire_after=1800)

def DatabaseLogging(command_name, database_value, user_name, user_id, guild):
    db_conn = psycopg2.connect(database_url, sslmode='require')
    db_cursor = db_conn.cursor()
    now = datetime.datetime.now()
    db_cursor.execute("INSERT INTO bakibot.log (command, logged_text, timestamp, username, user_id, guild_id) VALUES (%s, %s, %s, %s, %s, %s)", (command_name, database_value, now, user_name, user_id, guild))
    db_conn.commit()
    db_cursor.close()
    db_conn.close()

def GeneratePokemonDetails(random_color,ResponseJSON,pokemon_id):
            #Start pulling some basic information in that will always be simple to parse.
            #We remove the dashes and replace them with spaces so that alternate forms and some specific Paradox pokemon look nicer.
            #Then we capitalize all the words in the name
            pokemon_name = ResponseJSON["name"]
            try:
                pokemon_name = pokemon_name.replace('-', ' ').title()
            except:
                pokemon_name = pokemon_name.title()

            #This is just for troubleshooting purposes to know what pokemon is causing issues. 
            #print(pokemon_name)

            Pokemon_sprite = ResponseJSON["sprites"]["other"]["official-artwork"]["front_default"]
            pokemon_first_type = ResponseJSON["types"][0]["type"]["name"]
            pokemon_first_type = pokemon_first_type.capitalize()
            pokemon_height = ResponseJSON["height"]
            #The height is in decimeters so it has to be converted. 
            pokemon_height = pokemon_height * 3.937
            pokemon_height = round(pokemon_height, 2)
            pokemon_weight = ResponseJSON["weight"]
            #Weight is in hecagrams so it has tdo be taken care of uas well
            pokemon_weight = pokemon_weight / 4.536
            pokemon_weight = round(pokemon_weight, 2)

            #Now we start querying another API URL for some fun details like pokedex entries
            pokemon_species = ResponseJSON["species"]["url"]
            species_api_response = poke_session.get(pokemon_species)
            species_response_json = species_api_response.json()
            
            #Genus is the "Title" of the pokemon. We have to run through an array since the english translation isn't always in the same place. 
            #There can also be multiple english ones so we are just getting the first one. 
            #Sometimes there isn't even an english one in the API yet so we just have a generic text in that case.
            pokemon_genus_language_id = "0"
            pokemon_genus_array_selector = -1
            while pokemon_genus_language_id != "en":
                pokemon_genus_array_selector = pokemon_genus_array_selector + 1
                try:
                    pokemon_genus_language_id = species_response_json["genera"][pokemon_genus_array_selector]["language"]["name"]
                except:
                    pokemon_genus_array_selector = 101
                
                if pokemon_genus_array_selector > 100:
                    pokemon_genus = "No English Pokemon Genus Available"
                    break
            
            #Flavor text has the same issue as genus does. 
            pokemon_flavor_text_language_id = "0"
            pokemon_flavor_text_array_selector = -1
            while pokemon_flavor_text_language_id != "en":
                pokemon_flavor_text_array_selector = pokemon_flavor_text_array_selector + 1
                try:
                    pokemon_flavor_text_language_id = species_response_json["flavor_text_entries"][pokemon_flavor_text_array_selector]["language"]["name"]
                except:
                    pokemon_flavor_text_array_selector = 101

                if pokemon_flavor_text_array_selector > 100:
                    pokemon_flavor_text = "No English Pokedex Entry Available"
                    break
            
            #This sets the text to use the one that was selected by the loop. Just to make sure we don't miss it. 
            if pokemon_flavor_text_array_selector < 100:
                pokemon_flavor_text = species_response_json["flavor_text_entries"][pokemon_flavor_text_array_selector]["flavor_text"]
                
            if pokemon_genus_array_selector < 100:
                pokemon_genus = species_response_json["genera"][pokemon_genus_array_selector]["genus"]
            
            #This is the first generation the Pokemon appeared in. 
            pokemon_generation = species_response_json["generation"]["name"]
            pokemon_generation = pokemon_generation[11:].upper()
            
            #Now we are getting details about the evolution tree for pokemon. This starts to get difficult. 
            pokemon_chain = species_response_json["evolution_chain"]["url"]
            pokemon_evolution_chain_api_response = poke_session.get(pokemon_chain)
            pokemon_evolution_chain_response_json = pokemon_evolution_chain_api_response.json()

            try:
                pokemon_evolve_from = species_response_json["evolves_from_species"]["name"]
            except:
                pokemon_evolve_from = 0
            
            try:
                pokemon_second_type = ResponseJSON["types"][1]["type"]["name"]
            except:
                pokemon_second_type = 0
            
            try:
                pokemon_evolves_to = pokemon_evolution_chain_response_json["chain"]["evolves_to"][0]["species"]["name"]
            except:
                pokemon_evolves_to = 0

            if pokemon_genus == "No English Pokemon Genus Available":
                embed = discord.Embed(title=f"{pokemon_name}",
                color=random_color)
            else:
                embed = discord.Embed(title=f"{pokemon_name}: The {pokemon_genus}",
                color=random_color)
            
            embed.set_thumbnail(url=Pokemon_sprite)
            embed.add_field(name="Pokedex Entry:", value=f"{pokemon_flavor_text}", inline=False)
            embed.add_field(name="Pokedex Number:", value=f"{pokemon_id}", inline=False)
            embed.add_field(name="Original Generation:", value=f"{pokemon_generation}", inline=False)
            
            #This set of responses checks if our chosen pokemon is legendary, mythical, or a baby form. 
            pokemon_legendary_check = species_response_json["is_legendary"]
            pokemon_mythical_check = species_response_json["is_mythical"]
            pokemon_baby_check = species_response_json["is_baby"]

            if pokemon_legendary_check == True:
                embed.add_field(name="Classification:", value=f"Legendary", inline=False)

            if pokemon_mythical_check == True:
                embed.add_field(name="Classification:", value=f"Mythical", inline=False)

            if pokemon_baby_check == True:
                embed.add_field(name="Classification:", value=f"Baby", inline=False)

            #Evolve from is so much easier then To.
            if pokemon_evolve_from != 0:
                pokemon_evolve_from = pokemon_evolve_from.capitalize()
                embed.add_field(name="Evolves From:", value=f"{pokemon_evolve_from}", inline=False)

            #I'm sure there are numerous better ways to do this. Unfortunately I don't know any of them. 
            #I did try to build one that would be able to work around any scenario but I just kept running into brick walls. 
            #So as a result, I just hardcode ones that I know have bizarre situations that are pretty rare thankfully. 
            #This is a bit hacky but I think overall the number of edge cases is small enough that it isn't an issue really. 
            #Much of this comes down to how the API sorts the evolution tree which causes a ton of issues. 
            if pokemon_evolves_to != 0:
                pokemon_evolves_to = pokemon_evolves_to.capitalize()
                if pokemon_name == "Silcoon":
                    pokemon_evolves_to = "Beautifly"
                    embed.add_field(name="Evolves Into:", value=f"{pokemon_evolves_to}", inline=False)
                
                elif pokemon_name == "Cascoon":
                    pokemon_evolves_to = "Dustox"
                    embed.add_field(name="Evolves Into:", value=f"{pokemon_evolves_to}", inline=False)
                    
                elif pokemon_name == "Burmy":
                    pokemon_evolves_to = "♀ Wormadam or ♂ Mothrim"
                    embed.add_field(name="Evolves Into:", value=f"{pokemon_evolves_to}", inline=False)
                    
                elif pokemon_name == "Eevee":
                    pokemon_evolves_to = "Flareon, Jolteon, Vaporean, Umbreon, Espeon, Glaceon, Leafeon, or Sylveon"
                    embed.add_field(name="Evolves Into:", value=f"{pokemon_evolves_to}", inline=False)
                    
                elif pokemon_name == "Wurmple":
                    pokemon_evolves_to = "Silcoon or Cascoon"
                    embed.add_field(name="Evolves Into:", value=f"{pokemon_evolves_to}", inline=False)
                
                elif pokemon_name == "Hitmonchan" or pokemon_name == "Hitmonlee":
                    pass
                
                elif pokemon_name == "Shedinja" or pokemon_name == "Ninjask":
                    pass
                
                elif pokemon_name == "Nincada":
                    pokemon_evolves_to = "Ninjask and Shedinja with an extra Pokeball"
                    embed.add_field(name="Evolves Into:", value=f"{pokemon_evolves_to}", inline=False)

                elif "Urshifu" in pokemon_name:
                    pass
                
                #Because of the way the API has everything setup. The first evolves to you might run into could be themselves. 
                #So we have to dig deeper for a different one.
                elif pokemon_evolves_to == pokemon_name:
                    try:
                        pokemon_evolves_to = pokemon_evolution_chain_response_json["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
                        #Even after digging deeper though. Sometimes it is still the same name. 
                        if pokemon_evolves_to == pokemon_name:
                            pass
                                
                        else:
                            pokemon_evolves_to = pokemon_evolves_to.capitalize()
                            embed.add_field(name="Evolves Into:", value=f"{pokemon_evolves_to}", inline=False)
                    except:
                        pass
                
                elif pokemon_evolves_to == pokemon_evolve_from:
                    pass
                
                else:
                    embed.add_field(name="Evolves Into:", value=f"{pokemon_evolves_to}", inline=False)

            #Thankfully Gamefreak hasn't come out with tri-typing yet. 
            if pokemon_second_type != 0:
                pokemon_second_type = pokemon_second_type.capitalize()
                embed.add_field(name="Type:", value=f"{pokemon_first_type} / {pokemon_second_type}", inline=False)
                
            else:
                embed.add_field(name="Type", value=f"{pokemon_first_type}", inline=False) 
                
            embed.add_field(name="Height (in):", value=f"{pokemon_height}", inline=False)
            embed.add_field(name="Weight (lbs):", value=f"{pokemon_weight}", inline=False)
            embed.set_footer(text= "Data provided by pokeapi.co", icon_url="https://raw.githubusercontent.com/PokeAPI/media/master/logo/pokeapi_256.png")

            return embed

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def ownercheck(ctx):
        return ctx.message.author.id == int(owner_id)

    @app_commands.command(name='random-pokemon', description="Pick a random Pokemon.")
    @app_commands.checks.cooldown(1.0,3.0)
    async def randompokemon(self, interaction: discord.Interaction):
        #Start pulling in the initial API information
        max_pokemon_count_url = pokemon_api_url + "pokemon?limit=100000&offset=0"
        max_pokemon_response = requests.get(max_pokemon_count_url)
        max_pokemon_json = max_pokemon_response.json()
        max_pokemon_count = int(max_pokemon_json["count"]) - 1
        random_pokemon_id = random.randint(0, max_pokemon_count)
        #complete_api_url = pokemon_api_url + "pokemon/" + str(random_pokemon_id)
        complete_api_url = max_pokemon_json["results"][random_pokemon_id]["url"]
        Response = poke_session.get(complete_api_url)
        ResponseJSON = Response.json()

        DatabaseLogging("random-pokemon", ResponseJSON["name"], interaction.user.name, interaction.user.id, interaction.guild_id)

        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed = GeneratePokemonDetails(random_color,ResponseJSON, pokemon_id=random_pokemon_id)
        
        await interaction.response.send_message(embed=embed)

    #This command is built the same as the random one but it allows you to put in either a name or pokemon id. 
    @app_commands.command(name='pokemon', description="Pull the details of a specific Pokemon from PokeAPI")
    @app_commands.checks.cooldown(1.0,3.0)
    @app_commands.describe(pokemonidentity="Input the name or pokedex number you wish to query with")
    async def pokemon(self, interaction: discord.Interaction, pokemonidentity: str):
        #Here we give the possibility for multiple entries. This is to allow for pokemon with spaces in their names like Iron Leaves or Urshifu Single Strike. 
        #We also set the pokemonid to lowercase because the api doesn't accept it with capital letters in it.
        PokemonID = '-'.join(pokemonidentity)
        PokemonID = str(PokemonID).lower()
        
        #We check if there is actually a response from the API since we are relying on user input. 
        try:
            complete_api_url = pokemon_api_url + "pokemon/" + str(PokemonID)
            Response = poke_session.get(complete_api_url)
            ResponseJSON = Response.json()
        except:
            await interaction.response.send_message("Sorry, I don't recognize that Pokemon. Please try something else.")
            return
        
        random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        DatabaseLogging("pokemon", ResponseJSON["name"], interaction.user.name, interaction.user.id, interaction.guild_id)

        embed = GeneratePokemonDetails(random_color,ResponseJSON, PokemonID)

        await interaction.response.send_message(embed=embed)
  
async def setup(bot):
    await bot.add_cog(Pokemon(bot))
