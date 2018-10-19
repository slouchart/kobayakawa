from engine import events
from engine.events import GameEventTypes as Events
from engine.kobayakawa import GameEngine

from random import choice

import trials.trials as trials


def compute_statistics(data):
    avg_wins = {p: 0 for p in data[0].keys()}
    avg_gain = {p: 0 for p in data[0].keys()}

    n = {p: 1 for p in data[0].keys()}
    for line in data:
        for player in line.keys():
            # average number of wins / player
            avg_wins[player] = ((n[player] - 1) * avg_wins[player] + line[player][0]) / n[player]

            # average gain / player (we don't have data on losses nor on player elimination)
            avg_gain[player] = ((n[player] - 1) * avg_gain[player] + line[player][1]) / n[player]

            n[player] += 1

    print(avg_wins)
    print(avg_gain)


def prepare_trial(trial):
    d = {p: [0, 0] for p in trial['players'].keys()}
    return d


def run_trial(trial):
    num_games = trial['num_games']
    for game_number in range(0, num_games):

        game = GameEngine()

        for (name, cls) in trial['players'].items():
            game.attach_player(cls(game, name))

        first_player = choice(game.players_by_name)
        game.start_game(first_player)


if __name__ == '__main__':

    current_trial = trials.trials_5


    def on_game_end(event, winner, gain):
        def unused(e):
            return e

        unused(event)
        stats[winner][0] += 1
        stats[winner][1] += gain


    events.GameObserver().observe(Events.GAME_END_SINGLE_WINNER, on_game_end)

    trial_data = []

    for run in range(0, current_trial['num_simul']):
        stats = prepare_trial(current_trial)
        run_trial(current_trial)
        trial_data.append(stats)

    compute_statistics(trial_data)
