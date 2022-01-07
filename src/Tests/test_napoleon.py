import unittest


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


class MyTestCase(unittest.TestCase):

    def test_bidding(self):
        from ..Entities import suits
        from ..Entities import player
        from ..Interactor import implementations as impl
        number_of_players = 5
        players = player.create_players(number_of_players)

        bidding = impl.create_bidding()

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

        def get_all_face_cards(cards_):
            return tuple(c for c in cards_.all_cards if c.number in (1, 10, 11, 12, 13) and c.suit != suits.JOKER)

        interactor = Interactor(5, 10)
        cards = interactor.cards
        all_face_cards = get_all_face_cards(cards)
        interactor.set_all_face_cards(all_face_cards)
        interactor.plug_in_rules(plug_in_rules)
        self._test_expected_player_order(interactor)

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

        remaining_cards = interactor.remaining_cards
        print(remaining_cards)

        napoleon_index = interactor.get_player_index(interactor.napoleon)
        interactor.set_starting_player_index(napoleon_index)
        for game_round in range(interactor.total_number_of_game_rounds):
            for turn, player_index in enumerate(interactor.player_order):
                player = interactor.get_player(player_index)
                choice = 0
                card_played = player.chose_from_playable_cards(choice)
                interactor.play_card(game_round, player, card_played)
                if card_played == adjutant_card:
                    interactor.reveal_adjutant(player)

            # Evaluate game_round
            played_suits = interactor.get_played_suits(game_round)
            played_cards = interactor.get_played_cards(game_round)
            local_suit = interactor.get_local_suit(game_round)

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
            print(interactor._score_keeper)

        # Game over
        print(interactor._game)
        print(interactor._score_keeper)
        print()

        napoleon_score = interactor.get_score(interactor.napoleon)
        adjutant_score = interactor.get_score(interactor._adjutant)
        napoleon_army_score = napoleon_score + adjutant_score

        print(f'Napoleon [{interactor.napoleon}] scored {napoleon_score}')
        print(f'Adjutant [{interactor._adjutant}] scored {adjutant_score}')
        print(f'Napoleon Army scored {napoleon_army_score} vs minimum face cards {interactor.minimum_face_cards}')
        if napoleon_army_score >= interactor.minimum_face_cards:
            print('Napoleon Army won!')
        else:
            print('Alliance won!')

    def _test_expected_player_order(self, interactor):
        expected_player_order = {0: (0, 1, 2, 3, 4),
                                 1: (1, 2, 3, 4, 0),
                                 2: (2, 3, 4, 0, 1),
                                 3: (3, 4, 0, 1, 2),
                                 4: (4, 0, 1, 2, 3)}
        self.assertEqual(interactor._player_orders, expected_player_order)

    def test_main(self):
        from ..Interactor import Interactor
        from ..Entities import suits

        def get_all_face_cards(cards_):
            return tuple(c for c in cards_.all_cards if c.number in (1, 10, 11, 12, 13) and c.suit != suits.JOKER)

        interactor = Interactor(5, 10)
        interactor.present_setting_screen()
        number_of_players = int(input('Set number'))
        interactor.set_number_of_players(number_of_players)

        all_face_cards = get_all_face_cards(interactor.cards)
        interactor.set_all_face_cards(all_face_cards)
        interactor.plug_in_rules(plug_in_rules)
        interactor.shuffle_cards()
        print(f'Cards shuffled.')
        for player in interactor.players:
            print(player, player.cards)

        print('\nBidding started.')
        bidding_is_not_finished = True
        while bidding_is_not_finished:
            player_index, suit, minimum_face_cards = input('Input bidder, suit, minimum_face_cards: ').split(',')
            bidder = interactor.get_player(int(player_index))
            interactor.add_a_bid(bidder, suit, int(minimum_face_cards))
            print(f'Player{bidder} bid, {suit}, {minimum_face_cards}')

            if input('Finished bidding?').lower() in ['y', 'yes', 'true', 't']:
                bidding_is_not_finished = False
                print(f'Player{interactor.napoleon} is Napoleon!')

        suit, number = input('Input adjutant card 1)suit and 2) number.').split(',')
        adjutant_card = interactor.get_card(suit, int(number))
        print(f'Adjutant is {adjutant_card}\n')

        napoleon_cards = list(interactor.napoleon.cards) + list(interactor.remaining_cards)
        [print(f'{n}:{card}') for (n, card) in enumerate(napoleon_cards)]
        cards_to_dispose_index = input('Napoleon, choose 3 cards to dispose.').split(',')
        disposed_cards = tuple(napoleon_cards[int(n)] for n in cards_to_dispose_index)
        new_napoleon_cards = tuple(card for card in napoleon_cards if card not in disposed_cards)
        print(f'\nNapoleon disposed'
              f'\n1:{disposed_cards[0]}'
              f'\n2:{disposed_cards[1]}'
              f'\n3:{disposed_cards[2]}')
        interactor.napoleon.set_cards(new_napoleon_cards)

        napoleon_index = interactor.get_player_index(interactor.napoleon)
        interactor.set_starting_player_index(napoleon_index)
        for game_round in range(interactor.total_number_of_game_rounds):
            print(f'\nRound {game_round}')
            for turn, player_index in enumerate(interactor.player_order):
                player = interactor.get_player(player_index)
                print()
                [print(f'{n}:{c}') for (n, c) in enumerate(player.cards)]
                choice = input(f'Player{player}, chose which card to play')
                card_played = player.chose_from_playable_cards(int(choice))
                interactor.play_card(game_round, player, card_played)
                print(f'Player{player} played {card_played}.')
                if card_played == adjutant_card:
                    interactor.reveal_adjutant(player)

            # Evaluate game_round
            played_suits = interactor.get_played_suits(game_round)
            played_cards = interactor.get_played_cards(game_round)
            local_suit = interactor.get_local_suit(game_round)

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
            print(f'Player{winning_player_index} has won. Obtained {face_cards_obtained}')
            print(interactor._score_keeper)

        # Game over
        print(interactor._game)
        print(interactor._score_keeper)
        print()

        napoleon_score = interactor.get_score(interactor.napoleon)
        adjutant_score = interactor.get_score(interactor._adjutant)
        napoleon_army_score = napoleon_score + adjutant_score

        print(f'Napoleon [{interactor.napoleon}] scored {napoleon_score}')
        print(f'Adjutant [{interactor._adjutant}] scored {adjutant_score}')
        print(f'Napoleon Army scored {napoleon_army_score} vs minimum face cards {interactor.minimum_face_cards}')
        if napoleon_army_score >= interactor.minimum_face_cards:
            print('Napoleon Army won!')
        else:
            print('Alliance won!')


if __name__ == '__main__':
    unittest.main()
