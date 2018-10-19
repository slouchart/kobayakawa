from random import shuffle


class Deck:
    """
    I'm an abstraction of a Kobayakawa deck of fifteen cards from 1 to 15
    usages:
    init me
    deal -> returns a sequence of random cards
    deal_one -> returns one card at random
    draw are without replacement, each draw thus further depletes the deck
    use reset to make whole and shuffled the deck again
    """

    def __init__(self):
        self._deck = [card_number for card_number in range(1, 16)]
        shuffle(self._deck)

    def reset(self):
        self._deck = [card_number for card_number in range(1, 16)]
        shuffle(self._deck)

    def deal(self, num_cards):
        cards, self._deck = self._deck[:num_cards], self._deck[num_cards:]
        return cards

    def deal_one(self):
        return self.deal(1)[0]

    @property
    def all_cards(self):
        return [card for card in range(1, 16)]
