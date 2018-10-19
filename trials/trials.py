import agents

NUM_SIMUL = 50
GAMES_PER_SIMUL = 100

trials_1 = {'num_simul': NUM_SIMUL,
            'num_games': GAMES_PER_SIMUL,
            'players': {'P0': agents.KobayakawaRandom,
                        'P1': agents.KobayakawaRandom,
                        'P2': agents.KobayakawaRandom,
                        'P3': agents.KobayakawaRandom}}

trials_2 = {'num_simul': NUM_SIMUL,
            'num_games': GAMES_PER_SIMUL,
            'players': {'P0': agents.KobayakawaRandom,
                        'P1': agents.KobayakawaRandom,
                        'P2': agents.KobayakawaRandom,
                        'greedy': agents.KobayakawaGreedy}}

trials_3 = {'num_simul': NUM_SIMUL,
            'num_games': GAMES_PER_SIMUL,
            'players': {'P0': agents.KobayakawaRandom,
                        'P1': agents.KobayakawaRandom,
                        'P2': agents.KobayakawaRandom,
                        'smart': agents.KobayakawaHeuristicAgent}}

trials_4 = {'num_simul': NUM_SIMUL,
            'num_games': GAMES_PER_SIMUL,
            'players': {'random': agents.KobayakawaRandom,
                        'greedy': agents.KobayakawaGreedy,
                        'smart': agents.KobayakawaHeuristicAgent}}

trials_5 = {'num_simul': NUM_SIMUL,
            'num_games': GAMES_PER_SIMUL,
            'players': {'greedy_1': agents.KobayakawaGreedy,
                        'greedy_2': agents.KobayakawaGreedy,
                        'smart': agents.KobayakawaHeuristicAgent}}
