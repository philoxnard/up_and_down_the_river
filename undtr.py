class Card:
    """
    A class that represents a card
    """

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"Card({self.value}{nickname(self.suit)}"


class Player:
    """
    A class to model a player
    """

    def __init__(self):
        self.hand = None
        self.bid = None
        self.score = None
        self.tricks = None

    def __repr__(self):
        sorted_hand = sort_cards(self.hand)
        cards_repr = [f"{c.value}{nickname(c.suit)}" for c in sorted_hand]
        hand_repr = ', '.join(cards_repr)
        repr = f"Player({hand_repr})"
        return repr


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


def sort_cards(cards, suit_order=("CLUBS", "DIAMONDS", "SPADES", "HEARTS")):
    """

    :param cards:
    :param suit_order:
    :return:
    """
    suits_d = partition_by_suit(cards, suit_order)
    sorted_suits_d = sort_dict_values(suits_d, key=lambda card: card.value)
    sorted_hand = combine_partition(sorted_suits_d, suit_order)
    return sorted_hand


def partition_by_suit(cards, suit_order):
    """
    Break a list of cards down by suit.  Returns a dict whose keys
    are the suits of the cards

    :param cards: List[Card]
    :param suit_order: List[str]
    :return: Dict[str: List[Card]]
    """
    partition = {suit: [] for suit in suit_order}
    for card in cards:
        partition[card.suit].append(card)

    return partition


def sort_dict_values(d, key=None):
    """
    Sort the values of a dictionary's keys.

    Dict values must be some sortable type, e.g. List, Tuple

    :param d: Dict[Any: List]
    :param key: Function(Any -> Int)
    :return: Dict[Any: List]
    """
    sorted_d = dict.fromkeys(d.keys())
    for k, v in d.items():
        sorted_d[k] = sorted(v, key=key)

    return sorted_d


def combine_partition(partition, key_order):
    """
    Given a partition of cards, recombine them into a list.

    The elements are returned in the order specified by key_order.

    :param partition: Dict[str: List]
    :param key_order: List
    :return: List
    """
    sorted_list = []
    for key in key_order:
        for value in partition[key]:
            sorted_list.append(value)

    return sorted_list


def nickname(suit):
    """
    Map a suit name to a shorter version of the suit.

    :param suit: str
    :return: str
    """
    mapping = {
        "CLUBS": "CLB",
        "DIAMONDS": "DIM",
        "SPADES": "SPD",
        "HEARTS": "HRT",
    }
    return mapping.get(suit, suit)



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
