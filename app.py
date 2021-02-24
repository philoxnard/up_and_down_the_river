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
    print(index)
    active_player = game.ordered_players[game.active_player_index]
    print(active_player.hand)
    if active_player.sid == sid and game.state=="playing":
        game.play_card(int(index), active_player)
        for player, card in game.trick.items():
            card_list = [card.value, card.suit]
            game.trick_obj[player.name]=card_list
        hand_dict = {}
        for i, card in enumerate(player.hand):
            hand_dict[i]=[card.value, card.suit]
        print(active_player.hand)
        print(active_player.sid)
        socketio.emit("update hand", hand_dict, room=active_player.sid)
        socketio.emit("show trick", game.trick_obj)
        print(f"{game.trick_obj}")
        game.active_player_index += 1
        if game.active_player_index == len(game.players):
            socketio.emit("end trick", game.winner_message)
        else:
            next_player = game.ordered_players[game.active_player_index]
            socketio.emit("your turn", room=next_player.sid)

    else:
        print("its either not your turn, or its bidding time")

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
        socketio.emit("restart round")
    elif game.state == "between tricks":
        print("between tricks function not yet implemented")

# Short term to do list:
#
# TODO: Implement functionality for going from trick to trick
#       handle_continue_event when game.state == "between tricks"
# TODO: Fix the bug where the card that gets played is seemingly random
#       The index being passed from the client is correct, at least according
#       to what the user sees on the client view.
#       PROBLEM: The lists that make up each player's hands are not necessarily in
#                the same order on the server as they are in the client - no idea
#                why at the moment, no discernable pattern as of yet.
#       SOLUTION: send each card index to the client and somehow display the hand
#                   in order of index
# BUG : One of the hands in a test weirdly didn't display the entire hand, despite
#       the entire hand being recognized on the server... no idea what happened there
###################################################################
# Long term to do list:
#
# TODO: Prevent user from having the same name as another user
# TODO: Make another socketio.emit to show each player's bid in a table
# TODO: probably into a new div called bidTable or something
# TODO: Make it so clicking your hand doesn't remove bid field
#           probably put it in the update hand client function


if __name__ == '__main__':
    socketio.run(app, debug=True)