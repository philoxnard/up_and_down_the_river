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
    socketio.emit("player_added", [p.name for p in game.players])

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
    for i, player in enumerate(game.ordered_players):
        if i == game.bids_collected:
            socketio.emit("get bid", room=player.sid)

# @socketio.on("receive bid")
# def handle_bid(bid, sid, methods=["GET", "POST"]):
#     game.set_player_bid(bid, sid)
#     if len(game.players)==game.bids_collected:
#         for player in game.players:
#             print(f"{player.name.title()} bid {player.bid}")
########
######## Keeping this commented out until the functionality for passing bid around 
######## Is working as intended


if __name__ == '__main__':
    socketio.run(app, debug=True)