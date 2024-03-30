from deck import *
from player import Player
from games import Table, Card_Game, Poker

def main():
    table = Table()
    player_amount = table.get_player_amount()

    simple_poker = Poker('Simple Poker', [Player(f'Player {i}', 0) for i in range(1, int(player_amount)+1)], table, 3, 100)
    table.add_game(simple_poker)
    
    simple_poker.play()      
    
main()