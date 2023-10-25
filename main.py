import random

def main():
    jack = Player('Jack', Hand())
    jane = Player('Jane', Hand())
    

    for i in range(0, 50):

        new_deck = Deck()
        new_deck.generate_deck()
        new_deck.shuffle()
        jack.play_poker(jane, new_deck)
        print(jack.hand.decide_type(), jane.hand.decide_type())
        #print(jack.hand.decide_type(), jane.hand.decide_type())
        #if jack.hand.decide_type()[0] == 'Straight' or  jane.hand.decide_type()[0] == 'Straight':
         #   print('FOUND!\n', jack.hand.decide_type(), jane.hand.decide_type(), jack.hand.lst_cards, jane.hand.lst_cards)
    print(jane.report())
    print(jack.report())

     
   
class Deck():
    def __init__(self):
        self.suits = ['Diamonds', 'Spades', 'Hearts', 'Clubs']
        self.ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.current_deck = []
    
    def check_deck(self):
        return self.current_deck
    
    def shuffle(self):
        if len(self.current_deck) == 0:
            raise Exception('Can\'t shuffle empty deck.') 
        random.shuffle(self.current_deck)

    def generate_deck(self):
        for rank in self.ranks:
            for suit in self.suits:
                self.current_deck.append(Card(rank, suit))
        
    def deal_card(self):
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
    def __init__(self): 
        #Card(1, 'Spades'), Card(1, 'Diamonds'), Card(2, 'Hearts'), Card(5, 'Diamonds'), Card(6, 'Hearts')
        self.lst_cards = []
        #self.type = None #(type, type of pair/'n/a')
        # self.possible_ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    
    def decide_type(self):
        if self.is_royal() and self.is_flush():
            return ('Royal Flush', 'n/a')
        elif self.is_flush() and self.is_straight():
            return ('Straight Flush', 'n/a')
        elif self.has_pairs():
            results = self.find_pairs()
            if results[0] == 'Four of a Kind' or results[0] == 'Full House':
                return results
        elif self.is_flush():
            return ('Flush', 'n/a')
        elif self.is_straight():
            return ('Straight', 'n/a')
        elif self.has_pairs():
            results = self.find_pairs()
            return results
        return ('High Card', self.find_high_card(), self.has_pairs())

    def is_flush(self):
        suit_count = self.make_sorted_value_dict(False)
        if len(suit_count) == 1:
            return True
        return False

    def is_royal(self):
        royal_cards = [10, 11, 12, 13, 14]
        for card in self.lst_cards:
            if card.rank in royal_cards:
                royal_cards.remove(card.rank)
            else:
                return False
        return True

    def is_straight(self):
        rank_count = {card.rank for card in self.lst_cards}
        return (max(rank_count) - min(rank_count)+1) == len(self.lst_cards) and len(rank_count) == len(self.lst_cards)
                    
    def find_high_card(self):
        highest_card = -1
        for card in self.lst_cards:
            if card.rank > highest_card:
                highest_card = card.rank
        return highest_card
        
    def has_pairs(self):
        rank_count = self.make_sorted_value_dict(True)
        if len(rank_count) != 5:
            return True
        return False 

    def find_pairs(self):
        rank_count = self.make_sorted_value_dict(True)

        if len(rank_count) == 2:
            if rank_count[0][1] == 3 and rank_count[1][1] == 2:
                return('Full House', rank_count[0][0], rank_count[1][0])
            else:
                return ('Four of a Kind', rank_count[0][0])
        
        elif len(rank_count) == 3:
            if rank_count[0][1] == 2 and rank_count[1][1] == 2:
                return ('Two Pairs', rank_count[0][0], rank_count[1][0])
            else:
                return ('Three of a Kind', rank_count[0][0])

        elif len(rank_count) == 4:
            return ('One Pair', rank_count[0][0])
        
        raise Exception('Something went wrong')

    
    def make_sorted_value_dict(self, rank_or_suit=True):
        if rank_or_suit == True:
            rank_count = {}

            for card in self.lst_cards:
                if card.rank not in rank_count:
                    rank_count[card.rank] = 1
                else:
                    rank_count[card.rank] += 1
            return tuple(sorted(rank_count.items(), key=lambda item: item[1], reverse=True))

        suit_count = {}
        for card in self.lst_cards:
            if card.suit not in suit_count:
                suit_count[card.suit] = 1
            else:
                suit_count[card.suit] += 1 
        return tuple(sorted(suit_count.items(), key=lambda item: item[1], reverse=True))

    def clear(self):
        self.lst_cards = []

    def populate_poker(self, deck):
        for i in range(0, 5):
            self.lst_cards.append(deck.deal_card())

class Player():
    def __init__(self, name, hand):
        self.hand_types = ['High Card', 'One Pair', 'Two Pairs', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']
        self.hand = hand
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0 

    def decide_win(self, target, self_value, target_value):
        try:
            if self_value > target_value:
                self.win(target)
            elif self_value < target_value:
                target.win(self)
            else:
                return False
        except:
            raise Exception('Something went wrong', self_value, target_value)
        
    def win(self, loser):
        self.wins += 1
        loser.losses += 1
    
    def tie(self, target):
        self.ties += 1
        target.ties += 1

    def play_poker(self, other_player, deck):
        self.hand.clear()
        other_player.hand.clear()

        self.hand.populate_poker(deck)
        other_player.hand.populate_poker(deck)

        p1_results = self.hand.decide_type()
        p2_results = other_player.hand.decide_type()
        
        p1_type_index = self.hand_types.index(p1_results[0])
        p2_type_index = other_player.hand_types.index(p2_results[0])
        
        if self.decide_win(other_player, p1_type_index, p2_type_index) == False:

            if self.decide_win(other_player, p1_results[1], p2_results[1]) == False:

                if p1_results[0] == 'Two Pairs' or p1_results[0] == 'Full House':

                    if self.decide_win(other_player, p1_results[2], p2_results[2]) == False:
                        if self.decide_win(other_player, self.hand.find_high_card(), other_player.hand.find_high_card()) == False:
                            self.tie(other_player)
                elif self.decide_win(other_player, self.hand.find_high_card(), other_player.hand.find_high_card()) == False:
                            self.tie(other_player)
 
    def report(self):
        return f'\n-----{self.name}-----\n*Total wins: {self.wins}\n*Total losses: {self.losses}\n*Total draws: {self.ties}\n--------------'

main()