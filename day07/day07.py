import numpy as np
from collections import defaultdict
from math import prod, sqrt, floor, ceil
import pandas as pd

from collections import Counter


def score_row(row):
    hand = row['hand']
    score = 0

    # reverse the card ranks so that increasing indexes correspond to higher ranks of cards
    card_rank = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'][::-1]
    # for scoring, we'll add one to the index into this array
    card_rank_score = lambda x: card_rank.index(x) + 1

    # KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    # to turn this into a consistent score, we'll introduce a tiebreaker_score:
    # since there are 13 card ranks, that can be represented as two digits in base10.
    # the tiebreaker is the result of adding up the card rank score for each card in reverse order, since
    # the first card counts for more than any of the others, but it has index=0
    tiebreaker_score = sum([10 ** (2 * ix_) * card_rank_score(card_) for ix_, card_ in enumerate(hand[::-1])])

    card_counts = Counter(hand)
    # first_card_rank = card_rank.index(hand[0]) + 1

    js = card_counts.get('J', 0)
    five_of_a_kind = [k for k, v in card_counts.items() if v == 5 and k != 'J']
    four_of_a_kind = [k for k, v in card_counts.items() if v == 4 and k != 'J']
    three_of_a_kind = [k for k, v in card_counts.items() if v == 3 and k != 'J']
    two_of_a_kind = [k for k, v in card_counts.items() if v == 2 and k != 'J']

    # JJJJJ or JJJJX can both make a five of a kind, where X is any non-J
    # other 5s: JJJXX JJXXX JXXXX
    if five_of_a_kind \
            or js >= 4 \
            or js == 3 and two_of_a_kind \
            or js == 2 and three_of_a_kind \
            or js == 1 and four_of_a_kind:
        hand_kind_score = 10
    elif four_of_a_kind \
            or js == 3 \
            or js == 2 and two_of_a_kind \
            or js == 1 and three_of_a_kind:
        # XXXXY, XXXJY, XXJJY, XJJJY
        hand_kind_score = 9
    elif three_of_a_kind and two_of_a_kind \
            or len(two_of_a_kind) == 2 and js == 1 \
            or two_of_a_kind and js == 2:
        # full houses are tricky because the Js can make either a 3 of a kind or a 2 of a kind
        # XXXYY, XXYYJ, XXYJJ
        hand_kind_score = 8
    elif three_of_a_kind \
            or js == 2 \
            or js == 1 and two_of_a_kind:
        # just 3 of a kind: XXXYZ, XXJYZ, XJJYZ
        hand_kind_score = 7
    elif len(two_of_a_kind) == 2 and js == 0:
        # two pair: XXYYZ. Adding any Js will turn this into 3 of a kind or full house!
        hand_kind_score = 6
    elif two_of_a_kind and js == 0 \
            or js == 1:
        # one pair: WXXYZ, VWXYJ
        hand_kind_score = 5
    else:
        # high card
        hand_kind_score = 4

    score = 10 ** 28 * hand_kind_score + tiebreaker_score

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
