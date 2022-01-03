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
        from ..Entities import suits
        from ..Entities import player
        from .. import Interactor as interactor
        number_of_players = 5
        players = player.create_players(number_of_players)

        bidding = interactor.create_bidding()

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
        from ..Entities import suits
        from ..Entities import player
        from .. import Interactor as interactor

        number_of_turns_to_be_played = 10
        players = player.create_players(5)
        cards = Cards()

        interactor.shuffle_cards(cards, players)

        bidding = interactor.create_bidding()
        bidding.add_a_bid(players[0], suits.SPADE, 5)
        bidding.add_a_bid(players[1], suits.DIAMOND, 6)
        bidding.add_a_bid(players[2], suits.HEART, 6)
        bidding.add_a_bid(players[3], suits.CLUB, 7)
        bidding.add_a_bid(players[0], suits.SPADE, 7)
        napoleon = bidding.napoleon
        trump = bidding.trump
        minimum_face_cards = bidding.minimum_face_cards

        self.assertEqual(napoleon, players[0])
        self.assertEqual(trump, suits.SPADE)
        self.assertEqual(minimum_face_cards, 7)

        game = Game()
        player_orders = interactor.create_player_orders(len(players))
        expected_player_order = {0: (0, 1, 2, 3, 4),
                                 1: (1, 2, 3, 4, 0),
                                 2: (2, 3, 4, 0, 1),
                                 3: (3, 4, 0, 1, 2),
                                 4: (4, 0, 1, 2, 3)}
        self.assertEqual(player_orders, expected_player_order)

        score_all_mighty = 'all_mighty'
        score_same_two = 'same_two'
        score_face_jack = 'face_jack'
        score_reverse_jack = 'reverse_jack'
        score_trump = 'trump'
        score_local_suit = 'local_suit'
        scores = {
            score_all_mighty: 100,
            score_same_two: 100,
        }
        starting_player_index = players.index(napoleon)
        for game_round in range(number_of_turns_to_be_played):
            player_order = player_orders[starting_player_index]
            for turn, player_index in enumerate(player_order):
                player = players[player_index]
                choice = game_round  # arbitrary
                card_played = player.chose_from_playable_cards(choice)
                game.play_card(game_round, player, card_played)

            # Evaluate game_round
            played_suits = game.get_played_suits(game_round)
            played_cards = game.get_played_cards(game_round)
            local_suit = played_cards[0].suit
            if local_suit == suits.JOKER:
                local_suit = played_cards[1].suit

            card_scores = dict(zip(played_cards, tuple(0 for _ in played_cards)))
            all_suits_are_the_same = len(set(played_suits)) == 1
            card_same_two = cards.get(local_suit, 2)
            if all_suits_are_the_same and card_same_two in played_cards:
                print(f'{game_round}: Local suit: {local_suit}, Same2 = {card_same_two}')
                card_scores[card_same_two] += scores[score_same_two]
            starting_player_index = 1

        winners = game.get_winner_team()
        print(game)


if __name__ == '__main__':
    unittest.main()
