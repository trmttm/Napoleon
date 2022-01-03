from typing import Any
from typing import Callable
from typing import Dict


def the_card_is_all_mighty(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    spade = kwargs.get('spade')
    return (suit == spade) and (number == 1)


def started_with_joker(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    joker = kwargs.get('joker')
    game_round = kwargs.get('game_round')
    return (game_round == 0) and (suit == joker) and (number == 1)


def same_two_applies(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    played_suits = kwargs.get('played_suits')
    all_suits_are_the_same = len(set(played_suits)) == 1
    return (suit == suit) and (number == 2) and all_suits_are_the_same


def is_a_face_jack(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    trump = kwargs.get('trump')
    return (suit == trump) and (number == 11)


def is_a_reverse_jack(**kwargs) -> bool:
    suit = kwargs.get('suit')
    number = kwargs.get('number')
    reverse = kwargs.get('reverse')
    return (suit == reverse) and (number == 11)


def is_a_trump(**kwargs) -> bool:
    suit = kwargs.get('suit')
    trump = kwargs.get('trump')
    return suit == trump


def is_a_local_suit(**kwargs) -> bool:
    suit = kwargs.get('suit')
    local_suit = kwargs.get('local_suit')
    return suit == local_suit


class Rules:
    all_mighty = 'Almighty'
    joker = 'Joker'
    same_two = 'Same Two'
    face_jack = 'Face Jack'
    reverse_jack = 'Reverse Jack'
    trump = 'Trump'
    local_suit = 'Local Suit'

    def __init__(self):
        self._table = {
            self.all_mighty: 700,
            self.joker: 600,
            self.same_two: 500,
            self.face_jack: 400,
            self.reverse_jack: 300,
            self.trump: 200,
            self.local_suit: 100,
        }
        self._rules = {
            self.all_mighty: the_card_is_all_mighty,
            self.joker: started_with_joker,
            self.same_two: same_two_applies,
            self.face_jack: is_a_face_jack,
            self.reverse_jack: is_a_reverse_jack,
            self.trump: is_a_trump,
            self.local_suit: is_a_local_suit,
        }

    @property
    def score_table(self) -> dict:
        return self._table

    def set_score(self, rule_name, score: int):
        self._table[rule_name] = score

    def remove_rule(self, rule_name):
        try:
            del self._table[rule_name]
        except KeyError:
            pass
        try:
            del self._rules[rule_name]
        except KeyError:
            pass

    def add_new_rule(self, rule_name, rule: Callable, score):
        self._table[rule_name] = score
        self._rules[rule_name] = rule

    @property
    def default_rules(self) -> Dict[Any, Callable]:
        return self._rules

    def get_score(self, rule_name) -> int:
        return self._table.get(rule_name, 0)
