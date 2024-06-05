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
- Choose: Randomly select an option from the provided options. e.g. !choose Lead Salt Diesel
- Color: Post a random color and display the Hex and RGB values and an example of the color. 
- Diceroll: Roll a die of the size of your choosing. e.g. !diceroll 20
- dmhelp: Sends you a message of the current commands available
- eightball or 8ball: Ask the magic 8 Ball a question. 
- findthem: Baki will call someone in the server mean names.
- Gamelist: Posts the current game list. This can be modified in games.py. Currently set to be configured per server.
- Help: Posts the content of the help command in the current channel. 
- Randombaki: Posts a random quote from the Manga/Anime series [Baki the Grappler](https://en.wikipedia.org/wiki/Baki_the_Grappler). These are located in random.py. 
- Randomgame: Pick a random game from the full game list. This can be modified in games.py. Currently set to be configured per server.
- Weather: Pulls the current weather for a specified city using OpenWeatherMap.org
- whoisit: Baki will choose from a list you provide and call someone mean names.

### Magic the Gathering Commands
- Jhoira: Generate three random instants or sorceries for use in MoJhoSto.
- MoJhoSto: A short explanation of the MoJhoSto format.
- Momir: Generate a random creature for use in Momir Basic.
- Randomcommander: Pick a random EDH legal Legendary Creature.
- Randommtg: Pick a random Magic the Gathering card.
- Stonehewer: Generate a random equipment for use in MoJhoSto.


### Pokemon Commands
- Pokemon: Highlight a pokemon by using either it's Pokedex number or it's name.
- Randompokemon: Picks a random pokemon from the list of all released ones. 