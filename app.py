from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/name_players", methods=["POST"])
def name_players():
        player_count = request.form.get("player_count")
        return render_template("name_players.html", player_count=int(player_count))

@app.route("/show_players", methods=["POST"])
def show_players():
    name_list = []
    for i in range(3): # Hardcoded for testing, but this needs to somehow get teh length of the list
        name = request.form.get(str(i))
        name_list.append(name)
    return render_template("show_players.html", name_list=name_list)

app.run(debug=True)