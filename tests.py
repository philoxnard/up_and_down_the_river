import unittest
import undtr


class TestDetermineWinningCard(unittest.TestCase):

    def test_two_same_suit(self):
        p1 = undtr.Player()
        p2 = undtr.Player()

        p1_card = undtr.Card(3, "CLUBS")
        p2_card = undtr.Card(8, "CLUBS")

        led_suit = "CLUBS"
        trump = "HEARTS"

        cards_d = {p1: p1_card, p2: p2_card}
        winner = undtr.determine_winning_card(cards_d, led_suit, trump)

        self.assertEqual(winner, p2)

    def test_three_same_suit(self):
        p1 = undtr.Player()
        p2 = undtr.Player()
        p3 = undtr.Player()

        p1_card = undtr.Card(10, "CLUBS")
        p2_card = undtr.Card(8, "CLUBS")
        p3_card = undtr.Card(4, "CLUBS")

        led_suit = "CLUBS"
        trump = "DIAMONDS"

        cards_d = {p1: p1_card, p2: p2_card, p3: p3_card}
        winner = undtr.determine_winning_card(cards_d, led_suit, trump)

        self.assertEqual(winner, p1)

    def test_all_trump(self):
        p1 = undtr.Player()
        p2 = undtr.Player()
        p3 = undtr.Player()

        p1_card = undtr.Card(3, "CLUBS")
        p2_card = undtr.Card(11, "CLUBS")
        p3_card = undtr.Card(6, "CLUBS")

        led_suit = "DIAMONDS"
        trump = "CLUBS"

        cards_d = {p1: p1_card, p2: p2_card, p3: p3_card}
        winner = undtr.determine_winning_card(cards_d, led_suit, trump)

        self.assertEqual(winner, p2)

    def test_one_trump(self):
        p1 = undtr.Player()
        p2 = undtr.Player()
        p3 = undtr.Player()

        p1_card = undtr.Card(3, "DIAMONDS")
        p2_card = undtr.Card(11, "CLUBS")
        p3_card = undtr.Card(6, "CLUBS")

        trump = "DIAMONDS"
        led_suit = "CLUBS"

        cards_d = {p1: p1_card, p2: p2_card, p3: p3_card}
        winner = undtr.determine_winning_card(cards_d, led_suit, trump)

        self.assertEqual(winner, p1)               

    def test_only_one_of_leading(self):
        p1 = undtr.Player()
        p2 = undtr.Player()
        p3 = undtr.Player()

        p1_card = undtr.Card(3, "DIAMONDS")
        p2_card = undtr.Card(11, "CLUBS")
        p3_card = undtr.Card(6, "CLUBS")

        trump = "HEARTS"
        led_suit = "DIAMONDS"

        cards_d = {p1: p1_card, p2: p2_card, p3: p3_card}
        winner = undtr.determine_winning_card(cards_d, led_suit, trump)

        self.assertEqual(winner, p1)


class TestSortHand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.club_2 = undtr.Card(2, "CLUBS")
        cls.club_10 = undtr.Card(10, "CLUBS")
        cls.diam_2 = undtr.Card(2, "DIAMONDS")
        cls.diam_10 = undtr.Card(10, "DIAMONDS")
        cls.spds_2 = undtr.Card(2, "SPADES")
        cls.hrts_2 = undtr.Card(2, "HEARTS")
        cls.sort_order = ("CLUBS", "DIAMONDS", "SPADES", "HEARTS")

    def test_sort_four(self):
        cards = [self.diam_2, self.club_10, self.club_2, self.diam_10]
        sorted_cards = undtr.sort_cards(cards, self.sort_order)
        expected_cards = [self.club_2, self.club_10, self.diam_2, self.diam_10]
        self.assertEqual(sorted_cards, expected_cards)

    def sort_none(self):
        cards = []
        sorted_cards = undtr.sort_cards(cards, self.sort_order)
        expected_cards = []
        self.assertEqual(sorted_cards, expected_cards)

    def test_sort_all_same_value(self):
        cards = [self.hrts_2, self.diam_2, self.club_2, self.spds_2]
        sorted_cards = undtr.sort_cards(cards, self.sort_order)
        expected_cards = [self.club_2, self.diam_2, self.spds_2, self.hrts_2]
        self.assertEqual(sorted_cards, expected_cards)


if __name__ == "__main__":
    unittest.main()