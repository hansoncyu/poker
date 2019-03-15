from flask import (
    Blueprint,
    jsonify,
    session as user_session,
)
from werkzeug.exceptions import Conflict, Unauthorized

from poker.database import db
from poker.lib import round as lib
from poker.lib.validation import validate_body
from poker.validation_schemas.round import (
    PLAYER_ACTION,
)


round_page = Blueprint("round", __name__)


@round_page.before_request
def require_login_and_ingame():
    if not user_session.get("user_id", False):
        return Unauthorized()

    if not user_session.get("round_id", False):
        return Conflict("User is not in a game.")


@round_page.route("/status", methods=["GET"])
def round_status():
    resp = lib.get_round_status(db.session, user_session)

    return jsonify(resp)


@round_page.route("/action", methods=["POST"])
@validate_body(PLAYER_ACTION)
@lib.validate_player_turn(db.session, user_session)
def player_action(user, current_round, request_data):
    action = request_data["action"]

    if action == "fold":
        resp = lib.player_fold(user, current_round)
    elif action == "check":
        resp = lib.player_check(user, current_round)
    elif action == "call":
        resp = lib.player_call(user, current_round)
    elif action == "bet":
        resp = lib.player_bet(user, current_round, request_data["amount"])
    elif action == "raise":
        resp = lib.player_raise(user, current_round, request_data["amount"])

    return jsonify(resp)
