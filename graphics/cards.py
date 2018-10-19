from PIL import Image, ImageTk
from engine.deck import Deck


class Cards:
    def __init__(self):
        self.card_images = []
        deck = Deck().all_cards
        for card in deck:
            photo = Image.open('graphics/images/c{}.jpg'.format(card))
            self.card_images.append(ImageTk.PhotoImage(photo))

        photo = Image.open('graphics/images/cardback.jpg')
        self.card_back = ImageTk.PhotoImage(photo)

    def __getitem__(self, item):
        if item == 0:
            return self.card_back
        else:
            return self.card_images[item-1]
