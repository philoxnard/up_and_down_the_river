from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send

from game import Game

game = Game()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

# Provides connected users their landing view
@app.route('/')
def sessions():
    return render_template('index.html')

@socketio.on('new user')
def handle_new_user_event(name, sid, methods=['GET', "POST"]):
    """
    Event handler for when a new player enters the game.

    :param name: String populated by the form filled out on the client side
    :param sid: String of socket ID from the client who hit submit
    """
    game.add_player(name, sid)
    print(f"there are {len(game.players)} players in the game")
    for player in game.players:
        print(player.name + " is in the game")

@socketio.on("round start")
def handle_game_start_event(methods=["GET", "POST"]):
    """
    Event handler for when all players have been entered and the "Start Game"
    button gets clicked. Creates and shuffles the deck, deals out the cards, and 
    determines the trump card. Note that the trump is passed to each player as part
    of the object that this function returns, but it is not a part of their hand

    :return: Dictionary with the trump card and the player's hand, received by client
    as a Javastring object
    """
    print("start the round")
    game.start_round()
    for player in game.ordered_players:
        hand_dict = {
            "trump": [game.trump_value, game.trump]
        }
        for card in player.hand:
            hand_dict[card.value]=card.suit
        socketio.emit("deal hand", hand_dict, room=player.sid)

@socketio.on("request bid")
def handle_start_bidding_event(methods=["GET", "POST"]):
    """
    Event handler for when a new bid must be requested. Creates an input field
    where the player whose turn it is can input their bid and submit it.
    When all bids have been collected, this function instead switches the game
    state to "playing" and sends a message to the player whose turn it is that
    they may now start playing cards.

    """
    if game.active_player_index == len(game.ordered_players):
        game.active_player_index = 0
        active_player = game.ordered_players[game.active_player_index]
        game.state = "playing"
        socketio.emit("your turn", room=active_player.sid)
    else:
        active_player = game.ordered_players[game.active_player_index]
        if not active_player.bid_active:
            socketio.emit("make bid field", room=active_player.sid)
            active_player.bid_active = True

@socketio.on("receive bid")
def handle_bid(bid, sid, methods=["GET", "POST"]):
    """
    Event handler for when a player submits their bid. Takes the user input and
    assigns it to player.bid, then bounces a quick emit back to the client so
    the client can again bounce the "request bid" function to the next client.

    :param bid: String that represents the player's bid for that round
    :param sid: String of socket ID from the bidding player
    """
    game.set_player_bid(bid, sid)
    game.active_player_index += 1
    socketio.emit("get next bid")
    for player in game.ordered_players:
        print(f"{player.name}'s bid is {player.bid}")

@socketio.on("play card")
def handle_card_click_event(index, sid, methods=["GET", "POST"]):
    """
    Event handler for when a player clicks on a card in their hand. First, checks 
    to make sure that the game state is "playing" and that it is the respective client's
    turn. If not, it refuses to play the card. If it is, then the card is added to
    the current trick on the table amd passes priority to the next player in line.
    Also updates the player's hand who just played a card.

    :param index: String of the clicked card's numerical index in the player hand
    :param sid: String of socket ID from the player who clicked their card
    :return: List player.hand of the player who played a card
    :return: Dictionary {player name: [card value, card suit]} to be read as active trick
    """
    active_player = game.ordered_players[game.active_player_index]
    if active_player.sid == sid and game.state=="playing":
        print("active player is playing card")
        game.play_card(int(index), active_player)
        game.active_player_index += 1
        if game.active_player_index == len(game.ordered_players):
            game.active_player_index = 0
            # TODO: Create an "end round" function
            # TODO: Somehow make it happen after all the following code
            # TODO: Let all the info sit on screen, put in a button to let the
            # TODO: players progress to the next round when they want to
            # TODO: Make another socketio.emit to show each player's bid in a table
            # TODO: probably into a new div called bidTable or something
            socketio.emit("end round")
        else:
            socketio.emit("update hand", active_player.hand, room=active_player.sid)
            next_player = game.ordered_players[game.active_player_index]
            socketio.emit("your turn", room=next_player.sid)
            trick_obj = {}
            for player, card in game.trick.items():
                card_list = [card.value, card.suit]
                trick_obj[player.name]=card_list
            print(trick_obj)
            socketio.emit("show trick", trick_obj)
    else:
        print("its either not your turn, or its bidding time")






if __name__ == '__main__':
    socketio.run(app, debug=True)