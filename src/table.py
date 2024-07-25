from cards import Hand
from format import *

class Table():
    def __init__(self):
        self.hand = Hand()
        self.game = None
    
    def print_hand(self): # Returns: None
        print(f'Table cards:\n{self.table.hand}\n')

    def add_game(self, game): # Returns: None
        self.game = game

    def get_player_amount(self): # Returns: String
        valid_answers = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
        player_input = input('How many players? (2-10) ')
        
        while player_input not in valid_answers:
            if player_input == 'q':
                print('Quitting...')
                exit()
            player_input = input('\nInput a number between 2 and 10: ')
        return player_input
    
    def trade(self, player): # Returns: None
    
        table_cards = self.hand.cards
        player_cards = player.hand.cards

        print(' ◼◼◼◼    ' + '◻◻◻◻    ' * (len(table_cards) - 1)) # ◼ ◻

        first_card_input = self.game.retry_int_loop(player, len(table_cards), f'Press \'d\' when done. (1-{len(table_cards)}) ')
        if first_card_input == 'd':
            print('Done trading.')
            return 

        chosen_card = table_cards[first_card_input -1]

        print_wrapper(f'{chosen_card} {chosen_card.text_format()} choosen.', bolden, stand_out)

        second_card_input = self.game.retry_int_loop(player, len(player_cards), f'What card would you like to switch out? (1-{len(player_cards)}) ')
        if second_card_input == 'd':
            print('Done trading.')
            return 

        print_wrapper(f'{player_cards[second_card_input-1]} choosen.', bolden, stand_out)

        table_card = self.hand.cards.pop(first_card_input-1)
        player_card = player_cards.pop(second_card_input-1)

        player.hand.add_card(table_card)
        self.hand.add_card(player_card)
        
        print(f'New cards:\n{self.hand}\nYour hand:\n{player.hand}')
        print('Done trading.')
        return
