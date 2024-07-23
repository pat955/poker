from cards import Hand

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
