from functools import wraps

from werkzeug.exceptions import Conflict, NotFound

from poker.database.models import Round, User


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

            return func(*args, **kwargs)

        return wrapper

    return decorator


def player_fold(db_session, user_session):
    pass

def player_check(db_session):
    pass
def player_call(db_session):
    pass
def player_bet(db_session):
    pass
def player_raise(db_session):
    pass
