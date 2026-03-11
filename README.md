# BakiBot
The code for a personal discord bot built in Python. Originally developed because finding a bot that let you pick from a list was harder then it sounded. It's expanded from there to whatever ideas I have that I want to implement.

## Requirements
Tested with [Python 3.8.3](https://www.python.org/downloads/release/python-383/). It should work with any recent version. 

## Cooldown
There is a short cooldown implemented on commands. This can be removed from the commands by removing the @commands.cooldown() from the commands code.

## Commands
Current command prefix is set to !

### General Commands
- choose: Randomly select an option from the provided options. e.g. !choose Lead Salt Diesel
- color: Post a random color and display the Hex and RGB values and an example of the color. 
- dieroll: Roll a die of the size of your choosing. e.g. /diceroll 20
- dmhelp: Sends you a message of the current commands available
- eightball or 8ball: Ask the magic 8 Ball a question. 
- findthem: Baki will call someone in the server mean names.
- flip: Flip a coin
- list-commands: Post the command list
- lunchtime: Picks3 random restaurant from a list for lunchtime."
- random-baki: Posts a random quote from the Manga/Anime series [Baki the Grappler](https://en.wikipedia.org/wiki/Baki_the_Grappler). These are located in random.py. 
- random-game: Pick a random game from the full game list. 
- rolldie: Roll a die of the specified size.
- rolldice: Roll a set of dice in NdT format with N being the number of dice and T being how many sides are on the dice. Just like this: /roll 2d4
- source: Links BakiBots source code
- trivia: Posts a random trivia question
- weather: Pulls the current weather for a specified city using OpenWeatherMap.org
- whisper-commands: Whispers the current commands to the user who requested them
- whoisit: Baki will choose from a list you provide and call someone mean names.

### Magic the Gathering Commands
- jhoira: Generate three random instants or sorceries for use in MoJhoSto.
- mojhosto: A short explanation of the MoJhoSto format.
- momir: Generate a random creature for use in Momir Basic or MoJhoSto.
- mtg: Search a specific Magic the Gathering card. Just like this: /mtg Jace Beleren
- random-commander: Pick a random EDH legal Legendary Creature.
- random-mtg: Pick a random Magic the Gathering card.
- stonehewer: Generate a random equipment for use in MoJhoSto.

### Pokemon Commands
- pokemon: Highlight a pokemon by using either it's Pokedex number or it's name.
- random-pokemon: Picks a random pokemon from the list of all released ones. 