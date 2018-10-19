from .player import KobayakawaPlayer
from .outs import beaten_cards, hidden_cards

import engine.actions as actions


class CardComparator:
    """
    A helper class used only in this module
    contains the semantics on low/high cards
    a medium card is therefore neither low nor high
    """
    def __init__(self, card):
        self._card = card

    @property
    def is_low(self):
        return self._card < 5

    @property
    def is_high(self):
        return self._card > 11

    @property
    def is_medium(self):
        return not self.is_low and not self.is_high


class KobayakawaHeuristicAgent(KobayakawaPlayer):
    """
    autonomous agent player using heuristic derived from human play
    and statistics on random and greedy play strategies
    """
    keep_lowest = 'keep_lowest'
    keep_highest = 'keep_highest'
    deferred = 'deferred'

    def do(self, phase):
        """
        Inherited method from base class
        Called by the game engine
        :param phase: the current phase of the game
        :return: a move as one of the methods in engine.actions
        """
        what_i_can_see = self.game.sees(self.name)

        # decide move
        if {actions.draw_discard, actions.draw_cover} <= phase.actions:
            move = self._decide_move_card(what_i_can_see)
        elif actions.bet in phase.actions:
            move = self._decide_bet(what_i_can_see)
        elif actions.deal_player in phase.actions:
            move = actions.deal_player
        else:
            assert actions.fold in phase.actions
            move = actions.fold

        return move

    def discard(self, card):
        """
        Inherited method from base class
        Called by the game engine after move selection was draw_discard
        :param card: the card being dealt
        :return: a tuple of cards, the card being kept first and the card being discarded second
        """
        decision = self.future_decision
        assert decision is not None

        kept, discarded = None, None
        if decision == self.deferred:
            if CardComparator(card).is_low and CardComparator(self.has_card).is_low:
                if card > self.has_card:
                    kept, discarded = card, self.has_card
                else:
                    kept, discarded = self.has_card, card
            else:
                if card < self.has_card:
                    kept, discarded = card, self.has_card
                else:
                    kept, discarded = self.has_card, card
        elif decision == self.keep_lowest:
            if card < self.has_card:
                kept, discarded = card, self.has_card
            else:
                kept, discarded = self.has_card, card

        elif decision == self.keep_highest:
            if card > self.has_card:
                kept, discarded = card, self.has_card
            else:
                kept, discarded = self.has_card, card

        return kept, discarded

    """
    Internal heuristics
    """
    def _decide_bet(self, game_data):
        """
        TODO: simple heuristic: last_player? no other bets? bet and win!!!

        otherwise, compute outs from hand, kobayakawa, discarded previous koba's and discarded
        cards from other players hands

        bet if outs are > 0.5 and stack <= 6 and stack >= 3
        bet if outs are <= 0.5 and stack > 6
        bet if outs are >= 0.75 whatever the stack is
        otherwise fold

        :param game_data: game state information given by game engine
        :return: the decided move
        """
        last_to_bet = True
        for (player, bet) in game_data.bets.items():
            if player != self.name and bet > 0:
                last_to_bet = False
                break

        if last_to_bet:
            return actions.bet

        card = self.has_card
        kobayakawa = game_data.kobayakawa
        discarded = game_data.discarded

        outs = self._compute_outs(card, kobayakawa, discarded)
        if outs > 0.5:
            move = actions.bet
        elif self.stack > 6 and outs > 0.2:
            move = actions.bet
        else:
            move = actions.fold

        return move

    @staticmethod
    def _compute_outs(card, kobayakawa, discarded):
        hd = hidden_cards(card, kobayakawa, discarded)
        bt = beaten_cards(card, kobayakawa, discarded)

        return float(len(bt)/len(hd))

    def _decide_move_card(self, game_data):
        """
        # must decide between both

        # if card in hand is medium (>5 and <11)
        #       if kobayakawa is low (<=5)
        #           draw_discard, but keep highest card
        #       if kobayakawa is high (>=11)
        #           draw_discard as well but keep always the lowest card in hand

        # if card in hand is low (<=5)
        # if kobayakawa is low as well then draw_cover
        # if kobayakawa is high (>=11), draw_discard
        #    deferred : keep lowest if not low and low
        #               or keep highest if both low

        # if card in hand is high (>=11)
        # if kobayakawa is not low, draw_cover
        # if kobayakawa is low, discard_draw, always keeping highest

        :param game_data: game state information given by game engine
        :return: the decided move
        """

        kobayakawa = game_data.kobayakawa
        card_in_hand = self.has_card

        move = None

        if CardComparator(card_in_hand).is_medium:
            if CardComparator(kobayakawa).is_low:
                move = actions.draw_discard
                self.future_decision = self.keep_highest

            if CardComparator(kobayakawa).is_high:
                move = actions.draw_discard
                self.future_decision = self.keep_lowest

            if CardComparator(kobayakawa).is_medium:
                if card_in_hand < kobayakawa:
                    move = actions.draw_discard
                    self.future_decision = self.keep_lowest
                else:
                    move = actions.draw_cover

        if CardComparator(card_in_hand).is_low:
            if CardComparator(kobayakawa).is_low:
                move = actions.draw_cover
            if CardComparator(kobayakawa).is_high:
                move = actions.draw_discard
                self.future_decision = self.deferred
            if CardComparator(kobayakawa).is_medium:
                move = actions.draw_cover  # expecting to get a higher kobayakawa

        if CardComparator(card_in_hand).is_high:
            if CardComparator(kobayakawa).is_high or CardComparator(kobayakawa).is_medium:
                move = actions.draw_cover  # expecting to get a lower kobayakawa
            else:
                move = actions.draw_discard
                self.future_decision = self.keep_highest

        return move
