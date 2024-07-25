import random

class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.symbols = {10: '10', 11: '♞ ', 12: '♛ ', 13: '♚ ', 14: '1 '}

    def __repr__(self):
        card, reverse_card = self.get_formatted()
        return f'┌─────┐\n│ {card} │\n│     │\n│ {reverse_card} │\n└─────┘\n'

    def get_formatted(self):
        if self.rank in self.symbols:
            card = f'{self.symbols[self.rank]}{self.suit}'
            reverse_card = f'{self.suit}{self.symbols[self.rank]}'
            
        else:
            card = f'{self.rank} {self.suit}'
            reverse_card = f'{self.suit} {self.rank}'

        return (card, reverse_card)
        
    def text_format(self):
        return f'{self.rank} {self.suit}'
    

class Deck():
    def __init__(self):
        self.suits = ['♦', '♠', '♥', '♣']
        self.ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.current_deck = []

    def shuffle(self):
        if len(self.current_deck) == 0:
            raise Exception('Can\'t shuffle empty deck.') 
        random.shuffle(self.current_deck)

    def generate_deck(self):
        self.current_deck = [Card(rank,suit) for rank in self.ranks for suit in self.suits]
        
    def deal_card(self, index=-1):
        return self.current_deck.pop(index)

  
class Hand():
    def __init__(self): 
        self.cards = []

    def __repr__(self):
        n = len(self.cards)

        s = f'┌─────┐ ' * n +'\n'

        for i in range(0, n):
            card = self.cards[i].get_formatted()
            s += f'│ {card[0]} │ '
        
        s += '\n' + '│     │ ' * n +'\n'
        
        for i in range(0, n):
            card = self.cards[i].get_formatted()
            s += f'│ {card[1]} │ '

        s += '\n' + '└─────┘ ' * n +'\n'
        return s

    def add_card(self, card):
        self.cards.append(card)

    def clear(self):
        self.cards = []

    def decide_type(self):
        # From highest hand value to lowest to make sure wins are correct
        if self.is_royal() and self.is_flush():
            return ('Royal Flush', 'n/a')

        elif self.is_flush() and self.is_straight():
            return ('Straight Flush', 'n/a')

        elif self.has_pairs():
            # this hand could be foak, fh or simply pairs. foak and fh is higher than flush and straight but not pairs
            # therefore it checks if its a flush or straight before returning pair results
            # python ignores reused elif statements, thats why its set up this way. Probably cleaner ways
            pair_results = self.find_pairs()
            if pair_results[0] == 'Four of a Kind' or pair_results[0] == 'Full House':
                return pair_results

            elif not self.is_flush() and not self.is_straight():
                return pair_results

        elif self.is_flush():
            return ('Flush', 'n/a')

        elif self.is_straight():
            return ('Straight', 'n/a')

        return ('High Card', self.find_high_card(0))

    def is_flush(self):
        return len(self.make_sorted_value_dict(rank_or_suit=False)) == 1

    def is_royal(self):
        hand_ranks = [card.rank for card in self.cards]
        royal_ranks = [10, 11, 12, 13, 14]
        return hand_ranks == royal_ranks

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
        return len(self.make_sorted_value_dict(rank_or_suit=True)) != 5
    
    def find_pairs(self):
        rank_count = self.make_sorted_value_dict(rank_or_suit=True)

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
        # returns a sorted hand, lowest to highest unless reverse = True
        return sorted(self.cards, key=lambda card: card.rank, reverse=reverse)

    def make_sorted_value_dict(self, rank_or_suit=True):
        # count n of ranks or suits  show up in a hand in a dictionary format
        count = {}
        for card in self.cards:
            if rank_or_suit:
                typ = card.rank
            else:
                typ = card.suit

            if typ not in count:
                count[typ] = 0
            count[typ] += 1

        return tuple(sorted(count.items(), key=lambda item: (item[1], item[0]), reverse=True))