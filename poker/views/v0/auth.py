from flask import Blueprint, jsonify

from poker.database import db
from poker.lib.auth import (
    login_anonymous_user,
    register_user,
)
from poker.lib.validation import validate_body
from poker.validation_schemas.auth import (
    ANONYMOUS_LOGIN,
    REGISTER_USER,
)


auth_page = Blueprint("auth", __name__)


@auth_page.route("/register", methods=["POST"])
@validate_body(REGISTER_USER)
def register(request_data):
    resp = register_user(
        db.session,
        request_data["username"],
        request_data["password"],
        request_data["display_name"],
    )
    return jsonify(resp)


@auth_page.route("/login")
def login():
    return "logged in"


@auth_page.route("/anonymous_login", methods=["POST"])
@validate_body(ANONYMOUS_LOGIN)
def anonymous_login(request_data):
    resp = login_anonymous_user(
        db.session,
        request_data["display_name"],
    )
    return jsonify(resp)


@auth_page.route("/logout")
def logout():
    return "logged out"
