from .. import db

from poker.database.models import Deck


ROUND_CONSTANTS = {
    "state": {
        "preflop": 0,
        "flop": 1,
        "turn": 2,
        "river": 3,
        "ended": 4,
    }
}


class Round(db.Model):
    __tablename__ = "round"
    id = db.Column(db.Integer, primary_key=True)
    lobby_id = db.Column(db.Integer, db.ForeignKey("lobby.id"))
    state = db.Column(db.Integer, nullable=False, default=ROUND_CONSTANTS["state"]["preflop"])
    pot = db.Column(db.Integer, nullable=False, default=0)
    board = db.Column(db.ARRAY(db.Text))

    players = db.relationship("User", back_populates="round")
    deck = db.relationship("Deck", uselist=False)

    @property
    def current_player_turn(self):
        for player in self.players:
            if player.player_status.is_current_player:
                return player

    def get_state(self):
        for text, enum in ROUND_CONSTANTS["state"].items():
            if enum == self.state:
                return text

    def start_new_round(self, db_session, new_game=False):
        self.state = ROUND_CONSTANTS["state"]["preflop"]

        if new_game:
            new_deck = Deck.get_new_deck()
            self.deck = new_deck
        else:
            self.deck.shuffle_cards()

        db_session.flush()

        for player in self.players:
            new_hand = []
            new_hand.append(self.deck.get_card())
            new_hand.append(self.deck.get_card())

            player.player_status.hand = new_hand

    def deal_board(self, dealing_round):
        cards_to_deal = {
            "flop": 3,
            "turn": 1,
            "river": 1,
        }

        # New board for flop, otherwise append to existing board.
        if dealing_round == "flop":
            board = []

        for i in range(cards_to_deal[dealing_round]):
            board.append(self.deck.get_card())

        self.board = board
