from flask import Flask, render_template
from flask_socketio import SocketIO

from game import Game

game = Game()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('index.html')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', "POST"]):
    game.add_player(str(json))
    print(f"there are {str(len(game.players))} players in the game")
    for player in game.players:
        print(player.name + " is in the game")


if __name__ == '__main__':
    socketio.run(app, debug=True)