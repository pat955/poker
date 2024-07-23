from cards import Hand

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