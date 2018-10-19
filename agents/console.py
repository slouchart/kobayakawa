from .player import KobayakawaPlayer

import engine.actions as actions

import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class KobakayakawaUserAgent(KobayakawaPlayer):
    """
    Interface for a human player, solo game in an OS console
    """
    def __init__(self, game):

        name = input('Enter your name: ')

        super().__init__(game, name)

    def do(self, phase):

        if actions.deal_player in phase.actions:
            return actions.deal_player

        actions_list = list(phase.actions)
        kobayakawa = self.game.sees(self.name).kobayakawa
        prompt = 'Your card is a {}. Your stack is {}. The kobayakawa is {}. Enter your choice:'
        for move in actions_list:
            prompt += ' {}) {}'.format(actions_list.index(move) + 1, move.__name__)

        print(prompt.format(self.has_card, self.stack, kobayakawa))

        while True:
            try:
                move_inx = int(input()) - 1
                return actions_list[move_inx]
            except ValueError:
                print("Please enter the number of the move you chose")
            except IndexError:
                print('Select only a valid move')

    def discard(self, card):
        print("You've been dealt a {}, you have {}, choose which card to discard".format(card, self.has_card))

        while True:
            try:
                choice = int(input())
                if choice not in {card, self.has_card}:
                    raise ValueError
                break
            except ValueError:
                print("Enter the card number you want to discard")

        kept, discarded = {card, self.has_card} - {choice}, {choice}
        return kept.pop(), discarded.pop()

    def reset(self):
        print("Turn complete, your stack is now {}".format(self.stack))
        input("Press any key to continue")
        cls()
        super().reset()
