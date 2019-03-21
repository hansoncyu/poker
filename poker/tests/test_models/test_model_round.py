def test_award_winners_one(four_player_round):
    winner = four_player_round.players[0]
    four_player_round.pot = 100

    before_award = winner.player_status.money

    winnings = four_player_round.award_winners([winner])

    assert winner.player_status.money == before_award + 100
    assert len(winnings) == 1
    assert winnings[0][0].id == winner.id
    assert winnings[0][1] == 100


def test_award_winners_three_remainder(four_player_round):
    winners = four_player_round.players[:3]
    four_player_round.pot = 100

    for player in winners:
        player.player_status.money = 0

    winnings = four_player_round.award_winners(winners)

    assert winners[0].player_status.money == 34
    assert winners[1].player_status.money == 33
    assert winners[2].player_status.money == 33
    assert len(winnings) == 3


def test_update_game_end_score(four_player_round):
    winners = four_player_round.players[:2]

    winnings = [(winner, 100) for winner in winners]

    player_hand_and_rankings = []
    for i, player in enumerate(four_player_round.players):
        player_hand_and_rankings.append([player, "H3, D5", i])

    four_player_round._update_game_end_score(player_hand_and_rankings, winnings)

    game_end_score = four_player_round.last_game_end_score

    assert len(game_end_score.winnings) == 2
    for winning in game_end_score.winnings:
        assert winning["winning"] == 100
    assert len(game_end_score.users_and_hands) == 4
    for user_hand in game_end_score.users_and_hands:
        assert user_hand["hand"] == "H3, D5"
