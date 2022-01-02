class Card:
    def __init__(self, suit, number):
        self._number = number
        self._suit = suit

    def __repr__(self) -> str:
        return f'{self._suit}{self._number}'

    def __lt__(self, other: 'Card') -> bool:
        if self._suit != other._suit:
            return self._suit < other._suit
        else:
            return self._number < other._number
