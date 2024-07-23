from cards import Deck
from player import Player
from card_game import Card_Game

class Poker(Card_Game):
    def __init__(self, name, players, table, rounds=5, funds_added_each_round=100, deck=Deck()):
        super().__init__(name, players, deck)
        self.table = table
        self.rounds = rounds
        self.funds_added_each_round = funds_added_each_round
        self.active_players = players
        self.pool = 0
        self.current_round_active = False
        self.highest_caller = None
        self.someone_has_called = False
    
    def poker_populate(self, player, amount=5):
        for i in range(amount):
            player.hand.cards.append(self.deck.deal_card())

    def call_for_all(self, players, funcs):
        # Inputted functions(dict) will be executed for all players(list) as well as table if in player list.  
        # ex. funcs={<function> : <arguements> or [<arg>, <arg>, ...]}
        # ex. {Player.add_funds: self.funds_added_each_round, Player.clear_hand: None}
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
        # Prints table cards, and player hand. Offers trade, offers to call
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
        # only returns if in valid answers or 'q'.
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
        # Compares two values. Returns True if first val wins
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
        devided_pool = self.pool // len(players)
        for p in players:
            p.balance += devided_pool