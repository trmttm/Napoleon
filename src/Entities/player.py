from typing import Iterable
from typing import Tuple

from .cards import Card


class Player:
    def __init__(self, name):
        self._cards: Iterable[Card] = ()
        self._name = name

    def chose_from_playable_cards(self, index_: int) -> Card:
        return tuple(self._cards)[index_]

    def set_cards(self, cards: Iterable[Card]):
        self._cards = cards

    @property
    def cards(self) -> Iterable[Card]:
        return self._cards

    def __repr__(self) -> str:
        return f'{self._name}'


def create_players(number_of_players) -> Tuple[Player]:
    players = tuple(Player(n) for n in range(number_of_players))
    return players
