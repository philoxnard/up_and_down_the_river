import random

import undtr


class Game:
    """
    A class to model a game of Up & Down the River
    """

    def __init__(self):
        self.player_count = None
        self.players = []
        self.ordered_players = None
        self.deck = []
        self.active_player_index = 0
        self.winner_index = 0
        self.winner_message = None
        self.state = "initializing"
        self.trump = None
        self.trump_value = None
        self.max_hand_size = None
        self.round = 1
        self.round_already_started = False
        self.trick = {}
        self.trick_obj = {}
        self.tricks_played = 0
        self.led_suit = None
        self.score_dict = {}
        self.bids_collected = 0

    # Method used for testing to show all the relevant information in the game

    def get_status(self):
        for player in self.players:
            print(f"{player.name.title()}'s hand is:")
            for card in player.hand:
                print(f"{card.value} of {card.suit}")
        print(f"The trump is currently {self.trump}")
        for player in self.players:
            print(f"{player.name.title()}'s score is {player.score}")

    # Main loop of the game

    def run_game(self):
        self.initialize_game()
        # Some kind of loop relating to self.max_hand_size
        self.execute_round()
        self.end_game()

    # The following methods operate the highest level logic of the game

    def initialize_game(self):
        self.create_deck()
        self.how_many_players()
        self.get_player_names()

    def execute_round(self):
        self.deal_cards()
        self.determine_trump()
        self.take_bids()
        self.play_hand()
        self.round_cleanup()

    def end_game(self):
        self.display_score()
        self.play_again()

    # The following methods are used in the initialize_game method

    def create_deck(self):
        # Method that will create a list called deck which will be filled with card objects
        self.deck = []
        for i in range(2,15):
            card = undtr.Card(i, "&heartsuit;")
            self.deck.append(card)
            card = undtr.Card(i, "&diamondsuit;")
            self.deck.append(card)
            card = undtr.Card(i, "&clubsuit;")
            self.deck.append(card)
            card = undtr.Card(i, "&spadesuit;")
            self.deck.append(card)
        random.shuffle(self.deck)

    def add_player(self, player_name, sid):
        if self.state == "initializing":
            player = undtr.Player(player_name, sid)
            self.players.append(player)

            # self.player_count is set by user, how many players will be initialized.
            # self.players is the list of players that have been initialized.
            # Once all players are initialized, move on to bidding
            if len(self.players) == self.player_count:
                self.ordered_players = self.players
                self.state = "bidding"
                self.create_deck()
                self.deal_cards()
                self.determine_trump()

    def start_round(self):
        if not self.ordered_players:
            self.ordered_players = self.players
        self.state = "bidding"
        self.create_deck()
        self.deal_cards()
        self.determine_trump()

    def set_player_bid(self, bid, sid):
        if self.state == "bidding":
            for player in self.players:
                if sid == player.sid:
                    player.bid = bid
                    self.bids_collected += 1
            
            # If all players have bid, game state progresses to playing state
            if self.bids_collected == len(self.players):
                self.state = "playing"

    def construct_cards_d(self):
        pass

    def play_card(self, hand_index, player):
        if self.state == "playing":
            card = player.hand.pop(hand_index)
            self.trick[player] = card
            
            # If the card is the first one in the suit, it will modify game.led_suit
            if len(self.trick) == 1:
                self.led_suit = card.suit

            # If each player has played a card, resolve the trick
            # Gives a printout for the terminal
            if len(self.trick) == len(self.players):
                for key, value in self.trick.items():
                    print(f"{key.name.title()} played the {value.value} of {value.suit}")
                winner = undtr.determine_winning_card(self.trick, self.led_suit, self.trump)
                winner.tricks += 1
                print(f"{winner.name.title()} won the trick and now has {winner.tricks} trick(s)")
                self.winner_index = self.players.index(winner)
                self.tricks_played += 1

                # Decides whether the state should be between tricks or between rounds
                if self.tricks_played == self.max_hand_size:
                    self.winner_message = f"{winner.name.title()} won the trick!"
                    self.state = "between rounds"

    def between_tricks(self):
        # Pass priority to whoever won the trick
        if self.state == "between tricks":
            self.trick = {}
            self.trick_obj = {}
            self.ordered_players = self.players[self.winner_index:] + self.players[:self.winner_index]
            self.state = "playing"

    def between_rounds(self):
        # Once all players' hands are empty
        # This is all a lot of clean up that could be organized better
        if self.state == "between rounds":
            self.trick = {}
            self.trick_obj = {}
            self.active_player_index = 0
            self.round += 1
            self.state = "bidding"
            self.round_already_started = False
            self.tally_scores()
            self.check_end_game()
            if self.state == "bidding":
                for player in self.players:
                    player.tricks = 0
                    player.bid_active = False
                    player.bid = 0
                self.tricks_played = 0
                self.bids_collected = 0
                # This makes sure the following round starts with the next player in the circle
                next_dealer = self.players[(self.round - 1) % len(self.players)]
                next_dealer_index = self.players.index(next_dealer)
                self.ordered_players = self.players[next_dealer_index:] + self.players[:next_dealer_index]

    def tally_scores(self):
        for player in self.players:
            player.score += player.tricks
            print(f"{player.name.title()} had a bid of {player.bid}")
            print(f"{player.name.title()} won {player.tricks} tricks")
            if player.bid == player.tricks:
                player.score += 10
                print(f"{player.name.title()} made their bid!")

    def check_end_game(self):
        if self.round == 14:
            self.state="game_over"
            self.get_score()

    def get_score(self):
        if self.state == "game_over":
            for player in self.players:
                self.score_dict[player.name] = player.score
            self.determine_winning_player()

    def determine_winning_player(self):
        winner = max(self.score_dict, key=self.score_dict.get)
        print(winner.title + "wins the game!")

    # The following methods are used in the execute_round method

    def check_hand_size(self):
        if self.round <= 7:
            self.max_hand_size = self.round
        else:
            self.max_hand_size = 14-self.round

    def deal_cards(self):
        self.check_hand_size()
        for player in self.players:
            for i, card in enumerate(self.deck[0:self.max_hand_size]):
                dealt_card=self.deck.pop()
                dealt_card.index = i
                player.hand.append(dealt_card)

    def determine_trump(self):
        trump_card=self.deck.pop()
        self.trump=trump_card.suit
        self.trump_value=trump_card.value

    def take_bids(self):
        for player in self.players:
            player.bid=int(input("What is your bid?"))
            # Needs a check to make sure the input is an integer
            # Needs a check to make sure the input is less than or equal to game.max_hand_size

    def play_hand(self):
        # This is where the bulk of the difficult code will be
        # Likely will be broken up into lots of different methods
        pass

    def round_cleanup(self):
        # This is where scores will get calculated
        # Not actually positive what will go in here
        # Don't need to worry about clearing player hands or making a new deck, that's handled elsewhere
        # This method might actually not be necessary at all
        pass

    # The following methods are used in the end_game method

    def play_again():
        # Code to prompt a rematch
        # Not really necessary
        # Also hard to code until we know exactly how the high logic operates
        pass