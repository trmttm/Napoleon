from typing import Callable
from typing import List

from .cards import Card
from .cards import Cards


class GameRules:
    def __init__(self, cards: Cards):
        self._cards = cards
        self._conditions: List[Callable[[dict], bool]] = []
        self._score_keys: list = []

    def add_a_rule(self, condition: Callable[[dict], bool], score_key):
        self._conditions.append(condition)
        self._score_keys.append(score_key)

    @property
    def conditions(self) -> List[Callable[[dict], bool]]:
        return self._conditions

    @property
    def score_keys(self) -> list:
        return self._score_keys
