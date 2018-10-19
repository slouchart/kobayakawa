class KobayakawaPlayer:
    """
    defines:
     - all player specific gale state
     - agent API viewed from game engine
    """

    def __init__(self, game, name):
        self.game = game
        self.name = name

        self.has_card = None
        self.has_bet = -1
        self.discarded = []
        self.initial_stack = 4
        self.stack = self.initial_stack

    def reset(self):
        self.has_card = None
        self.has_bet = -1
        self.discarded = []

    def do(self, phase):
        raise NotImplemented

    def discard(self, card):
        raise NotImplemented

    def done(self):
        pass

    def __str__(self):
        data = self.name, self.has_card, self.stack, self.discarded
        return 'PLAYER: {}, card {}, stack {}, discarded {}\n'.format(*data)
