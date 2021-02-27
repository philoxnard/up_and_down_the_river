
# up_and_down_the_river

Up and Down the River is an online multiplayer web app modeled after the card game of the same name. The back-end is written in Python utilizing the Flask framework, and the front end combines HTML, CSS, and Javascript, as well as the Socket.IO library to allow for multiple players to join.

## How to Play

Each round, the players will be given a hand of cards, as well as being shown that round's trump card. Before playing, each player will, in turn, make a bid on how many tricks they think they will win during the round. Playeres earn a point for each trick they win, plus an additional 10 points if they end the round with the same amount of tricks as they bid earlier.

![bidding](https://user-images.githubusercontent.com/68870846/109394305-521e4180-78f4-11eb-82d2-f5f7438697c6.png)

Rounds play out with each player, in turn, playing a card. Players must follow suit with whoever played the first card in the trick if possible. When all players have played their card in the trick, the trick will be awarded to whoever played the highest card of the led suit. However, if a card in the trick is the same suit as the trump card, that card will take priority over the led suit. If there are multiple trump cards in the suit, the winning card is the highest trump.

![trick](https://user-images.githubusercontent.com/68870846/109394321-6cf0b600-78f4-11eb-8da0-0dd4637cee0c.png)

Successive rounds have different hand sizes. The first round has a hand size of one, the second round a hand size of two, following the same pattern up to seven. After the seventh round, though, the following round has a six card hand, followed by a five card hand, following that same pattern back down to one. After the second one-card hand has been played, the game is over and the player with the highest score wins.

## Project Goals

Through this project, I aimed to gain a deeper understanding of multiple different facets of web design: How to use Python to create a functioning web app, how to allow different clients to communicate with a central server, and how to use Javascript to manipulate the DOM on the fly and write HTML dynamically. 

## Future Updates

Although the project is fully functional, there are some small QoL changes I would like to make:

The current display works, but it is pretty bare bones. I would like to update the design to make it more aesthetically pleasing, easy to read, and usable across different devices.

Most, if not all, of the code could use some cleaning up and refactoring. There is lots of vestigial code that can be snipped entirely, lots of code that needs an update in documentation, and lots of code that can be clipped, trimmed, and reformatted.

In the app's current state, everyone who logs in is in the same game room. An eventual goal is for players to be able to specify which lobby they want to join with a room code. Furthermore, I would like to implement functionality for a player who has disconnected to be able to rejoin the game.

## Lessons Learned

Over the course of completing this project, I've learned so much about how to most efficiently and effectively create a web app, including but not limited to the following:

Understanding what networking multiple different clients together looks like in a practical sense as well as in a conceptual sense. Although I have played my fair share of multiplayer games, I had no idea of the structure of how different computers communicate with a central server. Researching the Socket.IO documentation, as well as looking at different methods of networking, gave me a much stronger schema for understanding how machines can communicate.

How to cleanly write an HTML document dynamically with Javascript. Earlier versions of the Javascript document attempted to write/draw all the relevant information to a single div on the DOM, which, predictably, led to a tangled web of rewriting and overwriting and tiptoeing to avoid mangling the display. Realizing that information can (and should) be separated into neat divs so that each div can be manipulated in a more granular manner was paramount in displaying all of the information that I wanted to display.

The importance of keeping server-side logic separate from client-side logic, and the importance of making sure the former is complete before integrating it with the latter. Fortunately, the entirety of this program was operable in Python via the terminal prior to including any HTML, CSS, Javascript, or networking. As I started developing the client-side code, I was so frequently happy that I had server-side code that I could rely on to be correct. Although small tweaks had to be made to make the information generated by the server more easily readable, it was an enormous boon to only need to playtest for the front-end code, knowing that the back-end code was already doing what I wanted it to do.
