import unittest

import src.Interactor.implementations


def yoromeki(**kwargs) -> bool:
    played_cards_ = kwargs.get('played_cards')
    spade = kwargs.get('spade')
    heart = kwargs.get('heart')
    almighty_is_played = (spade, 1) in played_cards_
    hear_queen_is_played = (heart, 12) in played_cards_
    return almighty_is_played and hear_queen_is_played


plug_in_rules = [
    ('Yoromeki', yoromeki, 800),
]


def get_local_suit(played_cards):
    from ..Entities import suits
    local_suit = played_cards[0].suit
    if local_suit == suits.JOKER:
        local_suit = played_cards[1].suit
    return local_suit


class MyTestCase(unittest.TestCase):

    def test_bidding(self):
        from ..Entities import suits
        from ..Entities import player
        number_of_players = 5
        players = player.create_players(number_of_players)

        bidding = src.Interactor.implementations.create_bidding()

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
        # Set up
        from ..Entities import suits
        from ..Interactor import Interactor

        n_total_turns = 10
        n_players = 5
        interactor = Interactor(n_players, n_total_turns)
        expected_player_order = {0: (0, 1, 2, 3, 4),
                                 1: (1, 2, 3, 4, 0),
                                 2: (2, 3, 4, 0, 1),
                                 3: (3, 4, 0, 1, 2),
                                 4: (4, 0, 1, 2, 3)}
        self.assertEqual(interactor.player_orders, expected_player_order)
        cards = interactor.cards

        interactor.plug_in_rules(plug_in_rules)
        all_face_cards = tuple(c for c in cards.all_cards if c.number in (1, 10, 11, 12, 13) and c.suit != suits.JOKER)
        interactor.set_all_face_cards(all_face_cards)
        # Game Play
        interactor.shuffle_cards()

        interactor.add_a_bid(interactor.get_player(0), suits.SPADE, 5)
        interactor.add_a_bid(interactor.get_player(1), suits.DIAMOND, 6)
        interactor.add_a_bid(interactor.get_player(2), suits.HEART, 6)
        interactor.add_a_bid(interactor.get_player(3), suits.CLUB, 7)
        interactor.add_a_bid(interactor.get_player(0), suits.SPADE, 7)
        adjutant_card = cards.spade_ace

        self.assertEqual(interactor.napoleon, interactor.get_player(0))
        self.assertEqual(interactor.trump, suits.SPADE)
        self.assertEqual(interactor.minimum_face_cards, 7)

        napoleon_index = interactor.get_player_index(interactor.napoleon)
        interactor.set_starting_player_index(napoleon_index)
        for game_round in range(n_total_turns):
            for turn, winning_player_index in enumerate(interactor.player_order):
                player = interactor.get_player(winning_player_index)
                choice = game_round  # arbitrary
                card_played = player.chose_from_playable_cards(choice)
                interactor.play_card(game_round, player, card_played)
                if card_played == adjutant_card:
                    interactor.reveal_adjutant(player)

            # Evaluate game_round
            played_suits = interactor.get_played_suits(game_round)
            played_cards = interactor.get_played_cards(game_round)
            local_suit = get_local_suit(played_cards)

            for turn, card in enumerate(played_cards):
                data_transfer_object = {
                    'game_round': game_round,
                    'turn': turn,
                    'suit': card.suit,
                    'reverse': suits.get_reverse(interactor.trump),
                    'number': card.number,
                    'trump': interactor.trump,
                    'local_suit': local_suit,
                    'played_suits': played_suits,
                    'played_cards': tuple((c.suit, c.number) for c in played_cards),
                    'spade': suits.SPADE,
                    'heart': suits.HEART,
                    'diamond': suits.DIAMOND,
                    'club': suits.CLUB,
                    'joker': suits.JOKER,
                }
                for condition, rule_name in zip(interactor.conditions, interactor.rule_names):
                    if condition(**data_transfer_object):
                        # card_evaluator.assign_score(card, rule_name, game_round)
                        interactor.assign_score(card, rule_name, game_round)

            winning_player_index = interactor.next_player_index(game_round)
            face_cards_obtained = interactor.face_cards_obtained(game_round)
            interactor.assign_face_cards(winning_player_index, face_cards_obtained)
            interactor.set_starting_player_index(winning_player_index)
            print(interactor.score_keeper)

        # Game over
        print(interactor.game)
        print(interactor.score_keeper)
        print()

        napoleon_score = interactor.get_score(interactor.napoleon)
        adjutant_score = interactor.get_score(interactor.adjutant)
        napoleon_army_score = napoleon_score + adjutant_score

        print(f'Napoleon [{interactor.napoleon}] scored {napoleon_score}')
        print(f'Adjutant [{interactor.adjutant}] scored {adjutant_score}')
        print(f'Napoleon Army scored {napoleon_army_score} vs minimum face cards {interactor.minimum_face_cards}')
        if napoleon_army_score >= interactor.minimum_face_cards:
            print('Napoleon Army won!')
        else:
            print('Alliance won!')


if __name__ == '__main__':
    unittest.main()
