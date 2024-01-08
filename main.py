from deck import *
def main():
    table = Table()
    player_amount = table.get_player_amount()

    simple_poker = Poker('Simple Poker', [Player(f'Player {i}', 0) for i in range(1, int(player_amount)+1)], table, 3, 100)
    table.add_game(simple_poker)
    
    simple_poker.play()      
    

class Table():
    def __init__(self):
        self.hand = Hand()
        self.game = None


    def add_game(self, game):
        self.game = game


    def get_player_amount(self):
        valid_answers = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
        player_input = input('How many players? (2-10) ')
        
        while player_input not in valid_answers:
            if player_input == 'q':
                print('Quitting...')
                exit()
        
            player_input = input('\nInput a number between 2 and 10: ')
        return player_input
    

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

        player.hand.add_card(table_card)
        self.hand.add_card(player_card)
        
        print(f'New cards: {self.hand}\nYour hand: {player.hand}')
        return 'Done trading.'

    
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
        self.active = True


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
        # Returns formatted str of name, wins, losses, ties and win rate but if wins and losses are 0,
        # does not calculate win rate to avoid zero devision error
        if self.wins == 0 and self.losses == 0:
            return f'\n-----{self.name}-----\n~ Total wins: {self.wins}\n~ Total losses: {self.losses}\n~ Total ties: {self.ties}\n~ Win rate: -\n------------------'
        
        win_rate = (self.wins/(self.wins + self.losses))*100
        return f'\n-----{self.name}-----\n~ Total wins: {self.wins}\n~ Total losses: {self.losses}\n~ Total ties: {self.ties}\n~ Win rate: {win_rate:.2f}%\n------------------'


class Card_Game():
    def __init__(self, name, deck=Deck()):
        self.name = name
        self.deck = deck 


    def create_shuffled_deck(self):
        self.deck = Deck()
        self.deck.generate_deck()
        self.deck.shuffle()


class Poker(Card_Game):
    def __init__(self, name, players, table, rounds=5, funds_added_each_round=100, deck=Deck()):
        # Name to maybe print out if im making variations of poker, player list can be useful when making more than 2 player games
        # table for trades, deck for obvious reasons i hope and rounds that default to 5 if nothing is else is told.
        # pool for funds that will be awarded to winner and current_round_active tells you if a round is ongoing.
        super().__init__(name, deck)
        self.table = table
        self.funds_added_each_round = funds_added_each_round
        self.players = players
        self.active_players = players
        self.pool = 0
        self.rounds = rounds
        self.current_round_active = False
        self.highest_caller = None
        self.someone_has_called = False


    def quit(self):
        for p in self.players:
            print(p.report())
        
        print('Quitting...')
        exit()
    

    def poker_populate(self, player, amount=5):
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

    def play(self):
        print('---Quit anytime by pressing "q".---') 

        for i in range(self.rounds):
            self.current_round_active = True
            self.highest_caller = None
            self.someone_has_called = False
            self.active_players = self.players
            print(f'--------\nRound {i+1}!\n--------')

            self.call_for_all(self.players, {Player.add_funds: self.funds_added_each_round, Player.clear_hand: None, Player.able_to_play: None})
            self.create_shuffled_deck()

            self.table.hand.clear()
            self.poker_populate(self.table)

            self.call_for_all(self.players, {self.poker_populate:3, self.poker_round_intro: None})
            
            self.call_for_all(self.players, {self.poker_populate:1})
            
            self.game_loop()
            if self.current_round_active == False:
                continue

            self.call_for_all(self.players, {self.poker_populate:1})
            for player in self.active_players:
                if player.currently_called == 0:
                    self.deactivate_player(player)

            formatting = '='*(len(f'{player.name}{self.players[0].hand.decide_type()[0]}{str(self.players[0].hand)}')//2)
            for player in self.active_players:
                print(f'{player.name}: {player.hand.decide_type()[0]} {player.hand}\n{formatting}VS{formatting}')
            print(self.compare_hand_types(), '\n')


    def game_loop(self):
        for player in self.players:
            print(f'Table cards:\n{self.table.hand}')
            print(f'\n{player.name}\n{player.hand}')
            trade_input = self.retry_loop(player, ['y', 'n'], f'\nDo you want to trade? (y/n) ')

            if trade_input == 'y':
                print(self.table.trade(player))

            if self.someone_has_called == False:
                player_input = self.retry_loop(player, ['y','n'],'\nDo you want to call? (y/n) ')

                if player_input == 'y':   
                    self.call(player)
                
            elif self.able_to_raise(player):
                player_input = self.retry_loop(player, ['r', 'f', 'n'], '\nDo you want to raise, fold or do nothing? (r/f/n) ') 
            
                if player_input == 'r':  
                    self.raisee(player)

                elif player_input == 'f':
                    self.fold(player)
            else:
                player_input = self.retry_loop(player, ['f', 'n'], '\nFold or do nothing? (f/n) ' )
                if player_input == 'f':
                    self.fold(player)
            self.player_switch()


    def able_to_raise(self, player):
        return player.balance >= self.highest_caller.currently_called



    def player_switch(self):
        button_pressed = input('Press any button when done. ')
        print('\n---------------------\n'*7)
        button_pressed = input('Next player, press any button. ')
    

    def poker_round_intro(self, player):
        # Prints table cards, and player hand.
        # Offers to trade, if y start trade, if not continue and ask if player want to call.

        print(f'Table cards:\n{self.table.hand}')
        print(f'\n{player.name}\n{player.hand}')
        
        trade_input = self.retry_loop(player, ['y', 'n'], f'\nDo you want to trade? (y/n) ')

        if trade_input == 'y':
            print(self.table.trade(player))

        player_input = self.retry_loop(player, ['y','n'],'\nDo you want to call? (y/n) ')

        if player_input == 'y':   
            self.call(player)
        self.player_switch()

        
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


    def make_overall_res_dict(self):
        overall_results = []

        for player in self.active_players:
            results = player.hand.decide_type()
            overall_results.append((player, results))
        return overall_results


    def update_active_players(self):
        self.active_players = []
        for player in self.players:
            if player.active == True:
                self.active_players.append(player)


    def deactivate_player(self, player):
        player.active = False
        self.lose(player)
        self.update_active_players()


    def compare_hand_types(self, index=0):
        if len(self.active_players) == 0:
            return 'Nobody won, somebody has to call!'
        if len(self.active_players) == 1:
            return self.win()
        o_res = self.make_overall_res_dict()

        p1 = o_res[index][0]
        p2 = o_res[index +1][0]
        type_index = p1.hand_types.index(o_res[index][1][0])
        type_index2 = p2.hand_types.index(o_res[index +1][1][0])

        type_comp = self.does_val1_win(type_index, type_index2)
        if type(type_comp) == bool:
            if type_comp == True:
                self.deactivate_player(p1)
            else:
                self.deactivate_player(p2)
            return self.compare_hand_types()
        
        rank_comp = self.does_val1_win(o_res[index][1][1], o_res[index+1][1][1])
        
        if type(rank_comp) == bool:
            if type_comp == True:
                self.deactivate_player(p1)
            else:
                self.deactivate_player(p2)
            return self.compare_hand_types()
            
        elif o_res[index][1][0] == 'Two Pairs' or o_res[index+1][1][0] == 'Full House':
            secondary_rank_comp = self.does_val1_win(o_res[index][1][2], o_res[index+1][1][2])
                
            if type(secondary_rank_comp) == bool:
                if type_comp == True:
                    self.deactivate_player(p1)
                else:
                    self.deactivate_player(p2)
                return self.compare_hand_types()
            
            return self.next_card_loop(o_res[index][0], o_res[index+1][0])

        return self.next_card_loop(o_res[index][0], o_res[index+1][0])


    def next_card_loop(self, p1, p2):
        # Used in case of between hand types and hand type value, compares highest card until not a tie
        # If it reaches the end then calls tie function. it is very rare to see a true tie.
        index = 0
        while self.does_val1_win(p1.hand.find_high_card(index), p2.hand.find_high_card(index))  == 'Tie':
            if index == 4 and len(self.active_players) == 2:
                return self.tie()
            elif index == 4 and len(self.active_players) > 2:
                return self.compare_hand_types(-1)
            index += 1

        return 'welp!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n!!!!!!!!!!!!!!!\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!'


    def win(self):
        if len(self.active_players) == 1:
            winner = self.active_players[0]
            winner.wins += 1
            profit =  self.pool - winner.currently_called
            winner.balance += self.pool
            winner.currently_called = 0 
        else:
            raise Exception('oh no', len(self.active_players), self.active_players, self.pool, winner.balance)
        self.pool = 0
        return f'{winner.name} wins! They won: {profit}!'


    def lose(self, player):
        player.losses += 1 
        player.currently_called = 0
    

    def tie(self):
        # resets pool, returns and resets called funds. Also adds ties for each player. 
        self.pool = 0 
        for player in self.active_players:
            player.balance += player.currently_called 
            player.currently_called = 0
            player.ties += 1
        

    def call(self, player):
        # asks player for amount and adds that to pool
        self.someone_has_called = True
        call_message = f'Your balance: {player.balance}\nHow much would you like to call? : '
        call_input = self.retry_int_loop(player, player.balance, call_message)

        self.add_to_pool(player, call_input)
        if self.highest_caller == None:
            self.highest_caller = player

        elif self.highest_caller.currently_called < call_input:
            self.highest_caller = player


    def raisee(self, player):
        matched_balance = player.balance - self.highest_caller.currently_called
        raise_input = self.retry_int_loop(player, matched_balance, f'Balance after matching: {matched_balance}.\nHow much would you like to raise (0 - {matched_balance})? ')
        
        self.add_to_pool(player, raise_input + self.highest_caller.currently_called)
        self.highest_caller = player


    def fold(self, player):
        
        self.deactivate_player(player)

        print(f'\n{player.name} folded! Your funds returned.\n')
        player.balance += player.currently_called
        self.pool -= player.currently_called
        player.currently_called = 0
        
        if len(self.active_players) == 0:
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