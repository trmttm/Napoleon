from typing import Dict
from typing import List
from typing import Tuple

from .cards import Card
from .player import Player


class ScoreKeeper:
    def __init__(self, players: Tuple[Player, ...]):
        self._score: Dict[Player, List[Card, ...]] = dict(zip(players, tuple([] for _ in players)))

    def assign_face_cards(self, player: Player, face_cards: Tuple[Card, ...]):
        self._score[player] += list(face_cards)

    def get_score(self, player: Player) -> int:
        return len(self._score[player])

    def __repr__(self):
        text = ''
        for player, cards in self._score.items():
            text += f'\nPlayer {player} got {len(cards)} face cards: {sorted(cards)}'
        return text
