import random

from .. import db
from .round import Round


LOBBY_CONSTANTS = {
    "state": {
        "ready": 0,
        "ingame": 1,
        "ended": 2,
    },
    "max_players": 6,
}


class Lobby(db.Model):
    __tablename__ = "lobby"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer, nullable=False)
    code = db.Column(db.Text, index=True)

    players = db.relationship("User", back_populates="lobby")
    round = db.relationship("Round", uselist=False)

    def is_at_capacity(self):
        return len(self.players) >= self.capacity

    @property
    def capacity(self):
        return LOBBY_CONSTANTS["max_players"]

    def get_state(self):
        for text, enum in LOBBY_CONSTANTS["state"].items():
            if enum == self.state:
                return text

    def clean_up_if_empty(self):
        if len(self.players) == 0:
            self.state = LOBBY_CONSTANTS["state"]["ended"]

    def start_new_game(self, db_session):
        self.state = LOBBY_CONSTANTS["state"]["ingame"]

        new_round = Round(lobby_id=self.id)
        new_round.players = self.players

        for player in self.players:
            player.initialize_player_status()

        self.assign_player_order()

        new_round.start_new_round(db_session, new_game=True)
        self.round = new_round
        db_session.flush()

        return new_round

    def assign_player_order(self):
        random.shuffle(self.players)

        for order, player in enumerate(self.players):
            player.player_status.player_turn = order
            if order == 0:
                player.player_status.is_current_player = True
            if order == len(self.players) - 1:
                player.player_status.blind = "big"
            # In 2 player game, first player will be current player
            # and small blind.
            if order == len(self.players) - 2:
                player.player_status.blind = "small"
