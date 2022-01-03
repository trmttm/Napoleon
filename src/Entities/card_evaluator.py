from typing import Any
from typing import Dict
from ..Entities.cards import Card


class CardEvaluator:
    def __init__(self, n_total_turns: int, score_table: Dict[Any, int]):
        self._score_table = score_table
        self._card_scores = dict(zip(range(n_total_turns), tuple({} for _ in range(n_total_turns))))

    def assign_score(self, card: Card, score_key, game_round: int):
        current_score = self._get_card_score(game_round, card)
        new_score = self._score_table[score_key] + card.number
        score = max(current_score, new_score)
        self._set_card_score(game_round, card, score)

    def _get_card_score(self, game_round: int, card) -> int:
        return self._card_scores[game_round].get(card, 0)

    def _set_card_score(self, game_round, card: Card, score):
        self._card_scores[game_round][card] = score

    def get_winning_card(self, game_round: int) -> Card:
        scores_in_the_round = self._card_scores[game_round]
        for card, score in scores_in_the_round.items():
            if score == self.get_highest_score(game_round):
                return card

    def get_highest_score(self, game_round: int) -> int:
        scores_in_the_round = self._card_scores[game_round]
        highest_score = max(scores_in_the_round.values())
        return highest_score
