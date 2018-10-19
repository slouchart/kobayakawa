from .events import GameEvent
from .events import GameEventTypes as Events

from engine.actions import deal_player, draw_cover, draw_discard, bet, fold


GAME_PHASES = ['deal', 'card', 'bet']


class GamePhase:

    actions = None

    """
    I provide a default API for all game phases
    """
    def __init__(self, game):
        self.game = game

    def on_start(self):
        pass

    def on_end(self):
        pass

    @classmethod
    def legal(cls):
        return cls.actions


class PhaseDeal(GamePhase):
    actions = {deal_player}
    name = GAME_PHASES[0]

    def on_end(self):
        self.game.kobayakawa = self.game.deck.deal_one()
        GameEvent(Events.KOBAYAKAWA, self.game.kobayakawa)


class PhaseCard(GamePhase):
    actions = {draw_discard, draw_cover}
    name = GAME_PHASES[1]


class PhaseBet(GamePhase):
    actions = {fold, bet}
    name = GAME_PHASES[2]

    def on_start(self):
        self.game.place_forced_bet()


class GamePhaseOrder:
    def __init__(self, game):
        self.phases = [PhaseDeal(game), PhaseCard(game), PhaseBet(game)]

    def __getitem__(self, item):
        return self.phases[item]

    def __len__(self):
        return len(self.phases)

    def __iter__(self):
        return iter(self.phases)
