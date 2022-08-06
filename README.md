# BakiBot
The code for a personal discord bot built in Python. Mainly used for picking random things from a list as a result of indecisiveness when it comes to picking the game of the night.

## Requirements
Tested with [Python 3.8.3](https://www.python.org/downloads/release/python-383/). It should work with any recent version. 

## Commands
Current command prefix is set to !

- Choose: Randomly select an option from the provided options. e.g. !choose Lead Salt Diesel
- Color: Post a random color and display the Hex and RGB values and an example of the color. 
- Diceroll: Roll a die of the size of your choosing. e.g. !diceroll 20
- Gamelist: Posts the current game list. This can be modified in util.py. 
- Help: Sends a direct message with the command list to the user requesting the help. 
- Randombaki: Posts a random quote from the Manga/Anime series [Baki the Grappler](https://en.wikipedia.org/wiki/Baki_the_Grappler). These are located in util.py. 
- Randomgame: Pick a random game from the full game list. 
- tts: Send a TTS message to all users. 
