from passlib.context import CryptContext
from werkzeug.exceptions import Unauthorized

from poker.database.models.user import User

PWD_CONTEXT = CryptContext(
    schemes=["pbkdf2_sha256"],
)


def register_user(db_session, username, password, display_name):
    if db_session.query(User).filter(User.username == username).one_or_none():
        return {"error": "Username already taken."}

    new_user = User(
        username=username,
        password=PWD_CONTEXT.hash(password),
        display_name=display_name,
    )

    db_session.add(new_user)
    db_session.flush()

    return {
        "username": new_user.username,
        "display_name": new_user.name,
    }


def login_anonymous_user(db_session, user_session, display_name):
    if user_session.get("user_id", False):
        return {"message": "User is already logged in."}

    new_user = User(is_anonymous=True, display_name=display_name)

    db_session.add(new_user)
    db_session.flush()

    user_session["user_id"] = new_user.id

    if not new_user.display_name:
        new_user.display_name = "anon_{}".format(new_user.id)

    return {
        "display_name": new_user.name,
    }


def login_user(db_session, user_session, username, password):
    if user_session.get("user_id", False):
        return {"message": "User is already logged in."}

    user = db_session.query(User).filter(User.username == username).one_or_none()

    if user is None or not PWD_CONTEXT.verify(password, user.password):
        raise Unauthorized()

    refresh_user_session(user_session, user)

    return {
        "username": user.username,
        "display_name": user.name,
    }


def refresh_user_session(user_session, user):
    user_session["user_id"] = user.id
    user_session["lobby_id"] = user.lobby.id


def logout_user(user_session):
    if not user_session.get("user_id", False):
        return {"message": "Not logged in."}

    user_session.clear()

    return {
        "message": "User successfully logged out.",
    }
