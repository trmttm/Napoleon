from typing import Callable
from typing import List
from typing import Tuple

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


class Interactor:
    def __init__(self, n_players: int, n_game_rounds: int):
        self.total_number_of_game_rounds = n_game_rounds
        self.players = player.create_players(n_players)
        self.player_orders = impl.create_player_orders(n_players)
        self.bidding = impl.create_bidding()
        self.cards = Cards()
        self.game = Game()
        self.score_keeper = ScoreKeeper(self.players)
        self.rules = Rules()
        self.rule_register = RuleRegiser(self.cards)
        self.card_evaluator = CardEvaluator(n_game_rounds, self.rules.score_table)

        self._all_face_cards = None
        self.adjutant = None
        self._starting_player_index = None

    def plug_in_rules(self, plug_in_rules: List[Tuple[str, Callable, int]]):
        rules = self.rules
        for rule_name, rule, score in plug_in_rules:
            rules.add_new_rule(rule_name, rule, score)
        self._register_rules()

    def set_all_face_cards(self, all_face_cards: Tuple[Card, ...]):
        self._all_face_cards = all_face_cards

    def _register_rules(self):
        rules = self.rules
        rule_register = self.rule_register
        for rule_name, rule in rules.default_rules.items():
            rule_register.add_a_rule(rule, rule_name)

    def get_player(self, index_: int) -> Player:
        return self.players[index_]

    def get_player_index(self, player_: Player) -> int:
        return self.players.index(player_)

    def shuffle_cards(self):
        impl.shuffle_cards(self.cards, self.players)

    @property
    def remaining_cards(self) -> Tuple[Card, ...]:
        players = self.players
        cards = self.cards
        return impl.get_remaining_cards(cards, players)

    def add_a_bid(self, player_: Player, suit, minimum_face_cards: int):
        self.bidding.add_a_bid(player_, suit, minimum_face_cards)

    @property
    def napoleon(self) -> Player:
        return self.bidding.napoleon

    @property
    def trump(self) -> Card:
        return self.bidding.trump

    @property
    def minimum_face_cards(self) -> int:
        return self.bidding.minimum_face_cards

    def set_starting_player_index(self, index_: int):
        self._starting_player_index = index_

    @property
    def starting_player_index(self) -> int:
        return self._starting_player_index

    @property
    def player_order(self) -> Tuple[int, ...]:
        return self.player_orders[self.starting_player_index]

    def play_card(self, game_round: int, player_: Player, card: Card):
        self.game.play_card(game_round, player_, card)
        player_.set_cards(tuple(c for c in player_.cards if c != card))

    def get_played_cards(self, game_round: int) -> Tuple[Card, ...]:
        return self.game.get_played_cards(game_round)

    def get_played_suits(self, game_round: int) -> tuple:
        return self.game.get_played_suits(game_round)

    def get_local_suit(self, game_round: int):
        return impl.get_local_suit(self.get_played_cards(game_round))

    def assign_score(self, card: Card, rule_name, game_round: int):
        self.card_evaluator.assign_score(card, rule_name, game_round)

    @property
    def rule_names(self) -> list:
        return self.rule_register.rule_names

    @property
    def conditions(self) -> List[Callable[[dict], bool]]:
        return self.rule_register.conditions

    def reveal_adjutant(self, adjutant: Player):
        self.adjutant = adjutant

    def face_cards_obtained(self, game_round: int) -> Tuple[Card, ...]:
        played_cards = self.get_played_cards(game_round)
        face_cards_obtained = tuple(card for card in played_cards if card in self._all_face_cards)
        return face_cards_obtained

    def next_player_index(self, game_round: int) -> int:
        player_order = self.player_orders[self.starting_player_index]
        played_cards = self.get_played_cards(game_round)
        winning_card = self.card_evaluator.get_winning_card(game_round)
        return impl.get_winning_player_index(played_cards, player_order, winning_card)

    def assign_face_cards(self, next_payer_index: int, face_cards_obtained: Tuple[Card, ...]):
        winning_player = self.players[next_payer_index]
        self.score_keeper.assign_face_cards(winning_player, face_cards_obtained)

    def get_score(self, player_: Player) -> int:
        return self.score_keeper.get_score(player_)
