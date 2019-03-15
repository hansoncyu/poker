from .. import db


PLAYER_STATUS_CONSTANTS = {
    "action": {
        "check": 0,
        "bet": 1,
        "fold": 2,
        "raise": 3,
        "call": 4,
    },
}


class PlayerStatus(db.Model):
    __tablename__ = "player_status"
    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.Integer, nullable=False)
    in_round = db.Column(db.Boolean, nullable=False)
    bet = db.Column(db.Integer)
    last_action = db.Column(db.Integer)
    is_current_player = db.Column(db.Boolean, nullable=False, default=False)
    player_turn = db.Column(db.Integer)
    hand = db.Column(db.ARRAY(db.Text))
    blind = db.Column(db.Text)
