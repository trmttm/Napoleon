from typing import Dict
from typing import Tuple
from typing import Tuple

from src.Entities import suits
from src.Entities import suits
from src.Entities.bidding import Bidding
from src.Entities.cards import Card
from src.Entities.cards import Cards
from src.Entities.cards import Cards
from src.Entities.player import Player
from src.Entities.player import Player


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


def get_winning_player_index(played_cards: Tuple[Card, ...], player_order: Tuple[int, ...], winning_card: Card) -> int:
    winning_card_turn = played_cards.index(winning_card)
    winning_player_index = player_order[winning_card_turn]
    return winning_player_index


def get_local_suit(played_cards):
    local_suit = played_cards[0].suit
    if local_suit == suits.JOKER:
        local_suit = played_cards[1].suit
    return local_suit


def get_remaining_cards(cards: Cards, players: Tuple[Player, ...]):
    dealt_cards = []
    for player in players:
        dealt_cards += list(player.cards)
    remaining_cards = set(cards.all_cards) - set(dealt_cards)
    return tuple(remaining_cards)