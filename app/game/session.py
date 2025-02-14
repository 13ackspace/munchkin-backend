# app/game/session.py
from app.game import assets, game_logic

class GameSession:
    def __init__(self, room_code, players):
        self.room_code = room_code
        self.players = players  # List of player nicknames or IDs
        self.deck = game_logic.shuffle_deck(assets.get_standard_deck())
        self.hands, self.deck = game_logic.deal_initial_hands(self.deck, len(players))
        self.discard_pile = []
        self.current_turn = 0  # Index into self.players
        self.play_direction = 1  # 1 for clockwise, -1 for counter-clockwise

        # Start the game by drawing the first card from the deck to the discard pile.
        self.current_card = self.deck.pop()
        self.discard_pile.append(self.current_card)

    def advance_turn(self, skip=False):
        # Calculate next turn based on play direction.
        step = 2 if skip else 1
        self.current_turn = (self.current_turn + step * self.play_direction) % len(self.players)

    def reverse_play_order(self):
        self.play_direction *= -1

    def next_player_draw(self, num_cards):
        next_turn = (self.current_turn + self.play_direction) % len(self.players)
        # Ensure there are enough cards in the deck; if not, reshuffle the discard pile.
        drawn_cards = []
        for _ in range(num_cards):
            if not self.deck:
                self.reshuffle_discard_into_deck()
            drawn_cards.append(self.deck.pop())
        self.hands[next_turn].extend(drawn_cards)

    def reshuffle_discard_into_deck(self):
        # Leave the top card in the discard pile, shuffle the rest, and set as new deck.
        top_card = self.discard_pile.pop()
        self.deck = game_logic.shuffle_deck(self.discard_pile)
        self.discard_pile = [top_card]

    def play_card(self, player_index, card):
        # Check if the move is valid.
        if not game_logic.is_valid_move(self.current_card, card):
            raise ValueError("Invalid move")
        # Remove card from player's hand.
        try:
            self.hands[player_index].remove(card)
        except ValueError:
            raise ValueError("Player does not have that card")
        # Place card on the discard pile and update the current card.
        self.discard_pile.append(card)
        self.current_card = card
        # Apply card effect if any.
        game_logic.apply_card_effect(card, self)
        # Check win condition (e.g., no cards left)
        if not self.hands[player_index]:
            return f"Player {self.players[player_index]} wins!"
        # Return current game state for further processing
        return self.get_state()

    def get_state(self):
        # Return a summary of the game state for front-end updates.
        return {
            "room_code": self.room_code,
            "players": self.players,
            "current_turn": self.players[self.current_turn],
            "current_card": self.current_card,
            "hands_count": {player: len(hand) for player, hand in zip(self.players, self.hands.values())},
            # Optionally include more details as needed.
        }
