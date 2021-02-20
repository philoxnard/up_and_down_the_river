from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send

from game import Game

game = Game()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('index.html')

@socketio.on('new user')
def handle_new_user_event(name, sid, methods=['GET', "POST"]):
    game.add_player(name, sid)
    print(f"there are {len(game.players)} players in the game")
    for player in game.players:
        print(player.name + " is in the game")

@socketio.on("round start")
def handle_game_start_event(methods=["GET", "POST"]):
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
    game.set_player_bid(bid, sid)
    game.active_player_index += 1
    socketio.emit("get next bid")
    for player in game.ordered_players:
        print(f"{player.name}'s bid is {player.bid}")

@socketio.on("play card")
def handle_card_click_event(index, sid, methods=["GET", "POST"]):
    active_player = game.ordered_players[game.active_player_index]
    if active_player.sid == sid and game.state=="playing":
        print("active player is playing card")
        game.play_card(int(index), active_player)
        game.active_player_index += 1
        if game.active_player_index == len(game.ordered_players):
            game.active_player_index = 0
            # Put in some code here to re deal hands I guess?
        else:
            socketio.emit("update hand", active_player.hand, room=active_player.sid)
            next_player = game.ordered_players[game.active_player_index]
            socketio.emit("your turn", room=next_player.sid)
    else:
        print("its either not your turn, or its bidding time")






if __name__ == '__main__':
    socketio.run(app, debug=True)