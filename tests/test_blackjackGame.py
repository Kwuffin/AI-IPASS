import unittest
import blackjackGame as bg


class TestBlackjackGame(unittest.TestCase):

    def test_dealerAfterDraw(self):
        deck = ["10", "6"]

        bg.dealerAfter(deck)

        self.assertTrue(len(deck) > 2)

    def test_dealerAfterNoDraw(self):
        deck = ["10", "7"]

        bg.dealerAfter(deck)

        self.assertTrue(len(deck) == 2)
