import undtr


class Game:
    """
    A class to model a game of Up & Down the River
    """

    def __init__(self):
        self.player_count = None
        self.players = []
        self.deck = []
        self.active_player = None
        self.state = "initializing"
        self.trumps = None
        self.max_hand_size = None
        self.round = 1
        self.trick = {}
        self.tricks_played = 0
        self.led_suit = None
        self.score_dict = {}

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
        # TODO: Make this prettier lol
        for i in range(13):
            card = undtr.Card(i, "HEARTS")
            self.deck.append(card)
            card = undtr.Card(i, "DIAMONDS")
            self.deck.append(card)
            card = undtr.Card(i, "CLUBS")
            self.deck.append(card)
            card = undtr.Card(i, "SPADES")
            self.deck.append(card)

    def add_player(self, player_name):
        if self.state == "initializing":
            player = undtr.Player(player_name)
            self.players.append(player)

            # self.player_count is set by user, how many players will be initialized.
            # self.players is the list of players that have been initialized.
            # Once all players are initialized, move on to bidding
            # TODO: Take the below snippet and make it its own func/method (round start) cause it'll get called elsewhere too
            if len(self.players) == self.player_count:
                self.state = "bidding"
                self.create_deck()
                self.deal_cards()
                self.determine_trump()

    def get_player_bids(self):
        d = {}
        for player in self.players:
            d[player] = player.bid
        return d

    def set_player_bid(self, bid, player):
        if self.state == "bidding":
            player.bid = bid

            # Check wither all bids have been collected and move on if necessary
            player_bids = self.get_player_bids()
            num_bids = 0
            for bid in player_bids.values():
                if bid is not None:
                    num_bids += 1

            if num_bids == len(self.players):
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
            if len(self.trick) == len(self.players):
                winner = undtr.determine_winning_card(self.trick, self.led_suit, self.trumps)
                winner.tricks += 1
                self.trick = {}
                self.tricks_played += 1

            # Once all players' hands are empty
            if self.tricks_played == self.max_hand_size:
                self.round += 1
                self.state = "bidding"
                self.tally_scores()
                self.check_end_game()
                if self.state == "bidding":
                    self.tricks_played = 0
                    self.create_deck()
                    self.deal_cards()
                    self.determine_trump()

    def tally_scores(self):
        for player in self.players:
            player.score += player.tricks
            if player.bid == player.tricks:
                player.score += 10

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
        #TODO: Cover circumstances where there's a tie

    # The following methods are used in the execute_round method
    # NOTE: These methods don't address who the active player is yet

    def check_hand_size(self):
        if self.round <= 7:
            self.max_hand_size = self.round
        else:
            self.max_hand_size = 14-self.round

    def deal_cards(self):
        self.check_hand_size()
        print("the hand size for this round is " + str(self.max_hand_size))
        print("the current round is round number  " + str(self.round))
        for player in self.players:
            for card in self.deck[0:self.max_hand_size]:
                dealt_card=self.deck.pop()
                player.hand.append(dealt_card)

    def determine_trump(self):
        trump_card=self.deck.pop()
        self.trump=trump_card.suit

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