import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        from ..Entities.game_config import GameConfigurations
        from ..Entities.cards import Cards
        from ..Entities.bidding import Bidding

        bidding = Bidding()
        napoleon = bidding.napoleon
        minimum_face_cards = bidding.minimum_face_cards

        cards = Cards()
        adjutant_card = cards.spade_ace

        game_configurations = GameConfigurations()
        game_configurations.set_napoleon(napoleon)
        game_configurations.set_adjutant_card(adjutant_card)
        game_configurations.set_minimum_face_cards(minimum_face_cards)

    def test_bidding(self):
        from ..Entities.player import Player
        from ..Entities.bidding import Bidding
        from ..Entities.cards import SPADE, HEART, DIAMOND, CLUB
        number_of_players = 5
        players = tuple(Player() for _ in range(number_of_players))

        bidding = Bidding()
        bidding.set_suit_weight(CLUB, 0)
        bidding.set_suit_weight(DIAMOND, 1)
        bidding.set_suit_weight(HEART, 2)
        bidding.set_suit_weight(SPADE, 3)

        bidding.add_a_bid(players[0], SPADE, 5)
        self.assertEqual(bidding.napoleon, players[0])
        self.assertEqual(bidding.minimum_face_cards, 5)
        self.assertEqual(bidding.trump, SPADE)

        bidding.add_a_bid(players[1], HEART, 4)
        self.assertEqual(bidding.napoleon, players[0])  # Invalid bid players[0] is still napoleon
        self.assertEqual(bidding.minimum_face_cards, 5)
        self.assertEqual(bidding.trump, SPADE)

        bidding.add_a_bid(players[1], HEART, 5)
        self.assertEqual(bidding.napoleon, players[0])  # Invalid bid players[0] is still napoleon
        self.assertEqual(bidding.minimum_face_cards, 5)
        self.assertEqual(bidding.trump, SPADE)

        bidding.add_a_bid(players[1], HEART, 6)
        self.assertEqual(bidding.napoleon, players[1])  # Now players[1] is napoleon
        self.assertEqual(bidding.minimum_face_cards, 6)
        self.assertEqual(bidding.trump, HEART)


if __name__ == '__main__':
    unittest.main()
