from agents import KobakayakawaUserAgent, KobayakawaHeuristicAgent
from engine.events import GameEventTypes as Events
from engine.events import GameObserver
from engine.kobayakawa import GameEngine
from engine import __version__ as version, __author__ as author

from random import choice, shuffle
from agents.console import cls


"""
    Game constants
"""
NUM_PLAYERS = 4
DEFAULT_PLAYERS = ['Rachel', 'Lisa', 'Roy']

if __name__ == '__main__':

    cls()
    print('Kobayakawa Game version {} by {}'.format(version, author))
    num_players = NUM_PLAYERS

    feedback = GameObserver()
    elimination = GameObserver()

    def cb(event_name, *args):
        print(event_name.format(*args))

    for event in set(Events.ALL_EVENTS) - {Events.END_OF_PHASE}:
        feedback.observe(event, cb)

    game = GameEngine()
    player_names = DEFAULT_PLAYERS[:]
    shuffle(player_names)

    for name in player_names:
        game.attach_player(KobayakawaHeuristicAgent(game, name))

    user_agent = KobakayakawaUserAgent(game)
    game.attach_player(user_agent)

    def check_elimination(_, player_name):
        if player_name == user_agent.name:
            raise KeyboardInterrupt

    elimination.observe(Events.PLAYER_OFF, check_elimination)

    first_player = choice(game.players_by_name)

    cls()
    try:
        game.start_game(first_player)
    except KeyboardInterrupt:
        pass
    finally:
        game.terminate()
