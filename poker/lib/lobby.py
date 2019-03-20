import random
import string

from werkzeug.exceptions import Conflict, NotFound

from poker.database.models import (
    Lobby,
    LOBBY_CONSTANTS,
    User,
)


def create_lobby(db_session, user_session):
    user = db_session.query(User).get(user_session["user_id"])

    if user.lobby is not None:
        raise Conflict("User is already in a lobby.")

    new_lobby = Lobby(
        state=LOBBY_CONSTANTS["state"]["ready"],
        code=_get_new_lobby_code(db_session),
    )
    db_session.add(new_lobby)
    db_session.flush()

    user.lobby = new_lobby
    user_session["lobby_id"] = new_lobby.id

    return {"lobby_code": new_lobby.code}


def _get_new_lobby_code(db_session):
    lobby_exists = True

    while lobby_exists:
        new_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

        existing_lobby = (
            db_session.query(Lobby)
            .filter(Lobby.state.in_([
                LOBBY_CONSTANTS["state"]["ready"],
                LOBBY_CONSTANTS["state"]["ingame"],
            ]))
            .filter(Lobby.code == new_code)
        )
        lobby_exists = db_session.query(existing_lobby.exists()).scalar()

    return new_code


def join_lobby(db_session, user_session, lobby_code):
    user = db_session.query(User).get(user_session["user_id"])

    if user.lobby is not None:
        raise Conflict("User is already in a lobby.")

    lobby = (
        db_session.query(Lobby)
        .filter(Lobby.code == lobby_code)
        .filter(Lobby.state == LOBBY_CONSTANTS["state"]["ready"])
    ).one_or_none()

    if lobby is None:
        raise NotFound(
            f"No lobby with code {lobby_code} was found."
        )

    if lobby.is_at_capacity():
        raise Conflict(
            f"Max number of {lobby.capacity} players exceeded."
        )

    user.lobby = lobby
    user_session["lobby_id"] = lobby.id

    return {
        "state": lobby.get_state(),
        "players": [player.name for player in lobby.players],
    }


def leave_lobby(db_session, user_session):
    user = db_session.query(User).get(user_session["user_id"])

    if user.lobby is None:
        raise NotFound("User is not in a lobby.")

    lobby = user.lobby
    user.lobby = None
    user_session.pop("lobby_id", None)
    user_session.pop("round_id", None)

    db_session.flush()

    lobby.clean_up_if_empty()

    return {"message": "Successfully left lobby."}


def get_lobby_status(db_session, user_session):
    if user_session.get("lobby_id", None) is None:
        raise NotFound("User is not in a lobby.")

    lobby_id = user_session["lobby_id"]
    lobby = db_session.query(Lobby).get(lobby_id)

    return {
        "state": lobby.get_state(),
        "players": [player.name for player in lobby.players],
    }


def start_game(db_session, user_session):
    if user_session.get("lobby_id", None) is not None:
        lobby_id = user_session["lobby_id"]
        lobby = db_session.query(Lobby).get(lobby_id)
    else:
        raise NotFound("User is not in a lobby.")

    if user_session.get("round_id", None) is not None:
        raise Conflict("User is already in a game.")

    if not len(lobby.players) > 2:
        raise Conflict("Lobby must have at least 2 players to start game.")

    new_round = lobby.start_new_game(db_session)

    user_session["round_id"] = new_round.id

    return {
        "round_id": new_round.id
    }
