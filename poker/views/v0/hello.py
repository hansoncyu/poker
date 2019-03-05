from flask import Blueprint

hello_page = Blueprint("hello", __name__)


@hello_page.route("/")
def hello_world():
    return "hello world"
