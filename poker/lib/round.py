from functools import wraps

from werkzeug.exceptions import Conflict

from poker.database.models import Round, User
from poker.database.models.player_status import PLAYER_STATUS_CONSTANTS
from poker.database.models.user import OutOfMoney


def get_round_status(db_session, user_session):
    current_round = db_session.query(Round).get(user_session.get("round_id"))
    user = db_session.query(User).get(user_session["user_id"])

    player_statuses = {}
    for player in current_round.players:
        status = player.player_status
        player_statuses[player.name] = {}
        player_statuses[player.name]["money"] = status.money
        player_statuses[player.name]["in_round"] = status.in_round
        player_statuses[player.name]["bet"] = status.bet
        player_statuses[player.name]["last_action"] = status.last_action
        player_statuses[player.name]["player_turn"] = status.player_turn
        player_statuses[player.name]["blind"] = status.blind

    resp = {}
    resp["player_statuses"] = player_statuses
    resp["current_player_turn"] = current_round.current_player_turn.name
    resp["pot"] = current_round.pot
    resp["board"] = current_round.board
    resp["round"] = current_round.get_state()

    resp["hand"] = user.player_status.hand

    return resp


def validate_player_turn(db_session, user_session):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_round = db_session.query(Round).get(user_session.get("round_id"))
            user = db_session.query(User).get(user_session["user_id"])

            if current_round.current_player_turn is not user:
                raise Conflict("It is currently another player's turn.")

            return func(user, current_round, *args, **kwargs)

        return wrapper

    return decorator


def player_fold(player, current_round):
    player.player_status.in_round = False
    player.player_status.last_action = PLAYER_STATUS_CONSTANTS["action"]["fold"]
    player.player_status.bet = 0

    if current_round.check_for_game_end():
        current_round.score_round()
        current_round.start_new_round()
    elif current_round.check_for_round_end():
        current_round.start_next_phase()
    else:
        current_round.go_to_next_player(folded_player=player)

    return {"message": "User has successfully folded hand."}


def player_check(player, current_round):
    if player.player_status.bet is not None and \
            player.player_status.bet < current_round.current_bet:
        raise Conflict(
            "User can not check on current betting round. "
            "Current bet is {}.".format(current_round.current_bet)
        )

    player.player_status.last_action = PLAYER_STATUS_CONSTANTS["action"]["check"]
    if player.player_status.bet is None:
        player.player_status.bet = 0

    if current_round.check_for_game_end():
        current_round.score_round()
        current_round.start_new_round()
    elif current_round.check_for_round_end():
        current_round.start_next_phase()
    else:
        current_round.go_to_next_player()

    return {"message": "User has successfully checked."}


def player_call(player, current_round):
    if player.player_status.bet and \
            player.player_status.bet >= current_round.current_bet:
        raise Conflict("User does not need to call. Try checking instead.")

    try:
        player_current_bet = player.player_status.bet or 0
        amount_to_call = current_round.current_bet - player_current_bet
        player.place_bet(amount_to_call, current_round.pot)
    except OutOfMoney:
        raise Conflict("User does not have sufficient money to call.")

    player.player_status.last_action = PLAYER_STATUS_CONSTANTS["action"]["call"]

    if current_round.check_for_game_end():
        current_round.score_round()
        current_round.start_new_round()
    elif current_round.check_for_round_end():
        current_round.start_next_phase()
    else:
        current_round.go_to_next_player()

    return {"message": "User has successfully called."}


def player_bet(player, current_round, amount):
    if current_round.current_bet > 0:
        raise Conflict("There is already a bet. Try raising or calling.")

    try:
        player.place_bet(amount, current_round.pot)
    except OutOfMoney:
        raise Conflict("User does not have sufficient money to bet.")

    player.player_status.last_action = PLAYER_STATUS_CONSTANTS["action"]["bet"]
    current_round.go_to_next_player()

    return {"message": "User has successfully bet."}


def player_raise(player, current_round, amount):
    if current_round.current_bet == 0:
        raise Conflict("There isn't a bet this round. Try betting.")

    player_current_bet = player.player_status.bet or 0
    if player_current_bet + amount <= current_round.current_bet:
        raise Conflict("Must raise an amount larger than the current bet.")

    try:
        player.place_bet(amount, current_round.pot)
    except OutOfMoney:
        raise Conflict("User does not have sufficient money to bet.")

    player.player_status.last_action = PLAYER_STATUS_CONSTANTS["action"]["raise"]
    current_round.go_to_next_player()

    return {"message": "User has successfully raised."}
