import unittest
import Card


class CardTest(unittest.TestCase):
    def setUp(self):
        self.card = Card.Card()

    def testLock(self):
        self.card.lockCard()
        self.assertTrue(self.card.locked)

        self.card.unlockCard()
        self.assertFalse(self.card.locked)


if __name__ == "__main__":
    unittest.main()
