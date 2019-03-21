from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from .. import db


class CastingArray(ARRAY):
    def bind_expression(self, bindvalue):
        return cast(bindvalue, self)


class GameEndScore(db.Model):
    __tablename__ = "game_end_score"
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"))
    users_and_hands = db.Column(CastingArray(JSONB))
    winnings = db.Column(CastingArray(JSONB))
