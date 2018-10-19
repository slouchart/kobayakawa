from agents import KobayakawaRandom, KobayakawaGreedy, KobayakawaHeuristicAgent
from engine.events import GameEventTypes as Events
from engine.events import GameObserver
from engine.kobayakawa import GameEngine

from random import choice


def test_prepare(observer):

    def cb(event_name, *args):
        print(event_name.format(*args))

    for event in Events.ALL_EVENTS:
        observer.observe(event, cb)

    return GameEngine()


def test_base(engine):
    engine.attach_player(KobayakawaRandom(game, 'P1'))
    engine.attach_player(KobayakawaRandom(game, 'P2'))
    engine.attach_player(KobayakawaRandom(game, 'P3'))

    first = choice(engine.players_by_name)

    engine.start_game(first)
    engine.terminate()


def test_player_elimination(engine):

    engine.attach_player(KobayakawaRandom(engine, 'P1'))
    engine.attach_player(KobayakawaGreedy(engine, 'Mr Fish'))
    engine.attach_player(KobayakawaHeuristicAgent(engine, 'Mr Smart'))

    first = choice(engine.players_by_name)

    engine.start_game(first)
    engine.terminate()

if __name__ == '__main__':

    o = GameObserver()
    game = test_prepare(o)
    test_player_elimination(game)
