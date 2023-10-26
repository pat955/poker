import random

def main():
    p1 = Player('Player 1', Hand())
    p2 = Player('Player 2', Hand())

    for i in range(0, 1000):
        new_deck = Deck()
        new_deck.generate_deck()
        new_deck.shuffle()
        p1.play_poker(p2, new_deck)
    
        
    print(p1.report(), p2.report())


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
        num_to_name = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
        if self.rank in num_to_name:
            return f'{num_to_name[self.rank]} of {self.suit}'
        return f'{self.rank} of {self.suit}'

   


class Hand():
    def __init__(self): 
        self.lst_cards = []

    def decide_type(self):
        # From highest value to lowest to make sure wins are correct

        if self.is_royal() and self.is_flush():
            return ('Royal Flush', 'n/a')

        elif self.is_flush() and self.is_straight():
            return ('Straight Flush', 'n/a')

        elif self.has_pairs():
            results = self.find_pairs()
            if results[0] == 'Four of a Kind' or results[0] == 'Full House':
                return results
            elif not self.is_flush() and not self.is_straight():
                return results

        elif self.is_flush():
            return ('Flush', 'n/a')

        elif self.is_straight():
            return ('Straight', 'n/a')

        return ('High Card', self.find_high_card(0))

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
                    
    def find_high_card(self, index):
        # Index parameter added so that you can find the second highest card in case of a tie
        highest_card = -1
        for card in self.lst_cards[index:]:
            if card.rank > highest_card:
                highest_card = card.rank
        return highest_card
        
    def has_pairs(self):
        rank_count = self.make_sorted_value_dict(True)
        if len(rank_count) != 5:
            return True
        return False 

    def find_pairs(self):
        # read length of rank count ex. {11:3, 12:1, 9:1} to tell with type it is 
        rank_count = self.make_sorted_value_dict(True)

        if len(rank_count) == 2:
            if rank_count[0][1] == 3 and rank_count[1][1] == 2:
                return('Full House', rank_count[0][0], rank_count[1][0])
            return ('Four of a Kind', rank_count[0][0])
        
        elif len(rank_count) == 3:
            if rank_count[0][1] == 2 and rank_count[1][1] == 2:
                return ('Two Pairs', rank_count[0][0], rank_count[1][0])
            return ('Three of a Kind', rank_count[0][0])

        elif len(rank_count) == 4:
            return ('One Pair', rank_count[0][0])

        raise Exception('Something went wrong, remember to raise has_pairs() function first')
    
    def make_sorted_value_dict(self, rank_or_suit=True):
        # count amount of ranks or suits in a dictionary format

        if rank_or_suit == True:
            rank_count = {}
            for card in self.lst_cards:
                if card.rank not in rank_count:
                    rank_count[card.rank] = 1
                else:
                    rank_count[card.rank] += 1
            return tuple(sorted(rank_count.items(), key=lambda item: (item[1], item[0]), reverse=True))

        suit_count = {}
        for card in self.lst_cards:
            if card.suit not in suit_count:
                suit_count[card.suit] = 1
            else:
                suit_count[card.suit] += 1 
        return tuple(sorted(suit_count.items(), key=lambda item: (item[1], item[0]), reverse=True))

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
        # register win and loss and if tie return false so you can set up other conditions
        if self_value > target_value:
            self.win(target)
        elif self_value < target_value:
            target.win(self)
        else:
            return False

    def decide_total_win(self, p2):
        # Get results, type index to spare place
        p1_results = self.hand.decide_type()
        p2_results = p2.hand.decide_type()
        
        p1_type_index = self.hand_types.index(p1_results[0])
        p2_type_index = p2.hand_types.index(p2_results[0])
        index = 0 

        if self.decide_win(p2, p1_type_index, p2_type_index) == False:
            # If theres a tie between p1 and 2 hands, continue

            if self.decide_win(p2, p1_results[1], p2_results[1]) == False:
                # if the rank of their type is the same continue

                if p1_results[0] == 'Two Pairs' or p1_results[0] == 'Full House':
                    # if their type is two pairs or fullhouse, check their secondary type

                    if self.decide_win(p2, p1_results[2], p2_results[2]) == False:
                        
                        #raise Exception('something wrong', p1_results, p2_results, p1_results[1], p2_results[1])
                        # if  secondary rank types from full house and two pairs are still the same,
                        # compare the next highest card until no more are present

                        while self.decide_win(p2, self.hand.find_high_card(index), p2.hand.find_high_card(index)) == False:
                            if index == 4:
                                self.tie(p2)
                                break
                            index += 1
                else:
                    # If the types arent two pairs or fullhouse, compare the next high card until no more are present
                    while self.decide_win(p2, self.hand.find_high_card(index), p2.hand.find_high_card(index)) == False:
                        if index == 4:
                            self.tie(p2)
                            break
                        index += 1
 
    def win(self, loser):
        self.wins += 1
        loser.losses += 1
    
    def tie(self, target):
        self.ties += 1
        target.ties += 1

    def play_poker(self, p2, deck):
        # Clears last hand
        self.hand.clear()
        p2.hand.clear()

        # Populate their hands with 5 cards 
        self.hand.populate_poker(deck)
        p2.hand.populate_poker(deck)

        # Decide who wins
        self.decide_total_win(p2)
     
    def report(self):
        win_rate = (self.wins/(self.wins + self.losses))*100
        return f'\n-----{self.name}-----\n*Total wins: {self.wins}\n*Total losses: {self.losses}\n*Total draws: {self.ties}\n*Win rate not incl. ties: {win_rate:.2f}%\n------------------'

main()