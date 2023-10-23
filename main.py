import random

def main():
    p1_hand = []
    p2_hand = []
    new_deck = Deck()
    new_deck.generate_deck()
    new_deck.shuffle()
    for i in range(0,5):
        p1_hand.append(new_deck.pick_top_card())
        p2_hand.append(new_deck.pick_top_card())
    
    print(f'Player 1 deck:{p1_hand}\n Player 2 deck: {p2_hand}')
    
    
def decide_winner(hand1, hand2):
    hand1.sort()
    hand2.sort()
    


class Deck():
    def __init__(self):
        self.suits = ['Diamond', 'Spades', 'Hearts', 'Aces']
        self.ranks = []
        current_deck = []
    
    def check_deck(self):
        return current_deck
    
    def shuffle(self):
        if len(current_deck) == 0:
            return None
            
        random.shuffle(current_deck)
            
    def generate_deck(self):
        for rank in self.ranks:
            for suit in self.suits:
                current_deck.append(Card(rank, suit))
        
    def pick_top_card(self):
        return current_deck.pop()

    
class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        ###############3self.rank_value = index(Deck.ranks[
        self.suit = suit
    
    def check_card(self):
        return f'{self.rank} of {self.suit}'
 
 

 
 
class Hand():
    def __init__(self, lst_cards):
        self.lst_cards = lst_cards
        self.type = None
    
    def decide_type:
        
        highest_card = -'inf'
        for card in self.lst_cards:
            if card.rank > highest_card:
                card.rank = highest_card
            

    
class Player():
    def __init__(self, name, wins, losses):
main()





hand_types = {
    'High Card',
    'One Pair',
    'Two Pairs': [],
    'Straight Flush': [n, n+1, n+2, n+3, n+4],
    'Royal Flush': ['Ten', 'Jack', 'Queen', 'King', 'Ace']}



poker.py
Viser poker.py.