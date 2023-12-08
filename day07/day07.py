import numpy as np
from collections import defaultdict
from math import prod, sqrt, floor, ceil
import pandas as pd

from collections import Counter


def score_row(row):
    hand = row['hand']
    score = 0

    # reverse the card ranks so that increasing indexes correspond to higher ranks of cards
    card_rank = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'][::-1]
    # for scoring, we'll add one to the index into this array

    card_counts = Counter(hand)
    first_card_rank = card_rank.index(hand[0]) + 1

    is_five_of_a_kind = any((count_ == 5 for count_ in card_counts.values()))
    if is_five_of_a_kind:
        score += 500000 + first_card_rank

    is_four_of_a_kind = any((count_ == 4 for count_ in card_counts.values()))
    if is_four_of_a_kind:
        score += 400000 + first_card_rank

    is_three_of_a_kind = any((count_ == 3 for count_ in card_counts.values()))
    num_pairs = sum((count_ == 2 for count_ in card_counts.values()))
    if is_three_of_a_kind:
        if num_pairs == 1:
            # full house
            score += 300000 + first_card_rank
        else:
            # just 3 of a kind
            score += 200000 + first_card_rank
    elif num_pairs == 2:
        # two pair
        score += 100000 + first_card_rank
    elif num_pairs == 1:
        # one pair
        score += 50000 + first_card_rank
    else:
        # high card
        highest_rank = max([card_rank.index(card_) for card_ in hand]) + 1
        score += 10000 + 100*highest_rank + first_card_rank

    return score


def main():
    df = pd.read_csv("test_input.txt", sep=' ', header=None, names=('hand', 'bid'))
    # add some testcases for high card
    df.loc[len(df)] = '32T89', 10
    df.loc[len(df)] = '32T8Q', 15
    df['score'] = df.apply(score_row, axis=1)
    df.sort_values(by='score', inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(df)


if __name__ == '__main__':
    main()
