import unittest


class MyTestCase(unittest.TestCase):
    def test_configurations(self):
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
        from ..Entities.bidding import Bidding
        from ..Entities import suits
        from ..Entities import player
        number_of_players = 5
        players = player.create_players(number_of_players)

        bidding = Bidding()
        bidding.set_suit_weight(suits.CLUB, 0)
        bidding.set_suit_weight(suits.DIAMOND, 1)
        bidding.set_suit_weight(suits.HEART, 2)
        bidding.set_suit_weight(suits.SPADE, 3)

        bidding.add_a_bid(players[0], suits.SPADE, 5)
        self.assertEqual(bidding.napoleon, players[0])
        self.assertEqual(bidding.minimum_face_cards, 5)
        self.assertEqual(bidding.trump, suits.SPADE)

        bidding.add_a_bid(players[1], suits.HEART, 4)
        self.assertEqual(bidding.napoleon, players[0])  # Invalid bid players[0] is still napoleon
        self.assertEqual(bidding.minimum_face_cards, 5)
        self.assertEqual(bidding.trump, suits.SPADE)

        bidding.add_a_bid(players[1], suits.HEART, 5)
        self.assertEqual(bidding.napoleon, players[0])  # Invalid bid players[0] is still napoleon
        self.assertEqual(bidding.minimum_face_cards, 5)
        self.assertEqual(bidding.trump, suits.SPADE)

        bidding.add_a_bid(players[1], suits.HEART, 6)
        self.assertEqual(bidding.napoleon, players[1])  # Now players[1] is napoleon
        self.assertEqual(bidding.minimum_face_cards, 6)
        self.assertEqual(bidding.trump, suits.HEART)

    def test_game_interface(self):
        from ..Entities.game import Game
        from ..Entities.cards import Cards
        from ..Entities import player

        number_of_players = 5
        number_of_turns_to_be_played = 10
        players = player.create_players(number_of_players)
        cards = Cards()

        game = Game()
        game.deal_cards()
        for turn in range(number_of_turns_to_be_played):
            game.play_card(players[0], cards.club_ace)
            game.play_card(players[1], cards.club_2)
            game.play_card(players[2], cards.club_3)
            game.play_card(players[3], cards.club_4)
            game.play_card(players[4], cards.club_5)
            if game.is_over:
                break

        winners = game.get_winner_team()
        print(winners)


if __name__ == '__main__':
    unittest.main()
