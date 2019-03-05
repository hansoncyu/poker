from .. import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    display_name = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False)
