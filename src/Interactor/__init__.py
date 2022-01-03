from typing import Dict
from typing import Tuple

from ..Entities import suits
from ..Entities.bidding import Bidding
from ..Entities.cards import Cards
from ..Entities.player import Player


def create_bidding() -> Bidding:
    bidding = Bidding()
    bidding.set_suit_weight(suits.CLUB, 0)
    bidding.set_suit_weight(suits.DIAMOND, 1)
    bidding.set_suit_weight(suits.HEART, 2)
    bidding.set_suit_weight(suits.SPADE, 3)
    return bidding


def shuffle_cards(cards: Cards, players: Tuple[Player]):
    number_of_players = len(players)
    shuffled_cards = cards.deal_cards(number_of_players, 10)
    for player, dealt_cards in zip(players, shuffled_cards):
        player.set_cards(dealt_cards)


def create_player_orders(number_of_players: int) -> Dict[int, tuple]:
    player_order = {}
    for n in range(number_of_players):
        if n > 0:
            player_order[n] = (0, 1, 2, 3, 4)[n:] + (0, 1, 2, 3, 4)[:n]
        else:
            player_order[n] = (0, 1, 2, 3, 4)[:n] + (0, 1, 2, 3, 4)[n:number_of_players]
    return player_order
