from game import Game

if __name__ == "__main__":

    game = Game()

    while True:
        if game.state == "initializing":
            # Get number of players
            # Get names of each player
            game.player_count = int(input("How many players?"))
            game.players = []
            for player in range(game.player_count):
                player_name = input("What is this player's name?")
                game.add_player(player_name)
        elif game.state == "bidding":
            # Deal hands
            # Show trump card
            # Collect bid from each player
            for player in game.players:
                bid = int(input(f"{player.name.title()}, what is your bid?"))
                game.set_player_bid(bid, player)
        elif game.state == "playing":
            # For i in range(hand_szie), for each player:
            # Ask for input on which card the player wants to play
            # add that card to the active trick
            # determine the winning card + player
            # clear trick
            # assign points
            for i in range(game.hand_size):
                for player in game.players:
                    card = int(input(f"{player.name.title()}, what card do you want to play?"))
                    game.play_card(card, player)
        elif game.state == "game_over":
            # determine winner + display (done, exists in game.get_score and game.determine_winning_player)
            # request to play again
            #TODO: Take input from user if they want to play again
            pass
