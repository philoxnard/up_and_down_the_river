class Card:
    """
    A class that represents a card
    """

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


class Player:
    """
    A class to model a player
    """

    def __init__(self):
        self.hand = None
        self.bid = None
        self.score = None
        self.tricks = None


class Game:
    """
    A class to model a game of Up & Down the River
    """

    def __init__(self, players, deck, max_hand_size):
        self.players = tuple(pl for pl in players)
        self.deck = deck
        self.active_player = None
        self.stage = "bidding"
        self.trumps = None
        self.max_hand_size = max_hand_size
        self.hand_size = None
        self.scores = None
        self.current_tricks = None
        self.led_suit = None


def determine_winning_card(cards_d, led_suit, trump):
    """
    Determine which card was the highest from a list of cards:

    :param cards_d: Dict[Player: Card], the list of cards in the order in which they were played
    :param led_suit: Str
    :param trump: Str
    :returns: Player
    """
    eligible_cards_d = {}

    for player, card in cards_d.items():
        if card.suit == trump:
            eligible_cards_d[player] = card.value

    if bool(eligible_cards_d):
        winner = max(eligible_cards_d, key=eligible_cards_d.get)

    else:
        for player, card in cards_d.items():
            if card.suit == led_suit:
                eligible_cards_d[player] = card.value
        winner = max(eligible_cards_d, key=eligible_cards_d.get)

    return winner


if __name__ == "__main__":

    # Hard-coded sample game, for initial testing and mockup of Game API
    NUM_PLAYERS = 2
    MAX_HAND_SIZE = 2

    players = [Player() for i in range(NUM_PLAYERS)]
    deck = Deck()  # TODO: Implement Deck class
    game = Game(players=players, deck=deck, max_hand_size=MAX_HAND_SIZE)

    # One card in each hand -- bidding
    game.setup_bidding()
    game.make_bid(1)  # p1's bid
    game.rotate_player()
    game.make.bid(0)  # p2's bid

    # 1-Playing tricks -- 1 of 1
    game.setup_play()
    game.setup_trick()
    game.play_card((14, "CLUBS"))  # p1's play
    game.rotate_player()
    game.play_card((4, "HEARTS"))  # p2's play
    game.resolve_trick()

    # Up to 2 cards in each hand
    game.setup_bidding()
    game.make_bid(1)  # player *2* now, because dealer rotates
    game.rotate_player()
    game.make.bid(1)

    # playing tricks -- 1 of 2
    game.setup_play()
    game.setup_trick()
    game.play_card((12, "DIAMONDS"))
    game.rotate_player()
    game.play_card((3, "DIAMONDS"))
    game.resolve_trick()

    # playing tricks -- 2 of 2
    game.setup_trick()
    game.play_card((4, "HEARTS"))
    game.rotate_player()
    game.play_card((14, "SPADES"))
    game.resolve_trick()

    # Back down to 1 card in the hand
    game.setup_bidding()
    game.make_bid(1)  # Starts with p1 again
    game.rotate_player()
    game.make.bid(0)

    # 1-Playing tricks -- 1 of 1
    game.setup_play()
    game.setup_trick()
    game.play_card((14, "CLUBS"))
    game.rotate_player()
    game.play_card((4, "HEARTS"))
    game.resolve_trick()

    game.resolve_winner()
