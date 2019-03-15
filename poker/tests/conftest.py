import pytest

from poker.app import create_app
from poker.database import db
from poker.database.models import (
    Lobby,
    Round,
    User,
)
from poker.database.models.lobby import LOBBY_CONSTANTS


TEST_DB_URI = "postgresql+psycopg2://hyu:password@127.0.0.1/poker_test"
INIT_MODEL = True


@pytest.fixture(autouse=True, scope="session")
def test_app():
    settings_override = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DB_URI,
    }

    app = create_app(settings_override)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(autouse=True, scope="session")
def test_db(test_app):
    if not INIT_MODEL:
        return db

    db.drop_all()
    db.create_all()

    return db


@pytest.fixture(scope="session")
def root_session(test_db):
    root_session = test_db.session
    root_session.begin_nested()
    yield root_session

    # Tear Down:
    root_session.rollback()


@pytest.fixture(scope="function", autouse=True)
def test_session(root_session):
    """Test database session"""
    session = root_session.begin_nested().session
    # you shouldn't commit this. We'll force it to flush instead
    session.commit = session.flush
    yield session

    # Tear Down:
    session.rollback()


@pytest.fixture(scope="session")
def test_user(root_session):
    test_user = User(display_name="root_test_user", is_anonymous=True)

    root_session.add(test_user)
    root_session.flush()

    return test_user


@pytest.fixture(scope="session")
def four_player_round(root_session, test_user):
    new_lobby = Lobby(state=LOBBY_CONSTANTS["state"]["ready"])

    for i in range(3):
        new_user = User(display_name=f"testing{i}", is_anonymous=True)
        new_user.lobby = new_lobby

    test_user.lobby = new_lobby

    root_session.add(new_lobby)
    new_lobby.start_new_game(root_session)
    root_session.flush()

    return new_lobby.round
