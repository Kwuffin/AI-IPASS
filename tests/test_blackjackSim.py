import unittest
import blackjackSim as bs


class TestSim(unittest.TestCase):

    def test_hit(self):
        deck = ["5", "3"]
        bs.hit(deck)

        self.assertTrue(len(deck) == 3)

    def test_split(self):
        deck = ["3", "5"]
        d1, d2 = bs.split(deck)

        self.assertEqual(d1, ["3"])
        self.assertEqual(d2, ["5"])

    def test_initializeBot(self):
        bDeck = bs.bot()

        self.assertTrue(len(bDeck) == 2)

    def test_initializeDealer(self):
        dDeck = bs.dealerInitial()

        self.assertTrue(len(dDeck) == 2)

    def test_value1(self):  # Two number cards
        deck = ["5", "7"]

        self.assertEqual(bs.value(deck), 12)

    def test_value2(self):  # One face card
        deck = ["Q", "7"]

        self.assertEqual(bs.value(deck), 17)

    def test_value3(self):  # Two face cards
        deck = ["K", "J"]

        self.assertEqual(bs.value(deck), 20)

    def test_value4(self):  # One Ace and one face card
        deck = ["A", "J"]

        self.assertEqual(bs.value(deck), 21)

    def test_value5(self):  # Two Ace cards
        deck = ["A", "a"]

        self.assertEqual(bs.value(deck), 12)

    def test_value6(self):  # Three cards, hard ace
        deck = ["7", "a", "9"]

        self.assertEqual(bs.value(deck), 17)

    def test_value7(self):  # Five cards, multiple of the same card, face card
        deck = ["K", "2", "3", "2", "2"]

        self.assertEqual(bs.value(deck), 19)

    def test_dealerAfterDraw(self):  # Dealer should draw one card
        dDeck = ["6", "10"]
        self.assertEqual(bs.value(dDeck), 16)

        bs.dealerAfter(dDeck)
        self.assertTrue(len(dDeck) == 3)

    def test_dealerAfterNoDraw(self):  # Dealer should NOT draw any cards
        dDeck = ["7", "10"]
        self.assertEqual(bs.value(dDeck), 17)

        bs.dealerAfter(dDeck)
        self.assertTrue(len(dDeck) == 2)

    def test_checkAce_lower(self):  # Lowers the value of Ace card
        deck = ["10", "8", "A"]
        self.assertEqual(bs.value(deck), 29)

        deck = bs.checkAce(deck)
        self.assertEqual(bs.value(deck), 19)
        self.assertEqual(deck, ["10", "8", "a"])

    def test_checkAce_notLower(self):  # Does not lower the value of Ace card
        deck = ["9", "A"]
        self.assertEqual(bs.value(deck), 20)

        deck = bs.checkAce(deck)
        self.assertEqual(bs.value(deck), 20)
        self.assertEqual(deck, ["9", "A"])

    def test_checkBlackjack_True(self):  # Ace and 10-value card should result in a blackjack
        deck = ["A", "J"]
        self.assertEqual(bs.value(deck), 21)

        self.assertTrue(bs.checkBlackjack(deck))

    def test_checkBlackjack_False(self):  # Ace and non-10-value card should NOT result in a blackjack
        deck = ["A", "9"]
        self.assertEqual(bs.value(deck), 20)

        self.assertFalse(bs.checkBlackjack(deck))

    def test_bust_True(self):  # Value higher than 21 should result in a bust
        deck = ["10", "7", "5"]
        self.assertEqual(bs.value(deck), 22)

        self.assertTrue(bs.bust(deck))

    def test_bust_False(self):  # Value lower than 22 should NOT result in a bust
        deck = ["10", "7", "4"]
        self.assertEqual(bs.value(deck), 21)

        self.assertFalse(bs.bust(deck))

    def test_compare_dealerWin(self):  # Dealer with higher value should win
        dDeck = ["10", "J"]
        pDeck = ["10", "9"]

        dw, pw = bs.compare(pDeck, dDeck)

        self.assertEqual(dw, 1)
        self.assertEqual(pw, 0)

    def test_compare_playerWin(self):  # Player with higher value should win
        dDeck = ["10", "9"]
        pDeck = ["10", "J"]

        dw, pw = bs.compare(pDeck, dDeck)

        self.assertEqual(dw, 0)
        self.assertEqual(pw, 1)

    def test_compare_push(self):  # Same value should push
        dDeck = ["10", "J"]
        pDeck = ["10", "J"]

        dw, pw = bs.compare(pDeck, dDeck)

        self.assertEqual(dw, 0)
        self.assertEqual(pw, 0)
