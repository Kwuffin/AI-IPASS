import unittest
import blackjackGame as bg


class TestBlackjackGame(unittest.TestCase):

    def test_dealerAfterDraw(self):  # Dealer should draw when value is below 17
        deck = ["10", "6"]

        bg.dealerAfter(deck)

        self.assertTrue(len(deck) > 2)

    def test_dealerAfterNoDraw(self):  # Dealer should NOT draw when value is above 17
        deck = ["10", "7"]

        bg.dealerAfter(deck)

        self.assertTrue(len(deck) == 2)
