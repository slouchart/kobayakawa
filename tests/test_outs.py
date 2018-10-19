from agents.outs import beaten_cards, hidden_cards


if __name__ == '__main__':

    card = 3
    kobayakawa = 1
    discarded = [8, 10, 2, 14]


    hd = hidden_cards(card, kobayakawa, discarded)
    bt = beaten_cards(card, kobayakawa, discarded)

    outs = len(bt)/len(hd)

    print(outs)
