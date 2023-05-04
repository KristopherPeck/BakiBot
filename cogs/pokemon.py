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

load_dotenv()
ownerID = os.getenv('DISCORD_OWNERID')
#This includes everything up through Paradox.
maxPokemon = 1010
PokemonAPIURL = "https://pokeapi.co/api/v2/"

#Implements a cache for responses
requests_cache.install_cache('db/pokemon_cache', backend='sqlite', expire_after=180)

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def ownercheck(ctx):
        return ctx.message.author.id == int(ownerID)

    @commands.command(name='randompokemon')
    async def randompokemon(self, ctx):
        #Start pulling in the initial API information
        RandomPokemonID = random.randint(1, maxPokemon)
        CompleteURL = PokemonAPIURL + "pokemon/" + str(RandomPokemonID)
        Response = requests.get(CompleteURL)
        ResponseJSON = Response.json()
        RandomColor = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        channel = ctx.message.channel
        
        async with channel.typing():
            #Start pulling some basic information in that will always be simple to parse.
            #We remove the dashes and replace them with spaces so that alternate forms and some specific Paradox pokemon look nicer.
            #Then we capitalize all the words in the name
            try:
                PokemonName = PokemonName.replace('-', ' ').title()
            except:
                PokemonName = PokemonName.title()

            #This is just for troubleshooting purposes to know what pokemon is causing issues. 
            #print(PokemonName)

            PokemonSprite = ResponseJSON["sprites"]["other"]["official-artwork"]["front_default"]
            PokemonFirstType = ResponseJSON["types"][0]["type"]["name"]
            PokemonFirstType = PokemonFirstType.capitalize()
            PokemonHeight = ResponseJSON["height"]
            #The height is in decimeters so it has to be converted. 
            PokemonHeight = PokemonHeight * 3.937
            PokemonHeight = round(PokemonHeight, 2)
            PokemonWeight = ResponseJSON["weight"]
            #Weight is in hecagrams so it has tdo be taken care of uas well
            PokemonWeight = PokemonWeight / 4.536
            PokemonWeight = round(PokemonWeight, 2)

            #Now we start querying another API URL for some fun details like pokedex entries
            PokemonSpecies = ResponseJSON["species"]["url"]
            SpeciesResponse = requests.get(PokemonSpecies)
            SpeciesResponseJSON = SpeciesResponse.json()
            
            #Genus is the "Title" of the pokemon. We have to run through an array since the english translation isn't always in the same place. 
            #There can also be multiple english ones so we are just getting the first one. 
            #Sometimes there isn't even an english one in the API yet so we just have a generic text in that case.
            PokemonGenusLanguage = "0"
            GenusArraySelector = -1
            while PokemonGenusLanguage != "en":
                GenusArraySelector = GenusArraySelector + 1
                try:
                    PokemonGenusLanguage = SpeciesResponseJSON["genera"][GenusArraySelector]["language"]["name"]
                except:
                    GenusArraySelector = 101
                
                if GenusArraySelector > 100:
                    PokemonGenus = "No English Pokemon Genus Available"
                    break
            
            #Flavor text has the same issue as genus does. 
            PokemonFlavorTextLanguage = "0"
            FlavorArraySelector = -1
            while PokemonFlavorTextLanguage != "en":
                FlavorArraySelector = FlavorArraySelector + 1
                try:
                    PokemonFlavorTextLanguage = SpeciesResponseJSON["flavor_text_entries"][FlavorArraySelector]["language"]["name"]
                except:
                    FlavorArraySelector = 101

                if FlavorArraySelector > 100:
                    PokemonFlavorText = "No English Pokedex Entry Available"
                    break
            
            #This sets the text to use the one that was selected by the loop. Just to make sure we don't miss it. 
            if FlavorArraySelector < 100:
                PokemonFlavorText = SpeciesResponseJSON["flavor_text_entries"][FlavorArraySelector]["flavor_text"]
                
            if GenusArraySelector < 100:
                PokemonGenus = SpeciesResponseJSON["genera"][GenusArraySelector]["genus"]
            
            #This is the first generation the Pokemon appeared in. 
            PokemonGeneration = SpeciesResponseJSON["generation"]["name"]
            PokemonGeneration = PokemonGeneration[11:].upper()
            
            #Now we are getting details about the evolution tree for pokemon. This starts to get difficult. 
            PokemonChain = SpeciesResponseJSON["evolution_chain"]["url"]
            ChainResponse = requests.get(PokemonChain)
            ChainResponseJSON = ChainResponse.json()

            try:
                PokemonEvolveFrom = SpeciesResponseJSON["evolves_from_species"]["name"]
            except:
                PokemonEvolveFrom = 0
            
            try:
                PokemonSecondType = ResponseJSON["types"][1]["type"]["name"]
            except:
                PokemonSecondType = 0
            
            try:
                PokemonEvolvesTo = ChainResponseJSON["chain"]["evolves_to"][0]["species"]["name"]
            except:
                PokemonEvolvesTo = 0

            if PokemonGenus == "No English Pokemon Genus Available":
                embed = discord.Embed(title=f"{PokemonName}",
                color=RandomColor)
            else:
                embed = discord.Embed(title=f"{PokemonName}: The {PokemonGenus}",
                color=RandomColor)
            
            embed.set_thumbnail(url=PokemonSprite)
            embed.add_field(name="Pokedex Entry:", value=f"{PokemonFlavorText}", inline=False)
            embed.add_field(name="Pokedex Number:", value=f"{RandomPokemonID}", inline=False)
            embed.add_field(name="Original Generation:", value=f"{PokemonGeneration}", inline=False)
            
            #This set of responses checks if our chosen pokemon is legendary, mythical, or a baby form. 
            LegendaryCheck = SpeciesResponseJSON["is_legendary"]
            MythicalCheck = SpeciesResponseJSON["is_mythical"]
            BabyCheck = SpeciesResponseJSON["is_baby"]

            if LegendaryCheck == True:
                embed.add_field(name="Classification:", value=f"Legendary", inline=False)

            if MythicalCheck == True:
                embed.add_field(name="Classification:", value=f"Mythical", inline=False)

            if BabyCheck == True:
                embed.add_field(name="Classification:", value=f"Baby", inline=False)

            #Evolve from is so much easier then To.
            if PokemonEvolveFrom != 0:
                PokemonEvolveFrom = PokemonEvolveFrom.capitalize()
                embed.add_field(name="Evolves From:", value=f"{PokemonEvolveFrom}", inline=False)

            #I'm sure there are numerous better ways to do this. Unfortunately I don't know any of them. 
            #I did try to build one that would be able to work around any scenario but I just kept running into brick walls. 
            #So as a result, I just hardcode ones that I know have bizarre situations that are pretty rare thankfully. 
            #This is a bit hacky but I think overall the number of edge cases is small enough that it isn't an issue really. 
            #Much of this comes down to how the API sorts the evolution tree which causes a ton of issues. 
            if PokemonEvolvesTo != 0:
                PokemonEvolvesTo = PokemonEvolvesTo.capitalize()
                if PokemonName == "Silcoon":
                    PokemonEvolvesTo = "Beautifly"
                    embed.add_field(name="Evolves Into:", value=f"{PokemonEvolvesTo}", inline=False)
                
                elif PokemonName == "Cascoon":
                    PokemonEvolvesTo = "Dustox"
                    embed.add_field(name="Evolves Into:", value=f"{PokemonEvolvesTo}", inline=False)
                    
                elif PokemonName == "Burmy":
                    PokemonEvolvesTo = "♀ Wormadam or ♂ Mothrim"
                    embed.add_field(name="Evolves Into:", value=f"{PokemonEvolvesTo}", inline=False)
                    
                elif PokemonName == "Eevee":
                    PokemonEvolvesTo = "Flareon, Jolteon, Vaporean, Umbreon, Espeon, Glaceon, Leafeon, or Sylveon"
                    embed.add_field(name="Evolves Into:", value=f"{PokemonEvolvesTo}", inline=False)
                    
                elif PokemonName == "Wurmple":
                    PokemonEvolvesTo = "Silcoon or Cascoon"
                    embed.add_field(name="Evolves Into:", value=f"{PokemonEvolvesTo}", inline=False)
                
                elif PokemonName == "Hitmonchan" or PokemonName == "Hitmonlee":
                    pass
                
                elif PokemonName == "Shedinja" or PokemonName == "Ninjask":
                    pass
                
                elif PokemonName == "Nincada":
                    PokemonEvolvesTo = "Ninjask and Shedinja with an extra Pokeball"
                    embed.add_field(name="Evolves Into:", value=f"{PokemonEvolvesTo}", inline=False)

                elif "Urshifu" in PokemonName:
                    pass
                
                #Because of the way the API has everything setup. The first evolves to you might run into could be themselves. 
                #So we have to dig deeper for a different one.
                elif PokemonEvolvesTo == PokemonName:
                    try:
                        PokemonEvolvesTo = ChainResponseJSON["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
                        #Even after digging deeper though. Sometimes it is still the same name. 
                        if PokemonEvolvesTo == PokemonName:
                            pass
                                
                        else:
                            PokemonEvolvesTo = PokemonEvolvesTo.capitalize()
                            embed.add_field(name="Evolves Into:", value=f"{PokemonEvolvesTo}", inline=False)
                    except:
                        pass
                
                elif PokemonEvolvesTo == PokemonEvolveFrom:
                    pass
                
                else:
                    embed.add_field(name="Evolves Into:", value=f"{PokemonEvolvesTo}", inline=False)

            #Thankfully Gamefreak hasn't come out with tri-typing yet. 
            if PokemonSecondType != 0:
                PokemonSecondType = PokemonSecondType.capitalize()
                embed.add_field(name="Type:", value=f"{PokemonFirstType} / {PokemonSecondType}", inline=False)
                
            else:
                embed.add_field(name="Type", value=f"{PokemonFirstType}", inline=False) 
                
            embed.add_field(name="Height (in):", value=f"{PokemonHeight}", inline=False)
            embed.add_field(name="Weight (lbs):", value=f"{PokemonWeight}", inline=False)
            
                
            await channel.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Util(bot))