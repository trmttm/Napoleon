from typing import Any
from typing import Dict
from typing import List

from .bid import Bid
from .. import suits
from ..player import Player


class Bidding:
    def __init__(self):
        self._bidding_data: List[Bid] = []
        self._suit_weight: Dict[Any, int] = {
            suits.SPADE: 0,
            suits.HEART: 0,
            suits.DIAMOND: 0,
            suits.CLUB: 0,
        }

    def set_suit_weight(self, suit, weight: int):
        self._suit_weight[suit] = weight

    def add_a_bid(self, player: Player, suit: str, minimum_face_cards: int):
        new_bid = Bid(player, suit.strip(), minimum_face_cards)
        score = self._evaluate_bid(new_bid)
        if score > self._highest_score:
            self._bidding_data.append(new_bid)

    def _evaluate_bid(self, bid_to_evaluate: Bid) -> int:
        return bid_to_evaluate.score + self._suit_weight.get(bid_to_evaluate.suit, 0)

    @property
    def _highest_score(self) -> int:
        if self._bidding_data:
            last_bid = self._bidding_data[-1]
            score = self._evaluate_bid(last_bid)
            return score
        else:
            return 0

    @property
    def napoleon(self) -> Player:
        if self._bidding_data:
            last_bid = self._bidding_data[-1]
            return last_bid.player

    @property
    def minimum_face_cards(self) -> int:
        if self._bidding_data:
            last_bid = self._bidding_data[-1]
            return last_bid.minimum_face_cards

    @property
    def trump(self):
        if self._bidding_data:
            last_bid = self._bidding_data[-1]
            return last_bid.suit
