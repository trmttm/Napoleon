import unittest


def the_card_is_all_mighty(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    spade = kwargs.get('spade')
    return (suit == spade) and (number == 1)


def started_with_joker(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    joker = kwargs.get('joker')
    game_round = kwargs.get('game_round')
    return (game_round == 0) and (suit == joker) and (number == 1)


def same_two_applies(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    played_suits = kwargs.get('played_suits')
    all_suits_are_the_same = len(set(played_suits)) == 1
    return (suit == suit) and (number == 2) and all_suits_are_the_same


def is_a_face_jack(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    trump = kwargs.get('trump')
    return (suit == trump) and (number == 11)


def is_a_reverse_jack(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    reverse = kwargs.get('reverse')
    return (suit == reverse) and (number == 11)


def is_a_trump(**kwargs) -> bool:
    suit = kwargs.get('suit')
    trump = kwargs.get('trump')
    return suit == trump


def is_a_local_suit(**kwargs) -> bool:
    suit = kwargs.get('suit')
    local_suit = kwargs.get('local_suit')
    return suit == local_suit


def get_local_suit(played_cards):
    from ..Entities import suits
    local_suit = played_cards[0].suit
    if local_suit == suits.JOKER:
        local_suit = played_cards[1].suit
    return local_suit


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
        from ..Entities.card_evaluator import CardEvaluator
        from ..Entities.game_rules import GameRules
        from ..Entities.score_keeper import ScoreKeeper
        from .. import Interactor as interactor

        n_total_turns = 10
        players = player.create_players(5)
        cards = Cards()

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

        game = Game()
        player_orders = interactor.create_player_orders(len(players))
        expected_player_order = {0: (0, 1, 2, 3, 4),
                                 1: (1, 2, 3, 4, 0),
                                 2: (2, 3, 4, 0, 1),
                                 3: (3, 4, 0, 1, 2),
                                 4: (4, 0, 1, 2, 3)}
        self.assertEqual(player_orders, expected_player_order)

        score_all_mighty = 'all_mighty'
        score_joker = 'jack'
        score_same_two = 'same_two'
        score_face_jack = 'face_jack'
        score_reverse_jack = 'reverse_jack'
        score_trump = 'trump'
        score_local_suit = 'local_suit'
        score_table = {
            score_all_mighty: 700,
            score_joker: 600,
            score_same_two: 500,
            score_face_jack: 400,
            score_reverse_jack: 300,
            score_trump: 200,
            score_local_suit: 100,
        }
        card_evaluator = CardEvaluator(n_total_turns, score_table)

        score_keeper = ScoreKeeper(players)

        all_face_cards = tuple(c for c in cards.all_cards if c.number in (1, 10, 11, 12, 13) and c.suit != suits.JOKER)
        game_rules = GameRules(cards)
        game_rules.add_a_rule(the_card_is_all_mighty, score_all_mighty)
        game_rules.add_a_rule(started_with_joker, score_joker)
        game_rules.add_a_rule(same_two_applies, score_same_two)
        game_rules.add_a_rule(is_a_face_jack, score_face_jack)
        game_rules.add_a_rule(is_a_reverse_jack, score_reverse_jack)
        game_rules.add_a_rule(is_a_trump, score_trump)
        game_rules.add_a_rule(is_a_local_suit, score_local_suit)

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
                    'played_cards': played_cards,
                    'spade': suits.SPADE,
                    'heart': suits.HEART,
                    'diamond': suits.DIAMOND,
                    'club': suits.CLUB,
                    'joker': suits.JOKER,
                }
                for condition, score_key in zip(game_rules.conditions, game_rules.score_keys):
                    if condition(**data_transfer_object):
                        card_evaluator.assign_score(card, score_key, game_round)
                        if score_key not in (score_local_suit, score_trump):
                            print(f'{game_round}: {card} is a {score_key}')

            winning_card = card_evaluator.get_winning_card(game_round)
            winning_card_turn = played_cards.index(winning_card)
            player_index = player_order[winning_card_turn]
            winning_player = players[player_index]
            face_cards = tuple(card for card in played_cards if card in all_face_cards)
            score_keeper.assign_face_cards(winning_player, face_cards)
            starting_player_index = player_index

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
