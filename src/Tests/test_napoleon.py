import unittest


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
        from ..Entities.card_evaluator import CardEvaluator
        from ..Entities.rule_register import RuleRegiser
        from ..Entities.score_keeper import ScoreKeeper
        from ..Entities.rules import Rules
        from .. import Interactor as interactor

        n_total_turns = 10

        players = player.create_players(5)
        cards = Cards()
        game = Game()
        rules = Rules()

        def yoromeki(**kwargs) -> bool:
            played_cards = kwargs.get('played_cards')
            spade = kwargs.get('spade')
            heart = kwargs.get('heart')
            almighty_is_played = (spade, 1) in played_cards
            hear_queen_is_played = (heart, 12) in played_cards
            return almighty_is_played and hear_queen_is_played

        rules.add_new_rule('Yoromeki', yoromeki, 800)
        rule_register = RuleRegiser(cards)
        card_evaluator = CardEvaluator(n_total_turns, rules.score_table)
        score_keeper = ScoreKeeper(players)

        all_face_cards = tuple(c for c in cards.all_cards if c.number in (1, 10, 11, 12, 13) and c.suit != suits.JOKER)
        for rule_name, rule in rules.default_rules.items():
            rule_register.add_a_rule(rule, rule_name)

        interactor.shuffle_cards(cards, players)
        adjutant = None
        adjutant_card = cards.spade_ace

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

        player_orders = interactor.create_player_orders(len(players))
        expected_player_order = {0: (0, 1, 2, 3, 4),
                                 1: (1, 2, 3, 4, 0),
                                 2: (2, 3, 4, 0, 1),
                                 3: (3, 4, 0, 1, 2),
                                 4: (4, 0, 1, 2, 3)}
        self.assertEqual(player_orders, expected_player_order)

        starting_player_index = players.index(napoleon)
        for game_round in range(n_total_turns):
            player_order = player_orders[starting_player_index]
            for turn, player_index in enumerate(player_order):
                player = players[player_index]
                choice = game_round  # arbitrary
                card_played = player.chose_from_playable_cards(choice)
                game.play_card(game_round, player, card_played)
                if card_played == adjutant_card:
                    adjutant = player

            # Evaluate game_round
            played_suits = game.get_played_suits(game_round)
            played_cards = game.get_played_cards(game_round)
            local_suit = get_local_suit(played_cards)

            for turn, card in enumerate(played_cards):
                data_transfer_object = {
                    'game_round': game_round,
                    'turn': turn,
                    'suit': card.suit,
                    'reverse': suits.get_reverse(trump),
                    'number': card.number,
                    'trump': trump,
                    'local_suit': local_suit,
                    'played_suits': played_suits,
                    'played_cards': tuple((c.suit, c.number) for c in played_cards),
                    'spade': suits.SPADE,
                    'heart': suits.HEART,
                    'diamond': suits.DIAMOND,
                    'club': suits.CLUB,
                    'joker': suits.JOKER,
                }
                for condition, rule_name in zip(rule_register.conditions, rule_register.score_keys):
                    if condition(**data_transfer_object):
                        card_evaluator.assign_score(card, rule_name, game_round)
                        if rule_name not in (rules.local_suit, rules.trump):
                            print(f'{game_round}: {card} is a {rule_name}')

            winning_card = card_evaluator.get_winning_card(game_round)
            winning_card_turn = played_cards.index(winning_card)
            player_index = player_order[winning_card_turn]
            winning_player = players[player_index]
            face_cards = tuple(card for card in played_cards if card in all_face_cards)
            score_keeper.assign_face_cards(winning_player, face_cards)
            starting_player_index = player_index
            print(score_keeper)

        print(game)
        print(score_keeper)
        print()

        napoleon_score = score_keeper.get_score(napoleon)
        adjutant_score = score_keeper.get_score(adjutant)
        napoleon_army_score = napoleon_score + adjutant_score

        print(f'Napoleon [{napoleon}] scored {napoleon_score}')
        print(f'Adjutant [{adjutant}] scored {adjutant_score}')
        print(f'Napoleon Army scored {napoleon_army_score} vs minimum face cards {minimum_face_cards}')
        if napoleon_army_score >= minimum_face_cards:
            print('Napoleon Army won!')
        else:
            print('Alliance won!')


if __name__ == '__main__':
    unittest.main()
