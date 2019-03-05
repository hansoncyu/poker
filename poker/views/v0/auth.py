from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

from poker.database import db
from poker.lib.auth import (
    login_anonymous_user,
    register_user,
)


auth_page = Blueprint("auth", __name__)


@auth_page.route("/register", methods=["POST"])
def register():
    resp = register_user(
        db.session,
        request.form["username"],
        request.form["password"],
        request.form["display_name"],
    )
    return jsonify(resp)


@auth_page.route("/login")
def login():
    return "logged in"


@auth_page.route("/anonymous_login", methods=["POST"])
def anonymous_login():
    user = login_anonymous_user(
        db.session,
        request.form["display_name"],
    )
    return jsonify({
        "user_id": user.id,
        "display_name": user.display_name,
    })


@auth_page.route("/logout")
def logout():
    return "logged out"
