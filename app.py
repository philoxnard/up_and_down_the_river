from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send
import logging
import datetime
import os
import sys

from game import Game

today = datetime.date.today()
date_str = today.strftime("%d_%m_%Y_%H_%M")
log_path = f"{os.path.dirname(__file__)}/logs/{date_str}.log"
file_handler = logging.FileHandler(log_path)
stream_handler = logging.StreamHandler()
handlers = [file_handler, stream_handler]

logging.basicConfig(handlers=handlers, encoding="utf-8", level=logging.DEBUG)
logging.debug("Starting app")


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
    Event handler for when a new round starts, whether by all players having been
    entered and the "Start Game" button gets clicked, or by continuing after a 
    prior round has ended. Creates and shuffles the deck, deals out the cards, and 
    determines the trump card. Note that the trump is passed to each player as part
    of the object that this function returns, but it is not a part of their hand

    :return: Dictionary with the trump card and the player's hand, received by client
    as a Javastring object
    """
    if not game.round_already_started:
        game.round_already_started = True
        print("start the round")
        game.start_round()
        for player in game.ordered_players:
            hand_dict = {
                "trump": [game.trump_value, game.trump]
            }
            for i, card in enumerate(player.hand):
                hand_dict[i]=[card.value, card.suit]
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
    bid_dict = {}
    for player in game.ordered_players:
        print(f"{player.name}'s bid is {player.bid}")
        bid_dict[player.name.title()]=player.bid
    socketio.emit("show bidTable", bid_dict)

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
    if game.state == "playing":
        print(index)
        active_player = game.ordered_players[game.active_player_index]
        print(active_player.hand)
        if active_player.sid == sid:
            game.play_card(int(index), active_player)
            if game.card_played == True:
                game.card_played = False
                for player, card in game.trick.items():
                    card_list = [card.value, card.suit]
                    game.trick_obj[player.name]=card_list
                hand_dict = {}
                for i, card in enumerate(player.hand):
                    hand_dict[i]=[card.value, card.suit]
                print(active_player.hand)
                print(active_player.sid)
                active_player.can_follow_suit = False
                socketio.emit("update hand", hand_dict, room=active_player.sid)
                socketio.emit("show trick", game.trick_obj)
                print(f"{game.trick_obj}")
                game.active_player_index += 1
                if game.active_player_index == len(game.players):
                    trick_table_dict = {}
                    for player in game.ordered_players:
                        trick_table_dict[player.name.title()]=player.tricks
                    socketio.emit("end trick", game.winner_message)
                    socketio.emit("update trick table", trick_table_dict)
                else:
                    next_player = game.ordered_players[game.active_player_index]
                    socketio.emit("your turn", room=next_player.sid)
        else:("Its not your turn")
    else:
        print("its not time for that")

@socketio.on("continue")
def handle_continue_event(methods=["GET", "POST"]):
    """
    Event handler for when a user clicks the "continue" button that appears after the end of a trick.
    If there are more tricks to be played, this function will continue to the rest of the round. If
    there are no more tricks to be played in the current round, this function will end the round, 
    reset the decks, hands, and trumps, and will start the next round.

    """
    if game.state == "between rounds":
        game.between_rounds()
        if not game.state == "game over":
            socketio.emit("restart round")
        elif game.state == "game over":
            socketio.emit("end game", game.score_dict)
    elif game.state == "between tricks":
        game.between_tricks()
        socketio.emit("next trick") 

@socketio.on("new trick")
def handle_new_trick_event(methods=["GET", "POST"]):
    active_player = game.ordered_players[game.active_player_index]
    socketio.emit("your turn", room=active_player.sid)

# Short term to do list:
# TODO: Refactor code to make the docs all a bit smaller and more manageable
# TODO: Make bidTable and trickTable display in same order as each other
#
###################################################################
#
# Long term to do list:
#
# TODO: Give players a button that restarts the game
# TODO: Replace print statements with logging statements
# TODO: Give some indication if it isn't your turn
# TODO: Can make it even prettier, but its not hoooooorrible right now
# TODO: Prevent user from having the same name as another user
# TODO: Make some fun emojis or something for if people do or don't make their bids


if __name__ == '__main__':
    socketio.run(app, port=5000, host="0.0.0.0", debug=True)
