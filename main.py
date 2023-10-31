import random
# Note to self: edittype returns winning card instead of rank number for cleaner interface.
# add funds_added_each_round=100 for poker class.
# why does deck=Deck() work but deck, ... super().__init__(deck) does not.
# check if raisee works as intended, sort cards in hand automatically. 
def main():

    p1 = Player('Player 1', 0)
    p2 = Player('Player 2', 0)
    
    table = Table()
    simple_poker = Poker('Simple Poker', [p1, p2], table, 5)
    table.add_game(simple_poker)
    
    simple_poker.play_2p(p1, p2)

    print(p1.report())
    print(p2.report())
    # print(f'Tie precentage: {(p1.ties/(p1.wins + p1.losses))*100:.2f}%')
    

class Deck():
    def __init__(self):
        self.suits = ['♦', '♠', '♥', '♣']
        self.ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.current_deck = []
    
    def check_deck(self):
        return self.current_deck
    
    def shuffle(self):
        if len(self.current_deck) == 0:
            raise Exception('Can\'t shuffle empty deck.') 

        random.shuffle(self.current_deck)

    def generate_deck(self):
        self.current_deck = [Card(rank,suit) for rank in self.ranks for suit in self.suits]
        
    def deal_card(self, index=-1):
        return self.current_deck.pop(index)


class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        # Everytime a card is printed it will show up in a "rank of suit" format,
        # if any of the cards are royal itll use their names instead of value index
        num_to_name = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
        if self.rank in num_to_name:
            return f'{num_to_name[self.rank]} {self.suit}'
        return f'{self.rank} {self.suit}'

  
class Hand():
    def __init__(self): 
        self.cards = []

    def __repr__(self):
        # when printed shows up as | Jack ♥ || 1 ♣ |... __str__ did not work, im unsure why
        self.printable_cards = ''
        for card in self.cards:
            self.printable_cards += f'| {card} |'
        return self.printable_cards
    
    def add_card(self, card):
        # It should work without return but doesnt for some reason
        self.cards.append(card)
        return self.cards

    def clear(self):
        self.cards = []

    def decide_type(self):
        # From highest value to lowest to make sure wins are correct
        
        if self.is_royal() and self.is_flush():
            return ('Royal Flush', 'n/a')

        elif self.is_flush() and self.is_straight():
            return ('Straight Flush', 'n/a')

        elif self.has_pairs():
            pair_results = self.find_pairs()
            if pair_results[0] == 'Four of a Kind' or pair_results[0] == 'Full House':
                return pair_results
            elif not self.is_flush() and not self.is_straight():
                """ 
                Ive set this up so that itll check that the hand isnt a flush or straight before returning pair pair_results
                Python ignores reused elif statement so i have to set it up this way for my current skill level
                It doesnt look the most clean but i can only think of doing this with a dictionary
                but i dont have the knowledge to execute that effectively.
                """
                return pair_results

        elif self.is_flush():
            return ('Flush', 'n/a')

        elif self.is_straight():
            return ('Straight', 'n/a')

        return ('High Card', self.find_high_card(0))

    def is_flush(self):
        return len(self.make_sorted_value_dict(False)) == 1

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
        return len(self.make_sorted_value_dict(True)) != 5
    
    def find_pairs(self):
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
        # returns a sorted hand, lowest to highest unless reverse = True
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
                count[typ] = 0
            count[typ] += 1

        return tuple(sorted(count.items(), key=lambda item: (item[1], item[0]), reverse=True))

class Table():
    def __init__(self):
        self.hand = Hand()
        self.game = None

    def add_game(self, game):
        self.game = game

    def trade(self, player):
        """
        Asks player for what card from table hand they would like to take, 1-5, the code will remove 1 so the index is correct.
        you can also input 'd' if youre done trading, thats why we dont remove 1 yet because the input can be a str.
        program tells player what they have choosen.
        repeat for player hand except if asks 1-(length of player hand)
        then the cards are removed and saved in table_card and player_card.
        when we finally switch in formatted string to save space, possibly changing this soon for more readability.
        repeat until player presses 'd'
        """
        print('\nPress "d" when done trading. Only one trade for now!')
         

        table_hand_index = self.game.retry_int_loop(player, 5, f'What card from table would you like? (1-5) ')
        if table_hand_index == 'd':
            return 'Done trading.'

        print(f'\n{self.hand.cards[table_hand_index-1]} choosen.\n')

        player_hand_index = self.game.retry_int_loop(player, len(player.hand.cards), f'What card would you like to switch out? (1-{len(player.hand.cards)}) ')
        if player_hand_index == 'd':
            return 'Done trading.'

        print(f'\n{player.hand.cards[player_hand_index-1]} choosen.\n')

        table_card = self.hand.cards.pop(table_hand_index-1)
        player_card = player.hand.cards.pop(player_hand_index-1)
    
        
        print(f'New cards: {self.hand.add_card(player_card)}\nYour hand: {player.hand.add_card(table_card)}')
        return 'Done trading.'

        """redo = self.game.retry_loop(player, ['y', 'n', 'd'], f'\nWould you like to trade more? (y/n) ')

        if redo == 'y':
            return self.trade(player)
        return 'Done trading.'"""

class Player():
    def __init__(self, name, balance=0):
        # hand types needed to determine win by type value
        # currently_called so i can keep track of bets and who will get what 
        self.hand_types = ['High Card', 'One Pair', 'Two Pairs', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']
        self.hand = Hand()
        self.name = name
        self.balance = balance
        self.currently_called = 0
        self.wins = 0
        self.losses = 0
        self.ties = 0 

    def clear_hand(self):
        self.hand.clear()

    def add_funds(self, amount):
        self.balance += amount

    def able_to_play(self):
        # checks if player is even able to play, quits, shouldnt happen unless no funds are added each round
        if self.balance == 0:
            print('Unable to play.')
            self.quit()
        return True

    def report(self):
        # Returns formatted str of name, wins, losses, ties and winrate but if wins and losses are 0,
        # does not calculate winrate to avoid zero devision error
        if self.wins == 0 and self.losses == 0:
            return f'\n-----{self.name}-----\n~Total wins: {self.wins}\n~Total losses: {self.losses}\n~Total ties: {self.ties}\n~Win rate unable to calculate\n------------------'
        
        win_rate = (self.wins/(self.wins + self.losses))*100
        return f'\n-----{self.name}-----\n~Total wins: {self.wins}\n~Total losses: {self.losses}\n~Total ties: {self.ties}\n~Win rate: {win_rate:.2f}%\n------------------'


class Card_Game():
    def __init__(self, name, deck=Deck()):
        self.name = name
        self.deck = deck 

    def create_shuffled_deck(self):
        # Create deck object, generate it and shuffle it to avoid reusing code.
        self.deck = Deck()
        self.deck.generate_deck()
        self.deck.shuffle()


class Poker(Card_Game):
    def __init__(self, name, players, table, rounds=5, deck=Deck()):
        # Name to maybe print out if im making variations of poker, player list can be useful when making more than 2 player games
        # table for trades, deck for obvious reasons i hope and rounds that default to 5 if nothing is else is told.
        # pool for funds that will be awarded to winner and current_round_active tells you if a round is ongoing.
        super().__init__(name, deck)
        self.table = table
        self.players = players
        self.pool = 0
        self.rounds = rounds
        self.current_round_active = False
    
    def quit(self):
        # Prints a report for all players and exits program, very useful for debugging.
        for p in self.players:
            print(p.report())
        print('Quitting...')
        exit()
    
    def poker_populate(self, player, amount=5):
        # Deal cards for player
        for i in range(amount):
            player.hand.cards.append(self.deck.deal_card())

    def call_for_all(self, players, funcs):
        # Inputted functions will be executed for all players in list as well as table if in player list.  
        # Works with multiple arguments if put in a list
        for func, args in funcs.items():
            for p in players:
                if type(args) == list:
                    func(p, *args)
                elif args == None:
                    func(p)
                else:
                    func(p, args)

    def play_2p(self, p1, p2):
        """
        Informs player, for everyround, funds will be added, hands will be cleared and checked if their able to play. 
        A new shuffled ready for use deck will be created. then each player will get 3 hards to start and start poker intros.
        Then the main poker "loop" will start, if any of the 2 players fold the round will stop and move on to the next.
        
        Formatting is simply '=' times x amount to make it look nice.
        Prints each player hand type and hand. Prints who won.
        
        """
        print('---Quit anytime by pressing "q".---')   

        for i in range(self.rounds):
            self.current_round_active = True
            print(f'--------\nRound {i+1}!\n--------')

            self.call_for_all([p1, p2], {Player.add_funds: 100, Player.clear_hand: None, Player.able_to_play: None})
            self.create_shuffled_deck()

            self.table.hand.clear()
            self.poker_populate(self.table)
            self.call_for_all([p1, p2], {self.poker_populate:3, self.poker_round_intro: None})
            
            self.call_for_all([p1, p2], {self.poker_populate:1})
            
            self.after_intros(p1, p2)
            if self.current_round_active == False:
                continue

            self.after_intros(p2, p1)
            if self.current_round_active == False:
                continue

            self.call_for_all([p1, p2], {self.poker_populate:1})

            formatting = '='*(len(f'{p1.hand.decide_type()[0]}{str(p1.hand)}')//2)
            print(f'\n{p1.hand.decide_type()[0]} {p1.hand}\n{formatting}VS{formatting}\n{p2.hand.decide_type()[0]} {p2.hand}\n\n')
            print(self.compare_hand_types(p1, p2), '\n')  

    def poker_round_intro(self, player):
        # Prints table cards, and player hand.
        # Offers to trade, if y start trade, if not continue and ask if player want to call.

        print(f'\nTable cards:\n{self.table.hand}')
        print(f'\n{player.name}\n{player.hand}')
        
        trade_input = self.retry_loop(player, ['y', 'n'], f'\nDo you want to trade? (y/n) ')

        if trade_input == 'y':
            print(self.table.trade(player))

        player_input = self.retry_loop(player, ['y','n'],'\nDo you want to call? (y/n) ')

        if player_input == 'y':   
            self.call(player)

    def after_intros(self, player, other_player):
        # Prints table and player hand, offers to trade this time with the player having more cards
        # after possible trade continues and if player has enough funds to raise other player is asked if they
        # want to raise, fold or do nothing. 
        print(f'\nTable cards:\n{self.table.hand}')
        print(f'\n{player.name}\n{player.hand}')

        trade_input = self.retry_loop(player, ['y', 'n'], f'\nDo you want to trade? (y/n) ')

        if trade_input == 'y':
            print(self.table.trade(player))

        if self.able_to_raise(player, other_player):
            player_input = self.retry_loop(player, ['r', 'f', 'n'], '\nDo you want to raise, fold or do nothing? (r/f/n) ') 
            
            if player_input == 'r':  
                self.raisee(player, other_player)

            elif player_input == 'f':
                self.fold(player, other_player)

        else:
            player_input = self.retry_loop(player, ['f', 'n'], '\nFold or do nothing? (f/n) ' )
            if player_input == 'f':
                self.fold(player, other_player)
    
                
    def retry_loop(self, player, valid_answers, input_message):
        # returns input only if in valid answers or 'q'.
        player_input = input(input_message)
        
        while player_input not in valid_answers:
            if player_input == 'q':
                self.quit()
        
            player_input = input('Something went wrong, please retry:\n'+ input_message)
        return player_input

    def retry_int_loop(self, player, valid_range, input_message):
        # Reccursion! integer loop is more complex than a str so i used reccursion.
        # 'd' input is more guarded so that by chance its more difficult to return d when not i a trade setting
        # it will try to convert str input to int, if unable, call function again, if it can check if in valid range.
        player_input = input(input_message)

        if player_input == 'q':
            self.quit()

        elif player_input == 'd' and valid_range in [1,2,3,4,5]:
            return 'd'
        try:
            int(player_input)
            if int(player_input) <= valid_range:
                return int(player_input)
            return self.retry_int_loop(player, valid_range, input_message)
            
        except:
            return self.retry_int_loop(player, valid_range, input_message)
    
    def does_val1_win(self, first_val, other_val):
        # Compares two values, if tie, returns tie, if first val wins, returns true.
        if first_val == other_val:
            return 'Tie'
        return first_val > other_val

    def compare_hand_types(self, p1, p2):
        # Get pair_results, type index to spare place
        p1_res = p1.hand.decide_type()
        p2_res = p2.hand.decide_type()
        
        p1_type_index = p1.hand_types.index(p1_res[0])
        p2_type_index = p2.hand_types.index(p2_res[0])

        index = 0 
        type_comp = self.does_val1_win(p1_type_index, p2_type_index)

        if type(type_comp) == bool:
            return self.win(type_comp, p1, p2)

        rank_comp = self.does_val1_win(p1_res[1], p2_res[1])
        
        if type(rank_comp) == bool:
            return self.win(rank_comp, p1, p2)

        elif p1_res[0] == 'Two Pairs' or p1_res[0] == 'Full House':
            
            secondary_rank_comp = self.does_val1_win(p1_res[2], p2_res[2])
                
            if type(secondary_rank_comp) == bool:
                return self.win(secondary_rank_comp, p1, p2)

            return self.next_card_loop(p1, p2)

        return self.next_card_loop(p1, p2)

    def next_card_loop(self, p1, p2):
        # Used in case of between hand types and hand type value, compares highest card until not a tie
        # If it reaches the end then calls tie function. it is very rare to see a true tie.
        index = 0
        while self.does_val1_win(p1.hand.find_high_card(index), p2.hand.find_high_card(index))  == 'Tie':
            if index == 4:
                return self.tie(p1, p2)
            index += 1
        return self.win(self.does_val1_win(p1.hand.find_high_card(index), p2.hand.find_high_card(index)), p1, p2)
     
    def win(self, win, p1, p2):
        # arg win is either true or false, true makes the first player the winner.
        # calculates profit, add to their balance as well as resets pool and currently called for both players
        if win:
            winner, loser = p1, p2
        else:
            winner, loser = p2, p1

        profit =  self.pool - winner.currently_called 
        return_message = (f'{winner.name} wins! They won: {profit}!')

        winner.balance += self.pool
        self.pool = 0 
        winner.currently_called = 0 
        loser.currently_called = 0 
        winner.wins += 1
        loser.losses += 1
        return return_message
        
    def tie(self, p1, p2):
        # resets pool, returns and resets called funds. Also adds ties for each player. 
        self.pool = 0 
        p1.balance += p1.currently_called 
        p1.currently_called = 0

        p2.balance += p2.currently_called 
        p2.currently_called = 0

        p1.ties += 1
        p2.ties += 1
        
    def call(self, player):
        # asks player for amount and adds that to pool
        call_message = f'Your balance: {player.balance}\nHow much would you like to call?: '
        call_input = self.retry_int_loop(player, player.balance, call_message)
        self.add_to_pool(player, call_input)

    def able_to_raise(self, player, other_player):
        # if player balance is more than the otherplayer has called, they can raise
        return player.balance >= other_player.currently_called 

    def raisee(self, player, other_player):
        matched_balance = player.balance - other_player.currently_called
        raise_input = self.retry_int_loop(player, matched_balance, f'Balance after matching: {matched_balance}.\nHow much would you like to raise (0 is valid)? ')
        
        self.add_to_pool(player, raise_input + other_player.currently_called)
    
    def fold(self, player, other_player):
        # When player inputs 'f', prints info and player balance, ties players and ends round
        print(f'\n{player.name} folded!\nAll funds returned.\n{player.name} balance: {player.balance}\n{other_player.name} balance: {other_player.balance}\n')
        self.tie(player, other_player)
        self.end_round()

    def add_to_pool(self, player, amount):
        # Takes away funds and adds to pool, used for call and raise
        player.balance -= amount
        player.currently_called += amount
        self.pool += amount

    def end_round(self):
        self.current_round_active = False
    
    def devide_pool(self, players):
        # In case of a total tie, this could be useful?
        devided_pool = self.pool // len(players)

        for p in players:
            p.balance += devided_pool

main()