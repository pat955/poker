import random

def main():
    p1_hand = Hand([Card(10, 'Diamond'), Card(11, 'Diamond'), Card(12, 'Diamond'), Card(13, 'Diamond'), Card(14, 'Diamond')])
    p2_hand = Hand([])
    new_deck = Deck()
    new_deck.generate_deck()
    new_deck.shuffle()

    #for i in range(0,5):
     #   p1_hand.lst_cards.append(new_deck.pick_top_card())
      #  p2_hand.lst_cards.append(new_deck.pick_top_card())
    
    print(f'Player 1 deck:{p1_hand.lst_cards}\n Player 2 deck: {p2_hand.lst_cards}\n')
    #print(f'Does player1s deck have a pair:{p1_hand.find_pairs()}\np2? {p2_hand.find_pairs()}')
    #print(f'\np1s highest card: {p1_hand.find_highest_card()}\np2 highest card: {p2_hand.find_highest_card()}')
    #print(f'Does player1 have a flush? {p1_hand.find_flush()}')
    print(p1_hand.is_royal(), p1_hand.is_flush())
   


class Deck():
    def __init__(self):
        self.suits = ['Diamond', 'Spades', 'Hearts', 'Aces']
        self.ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.current_deck = []
    

    def check_deck(self):
        return self.current_deck
    

    def shuffle(self):
        if len(self.current_deck) == 0:
            return None
            
        random.shuffle(self.current_deck)


    def generate_deck(self):
        for rank in self.ranks:
            for suit in self.suits:
                self.current_deck.append(Card(rank, suit))
        
# pop() fjerner det også fra listen
    def pick_top_card(self):
        return self.current_deck.pop()

    
class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def check_card(self):
        return f'{self.rank} of {self.suit}'


    def __repr__(self):
        return f'{self.rank} of {self.suit}'


    #def __str__(self):
        #return f'{self.rank} of {self.suit}'

 
class Hand():
    def __init__(self, lst_cards): 
        self.lst_cards = lst_cards
        self.type = None #(type, highestcard/type of pair) + secondary type?
        self.possible_ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        
        hand_types = ['High Card', 'One Pair', 'Two Pairs', 'Three of a Kind', 'Straight',
                    'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']
    
    
    def decide_type(self):
        if is_royal() and is_flush():
            self.type = ('Royal Flush', 'n/a')

        elif is_flush() and is_straight():
            self.type = ('Straight Flush', 'n/a')

        elif find_pairs()[0] == 'Four of a Kind':
            self.type == (find_pairs()[0], find_pairs[1])

        
        if find_pairs() == False:
            self.type == (hand_types[0], find_highest_card)
        elif find_pairs():
            self.type = find_pairs()

        

    def find_highest_card(self):
        highest_card = -1
        for card in self.lst_cards:
            if self.possible_ranks.index(card.rank) > highest_card:
                highest_card = self.possible_ranks.index(card.rank)
        return self.possible_ranks[highest_card]
        

    def find_pairs(self):
        rank_count = self.make_sorted_value_dict(True)

        if len(rank_count) == 5:
            return False

        elif len(rank_count) == 4:
            return ('One Pair', rank_count[0][1])

        elif len(rank_count) == 3:
            if rank_count[0][0] == 2 and rank_count[1][0] == 2:
                return ('Two Pairs', rank_count[0][1], rank_count[1][1])

            return ('Three of a Kind', rank_count[0][1])

        elif len(rank_count) == 2:
            if rank_count[0][0] == 3 and rank_count[1][0] == 2:
                return('Full House', rank_count[0][1], rank_count[1][1])
            return ('Four of a Kind', rank_count[0][1])

        else: 
            return 'Something else'

    def is_flush(self):
        suit_count = self.make_sorted_value_dict(False)
        
        
        if len(suit_count) == 1:
            return True
        return False


    def is_royal(self):
        royal_cards = [10,11,12,13,14]
        for card in self.lst_cards:
            if card.rank in royal_cards:
                royal_cards.remove(card.rank)
            else:
                return False
        return True
            

    def make_sorted_value_dict(self, rank_or_suit=True):
        if rank_or_suit == True:
            rank_count = {}

            for card in self.lst_cards:
                if card.rank not in rank_count:
                    rank_count[card.rank] = 1
                else:
                    rank_count[card.rank] += 1


            return dict(sorted(rank_count.items(), key=lambda item: item[1], reverse=True))

        suit_count = {}
        
        for card in self.lst_cards:
            if card.suit not in suit_count:
                suit_count[card.suit] = 1
            else:
                suit_count[card.suit] += 1 

        return dict(sorted(suit_count.items(), key=lambda item: item[1], reverse=True))

class Player():
    def __init__(self, name, hand):
        self.hand = hand
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0 
    
    def win(self, loser):
        self.wins += 1
        loser.losses += 1

    def play_poker(self, other_player):
        p1_type = decide_type(self.hand)
        p2_type = decide_type(other_player.hand)
        
        if hand_types.index(p1_type) > hand_types.index(p2_type):
            self.win(other_player)
        elif hand_types.index(p1_type) < hand_types.index(p2_type):
            other_player.win(self)
        elif hand_types.index(p1_type) == hand_types.index(p2_type):
            pass



"""
High Card: Highest value card.
One Pair: Two cards of the same value.
Two Pairs: Two different pairs.
Three of a Kind: Three cards of the same value.
Straight: All cards are consecutive values.
Flush: All cards of the same suit.
Full House: Three of a kind and a pair.
Four of a Kind: Four cards of the same value.
Straight Flush: All cards are consecutive values of same suit.
Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

"""
main()