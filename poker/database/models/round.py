from .. import db

from poker.database.models import Deck, GameEndScore
from poker.database.models.user import OutOfMoney
from poker.lib.hand_scoring import (
    get_best_hand_and_rank,
    get_winners_from_hands,
)


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
    game_end_score = db.relationship("GameEndScore", order_by=GameEndScore.id.desc())

    @property
    def current_player_turn(self):
        current_player = filter(
            lambda player: player.player_status.is_current_player,
            self.players,
        )
        current_player = list(current_player)
        # There shouldn't be more than one player marked as current player.
        assert len(current_player) == 1

        return current_player[0]

    @property
    def last_game_end_score(self):
        return self.game_end_score[0]

    def get_state(self):
        for text, enum in ROUND_CONSTANTS["state"].items():
            if enum == self.state:
                return text

    def start_new_round(self, db_session, new_game=False):
        self.board = []
        self.pot = 0
        self.state = ROUND_CONSTANTS["state"]["preflop"]

        if new_game:
            self.deck = Deck.get_new_deck()
            self.game_end_score.append(GameEndScore())
        else:
            self.deck.shuffle_cards()
            self._change_blinds()
            self.assign_new_round_starting_player()

        db_session.flush()

        self.deal_blinds()

        # deal hand
        for player in self.players:
            if player.is_in_game:
                new_hand = []
                new_hand.append(self.deck.get_card())
                new_hand.append(self.deck.get_card())

                player.player_status.hand = new_hand
            else:
                player.player_status.is_in_round = False

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

    def go_to_next_player(self, folded_player=None):
        # Make a copy of the round's players and order them by player turn.
        player_order = self.players[:]
        player_order = filter(
            lambda player: player.is_in_game and player.player_status.in_round,
            player_order,
        )
        player_order = list(player_order)
        if folded_player is not None:
            player_order.append(folded_player)
        player_order.sort(key=lambda player: player.player_status.player_turn)

        current_player_val = False
        next_player_val = False
        for player in player_order:
            next_player_val = player.player_status.is_current_player
            player.player_status.is_current_player = current_player_val
            if player.player_status.is_current_player:
                return player

            current_player_val = next_player_val
            next_player_val = False

        if current_player_val:
            player_order[0].player_status.is_current_player = current_player_val
            return player_order[0]

        raise Exception("Couldn't find next player.")

    @property
    def current_bet(self):
        bets = [
            player.player_status.bet for player in self.players
            if player.player_status.bet is not None
        ]
        if bets:
            return max(bets)
        else:
            return 0

    def deal_blinds(self):
        SMALL_BLIND = 5
        BIG_BLIND = 10

        for player in self.players:
            if player.player_status.blind == "small":
                try:
                    player.place_bet(SMALL_BLIND, self.pot)
                except OutOfMoney:
                    player.place_bet(player.money, self.pot)

            elif player.player_status.blind == "big":
                try:
                    player.place_bet(BIG_BLIND, self.pot)
                except OutOfMoney:
                    player.place_bet(player.money, self.pot)

    def check_for_round_end(self):
        everyone_has_bet = True

        for player in self.players:
            if player.player_status.bet != 0 and \
                    player.player_status.bet != self.current_bet:
                everyone_has_bet = False

        return everyone_has_bet

    def _change_blinds(self):
        # Make a copy of the round's players and order them by player turn.
        player_order = self.players[:]
        player_order = filter(lambda player: player.is_in_game, player_order)
        player_order = list(player_order)
        player_order.sort(key=lambda player: player.player_status.player_turn)

        current_blind_val = None
        next_blind_val = None
        for player in player_order:
            next_blind_val = player.player_status.blind
            player.player_status.blind = current_blind_val

            current_blind_val = next_blind_val
            next_blind_val = None

        if current_blind_val is not None:
            player_order[0].player_status.blind = current_blind_val

    def check_for_game_end(self):
        players_in_round = 0
        everyone_has_bet = True

        for player in self.players:
            if player.player_status.in_round:
                players_in_round += 1
            if player.player_status.bet != 0 and \
                    player.player_status.bet != self.current_bet:
                everyone_has_bet = False

        if players_in_round == 1:
            return True

        if everyone_has_bet and self.state == ROUND_CONSTANTS["state"]["river"]:
            return True

        return False

    def start_next_phase(self):
        self.state += 1

        for player in self.players:
            player.player_status.bet = None
            player.player_status.last_action = None

        self.deal_board(self.get_state())
        self.assign_new_round_starting_player()

    def assign_new_round_starting_player(self):
        # Set the current player as the big blind and then find the next
        # available player.
        for player in self.players:
            if player.player_status.blind == "big":
                player.player_status.is_current_player = True
            else:
                player.player_status.is_current_player = False

        self.go_to_next_player()

    def score_round(self):
        players_to_score = self.players[:]
        players_to_score = filter(lambda player: player.player_status.is_in_round)
        player_to_score = list(players_to_score)

        if len(player_to_score) == 1:
            self.award_winners([players_to_score[0]])

        player_hand_and_rankings = get_best_hand_and_rank(players_to_score, self.board)
        winners_and_hands = get_winners_from_hands(player_hand_and_rankings)
        winners = [item[0] for item in winners_and_hands]

        winnings = self.award_winners(winners)
        self._update_game_end_score(player_hand_and_rankings, winnings)

    def award_winners(self, winners):
        winnings = []
        split_pot = self.pot // len(winners)

        for player in winners:
            winnings.append([player, split_pot])

        remainder = self.pot % len(winners)
        for i in range(remainder):
            player_winning = winnings[i]
            player_winning[1] += 1

        for player_winning in winnings:
            player_winning[0].player_status.money += player_winning[1]

        return winnings

    def _update_game_end_score(self, player_hand_and_rankings, winnings):
        winnings_jsonb_list = []
        for player, winning in winnings:
            winnings_jsonb_list .append({
                "player_id": player.id,
                "winning": winning,
            })
        self.last_game_end_score.winnings = winnings_jsonb_list

        users_and_hands_jsonb_list = []
        for player, hand, ranking in player_hand_and_rankings:
            users_and_hands_jsonb_list.append({
                "player_id": player.id,
                "hand": hand,
                "hand_rank": ranking,
            })
        self.last_game_end_score.users_and_hands = users_and_hands_jsonb_list
