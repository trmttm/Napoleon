from typing import Iterable
from typing import Tuple

from .cards import Card


class Player:
    def __init__(self, name):
        self._cards = None
        self._name = name

    @property
    def playable_cards(self) -> Tuple[Card]:
        return tuple(self._cards)

    def set_cards(self, cards: Iterable[Card]):
        self._cards = cards

    def __repr__(self) -> str:
        return f'{self._name}'


def create_players(number_of_players) -> Tuple[Player]:
    players = tuple(Player(n) for n in range(number_of_players))
    return players
