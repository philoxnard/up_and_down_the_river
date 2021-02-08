import undtr


class Game:
    """
    A class to model a game of Up & Down the River
    """

    def __init__(self):
        self.player_count = None
        self.players = []
        self.deck = None
        self.active_player = None
        self.state = "initializing"
        self.trumps = None
        self.max_hand_size = None
        self.hand_size = None
        self.scores = None
        self.trick = {}
        self.tricks_played = 0
        self.led_suit = None

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

    def add_player(self, player_name):
        if self.state == "initializing":
            self.players.append(player_name)

            # self.player_count is set by user, how many players will be initialized.
            # self.players is the list of players that have been initialized.
            # Once all players are initialized, move on to bidding
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


    def play_card(self, card, player):
        player.hand.pop(card)
        self.trick[player] = card

        # If each player has played a card, resolve the trick
        if len(self.trick) == len(self.players):
            winner = undtr.determine_winning_card(self.trick, self.led_suit, self.trumps)
            winner.tricks_won += 1
            self.trick = {}
            self.tricks_played += 1

        # Once all players' hands are empty
        if self.tricks_played == self.max_hand_size:
            # TODO: increment hand size and assign scores
            raise NotImplementedError


    # The following methods are used in the execute_round method
    # NOTE: These methods don't address who the active player is yet

    def deal_cards(self):
        for player in self.players:
            for card in deck[0:self.max_hand_size]:
                player.hand=deck.pop()

    def determine_trump(self):
        trump_card=deck(pop)
        self.trump=trump_card.suit

    def take_bids(self)
        for player in self.players:
            player.bid=int(input("What is your bid?"))
            # Needs a check to make sure the input is an integer
            # Needs a check to make sure the input is less than or equal to game.max_hand_size

    def play_hand(self):
        # This is where the bulk of the difficult code will be
        # Likely will be broken up into lots of different methods

    def round_cleanup(self):
        # This is where scores will get calculated
        # Not actually positive what will go in here
        # Don't need to worry about clearing player hands or making a new deck, that's handled elsewhere
        # This method might actually not be necessary at all

    # The following methods are used in the end_game method

    def display_score(self):
        score_dict = {}
        for player in self.players:
            print(player.name.title() + "ended the game with + " player.score + "points")
            score_dict[player.name] = player.score

        winner = max(score_dict, key=score_dict.get)
        print(winner.title + "wins the game!")
        # Needs code to handle condition if two or more players tie for the win

    def play_again():
        # Code to prompt a rematch
        # Not really necessary
        # Also hard to code until we know exactly how the high logic operates