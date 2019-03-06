from flask import Blueprint, jsonify


lobby_page = Blueprint("lobby", __name__)


@lobby_page.route("/create", method=["GET"])
def create_lobby():
    return "lobby"
