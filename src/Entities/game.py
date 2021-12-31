from ..Entities.cards import Card
from ..Entities.player import Player


class Game:
    def deal_cards(self):
        pass

    def play_card(self, player: Player, card: Card):
        pass

    @property
    def is_over(self) -> bool:
        return

    def get_winner_team(self):
        pass
