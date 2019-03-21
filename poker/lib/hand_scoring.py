from collections import defaultdict
from functools import cmp_to_key


HAND_RANKINGS = {
    0: "High Card",
    1: "One Pair",
    2: "Two Pair",
    3: "Three of a Kind",
    4: "Straight",
    5: "Flush",
    6: "Full House",
    7: "Four of a Kind",
    8: "Straight Flush",
    9: "Royal Flush",
}

HAND_CHECK_AND_SORT_FUNCTIONS = [
    (lambda x: royal_flush_check(x), lambda x: royal_flush_sort(x), 9),
    (lambda x: straight_flush_check(x), lambda x: straight_flush_sort(x), 8),
    (lambda x: four_of_a_kind_check(x), lambda x: four_of_a_kind_sort(x), 7),
    (lambda x: full_house_check(x), lambda x: full_house_sort(x), 6),
    (lambda x: flush_check(x), lambda x: flush_sort(x), 5),
    (lambda x: straight_check(x), lambda x: straight_sort(x), 4),
    (lambda x: three_of_a_kind_check(x), lambda x: three_of_a_kind_sort(x), 3),
    (lambda x: two_pair_check(x), lambda x: two_pair_sort(x), 2),
    (lambda x: one_pair_check(x), lambda x: one_pair_sort(x), 1),
]


def get_best_hand_and_rank(players_to_score, board):
    player_hand_and_rankings = []
    for player in players_to_score:
        sorted_hand, ranking = sort_and_rank_hand(
            player.player_status.hand,
            board,
        )
        player_hand_and_rankings.append((player, sorted_hand, ranking))

    return player_hand_and_rankings


def sort_and_rank_hand(player_cards, board_cards):
    combined_hand = player_cards + board_cards
    combined_hand.sort(key=cmp_to_key(custom_card_value_sorter), reverse=True)
    for hand_check, hand_sort, rank in HAND_CHECK_AND_SORT_FUNCTIONS:
        if hand_check(combined_hand):
            return hand_sort(combined_hand), rank

    # Didn't pass any of the checks, so must be high card.
    return combined_hand[:5], 0


def custom_card_value_sorter(x, y):
    x_val = x[1:]
    y_val = y[1:]
    if x_val == "1":
        return 1
    elif y_val == "1":
        return -1
    else:
        return int(x_val) - int(y_val)


def get_winners_from_hands(player_hand_and_rankings):
    player_hand_and_rankings.sort(
        key=lambda player_hand_and_rankings: player_hand_and_rankings[2],
        reverse=True,
    )

    _, _, best_rank = player_hand_and_rankings[0]
    winners_and_hand = []

    for player, player_hand, rank in player_hand_and_rankings:
        if rank != best_rank:
            break
        winners_and_hand.append((player, player_hand))

    if len(winners_and_hand) > 1:
        winners = _break_ties(winners_and_hand)

    else:
        winner, _ = winners_and_hand[0]
        winners = [winner]

    return winners


def _break_ties(winners_and_hand):
    potential_winners = {
        i: player_hand[0] for i, player_hand
        in enumerate(winners_and_hand)
    }
    # Best five cards in each players_hand
    for i in range(5):
        max_num = 0
        for player, hand in winners_and_hand:
            current_val = hand[i][1:]
            if current_val == "1":
                current_val = "999"
            max_num = max(int(current_val), max_num)

        for j, player_hand in enumerate(winners_and_hand):
            _, hand = player_hand

            current_val = hand[i][1:]
            if current_val == "1":
                current_val = "999"
            if int(current_val) != max_num:
                try:
                    del potential_winners[j]
                except KeyError:
                    pass

    return [winner for winner in potential_winners.values()]


def royal_flush_check(cards):
    if flush_check(cards):
        flush_hand = flush_sort(cards)
    else:
        return False

    if flush_hand[0][1:] == "1" and straight_check(flush_hand):
        return True
    else:
        return False


def flush_check(cards):
    suit_count = defaultdict(int)
    for card in cards:
        suit_count[card[0]] += 1

    for count in suit_count.values():
        if count >= 5:
            return True

    return False


def flush_sort(cards):
    suit_cards = defaultdict(list)
    for card in cards:
        suit_cards[card[0]].append(card)

    for cards in suit_cards.values():
        if len(cards) >= 5:
            return cards[:5]

    raise Exception("No flush in hand.")


def straight_check(cards):
    unique_card_num = set([int(card[1:]) for card in cards])
    unique_card_num = list(unique_card_num)
    unique_card_num.sort()

    num_consecutive = 1
    last_card = unique_card_num[0]

    for card in unique_card_num:
        if card == last_card:
            pass
        elif card == last_card + 1:
            num_consecutive += 1
        # Detecting 10JQKA straight.
        else:
            num_consecutive = 1

        if card == 13 and unique_card_num[0] == 1:
            num_consecutive += 1

        if num_consecutive >= 5:
            return True

        last_card = card

    return False


def straight_sort(cards):
    highest_straight = []
    last_card = cards[0]
    for card in cards:
        if card == last_card:
            highest_straight.append(card)
        elif card[1:] == last_card[1:]:
            pass
        elif int(card[1:]) == int(last_card[1:]) - 1:
            highest_straight.append(card)
        elif card[1:] == "13" and last_card[1:] == "1":
            highest_straight.append(card)
        else:
            break

        if len(highest_straight) == 5:
            return highest_straight

        last_card = card

    raise Exception("No straight in hand.")


def royal_flush_sort(cards):
    flush_hand = flush_sort(cards)
    royal_flush_hand = straight_sort(flush_hand)

    return royal_flush_hand


def straight_flush_check(cards):
    if flush_check(cards):
        flush_hand = flush_sort(cards)
    else:
        return False

    if straight_check(flush_hand):
        return True
    else:
        return False


def straight_flush_sort(cards):
    flush_hand = flush_sort(cards)
    straight_flush_hand = straight_sort(flush_hand)

    return straight_flush_hand


def four_of_a_kind_check(cards):
    num_count = defaultdict(int)
    for card in cards:
        num_count[card[1:]] += 1

    for count in num_count.values():
        if count >= 4:
            return True

    return False


def four_of_a_kind_sort(cards):
    num_cards = defaultdict(set)
    for card in cards:
        num_cards[card[1:]].add(card)

    four_of_a_kind = None
    for cards_by_num in num_cards.values():
        if len(cards_by_num) == 4:
            four_of_a_kind = cards_by_num
            break

    for card in cards:
        if card not in four_of_a_kind:
            return list(four_of_a_kind) + [card]

    raise Exception("No four of a kind in hand.")


def full_house_check(cards):
    num_count = defaultdict(int)
    for card in cards:
        num_count[card[1:]] += 1

    has_three_of_a_kind = False
    has_two_of_a_kind = False
    for count in num_count.values():
        if count >= 2 and has_three_of_a_kind:
            has_two_of_a_kind = True
        elif count == 3:
            has_three_of_a_kind = True
        elif count == 2:
            has_two_of_a_kind = True

        if has_three_of_a_kind and has_two_of_a_kind:
            return True

    return False


def full_house_sort(cards):
    num_cards = defaultdict(list)
    for card in cards:
        num_cards[card[1:]].append(card)

    first_two_plus_match = None
    second_two_plus_match = None
    for cards_by_num in num_cards.values():
        if len(cards_by_num) >= 2:
            if first_two_plus_match is None:
                first_two_plus_match = cards_by_num
            else:
                second_two_plus_match = cards_by_num

    if len(first_two_plus_match) == len(second_two_plus_match):
        if int(first_two_plus_match[0][1:]) > int(second_two_plus_match[0][1:]):
            return first_two_plus_match[:3] + second_two_plus_match[:2]
        else:
            return second_two_plus_match[:3] + first_two_plus_match[:2]

    else:
        if len(first_two_plus_match) == 3:
            return first_two_plus_match[:3] + second_two_plus_match[:2]
        else:
            return second_two_plus_match[:3] + first_two_plus_match[:2]


def three_of_a_kind_check(cards):
    num_count = defaultdict(int)
    for card in cards:
        num_count[card[1:]] += 1

    for count in num_count.values():
        if count >= 3:
            return True

    return False


def three_of_a_kind_sort(cards):
    num_cards = defaultdict(set)
    for card in cards:
        num_cards[card[1:]].add(card)

    three_of_a_kind  = None
    for cards_by_num in num_cards.values():
        if len(cards_by_num) == 3:
            three_of_a_kind = cards_by_num
            break

    kickers = []
    for card in cards:
        if card not in three_of_a_kind:
            kickers.append(card)
        if len(kickers) == 2:
            return list(three_of_a_kind) + kickers

    raise Exception("No four of a kind in hand.")


def two_pair_check(cards):
    num_count = defaultdict(int)
    for card in cards:
        num_count[card[1:]] += 1

    has_one_pair = False
    for count in num_count.values():
        if count == 2 and has_one_pair:
            return True
        elif count == 2:
            has_one_pair = True

    return False


def two_pair_sort(cards):
    num_cards = defaultdict(list)
    for card in cards:
        num_cards[card[1:]].append(card)

    pairs = []
    for cards_by_num in num_cards.values():
        if len(cards_by_num) == 2:
            pairs.append(cards_by_num)

    pairs.sort(key=lambda cards: int(cards[0][1:]), reverse=True)
    two_pair = pairs[0] + pairs[1]

    for card in cards:
        if card not in two_pair:
            return two_pair + [card]

    raise Exception("No two pair in hand.")


def one_pair_check(cards):
    num_count = defaultdict(int)
    for card in cards:
        num_count[card[1:]] += 1

    for count in num_count.values():
        if count == 2:
            return True

    return False


def one_pair_sort(cards):
    num_cards = defaultdict(list)
    for card in cards:
        num_cards[card[1:]].append(card)

    pairs = []
    for cards_by_num in num_cards.values():
        if len(cards_by_num) == 2:
            pairs.append(cards_by_num)

    pairs.sort(key=lambda cards: int(cards[0][1:]), reverse=True)
    one_pair = pairs[0]

    kickers = []
    for card in cards:
        if card not in one_pair:
            kickers.append(card)

        if len(kickers) == 3:
            return one_pair + kickers

    raise Exception("No one pair in hand.")
