from .events import GameEvent
from .events import GameEventTypes as Events
"""
This module contains the code associated with all game actions
I decided to put this code in a separate module of the engine package
to have it handy outside of the kobayakawa.py module

Each function in this module is intended to be called from the engine
and each of them updates the game and player state
"""


def deal_player(player, game):
    player.has_card = game.deck.deal_one()
    player.done()


def draw_discard(player, game):
    card = game.deck.deal_one()
    kept, discarded = player.discard(card)
    player.discarded.append(discarded)
    player.has_card = kept
    GameEvent(Events.PLAYER_ACTION_DISCARD, player.name, discarded)


def draw_cover(player, game):
    card = game.deck.deal_one()
    game.discarded.append(game.kobayakawa)
    game.kobayakawa = card
    GameEvent(Events.PLAYER_ACTION_COVER, player.name)
    GameEvent(Events.KOBAYAKAWA, game.kobayakawa)
    player.done()


def fold(player, game):
    # sanity check
    assert player.name not in game.contenders

    player.has_bet = 0
    GameEvent(Events.PLAYER_ACTION_FOLD, player.name)
    player.done()


def bet(player, game):
    if game.transitions.turn_number < 7:
        minimum_bet = 1
    else:
        minimum_bet = 2

    if player.stack >= minimum_bet:
        actual_bet = minimum_bet
    elif minimum_bet == 2 and player.stack == 1:
        actual_bet = 1
    else:
        actual_bet = 0

    if actual_bet > 0:

        game.pot, player.stack, player.has_bet = game.pot + actual_bet, player.stack - actual_bet, actual_bet
        game.add_contender(player.name)

        GameEvent(Events.PLAYER_ACTION_BET, player.name, actual_bet)
        player.done()
    else:
        player.fold()
