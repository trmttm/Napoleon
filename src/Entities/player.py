from typing import Tuple


class Player:
    pass


def create_players(number_of_players) -> Tuple[Player]:
    players = tuple(Player() for _ in range(number_of_players))
    return players
