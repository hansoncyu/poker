from passlib.context import CryptContext

from poker.database.models.user import User

PWD_CONTEXT = CryptContext(
    schemes=["pbkdf2_sha256"],
)


def register_user(session, username, password):
    if session.query(User).filter(User.username == username).one_or_none():
        return {"error": "Username already taken."}

    new_user = User(
        username=username,
        password=PWD_CONTEXT.hash(password),
    )

    session.add(new_user)

    return new_user


def login_anonymous_user(session, display_name):
    new_user = User(is_anonymous=True, display_name=display_name)

    session.add(new_user)
    session.flush()

    return new_user
