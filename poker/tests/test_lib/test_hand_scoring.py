from functools import cmp_to_key

from poker.lib import hand_scoring as lib


def test_sort_and_rank_hand_high_card():
    board_cards = ["S2", "C4", "H5", "D8", "S7"]
    player_cards = ["H1", "C13"]

    sorted_hand, rank = lib.sort_and_rank_hand(player_cards, board_cards)
    assert sorted_hand == ["H1", "C13", "D8", "S7", "H5"]
    assert rank == 0


def test_get_winners_from_hands_no_ties(four_player_round):
    hand_and_rankings = [
        (["H1", "C13", "D8", "S7", "H5"], 0),
        (["H1", "H13", "H12", "H11", "H10"], 9),
        (["H1", "D1", "S13", "H13", "C5"], 2),
        (["H1", "H4", "H3", "H8", "H9"], 5),
    ]
    player_hand_and_rankings = []
    for i in range(4):
        val = (four_player_round.players[i],) + hand_and_rankings[i]
        player_hand_and_rankings.append(val)

        _, rank = hand_and_rankings[i]
        if rank == 9:
            winner = four_player_round.players[i]

    winners = lib._get_winners_from_hands(player_hand_and_rankings)
    assert len(winners) == 1
    assert winners[0] == winner


def test_get_winners_from_hands_two_tied(four_player_round):
    hand_and_rankings = [
        (["H1", "C13", "D8", "S7", "H5"], 0),
        (["H11", "S11", "H5", "C5", "H1"], 2),
        (["H11", "D11", "H5", "S5", "C1"], 2),
        (["H1", "D1", "H3", "H8", "H9"], 1),
    ]
    player_hand_and_rankings = []
    expected_winners = []
    for i in range(4):
        val = (four_player_round.players[i],) + hand_and_rankings[i]
        player_hand_and_rankings.append(val)

        _, rank = hand_and_rankings[i]
        if rank == 2:
            expected_winners.append(four_player_round.players[i])

    winners = lib._get_winners_from_hands(player_hand_and_rankings)
    assert len(winners) == 2
    for winner in winners:
        assert winner in expected_winners


def test_get_winners_from_hands_break_tie_one_winner(four_player_round):
    hand_and_rankings = [
        (["H1", "C13", "D8", "S7", "H5"], 0),
        (["H11", "S11", "H5", "C5", "H1"], 2),
        (["H11", "D11", "H5", "S5", "C13"], 2),
        (["H1", "D1", "H3", "H8", "H9"], 1),
    ]
    player_hand_and_rankings = []
    for i in range(4):
        val = (four_player_round.players[i],) + hand_and_rankings[i]
        player_hand_and_rankings.append(val)

        hand, rank = hand_and_rankings[i]
        if rank == 2 and hand[-1] == "H1":
            expected_winner = four_player_round.players[i]

    winners = lib._get_winners_from_hands(player_hand_and_rankings)
    assert len(winners) == 1
    assert winners[0] == expected_winner


def test_custom_card_value_sort():
    hand = ["S5", "S8", "S10", "S2", "S1", "S13"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert hand == ["S1", "S13", "S10", "S8", "S5", "S2"]


def test_royal_flush_check():
    hand = ["S10", "S11", "S12", "S13", "S1", "C13", "H11", "S2"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.royal_flush_check(hand)


def test_royal_flush_check_fail():
    hand = ["S10", "S11", "D12", "S13", "S1", "C13", "H11", "S2"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert not lib.royal_flush_check(hand)


def test_straight_flush_not_royal_flush():
    hand = ["S10", "S11", "S12", "S13", "S9", "C13", "H11", "S2"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert not lib.royal_flush_check(hand)
    assert lib.straight_flush_check(hand)


def test_royal_flush_sort():
    hand = ["S10", "S11", "S12", "S13", "S1", "C13", "H11", "S2"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.royal_flush_sort(hand) == ["S1", "S13", "S12", "S11", "S10"]


def test_flush_check():
    hand = ["H1", "H2", "H8", "H3", "H4", "H13", "C3"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.flush_check(hand)


def test_flush_check_fail():
    hand = ["H1", "S2", "H8", "C3", "H4", "H13", "C3"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert not lib.flush_check(hand)


def test_flush_sort():
    hand = ["H1", "H2", "H8", "H3", "H4", "H13", "C3"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.flush_sort(hand) == ["H1", "H13", "H8", "H4", "H3"]


def test_straight_check():
    hand = ["S10", "S11", "D12", "S13", "S1", "C13", "H11", "S2"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.straight_check(hand)


def test_straight_check_fail():
    hand = ["S4", "S11", "D8", "S13", "S1", "C13", "H11", "S2"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert not lib.straight_check(hand)


def test_straight_sort():
    hand = ["S10", "S11", "D12", "S5", "S1", "C13", "H11", "S2"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.straight_sort(hand) == ["S1", "C13", "D12", "S11", "S10"]


def test_four_of_a_kind_check():
    hand = ["S4", "D4", "C4", "H4", "C3", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.four_of_a_kind_check(hand)


def test_four_of_a_kind_sort():
    hand = ["S4", "D4", "C4", "H4", "C3", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    sorted_hand = lib.four_of_a_kind_sort(hand)
    sorted_hand_num = [card[1:] for card in sorted_hand]
    assert sorted_hand_num == ["4", "4", "4", "4", "1"]


def test_full_house_check():
    hand = ["S3", "D3", "C3", "S5", "D5", "C5", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.full_house_check(hand)

    hand = ["S3", "D3", "S5", "D5", "C5", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.full_house_check(hand)


def test_full_house_sort():
    hand = ["S3", "D3", "C3", "S5", "D5", "C5", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    sorted_hand = lib.full_house_sort(hand)
    sorted_hand_num = [card[1:] for card in sorted_hand]

    assert sorted_hand_num == ["5", "5", "5", "3", "3"]

    hand = ["S3", "D3", "S5", "D5", "C5", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    sorted_hand = lib.full_house_sort(hand)
    sorted_hand_num = [card[1:] for card in sorted_hand]

    assert sorted_hand_num == ["5", "5", "5", "3", "3"]


def test_three_of_a_kind_check():
    hand = ["S9", "D4", "C4", "H4", "C3", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.three_of_a_kind_check(hand)


def test_three_of_a_kind_sort():
    hand = ["S9", "D4", "C4", "H4", "C3", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    sorted_hand = lib.three_of_a_kind_sort(hand)
    sorted_hand_num = [card[1:] for card in sorted_hand]
    assert sorted_hand_num == ["4", "4", "4", "1", "9"]


def test_two_pair_check():
    hand = ["S9", "D4", "C9", "H4", "C3", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.two_pair_check(hand)


def test_two_pair_check_fail():
    hand = ["S9", "D4", "C2", "H4", "C3", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert not lib.two_pair_check(hand)


def test_two_pair_sort():
    hand = ["S9", "D4", "C9", "H4", "C3", "S3", "H1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    sorted_hand = lib.two_pair_sort(hand)
    sorted_hand_num = [card[1:] for card in sorted_hand]

    assert sorted_hand_num == ["9", "9", "4", "4", "1"]


def test_one_pair_check():
    hand = ["S9", "D2", "C9", "H4", "C3", "S1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    assert lib.one_pair_check(hand)


def test_one_pair_sort():
    hand = ["S9", "D4", "C9", "H4", "C10", "S3", "H1"]
    hand.sort(key=cmp_to_key(lib.custom_card_value_sorter), reverse=True)

    sorted_hand = lib.one_pair_sort(hand)
    sorted_hand_num = [card[1:] for card in sorted_hand]

    assert sorted_hand_num == ["9", "9", "1", "10", "4"]
