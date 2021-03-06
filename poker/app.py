from os import path

from flask import Flask
from flask_session import Session
import yaml


def create_app(settings_override=None, drop_create_db=False):
    app = Flask(__name__)

    config_path = path.join(app.root_path, "..", "config/poker.yml")
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        app.config.update(config["db"])
        app.config.update(config["session"])
    # for debug environment to hit error handlers
    app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False

    if settings_override:
        app.config.update(settings_override)

    from poker.database import db
    from poker.database import models

    db.init_app(app)

    sess = Session()
    sess.init_app(app)

    if drop_create_db:
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.session_interface.db.create_all()

    @app.route("/")
    def index():
        return "Welcome to Hanson's poker API!"

    @app.errorhandler(Exception)
    def rollback_database(exception):
        try:
            db.session.rollback()
        except Exception:
            pass

        return exception

    @app.teardown_request
    def database_cleanup(exception):
        try:
            db.session.commit()
        except Exception:
            pass

    configure_blueprints(app)

    return app


def configure_blueprints(app):
    from poker.views import v0
    API_VERSION = "v0"

    name_to_blueprint = {
        "auth": v0.auth_page,
        "lobby": v0.lobby_page,
        "round": v0.round_page,
    }
    for name, blueprint in name_to_blueprint.items():
        app.register_blueprint(blueprint, url_prefix="/api/{}/{}".format(API_VERSION, name))


if __name__ == "__main__":
    app = create_app()
    app.run()
