# BakiBot
The code for a personal discord bot built in Python. Originally developed because finding a bot that let you pick from a list was harder then it sounded. It's expanded from there to whatever ideas I have that I want to implement.

## Requirements
Tested with [Python 3.8.3](https://www.python.org/downloads/release/python-383/). It should work with any recent version. 

## Cooldown
There is a short cooldown implemented on commands. This can be removed from the commands by removing the @commands.cooldown() from the commands code.

## Commands
Current command prefix is set to !

### Audio Commands
Note: The commands tied to playing music in a voice channel is currently broken. 
- join: Force Baki to join a voice channel.
- stop: Stop the current Baki stream.
- stream: Play the requested video stream in the current voice channel.
- tts: Send a TTS message to all users. 
- Volume: Set Baki's volume for voice chat. 

### General Commands
- choose: Randomly select an option from the provided options. e.g. !choose Lead Salt Diesel
- color: Post a random color and display the Hex and RGB values and an example of the color. 
- dieroll: Roll a die of the size of your choosing. e.g. !diceroll 20
- dmhelp: Sends you a message of the current commands available
- eightball or 8ball: Ask the magic 8 Ball a question. 
- findthem: Baki will call someone in the server mean names.
- flip: Flip a coin
- gamelist: Posts the current game list. This can be modified in games.py. Currently set to be configured per server.
- help: Posts the content of the help command in the current channel. You can also use the following prefixes to get specific lists: audio, gen, mtg, pokemon
- lunchtime: Picks a random restaurant from a list for lunchtime. 
- randombaki: Posts a random quote from the Manga/Anime series [Baki the Grappler](https://en.wikipedia.org/wiki/Baki_the_Grappler). These are located in random.py. 
- randomgame: Pick a random game from the full game list. This can be modified in games.py. Currently set to be configured per server.
- roll: Roll a set of dice in NdT format with N being the number of dice and T being how many sides are on the dice. Just like this: !roll 2d4
- source: Links BakiBots source code
- trivia: Posts a random trivia question
- weather: Pulls the current weather for a specified city using OpenWeatherMap.org
- whoisit: Baki will choose from a list you provide and call someone mean names.

### Magic the Gathering Commands
- jhoira: Generate three random instants or sorceries for use in MoJhoSto.
- mojhosto: A short explanation of the MoJhoSto format.
- momir: Generate a random creature for use in Momir Basic or MoJhoSto.
- mtg: Search a specific Magic the Gathering card. Just like this: !mtg Jace Beleren
- randomcommander: Pick a random EDH legal Legendary Creature.
- randommtg: Pick a random Magic the Gathering card.
- stonehewer: Generate a random equipment for use in MoJhoSto.

### Pokemon Commands
- pokemon: Highlight a pokemon by using either it's Pokedex number or it's name.
- randompokemon: Picks a random pokemon from the list of all released ones. 