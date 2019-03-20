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
