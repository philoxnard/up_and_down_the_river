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

@socketio.on("game start")
def handle_game_start_event(methods=["GET", "POST"]):
    print("start the game")
    game.state = "bidding"
    for player in game.players:
        socketio.emit("success", player.name, room=player.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)