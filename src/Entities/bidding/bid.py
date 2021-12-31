from ...Entities import Player


class Bid:
    def __init__(self, player: Player, suit, minimum_face_cards: int):
        self._player = player
        self._suit = suit
        self._minimum_face_cards = minimum_face_cards

    @property
    def player(self) -> Player:
        return self._player

    @property
    def suit(self):
        return self._suit

    @property
    def minimum_face_cards(self) -> int:
        return self._minimum_face_cards

    @property
    def score(self) -> int:
        return self._minimum_face_cards * 10
