import random

def main():
    poker_hands_file = open('poker.txt', 'r')
    p1_wins = 0
    p1_losses = 0 
    
    for line in poker_hands_file.read().split('\n'):
        hand1 = line.split(' ')[:5]
        hand2 =  line.split(' ')[5:]
        complete_task(hand1, hand2, p1_wins, p1_losses)
    print(f'-----------\n~ Wins: {p1_wins}\n~ Losses: {p1_losses}\n-----------')
    

ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['C', 'D', 'S', 'H']
types = ['High Card', 'One Pair', 'Two Pairs', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']


def is_royal(hand):
    royal_ranks = ['T', 'J', 'Q', 'K', 'A']
    for card in hand:
        if card[1] in royal_ranks:
            royal_ranks.remove(card[1])
        else:
            return False
    return True

def is_straight(hand):
    sorted_hand = sorted(hand, key=lambda x: ranks.index(x[0]))
    prev_card_rank = sorted_hand[0][0]
    for card in sorted_hand[1:]:
        if card != ranks.index(prev_card_rank) + 1:
            return False
    return True
    
def is_flush(hand):
    return len(set([card[1] for card in hand])) == 1

def has_pairs(hand):
    return (len(make_sorted_value_dict(hand, True)) != 5)

def find_pairs(hand):
    r_count =  make_sorted_value_dict(hand, True)
    if len(r_count) == 2:
        if r_count[0][1] == 3 and r_count[1][1] == 2:
            return('Full House', r_count[0][0], r_count[1][0])
        return ('Four of a Kind', r_count[0][0])
    elif len(r_count) == 3:
        if r_count[0][1] == 2 and r_count[1][1] == 2:
            return ('Two Pairs', r_count[0][0], r_count[1][0])
        return ('Three of a Kind', r_count[0][0])
    elif len(r_count) == 4:
        return ('One Pair', r_count[0][0])
    else:
        raise Exception('something went wrong', hand)

def find_high_card(hand, index=0):
    return sort_hand(hand, True)[index]
 
def sort_hand(hand, reverse=False):
    return sorted(hand, key=lambda x: ranks.index(x[0]), reverse=reverse)
  
def make_sorted_value_dict(hand, rank_or_suit=True):
    # count amount of ranks or suits in a dictionary format
    if rank_or_suit == True:
        rank_count = {}
        for card in hand:
            if card[0] not in rank_count:
                rank_count[card[0]] = 1
            else:
                rank_count[card[0]] += 1
        return tuple(sorted(rank_count.items(), key=lambda item: (item[1], item[0]), reverse=True))

    suit_count = {}
    for card in hand:
        if card[1] not in suit_count:
            suit_count[card[1]] = 1
        else:
            suit_count[card[1]] += 1 
    return tuple(sorted(suit_count.items(), key=lambda item: (item[1], item[0]), reverse=True))

def is_flush(hand):
    suit_count = make_sorted_value_dict(hand, False)
    if len(suit_count) == 1:
        return True
    return False

def decide_type(hand):
    if is_royal(hand) and is_flush(hand):
        return ('Royal Flush', 'n/a')

    elif is_flush(hand) and is_straight(hand):
        return ('Straight Flush', 'n/a')

    elif has_pairs(hand):
        results = find_pairs(hand)
        if results[0] == 'Four of a Kind' or results[0] == 'Full House':
            return results
        elif not is_flush(hand) and not is_straight(hand):
            return results

    elif is_flush(hand):
        return ('Flush', 'n/a')

    elif is_straight(hand):
        return ('Straight', 'n/a')

    return ('High Card', find_high_card(hand, 0))

def decide_win(value1, value2, win_count, loss_count):
    if value1 > value2:
        
        win_count = 1
    elif value1 < value2:
        loss_count += 1
    else:
        return False

def complete_task(hand1, hand2, wins, losses):
    h1_type = decide_type(hand1)
    h2_type = decide_type(hand2)
    index = 0

    if decide_win(types.index(h1_type[0]), types.index(h2_type[0]), wins, losses) == False:
        if decide_win(h1_type[1], h2_type[1], wins, losses) == False:
            while decide_win(find_high_card(hand1, index)[0], find_high_card(hand2, index)[0], wins, losses) == False:
                index += 1

         
       
main()