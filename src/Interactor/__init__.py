from typing import Callable
from typing import List
from typing import Tuple

from .. import ResponseModel as response_model
from . import implementations as impl
from ..Entities import player
from ..Entities.card_evaluator import CardEvaluator
from ..Entities.cards import Card
from ..Entities.cards import Cards
from ..Entities.game import Game
from ..Entities.player import Player
from ..Entities.rule_register import RuleRegiser
from ..Entities.rules import Rules
from ..Entities.score_keeper import ScoreKeeper
from ..Interface.presenter import PresentersABC
from ..Presenters.default import PresentersDefault


class Interactor:
    def __init__(self, n_players: int, n_game_rounds: int, presenters: PresentersABC = None):
        self._total_number_of_game_rounds = n_game_rounds
        self._players = player.create_players(n_players)
        self._player_orders = impl.create_player_orders(n_players)
        self._bidding = impl.create_bidding()
        self._cards = Cards()
        self._game = Game()
        self._score_keeper = ScoreKeeper(self._players)
        self._rules = Rules()
        self._rule_register = RuleRegiser(self._cards)
        self._card_evaluator = CardEvaluator(n_game_rounds, self._rules.score_table)

        self._all_face_cards = None
        self._adjutant = None
        self._starting_player_index = None

        self._presenters = presenters if presenters is not None else PresentersDefault()

    def set_number_of_players(self, n_players: int):
        self.__init__(n_players, self._total_number_of_game_rounds)

    def plug_in_rules(self, plug_in_rules: List[Tuple[str, Callable, int]]):
        impl.plug_in_rules(plug_in_rules, self._rule_register, self._rules)

    def set_all_face_cards(self, all_face_cards: Tuple[Card, ...]):
        self._all_face_cards = all_face_cards

    def get_player(self, index_: int) -> Player:
        return self._players[index_]

    def get_player_index(self, player_: Player) -> int:
        return self._players.index(player_)

    def shuffle_cards(self):
        impl.shuffle_cards(self._cards, self._players)

    @property
    def remaining_cards(self) -> Tuple[Card, ...]:
        return impl.get_remaining_cards(self._cards, self._players)

    def add_a_bid(self, player_: Player, suit, minimum_face_cards: int):
        self._bidding.add_a_bid(player_, suit, minimum_face_cards)

    @property
    def napoleon(self) -> Player:
        return self._bidding.napoleon

    @property
    def trump(self) -> Card:
        return self._bidding.trump

    @property
    def minimum_face_cards(self) -> int:
        return self._bidding.minimum_face_cards

    def set_starting_player_index(self, index_: int):
        self._starting_player_index = index_

    @property
    def starting_player_index(self) -> int:
        return self._starting_player_index

    @property
    def player_order(self) -> Tuple[int, ...]:
        return self._player_orders[self.starting_player_index]

    def play_card(self, game_round: int, player_: Player, card: Card):
        self._game.play_card(game_round, player_, card)
        player_.set_cards(tuple(c for c in player_.cards if c != card))

    def get_played_cards(self, game_round: int) -> Tuple[Card, ...]:
        return self._game.get_played_cards(game_round)

    def get_played_suits(self, game_round: int) -> tuple:
        return self._game.get_played_suits(game_round)

    def get_local_suit(self, game_round: int):
        return impl.get_local_suit(self.get_played_cards(game_round))

    def assign_score(self, card: Card, rule_name, game_round: int):
        self._card_evaluator.assign_score(card, rule_name, game_round)

    @property
    def rule_names(self) -> list:
        return self._rule_register.rule_names

    @property
    def conditions(self) -> List[Callable[[dict], bool]]:
        return self._rule_register.conditions

    def reveal_adjutant(self, adjutant: Player):
        self._adjutant = adjutant

    def face_cards_obtained(self, game_round: int) -> Tuple[Card, ...]:
        played_cards = self.get_played_cards(game_round)
        face_cards_obtained = tuple(card for card in played_cards if card in self._all_face_cards)
        return face_cards_obtained

    def next_player_index(self, game_round: int) -> int:
        player_order = self._player_orders[self.starting_player_index]
        played_cards = self.get_played_cards(game_round)
        winning_card = self._card_evaluator.get_winning_card(game_round)
        return impl.get_winning_player_index(played_cards, player_order, winning_card)

    def assign_face_cards(self, next_payer_index: int, face_cards_obtained: Tuple[Card, ...]):
        winning_player = self._players[next_payer_index]
        self._score_keeper.assign_face_cards(winning_player, face_cards_obtained)

    def get_score(self, player_: Player) -> int:
        return self._score_keeper.get_score(player_)

    @property
    def total_number_of_game_rounds(self) -> int:
        return self._total_number_of_game_rounds

    @property
    def players(self) -> Tuple[Player, ...]:
        return self._players

    @property
    def cards(self) -> Cards:
        return self._cards

    def get_card(self, suit, number: int) -> Card:
        return self._cards.get(suit, number)

    def present_setting_screen(self):
        arg1 = len(self._player_orders)
        arg2 = self._total_number_of_game_rounds
        current_setting = response_model.get_current_settings(arg1, arg2)
        self._presenters.present_setting_screen(**current_setting)
