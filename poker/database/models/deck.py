import random

from .. import db


SUIT = {
    "C": "Clubs",
    "D": "Diamonds",
    "H": "Hearts",
    "S": "Spades",
}


class Deck(db.Model):
    __tablename__ = "deck"
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"))
    cards = db.Column(db.ARRAY(db.Text), nullable=False)
    # psql arrays starts at 1, not 0.
    current_card_position = db.Column(db.Integer, nullable=False, default=1)

    @classmethod
    def get_new_deck(cls):
        cards = []
        for suit in SUIT.keys():
            for i in range(1, 14):
                cards.append(suit + str(i))

        random.shuffle(cards)

        return cls(cards=cards)

    def shuffle_cards(self):
        random.shuffle(self.cards)

        self.current_card_position = 1

    def get_card(self):
        # Offset the position to adjust for python arrays starting at 0 vs
        # psql arrays starting at 1.
        card_position = self.current_card_position - 1
        card = self.cards[card_position]

        self.current_card_position += 1

        return card
