from cards import Deck

class Card_Game():
    def __init__(self, name, players, deck=Deck()):
        self.name = name        # str "Poker"
        self.players = players  # list [p1, p2, ...]
        self.deck = deck        # class Deck Deck()

    def create_shuffled_deck(self):
        self.deck = Deck()
        self.deck.generate_deck()
        self.deck.shuffle()

    def quit(self):
        for p in self.players:
            print(p.report())
        print('Quitting...')
        exit()

