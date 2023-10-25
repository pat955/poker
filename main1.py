import random

def main():
    p1_hand = Hand()
    p2_hand = Hand()
    new_deck = Deck()
    new_deck.generate_deck()
    new_deck.shuffle()
    p1_hand.populate(new_deck)
    p2_hand.populate(new_deck)
    print(p1_hand.lst_cards,'\n', p2_hand.lst_cards)



class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        return f'{self.rank} of {self.suit}'


class Deck():
    def __init__(self):
        self.ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.suits = ['Diamonds', 'Spades', 'Clubs', 'Hearts']
        self.current_deck = []
    
    def generate_deck(self):
        for rank in self.ranks:
            for suit in self.suits:
                self.current_deck.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.current_deck)
    
    def pick_top_card(self):
        return self.current_deck.pop()

class Hand():
    def __init__(self):
        self.lst_cards = []

    def decide_type(self):
        if self.is_flush() and self.is_royal:
            return ('Royal Flush', 'n/a')
    
    def is_flush(self):
        prev_suit = None
        for card in self.lst_cards:
            if prev_suit == None:
                prev_suit = card.suit
            elif card.suit != prev_suit:
                return False
        return True

    def is_royal(self):
        royal_cards = [10, 11, 12, 13, 14]
        for card in self.lst_cards:
            if card.rank in royal_cards:
                royal_cards.remove(card.rank)
            else:
                return False
        return True 

    def has_pairs(self):
        pass
    
    def populate(self, deck, amount=5):
        for i in range(0, amount):
            self.lst_cards.append(deck.pick_top_card())


main()