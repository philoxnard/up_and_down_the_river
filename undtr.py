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