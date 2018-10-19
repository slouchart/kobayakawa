from agents import KobakayakawaUserAgent, KobayakawaHeuristicAgent
from engine.events import GameEventTypes as Events
from engine.events import GameObserver
from engine.kobayakawa import GameEngine

from random import choice


if __name__ == '__main__':

    print('Kobayakawa Game. version 0.12 copyright 2018 S. Louchart')
    num_players = 4

    observer = GameObserver()

    def cb(event_name, *args):
        print(event_name.format(*args))

    for event in Events.ALL_EVENTS:
        observer.observe(event, cb)

    game = GameEngine()

    game.attach_player(KobayakawaHeuristicAgent(game, 'Rachel'))
    game.attach_player(KobayakawaHeuristicAgent(game, 'Roy'))
    game.attach_player(KobayakawaHeuristicAgent(game, 'Lisa'))
    game.attach_player(KobakayakawaUserAgent(game))

    first = choice(game.players_by_name)

    game.start_game(first)
    game.terminate()
