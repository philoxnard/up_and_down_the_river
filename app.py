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
        socketio.emit("begin play", room=active_player.sid)
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





if __name__ == '__main__':
    socketio.run(app, debug=True)