class GameObserver:
    """
    I am an event sink. Do not subclass me in a multiple inheritance fashion, I'm not a mixin
    Instantiate me if you need an event sink

    NOTE: this code is ugly, weakrefs should be used here
    """
    observers = []

    def __init__(self):
        self.observers.append(self)
        self.observables = {}

    def observe(self, event_name, callback):
        self.observables[event_name] = callback


class GameEvent:
    """
    Instantiate me when you need to fire an event
    """
    def __init__(self, name, *data, auto_fire=True):
        self.name = name
        self.data = data
        if auto_fire:
            self.fire()

    def fire(self):
        for observer in GameObserver.observers:
            if self.name in observer.observables:
                observer.observables[self.name](self.name, *self.data)


class GameEventTypes:
    """
    The repository of relevant Kobayakawa game events
    The name of an event is also the format string used to represent it as a string
    call me lazy
    """
    PLAYER_JOINED = 'Player {} has joined the game'
    PLAYER_ACTION_DISCARD = 'Player {} has discarded {}'
    PLAYER_ACTION_COVER = 'Player {} has drawn and covered'
    PLAYER_ACTION_FOLD = 'Player {} has passed'
    PLAYER_ACTION_BET = 'Player {} has bet {}'
    END_OF_PHASE = 'Turn {}, end of phase {}'
    KOBAYAKAWA = 'Kobayakawa is now {}'
    PLAYER_SHOWDOWN = 'Player {} shows card {}'
    TURN_WINNER = 'Turn winner is player {} with a gain of {}'
    PLAYER_OFF = 'Player {} is off the game'
    GAME_END_SINGLE_WINNER = 'Game finished, winner is player {} with a stack of {}'
    GAME_END_MULTIPLE_WINNERS = 'Game finished, winners are players {} with a stack of {}'
    WINNING_FIGURE_MIN = 'Winning combination is {}+{} versus {}'
    WINNING_FIGURE_MAX = 'Winning combination is {} versus {}+{}'
    DRAW = 'Combinations are at draw {} versus {}+{}'

    ALL_EVENTS = [
                    PLAYER_JOINED,
                    PLAYER_ACTION_DISCARD,
                    PLAYER_ACTION_COVER,
                    PLAYER_ACTION_FOLD,
                    PLAYER_ACTION_BET,
                    END_OF_PHASE,
                    KOBAYAKAWA,
                    PLAYER_SHOWDOWN,
                    TURN_WINNER,
                    PLAYER_OFF,
                    GAME_END_SINGLE_WINNER,
                    GAME_END_MULTIPLE_WINNERS,
                    WINNING_FIGURE_MIN,
                    WINNING_FIGURE_MAX,
                    DRAW
    ]
