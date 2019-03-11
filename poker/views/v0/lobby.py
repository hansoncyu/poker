from flask import (
    Blueprint,
    jsonify,
    request,
    session as user_session,
)
from werkzeug.exceptions import Unauthorized

from poker.database import db
from poker.lib import lobby as lib


lobby_page = Blueprint("lobby", __name__)


@lobby_page.before_request
def require_login():
    if not user_session.get("user_id", False):
        return Unauthorized()


@lobby_page.route("/create", methods=["GET"])
def create_lobby():
    resp = lib.create_lobby(db.session, user_session)

    return jsonify(resp)


@lobby_page.route("/join", methods=["GET"])
def join_lobby():
    resp = lib.join_lobby(
        db.session,
        user_session,
        request.args.get("lobby_code", ""),
    )

    return jsonify(resp)


@lobby_page.route("/leave", methods=["GET"])
def leave_lobby():
    resp = lib.leave_lobby(
        db.session,
        user_session,
    )

    return jsonify(resp)


@lobby_page.route("/status", methods=["GET"])
def lobby_status():
    resp = lib.get_lobby_status(
        db.session,
        user_session,
    )

    return jsonify(resp)


@lobby_page.route("/start_game", methods=["GET"])
def start_game():
    resp = lib.start_game(db.session, user_session)

    return jsonify(resp)
