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
        self._all_cards = (
            self.spade_king,
            self.spade_queen,
            self.spade_jack,
            self.spade_10,
            self.spade_9,
            self.spade_8,
            self.spade_7,
            self.spade_6,
            self.spade_5,
            self.spade_4,
            self.spade_3,
            self.spade_2,
            self.spade_ace,
            self.heart_king,
            self.heart_queen,
            self.heart_jack,
            self.heart_10,
            self.heart_9,
            self.heart_8,
            self.heart_7,
            self.heart_6,
            self.heart_5,
            self.heart_4,
            self.heart_3,
            self.heart_2,
            self.heart_ace,
            self.diamond_king,
            self.diamond_queen,
            self.diamond_jack,
            self.diamond_10,
            self.diamond_9,
            self.diamond_8,
            self.diamond_7,
            self.diamond_6,
            self.diamond_5,
            self.diamond_4,
            self.diamond_3,
            self.diamond_2,
            self.diamond_ace,
            self.club_king,
            self.club_queen,
            self.club_jack,
            self.club_10,
            self.club_9,
            self.club_8,
            self.club_7,
            self.club_6,
            self.club_5,
            self.club_4,
            self.club_3,
            self.club_2,
            self.club_ace,
            self.joker,
        )

    def deal_cards(self, n_players: int, n_cards_per_player: int) -> List[List[Card]]:
        all_cards = list(self._all_cards)
        random.shuffle(all_cards)
        dealt_cards = []
        for n in range(n_players):
            dealt_card = all_cards[n_cards_per_player * n:n_cards_per_player * (n + 1)]
            dealt_cards.append(sorted(dealt_card))
        dealt_cards.append(sorted(all_cards[n_cards_per_player * n_players:]))
        return dealt_cards
