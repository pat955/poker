import random

def main():
    poker_hands_file = open('poker.txt', 'r')
    wins = 0 
    loss = 0
    txt = poker_hands_file.read().split('\n')
    for line in txt:
        hand1 = line.split(' ')[:5]
        hand2 =  line.split(' ')[5:]
        if complete_task(hand1, hand2):
            wins += 1
        else:
            loss += 1

    print(f'-------------\n~ Wins: {wins}\n~ Loss: {loss}\n~ Total: {wins+loss}\n-------------')
    

ranks = ['n/a', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['C', 'D', 'S', 'H']
types = ['High Card', 'One Pair', 'Two Pairs', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']


def is_royal(hand):
    royal_ranks = ['T', 'J', 'Q', 'K', 'A']
    for card in hand:
        if card[0] in royal_ranks:
            royal_ranks.remove(card[0])
        else:
            return False
    return True

def is_straight(hand):
    rank_count = {ranks.index(card[0]) for card in hand}
    return (max(rank_count) - min(rank_count)+1) == len(hand) and len(rank_count) == len(hand)
    
def is_flush(hand):
    return len(set([card[1] for card in hand])) == 1

def has_pairs(hand):
    return (len(make_sorted_value_dict(hand, True)) != 5)

def find_pairs(hand):
    # returns the found pair, only call if has pairs == True
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
    raise Exception('something went wrong', hand)

def find_high_card(hand, index=0):
    return sort_hand(hand, True)[index][0]
 
def sort_hand(hand, reverse=False):
    return sorted(hand, key=lambda x: ranks.index(x[0]), reverse=reverse)
  
def make_sorted_value_dict(hand, rank_or_suit=True):
    # count amount of ranks or suits in a dictionary format
    count = {}
    for card in hand:
        if rank_or_suit:
            typ = card[0]
        else:
            typ = card[1]

        if typ not in count:
            count[typ] = 0
        count[typ] += 1

    return tuple(sorted(count.items(), key=lambda item: (item[1], item[0]), reverse=True))



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

def compare_values(value1, value2):
    if value1 == value2:
            return 'Tie'
    return value1 > value2

def complete_task(hand1, hand2):
    h1_type = decide_type(hand1)
    h2_type = decide_type(hand2)
    index = 0
    
    type_comparison_result = compare_values(types.index(h1_type[0]), types.index(h2_type[0]))
    

    if type_comparison_result == 'Tie':
        second_comparison_result = compare_values(ranks.index(h1_type[1]), ranks.index(h2_type[1]))

        if second_comparison_result == 'Tie':
            high_card_comparison_result = compare_values(find_high_card(hand1, index)[0], find_high_card(hand2, index)[0])

            while high_card_comparison_result == 'Tie':
                
                index += 1

            return high_card_comparison_result
        return second_comparison_result
    return type_comparison_result

    
main()