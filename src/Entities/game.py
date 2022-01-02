from typing import Dict
from typing import List
from typing import Tuple

from ..Entities.cards import Card
from ..Entities.player import Player


class Game:
    def __init__(self):
        self._played_cards: Dict[int, List[Tuple[Player, Card]]] = {}

    def play_card(self, game_round: int, player: Player, card: Card):
        if game_round in self._played_cards:
            self._played_cards[game_round].append((player, card))
        else:
            self._played_cards[game_round] = [(player, card)]

    @property
    def is_over(self) -> bool:
        return False

    def get_winner_team(self):
        pass

    def __repr__(self):
        text = ''
        for n, (game_turn, player_card) in enumerate(self._played_cards.items()):
            played_cards = '|'.join(align_width(make_text(pc), 11) + ' ' * 1 for pc in player_card)
            text += f'\n{n}:    {played_cards}'
        return text


def make_text(pc) -> str:
    player, card = pc
    return str(f'{player}_{card}')


def align_width(text: str, align: int):
    n_blank = align - len(text)
    return f'{text}{" " * n_blank}'
