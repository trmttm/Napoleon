import random
from typing import List

from .card import Card
from .. import suits


class Cards:
    spade_king = Card(suits.SPADE, 13)
    spade_queen = Card(suits.SPADE, 12)
    spade_jack = Card(suits.SPADE, 11)
    spade_10 = Card(suits.SPADE, 10)
    spade_9 = Card(suits.SPADE, 9)
    spade_8 = Card(suits.SPADE, 8)
    spade_7 = Card(suits.SPADE, 7)
    spade_6 = Card(suits.SPADE, 6)
    spade_5 = Card(suits.SPADE, 5)
    spade_4 = Card(suits.SPADE, 4)
    spade_3 = Card(suits.SPADE, 3)
    spade_2 = Card(suits.SPADE, 2)
    spade_ace = Card(suits.SPADE, 1)

    heart_king = Card(suits.HEART, 13)
    heart_queen = Card(suits.HEART, 12)
    heart_jack = Card(suits.HEART, 11)
    heart_10 = Card(suits.HEART, 10)
    heart_9 = Card(suits.HEART, 9)
    heart_8 = Card(suits.HEART, 8)
    heart_7 = Card(suits.HEART, 7)
    heart_6 = Card(suits.HEART, 6)
    heart_5 = Card(suits.HEART, 5)
    heart_4 = Card(suits.HEART, 4)
    heart_3 = Card(suits.HEART, 3)
    heart_2 = Card(suits.HEART, 2)
    heart_ace = Card(suits.HEART, 1)

    diamond_king = Card(suits.DIAMOND, 13)
    diamond_queen = Card(suits.DIAMOND, 12)
    diamond_jack = Card(suits.DIAMOND, 11)
    diamond_10 = Card(suits.DIAMOND, 10)
    diamond_9 = Card(suits.DIAMOND, 9)
    diamond_8 = Card(suits.DIAMOND, 8)
    diamond_7 = Card(suits.DIAMOND, 7)
    diamond_6 = Card(suits.DIAMOND, 6)
    diamond_5 = Card(suits.DIAMOND, 5)
    diamond_4 = Card(suits.DIAMOND, 4)
    diamond_3 = Card(suits.DIAMOND, 3)
    diamond_2 = Card(suits.DIAMOND, 2)
    diamond_ace = Card(suits.DIAMOND, 1)

    club_king = Card(suits.CLUB, 13)
    club_queen = Card(suits.CLUB, 12)
    club_jack = Card(suits.CLUB, 11)
    club_10 = Card(suits.CLUB, 10)
    club_9 = Card(suits.CLUB, 9)
    club_8 = Card(suits.CLUB, 8)
    club_7 = Card(suits.CLUB, 7)
    club_6 = Card(suits.CLUB, 6)
    club_5 = Card(suits.CLUB, 5)
    club_4 = Card(suits.CLUB, 4)
    club_3 = Card(suits.CLUB, 3)
    club_2 = Card(suits.CLUB, 2)
    club_ace = Card(suits.CLUB, 1)

    joker = Card(suits.JOKER, 1)

    def __init__(self, n_jokers: int = 1):
        self._all_cards = {
            (suits.SPADE, 13): self.spade_king,
            (suits.SPADE, 12): self.spade_queen,
            (suits.SPADE, 11): self.spade_jack,
            (suits.SPADE, 10): self.spade_10,
            (suits.SPADE, 9): self.spade_9,
            (suits.SPADE, 8): self.spade_8,
            (suits.SPADE, 7): self.spade_7,
            (suits.SPADE, 6): self.spade_6,
            (suits.SPADE, 5): self.spade_5,
            (suits.SPADE, 4): self.spade_4,
            (suits.SPADE, 3): self.spade_3,
            (suits.SPADE, 2): self.spade_2,
            (suits.SPADE, 1): self.spade_ace,

            (suits.HEART, 13): self.heart_king,
            (suits.HEART, 12): self.heart_queen,
            (suits.HEART, 11): self.heart_jack,
            (suits.HEART, 10): self.heart_10,
            (suits.HEART, 9): self.heart_9,
            (suits.HEART, 8): self.heart_8,
            (suits.HEART, 7): self.heart_7,
            (suits.HEART, 6): self.heart_6,
            (suits.HEART, 5): self.heart_5,
            (suits.HEART, 4): self.heart_4,
            (suits.HEART, 3): self.heart_3,
            (suits.HEART, 2): self.heart_2,
            (suits.HEART, 1): self.heart_ace,

            (suits.DIAMOND, 13): self.diamond_king,
            (suits.DIAMOND, 12): self.diamond_queen,
            (suits.DIAMOND, 11): self.diamond_jack,
            (suits.DIAMOND, 10): self.diamond_10,
            (suits.DIAMOND, 9): self.diamond_9,
            (suits.DIAMOND, 8): self.diamond_8,
            (suits.DIAMOND, 7): self.diamond_7,
            (suits.DIAMOND, 6): self.diamond_6,
            (suits.DIAMOND, 5): self.diamond_5,
            (suits.DIAMOND, 4): self.diamond_4,
            (suits.DIAMOND, 3): self.diamond_3,
            (suits.DIAMOND, 2): self.diamond_2,
            (suits.DIAMOND, 1): self.diamond_ace,

            (suits.CLUB, 13): self.club_king,
            (suits.CLUB, 12): self.club_queen,
            (suits.CLUB, 11): self.club_jack,
            (suits.CLUB, 10): self.club_10,
            (suits.CLUB, 9): self.club_9,
            (suits.CLUB, 8): self.club_8,
            (suits.CLUB, 7): self.club_7,
            (suits.CLUB, 6): self.club_6,
            (suits.CLUB, 5): self.club_5,
            (suits.CLUB, 4): self.club_4,
            (suits.CLUB, 3): self.club_3,
            (suits.CLUB, 2): self.club_2,
            (suits.CLUB, 1): self.club_ace,

            (suits.JOKER, 1): self.joker,
        }

    def deal_cards(self, n_players: int, n_cards_per_player: int) -> List[List[Card]]:
        all_cards = list(self._all_cards.values())
        random.shuffle(all_cards)
        dealt_cards = []
        for n in range(n_players):
            dealt_card = all_cards[n_cards_per_player * n:n_cards_per_player * (n + 1)]
            dealt_cards.append(sorted(dealt_card))
        dealt_cards.append(sorted(all_cards[n_cards_per_player * n_players:]))
        return dealt_cards

    def get(self, suit, number) -> Card:
        return self._all_cards[(suit, number)]
