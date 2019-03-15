from pytest import raises
from werkzeug.exceptions import Conflict

from poker.lib import round as lib
from poker.database.models.player_status import PLAYER_STATUS_CONSTANTS
from poker.database.models.round import ROUND_CONSTANTS


def test_get_round_status(test_session, test_user, four_player_round):
    user_session = {}
    user_session["user_id"] = test_user.id
    user_session["round_id"] = four_player_round.id

    resp = lib.get_round_status(test_session, user_session)

    assert len(resp["player_statuses"].keys()) == 4
    assert resp["pot"] == 0
    assert resp["round"] == "preflop"


def test_fold(test_session, four_player_round):
    current_player = four_player_round.current_player_turn

    resp = lib.player_fold(current_player, four_player_round)

    assert "success" in resp["message"]
    assert current_player.player_status.last_action == PLAYER_STATUS_CONSTANTS["action"]["fold"]
    assert not current_player.player_status.is_current_player
    assert current_player.player_status.bet == 0
    assert four_player_round.state == ROUND_CONSTANTS["state"]["preflop"]


def test_fold_end_round(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = 0

    current_player = four_player_round.current_player_turn
    resp = lib.player_fold(current_player, four_player_round)

    assert "success" in resp["message"]
    assert current_player.player_status.last_action is None
    assert four_player_round.state == ROUND_CONSTANTS["state"]["flop"]
    assert current_player.player_status.bet is None
    assert len(four_player_round.board) == 3


def test_check_end_round(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = 10

    current_player = four_player_round.current_player_turn

    resp = lib.player_check(current_player, four_player_round)

    assert "success" in resp["message"]
    assert current_player.player_status.last_action is None
    assert current_player.player_status.bet is None
    assert four_player_round.state == ROUND_CONSTANTS["state"]["flop"]
    assert len(four_player_round.board) == 3


def test_check(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = None

    current_player = four_player_round.current_player_turn

    resp = lib.player_check(current_player, four_player_round)

    assert "success" in resp["message"]
    assert current_player.player_status.last_action == PLAYER_STATUS_CONSTANTS["action"]["check"]
    assert current_player.player_status.bet == 0
    assert not current_player.player_status.is_current_player
    assert four_player_round.state == ROUND_CONSTANTS["state"]["preflop"]
    assert current_player.player_status.bet == 0


def test_check_conflict(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = 10

    current_player = four_player_round.current_player_turn
    current_player.player_status.bet = 5

    with raises(Conflict):
        lib.player_check(current_player, four_player_round)


def test_call_blind(test_session, four_player_round):
    blind = 0
    for player in four_player_round.players:
        if player.player_status.bet is not None:
            blind = max(blind, player.player_status.bet)

    current_player = four_player_round.current_player_turn
    before_bet_amount = current_player.player_status.money

    resp = lib.player_call(current_player, four_player_round)

    assert "success" in resp["message"]
    assert current_player.player_status.last_action == PLAYER_STATUS_CONSTANTS["action"]["call"]
    assert current_player.player_status.bet == blind
    assert current_player.player_status.money == before_bet_amount - blind
    assert not current_player.player_status.is_current_player
    assert four_player_round.state == ROUND_CONSTANTS["state"]["preflop"]


def test_call_end_round(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = 10

    current_player = four_player_round.current_player_turn
    current_player.player_status.bet = 5

    resp = lib.player_call(current_player, four_player_round)

    assert "success" in resp["message"]
    assert current_player.player_status.last_action is None
    assert current_player.player_status.bet is None
    assert four_player_round.state == ROUND_CONSTANTS["state"]["flop"]
    assert len(four_player_round.board) == 3


def test_call_out_of_money(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = 50

    current_player = four_player_round.current_player_turn
    current_player.player_status.money = 10
    current_player.player_status.bet = 5

    with raises(Conflict):
        lib.player_call(current_player, four_player_round)


def test_bet(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = None

    current_player = four_player_round.current_player_turn
    before_bet_amount = current_player.player_status.money

    resp = lib.player_bet(current_player, four_player_round, 10)

    assert "success" in resp["message"]
    assert current_player.player_status.last_action == PLAYER_STATUS_CONSTANTS["action"]["bet"]
    assert current_player.player_status.bet == 10
    assert current_player.player_status.money == before_bet_amount - 10
    assert not current_player.player_status.is_current_player
    assert four_player_round.state == ROUND_CONSTANTS["state"]["preflop"]


def test_bet_already_exists(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = 10

    current_player = four_player_round.current_player_turn

    with raises(Conflict):
        lib.player_bet(current_player, four_player_round, 10)


def test_raise(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = 10

    current_player = four_player_round.current_player_turn
    current_player.player_status.bet = 0

    resp = lib.player_raise(current_player, four_player_round, 20)

    assert "success" in resp["message"]
    assert current_player.player_status.last_action == PLAYER_STATUS_CONSTANTS["action"]["raise"]
    assert current_player.player_status.bet == 20
    assert not current_player.player_status.is_current_player
    assert four_player_round.state == ROUND_CONSTANTS["state"]["preflop"]


def test_raise_no_current_bet(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = 0

    current_player = four_player_round.current_player_turn

    with raises(Conflict):
        lib.player_raise(current_player, four_player_round, 20)


def test_raise_too_low(test_session, four_player_round):
    for player in four_player_round.players:
        player.player_status.bet = 10

    current_player = four_player_round.current_player_turn
    current_player.player_status.bet = 0

    with raises(Conflict):
        lib.player_raise(current_player, four_player_round, 10)
