from engine import events
from random import shuffle, choice


DEFAULT_PLAYER_NAMES = ['Roy', 'Lisa', 'Rachel']


class Controller(events.GameObserver):
    def __init__(self, game, view):
        self.game = game
        self.view = view
        super().__init__()

    def enable(self):

        cls = self.game.player_agent
        self.game.attach_player(cls(self.game, self.view, self))

        player_names = DEFAULT_PLAYER_NAMES[:]
        shuffle(player_names)

        cls = self.game.opponent_agent
        for name in player_names:
            self.game.attach_player(cls(self.game, name))

        self.view.mainloop()

