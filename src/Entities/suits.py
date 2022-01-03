SPADE = 'Spade'
HEART = 'Heart'
DIAMOND = 'Diamond'
CLUB = 'Club'
JOKER = 'Joker'
REVERSE = {
    SPADE: CLUB,
    HEART: DIAMOND,
    DIAMOND: HEART,
    CLUB: SPADE,
    JOKER: JOKER,
}


def get_reverse(suit):
    return REVERSE[suit]
