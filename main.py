import random

def main():
    p1 = Player('Player 1')
    p2 = Player('Player 2')

    for i in range(0, 10000):
        new_deck = Deck()
        new_deck.generate_deck()
        new_deck.shuffle()
        p1.play_poker(p2, new_deck) 
       
    print(p1.report(), p2.report())
    print(f'Tie precentage: {(p1.ties/(p1.wins + p1.losses))*100:.2f}%')


class Deck():
    def __init__(self):
        self.suits = ['Diamonds', 'Spades', 'Hearts', 'Clubs']
        self.ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.current_deck = []
    
    def check_deck(self):
        return self.current_deck
    
    def shuffle(self):
        # Returns nothing but shuffles current deck
        if len(self.current_deck) == 0:
            raise Exception('Can\'t shuffle empty deck.') 
        random.shuffle(self.current_deck)

    def generate_deck(self):
        self.current_deck = [Card(rank,suit) for rank in self.ranks for suit in self.suits]
        
    def deal_card(self):
        # pop() removes card but also returns it for use
        return self.current_deck.pop()


class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def check_card(self):
        return f'{self.rank} of {self.suit}'

    def __repr__(self):
        # Everytime a card is printed it will show up in a "rank of suit" format,
        # if any of the cards are royal itll use their names instead of value index

        num_to_name = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
        if self.rank in num_to_name:
            return f'{num_to_name[self.rank]} of {self.suit}'
        return f'{self.rank} of {self.suit}'

  
class Hand():
    def __init__(self): 
        self.cards = []

    def clear(self):
        self.cards = []

    def populate_poker(self, deck):
        # Want to redo this so that itll ask for an amount and then deal those cards so i can use it for more than poker.
        for i in range(0, 5):
            self.cards.append(deck.deal_card())

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
                """ 
                Ive set this up so that itll check that the hand isnt a flush or straight before returning pair results
                Python ignores reused elif statement so i have to set it up this way for my current skill level
                It doesnt look the most clean but i can only think of doing this with a dictionary
                but i dont have the knowledge to execute that effectively.
                """
                return results

        elif self.is_flush():
            return ('Flush', 'n/a')

        elif self.is_straight():
            return ('Straight', 'n/a')

        return ('High Card', self.find_high_card(0))

    def is_flush(self):
        # returns bool based on if the theres only one type of suit in hand
        return len(self.make_sorted_value_dict(False)) == 1

    def is_royal(self):
        royal_cards = [10, 11, 12, 13, 14]
        for card in self.cards:
            if card.rank in royal_cards:
                royal_cards.remove(card.rank)
            else:
                return False
        return True

    def is_straight(self):
        """
        Makes a set of all the ranks found in hand.
        Returns True if max value - min value + 1 is the length of hand and the set is as long as the hand.
        Example:
        (3,4,5,6,7) is the hand. 7 - 3 + 1 = 5 is the the length of hand and
        we have 5 different ranks so the length  of the set is the same as hand.
        (4, 5, 7, 8, 9) is almost straight but 9-4 +1 = 6 /= len(hand)
        """
        found_ranks = {card.rank for card in self.cards}
        return (max(found_ranks) - min(found_ranks)+1) == len(self.cards) and len(found_ranks) == len(self.cards)
                    
    def find_high_card(self, index):
        # Index parameter added so that you can find the next highest card in case of a tie
        highest_card = -1
        for card in self.cards[index:]:
            if card.rank > highest_card:
                highest_card = card.rank
        return highest_card
        
    def has_pairs(self):
        # (2:2, 6:1, 7:1, 3:1) = One Pair and the length isnt 5 so the hand has a pair
        return len(self.make_sorted_value_dict(True)) != 5
    
    def find_pairs(self):
        # read length of rank count ex. {11:3, 12:1, 9:1} to tell what type it is 
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

        raise Exception('Something went wrong, remember to raise has_pairs() first')

    def make_sorted_hand(self, reverse=False):
        # In case a sorted by rank hand is neeeded but not a suit or rank count
        return sorted(self.cards, key=lambda card: card.rank, reverse=reverse)

    def make_sorted_value_dict(self, rank_or_suit=True):
        # count amount of ranks or suits  show up in a hand in a dictionary format
        count = {}
        for card in self.cards:
            if rank_or_suit:
                typ = card.rank
            else:
                typ = card.suit

            if typ not in count:
                count[typ] = 1
            else:
                count[typ] += 1
        return tuple(sorted(count.items(), key=lambda item: (item[1], item[0]), reverse=True))


class Player():
    def __init__(self, name):
        # hand types needed to determine win by type value, hand is a hand object
        self.hand_types = ['High Card', 'One Pair', 'Two Pairs', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']
        self.hand = Hand()
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0 
        

    def decide_win(self, self_value, other_value):
        # registers win and loss but in case of tie, returns false so other conditions can be set up outside.
        if self_value == other_value:
            return 'Tie'
        return self_value > other_value

    def decide_total_win(self, p2):
        # Get results, type index to spare place
        p1_res = self.hand.decide_type()
        p2_res = p2.hand.decide_type()
        
        p1_type_index = self.hand_types.index(p1_res[0])
        p2_type_index = p2.hand_types.index(p2_res[0])

        index = 0 
        type_comp = self.decide_win(p1_type_index, p2_type_index)

        if type(type_comp) == bool:
            return self.win(type_comp, p2)

        rank_comp = self.decide_win(p1_res[1], p2_res[1])
        
        if type(rank_comp) == bool:
            return self.win(rank_comp, p2)

        elif p1_res[0] == 'Two Pairs' or p1_res[0] == 'Full House':
            
            secondary_rank_comp = self.decide_win(p1_res[2], p2_res[2])
                
            if type(secondary_rank_comp) == bool:
                return self.win(secondary_rank_comp, p2)

            return self.next_card_loop(p2)

        return self.next_card_loop(p2)


    def win(self, win, p2):

        if win:
            self.wins += 1
            p2.losses += 1
        else:
            self.losses += 1
            p2.wins += 1

    
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


    def next_card_loop(self, p2):
        index = 0
        while self.decide_win(self.hand.find_high_card(index), p2.hand.find_high_card(index))  == 'Tie':
            if index == 4:
                return self.tie(p2)
            index += 1
        return self.win(self.decide_win(self.hand.find_high_card(index), p2.hand.find_high_card(index)), p2)
     
    def report(self):
        if self.wins == 0 or self.losses == 0:
            return ('zero division error')
        win_rate = (self.wins/(self.wins + self.losses))*100
        return f'\n-----{self.name}-----\n~Total wins: {self.wins}\n~Total losses: {self.losses}\n~Total ties: {self.ties}\n~Win rate: {win_rate:.2f}%\n------------------'


main()