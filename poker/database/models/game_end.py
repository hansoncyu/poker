from sqlalchemy.dialects.postgresql import JSONB

from .. import db


class GameEndScore(db.Model):
    __tablename__ = "game_end_score"
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"))
    users_and_hands = db.Column(JSONB)
    winnings = db.Column(JSONB)
