from .. import db
from .player_status import PlayerStatus


class OutOfMoney(Exception):
    pass


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    display_name = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False)
    lobby_id = db.Column(db.Integer, db.ForeignKey("lobby.id"))
    player_status_id = db.Column(db.Integer, db.ForeignKey("player_status.id"))
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"))

    lobby = db.relationship("Lobby", back_populates="players")
    round = db.relationship("Round", back_populates="players")
    player_status = db.relationship("PlayerStatus")

    @property
    def name(self):
        return self.display_name or self.username

    @property
    def is_in_game(self):
        return self.player_status.money > 0

    def initialize_player_status(self):
        self.player_status = PlayerStatus(money=500, in_round=True)

    def place_bet(self, amount, round_pot):
        if self.player_status.bet is None:
            self.player_status.bet = 0
        self.player_status.bet += amount
        self.player_status.money -= amount
        round_pot += amount

        if self.player_status.money < 0:
            raise OutOfMoney()
