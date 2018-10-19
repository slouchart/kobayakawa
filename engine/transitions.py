from collections import namedtuple
from .iterators import GameIterator, GamePlayOrderIterator
from .phases import GamePhaseOrder


class GameStateIterator:
    """
    I am an iterator though the game turn, phases/turn, player/phase
    I implement the python sync iterator protocol
    I return a Transition instance (a named tuple) on each hit on __next__
    """
    transition_class_factory = namedtuple('Transition', 'turn_number current_phase active_player')

    def __init__(self, game, starting_player_name):

        self._players_iter = GamePlayOrderIterator(game.players_by_name, starting=starting_player_name)
        self._phases_iter = GameIterator(GamePhaseOrder(game))
        self._turns_iter = GameIterator(list(range(1, 8)))

        self._current_turn = None
        self._current_phase = None
        self._current_player = None

        self._initialized = False
        self._exhausted = False

    @property
    def start_of_phase(self):
        return self._players_iter.on_reset

    @start_of_phase.setter
    def start_of_phase(self, cb):
        self._players_iter.on_reset = cb

    @property
    def end_of_phase(self):
        return self._players_iter.on_stop

    @end_of_phase.setter
    def end_of_phase(self, cb):
        self._players_iter.on_stop = cb

    @property
    def start_of_turn(self):
        return self._phases_iter.on_reset

    @start_of_turn.setter
    def start_of_turn(self, cb):
        self._phases_iter.on_reset = cb

    @property
    def end_of_turn(self):
        return self._phases_iter.on_stop

    @end_of_turn.setter
    def end_of_turn(self, cb):
        self._phases_iter.on_stop = cb

    @property
    def start_of_game(self):
        return self._turns_iter.on_reset

    @start_of_game.setter
    def start_of_game(self, cb):
        self._turns_iter.on_reset = cb

    @property
    def end_of_game(self):
        return self._turns_iter.on_stop

    @end_of_game.setter
    def end_of_game(self, cb):
        self._turns_iter.on_stop = cb

    def __iter__(self):
        return self

    def __next__(self):
        if self._exhausted:
            raise StopIteration

        if not self._initialized:
            self._current_turn = self._turns_iter.__next__()
            self._current_phase = self._phases_iter.__next__()
            self._current_player = self._players_iter.__next__()

            self._initialized = True

            return self.transition_class_factory(self._current_turn, self._current_phase, self._current_player)

        try:
            self._current_player = self._players_iter.__next__()
            return self.transition_class_factory(self._current_turn, self._current_phase, self._current_player)

        except StopIteration:
            pass

        # NOTE: _players_iter may also be reset externally by a call to update_players_list
        self._players_iter.reset()
        self._current_player = self._players_iter.__next__()

        try:
            self._current_phase = self._phases_iter.__next__()
            return self.transition_class_factory(self._current_turn, self._current_phase, self._current_player)

        except StopIteration:
            pass

        self._phases_iter.reset()

        self._current_player = self._players_iter.__next__()
        self._current_phase = self._phases_iter.__next__()

        try:
            self._current_turn = self._turns_iter.__next__()
            return self.transition_class_factory(self._current_turn, self._current_phase, self._current_player)
        except StopIteration:
            self._exhausted = True
            raise

    def update_players_list(self, starting_player, players_by_name):
        """

        I reset the play order iterator providing a new list (optional)
        in case some players have been eliminated
        or by setting a new starting player

        :param starting_player: the name of the starting player
        :param players_by_name: an iterable on players names
        :return: nothing
        """

        # sanity check
        if players_by_name is not None and len(players_by_name) > 0:
            if starting_player is not None:
                assert starting_player in players_by_name

        self._players_iter.reset(starting_player, players_by_name)

    @property
    def active_player(self):
        return self._current_player

    @property
    def turn_number(self):
        return self._current_turn

    @property
    def current_phase(self):
        return self._current_phase

    def closest_from_first_player(self, player1, player2):
        return self._players_iter.compare(player1, player2)
