from typing import Callable
from typing import List

from .cards import Cards


class RuleRegiser:
    def __init__(self, cards: Cards):
        self._cards = cards
        self._conditions: List[Callable[[dict], bool]] = []
        self._rule_names: list = []

    def add_a_rule(self, condition: Callable[[dict], bool], score_key):
        self._conditions.append(condition)
        self._rule_names.append(score_key)

    @property
    def conditions(self) -> List[Callable[[dict], bool]]:
        return self._conditions

    @property
    def rule_names(self) -> list:
        return self._rule_names
