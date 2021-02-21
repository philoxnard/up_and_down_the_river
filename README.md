# up_and_down_the_river

Up and Down the River is an online multiplayer web app modeled after the card game of the same name. The back-end is written in Python utilizing the Flask framework, and the front end combines HTML, CSS, and Javascript, as well as the Socket.IO library to allow for multiple players to join.

## How to Play

Each round, the players will be given a hand of cards, as well as being shown that round's trump card. Before playing, each player will, in turn, make a bid on how many tricks they think they will win during the round. Playeres earn a point for each trick they win, plus an additional 10 points if they end the round with the same amount of tricks as they bid earlier.

Rounds play out with each player, in turn, playing a card. Players must follow suit with whoever played the first card in the trick if possible. When all players have played their card in the trick, the trick will be awarded to whoever played the highest card of the led suit. However, if a card in the trick is the same suit as the trump card, that card will take priority over the led suit. If there are multiple trump cards in the suit, the winning card is the highest trump.

Successive rounds have different hand sizes. The first round has a hand size of one, the second round a hand size of two, following the same pattern up to seven. After the seventh round, though, the following round has a six card hand, followed by a five card hand, following that same pattern back down to one. After the second one-card hand has been played, the game is over and the player with the highest score wins.

## Project Goals

Through this project, I aimed to gain a deeper understanding of multiple different facets of web design: How to use Python to create a functioning web app, how to allow different clients to communicate with a central server, and how to use Javascript to manipulate the DOM on the fly and write HTML dynamically. 

Although the project is not yet finished, the bulk of the work has already been done, and the bulk of the code has already been written. The back-end is entirely completed, with only bells and whistles still to add. The front end needs to be polished to be more user friendly, but the functionality of sending information between client and server is in place. Socket.IO allows information to be passed from client to server to another client without either client needing to refresh the page - information is updated for each player in real time.

## Future Updates

The project is not quite finished. Over the next few weeks, the following changes will be made:

Although the entirety of the game can be played in the terminal on the backend, the front end currently is not supported past the end of the first round. The highest priority update is to get the front end in line with the back end.

Plenty of information, both important and superfluous, will be shown to each client. This includes the names of each player, each player's bid for that round, a visual indicating how many cards each other player has, and what cards are currently on the table in the current trick.

In the app's current state, everyone who logs in is in the same game room. An eventual goal is for players to be able to specify which lobby they want to join with a room code. Furthermore, I would like to implement functionality for a player who has disconnected to be able to rejoin the game.