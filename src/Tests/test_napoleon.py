import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        from ..Entities.game_config import GameConfigurations
        from ..Entities import Player
        from ..Entities.cards import Cards

        cards = Cards()
        player1 = Player()
        minimum_face_cards = 12

        game_configurations = GameConfigurations()
        game_configurations.set_napoleon(player1)
        game_configurations.set_adjutant_card(cards.spade_ace)
        game_configurations.set_minimum_face_cards(minimum_face_cards)


if __name__ == '__main__':
    unittest.main()
