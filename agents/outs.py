"""
    This module contains two functions used by agents.agent.KobayakawaHeuristicAgent
    to estimate its odds of win
    Both methods work the same way: given a list of known cards (card in hand, kobayakawa
    and all discarded cards), hidden_cards returns a set of possible hidden cards
    and from this set, beaten_cards returns the set of all cards beaten by the hand
    composed of card or (card, kobayakawa)
"""


def hidden_cards(card, kobayakawa, discarded):

    cards = {card for card in range(1, 16)}
    cards -= {card, kobayakawa} | set(discarded)
    return cards


def beaten_cards(card, kobayakawa, discarded):

    cards = set()
    for c in hidden_cards(card, kobayakawa, discarded):
        if card > c and card > c + kobayakawa:
            cards.add(c)
        elif card < c < card + kobayakawa:
            cards.add(c)
    return cards

