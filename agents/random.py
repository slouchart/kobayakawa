from .player import KobayakawaPlayer

from random import choice

import engine.actions as actions


class KobayakawaRandom(KobayakawaPlayer):
    """
    Dummy player agent, plays by selecting a legal move at random
    """

    def do(self, phase):
        move = choice(list(phase.legal()))
        return move

    def discard(self, card):
        # chooses at random between card dealt and card in hand
        cards = [self.has_card, card]
        card_kept = choice([0, 1])
        return cards.pop(card_kept), cards[0]


class KobayakawaGreedy(KobayakawaRandom):
    """
    Aggressive player: it selects its move at random during the card phase
    but always bet in the bet phase
    """
    def do(self, phase):
        if actions.bet in phase.legal():
            return actions.bet
        else:
            return super().do(phase)
