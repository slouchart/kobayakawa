from engine.deck import Deck
from engine.events import GameEvent
from engine.events import GameEventTypes as Events
from engine.transitions import GameStateIterator

from itertools import chain


class GameEngine:
    """
    Administrates and monitors all aspect of a game of Kobayakawa
    Maintaining the progression indicator is delegated to GameTransitionIterator
    Dealing with players actions is delegated to functions in engine.actions
    """

    def __init__(self):

        # sub-objects
        self.players = dict()
        self.transitions = None
        self.deck = Deck()

        # shared game state
        self.pot = 0
        self.stack = 8
        self.kobayakawa = None
        self.discarded = []

        # transient state variables (used during betting round)
        self._contenders = []
        self._turn_winner = None

    """
        External API
    """

    def attach_player(self, player):
        self.players[player.name] = player
        GameEvent(Events.PLAYER_JOINED, player.name)

    def start_game(self, starting_player_name):

        assert len(self.players) > 0
        assert starting_player_name in self.players_by_name

        self.transitions = GameStateIterator(self, starting_player_name)
        self.transitions.start_of_phase = self._resolve_start_of_phase
        self.transitions.end_of_phase = self._resolve_end_of_phase
        self.transitions.end_of_turn = self._resolve_end_of_turn
        self.transitions.end_of_game = self._resolve_end_of_game

        self.pot = 0

        for transition in self.transitions:
            player_name = transition.active_player
            player = self.players[player_name]
            move = player.do(self.transitions.current_phase)
            move(player, self)

    def terminate(self):
        # detach all players from positions
        players = list(self.players.keys())
        for player in players:
            self.players[player] = None

    @property
    def players_by_name(self):
        return list(self.players.keys())

    def place_forced_bet(self):
        minimum_bet = 1
        if self.transitions.turn_number == 7:
            minimum_bet = 2
        self.pot, self.stack = self.pot + minimum_bet, self.stack - minimum_bet

    @property
    def contenders(self):
        return self._contenders[:]  # return a COPY of that list

    def add_contender(self, player_name):
        assert player_name in self.players_by_name
        assert player_name not in self._contenders
        self._contenders.append(player_name)

    """
        API for player agents
    """

    def sees(self, player_name):

        # can see all discarded cards
        # can see kobayakawa and previously covered kobayakawa
        # can see stack from players other than itself
        # can see current bets
        # can see past actions of all players in the current turn (redundant?)

        assert player_name in self.players_by_name
        players = self.players.values()
        discarded = set(self.discarded)
        for p in players:
            discarded = set(chain(discarded, p.discarded))
        players_stack = {p.name: p.stack for p in players}
        players_bet = {p.name: p.has_bet for p in players}

        from collections import namedtuple
        GameData = namedtuple('GameData', 'players discarded kobayakawa stacks bets')

        return GameData(self.players_by_name, discarded, self.kobayakawa, players_stack, players_bet)

    """
    State machine internal transition methods
    """
    def _resolve_start_of_phase(self):
        self.transitions.current_phase.on_start()

    def _resolve_end_of_phase(self):
        GameEvent(Events.END_OF_PHASE, self.transitions.turn_number, self.transitions.current_phase.name)
        self.transitions.current_phase.on_end()

    def _reset(self):
        """
        self called in between turns
        Note that self.stack is not reset
        """
        self.pot = 0
        self.kobayakawa = None
        self.discarded = []

        # get all cards into random.deck and shuffles
        for player in self.players.values():
            player.reset()

        self.deck.reset()

    def _ascertain_winner(self):
        """
        I tell who the winner is at the end of turn
        """

        if len(self._contenders) == 0:
            # this means that nobody has bet, can only happen by chance when all players positions
            # are random agents. the winner should be the last player to have played
            winner = self.transitions.active_player
        elif len(self._contenders) == 1:
            # automatic winner, no showdown
            winner = self._contenders[0]
        else:
            """
            SHOWDOWN!!!!!
            """
            for player_name in self._contenders:
                card = self.players[player_name].has_card
                GameEvent(Events.PLAYER_SHOWDOWN, player_name, card)

            player_cards = {self.players[name].has_card: name for name in self._contenders}
            min_card = min(player_cards.keys())
            max_card = max(player_cards.keys())

            if min_card + self.kobayakawa > max_card:
                winner = player_cards[min_card]
                GameEvent(Events.WINNING_FIGURE_MIN, min_card, self.kobayakawa, max_card)

            elif max_card > min_card + self.kobayakawa:
                winner = player_cards[max_card]
                GameEvent(Events.WINNING_FIGURE_MAX, max_card, min_card, self.kobayakawa)

            else:  # it's a draw
                GameEvent(Events.DRAW, max_card, min_card, self.kobayakawa)
                player_a = player_cards[min_card]
                player_b = player_cards[max_card]

                winner = self.transitions.closest_from_first_player(player_a, player_b)

        self._contenders = []

        return winner

    def _check_eliminated_players(self):
        """
        part of end of turn resolution
        I check whether players have a zero stack at the end of the turn
        so they can be eliminated from the game
        :return: the list of remaining players in the game (by name
        """
        eliminated = []
        kept_players = []
        for (player_name, player) in self.players.items():
            if player.stack == 0:
                eliminated.append(player_name)
            else:
                kept_players.append(player_name)

        if len(eliminated):
            for player_name in eliminated:
                GameEvent(Events.PLAYER_OFF, player_name)
                del self.players[player_name]

        return self.players_by_name

    def _resolve_end_of_turn(self):
        # who has won?
        self._turn_winner = self._ascertain_winner()

        # update game state and give the winner its reward
        gain = self.pot
        self.pot = 0
        self.players[self._turn_winner].stack += gain

        GameEvent(Events.TURN_WINNER, self._turn_winner, gain)

        # clean up broke players
        kept_players = self._check_eliminated_players()
        self.transitions.update_players_list(self._turn_winner, kept_players)

        # reset state for a new turn
        self._reset()

    def _resolve_end_of_game(self):
        players_stacks = [(player.stack, player.name) for player in self.players.values()]
        players_stacks = sorted(players_stacks, key=lambda t: t[0], reverse=True)
        gain, winner = players_stacks[0]
        winners = [winner]
        for (stack, player) in players_stacks[1:]:
            if stack == gain:
                winners.append(player)
        if len(winners) > 1:
            s = ', '.join(winners[:-1]) + ' and ' + winners[-1]
            GameEvent(Events.GAME_END_MULTIPLE_WINNERS, s, gain)
        else:
            GameEvent(Events.GAME_END_SINGLE_WINNER, winner, gain)
