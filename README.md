# BakiBot
The code for a personal discord bot built in Python. Mainly used for picking random things from a list as a result of indecisiveness when it comes to picking the game of the night.

## Requirements
Tested with [Python 3.8.3](https://www.python.org/downloads/release/python-383/). It should work with any recent version. 

## Commands
Current command prefix is set to !

- Choose: Randomly select an option from the provided options. e.g. !choose Lead Salt Diesel
- Color: Post a random color and display the Hex and RGB values and an example of the color. 
- Diceroll: Roll a die of the size of your choosing. e.g. !diceroll 20
- eightball or 8ball: Ask the magic 8 Ball a question. 
- Gamelist: Posts the current game list. This can be modified in games.py. Currently set to be configured per server.
- Help: Sends a direct message with the command list to the user requesting the help. 
- Join: Have Baki Join a voice chat channel. 
- Pokemon: Highlight a pokemon by using either it's Pokedex number or it's name.
- PostHelp: Posts the content of the help command in the current channel. 
- Randombaki: Posts a random quote from the Manga/Anime series [Baki the Grappler](https://en.wikipedia.org/wiki/Baki_the_Grappler). These are located in random.py. 
- Randomcommander: Pick a random EDH legal Legendary Creature.
- Randomgame: Pick a random game from the full game list. This can be modified in games.py. Currently set to be configured per server.
- Randommtg: Pick a random Magic the Gathering card.
- Randompokemon: Picks a random pokemon from the list of all released ones. 
- Stop: Stop the current Baki audio stream. 
- Stream: Have Baki stream the audio from a Youtube video. Must use Join first. 
- tts: Send a TTS message to all users. 
- Volume: Set Baki's volume for voice chat. 
- Weather: Pulls the current weather for a specified city using OpenWeatherMap.org
