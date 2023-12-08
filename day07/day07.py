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
    card_rank_score = lambda x: card_rank.index(x) + 1

    # KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    # to turn this into a consistent score, we'll introduce a tiebreaker_score:
    # since there are 13 card ranks, that can be represented as two digits in base10.
    # the tiebreaker is the result of adding up the card rank score for each card in reverse order, since
    # the first card counts for more than any of the others, but it has index=0
    tiebreaker_score = sum([10**(2*ix_) * card_rank_score(card_) for ix_, card_ in enumerate(hand[::-1])])

    card_counts = Counter(hand)
    # first_card_rank = card_rank.index(hand[0]) + 1

    five_of_a_kind = [k for k, v in card_counts.items() if v == 5]
    four_of_a_kind = [k for k, v in card_counts.items() if v == 4]
    three_of_a_kind = [k for k, v in card_counts.items() if v == 3]
    two_of_a_kind = [k for k, v in card_counts.items() if v == 2]

    if five_of_a_kind:
        hand_kind_score = 10
        hand_kind_card_score = card_rank_score(five_of_a_kind[0])
    elif four_of_a_kind:
        hand_kind_score = 9
        hand_kind_card_score = card_rank_score(four_of_a_kind[0])
    elif three_of_a_kind:
        if two_of_a_kind:
            # full house
            hand_kind_score = 8
            hand_kind_card_score = 100*card_rank_score(three_of_a_kind[0]) + card_rank_score(two_of_a_kind[0])
        else:
            # just 3 of a kind
            hand_kind_score = 7
            hand_kind_card_score = card_rank_score(three_of_a_kind[0])
    elif len(two_of_a_kind) == 2:
        # two pair
        hand_kind_score = 6
        hand_kind_card_score1 = card_rank_score(two_of_a_kind[0])
        hand_kind_card_score2 = card_rank_score(two_of_a_kind[0])
        if hand_kind_card_score1 < hand_kind_card_score2:
            hand_kind_card_score1, hand_kind_card_score2 = hand_kind_card_score2, hand_kind_card_score1

        hand_kind_card_score = 100 * hand_kind_card_score1 + hand_kind_card_score2
    elif two_of_a_kind:
        # one pair
        hand_kind_score = 5
        hand_kind_card_score = card_rank_score(two_of_a_kind[0])
    else:
        # high card
        hand_kind_score = 4
        hand_kind_card_score = max([card_rank_score(card_) for card_ in hand])

    # score = 10**28 * hand_kind_score + 10**20 * hand_kind_card_score + tiebreaker_score
    score = 10**28 * hand_kind_score + tiebreaker_score

    return score


def main():
    # df = pd.read_csv("test_input.txt", sep=' ', header=None, names=('hand', 'bid'))
    df = pd.read_csv("input.txt", sep=' ', header=None, names=('hand', 'bid'))

    # add some testcases for high card
    # df.loc[len(df)] = '32T89', 10
    # df.loc[len(df)] = '32T8Q', 15

    df['score'] = df.apply(score_row, axis=1)
    df.sort_values(by='score', inplace=True)
    df.reset_index(drop=True, inplace=True)
    total_winnings = np.sum((np.array(df.index) + 1) * df['bid'])
    print(df)
    print(f'total_winnings = {total_winnings}')


if __name__ == '__main__':
    main()
