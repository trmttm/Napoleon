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

        shuffled_cards = cards.deal_cards(number_of_players, 10)
        for player, dealt_cards in zip(players, shuffled_cards):
            player.set_cards(dealt_cards)

        game = Game()
        for game_round in range(number_of_turns_to_be_played):
            game.play_card(game_round, players[0], players[0].playable_cards[game_round])
            game.play_card(game_round, players[1], players[1].playable_cards[game_round])
            game.play_card(game_round, players[2], players[2].playable_cards[game_round])
            game.play_card(game_round, players[3], players[3].playable_cards[game_round])
            game.play_card(game_round, players[4], players[4].playable_cards[game_round])
            if game.is_over:
                break

        winners = game.get_winner_team()
        print(game)


if __name__ == '__main__':
    unittest.main()
