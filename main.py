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
            # Show trump card2
            # Collect bid from each player
            game.get_status()
            for player in game.ordered_players:
                bid = int(input(f"{player.name.title()}, what is your bid?"))
                game.set_player_bid(bid, player)
        elif game.state == "playing":
            # For i in range(hand_szie), for each player:
            # Ask for input on which card the player wants to play
            # add that card to the active trick
            # determine the winning card + player
            # clear trick
            # assign points
            # TODO: Force the player to follow suit if they can (not priority, basically part of the next todo item)
            # TODO: Write checks to ensure player input is legal (not priority)
            # TODO: Sort each player's hand by suit, then by number (not priority)
            for i in range(game.max_hand_size):
                for player in game.ordered_players:
                    hand_index = int(input(f"{player.name.title()}, what card do you want to play?"))
                    game.play_card(hand_index, player)
                    # I think the above two lines need to be looked at, seems like
                    # the code is pointing to an integer rather than a card.
                    # The integer input from the player is, at this point, meant to 
                    # point to a card in hand, not just be a floating integer
        elif game.state == "game_over":
            # determine winner + display (done, exists in game.get_score and game.determine_winning_player)
            # request to play again
            #TODO: Take input from user if they want to play again (not priority)
            #TODO: Cover cases where two scores tie for a win (not priority)
            pass
