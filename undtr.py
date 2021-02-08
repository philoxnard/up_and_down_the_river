class Card:
    """
    A class that represents a card
    """

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"Card({self.value}{nickname(self.suit)})"


class Player:
    """
    A class to model a player
    """

    def __init__(self):
        self.hand = None
        self.bid = None
        self.score = None
        self.tricks_won = 0

    def __repr__(self):
        sorted_hand = sort_cards(self.hand)
        cards_repr = [f"{c}" for c in sorted_hand]
        hand_repr = ', '.join(cards_repr)
        repr = f"Player( {hand_repr} )"
        return repr


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

