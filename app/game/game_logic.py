
import random
from game import assets

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck


#number of players should be specified at the start of the game according to the number of players in lobby
def deal_initial_hands(deck, num_players, hand_size=7):
    hands = {i: [] for i in range(num_players)}
    for _ in range(hand_size):
        for i in range(num_players):
            hands[i].append(deck.pop())
    return hands, deck

def is_valid_move(current_card, played_card):
    # A move is valid if the card colors match, the values match, or the played card is wild.
    if played_card["value"] in assets.WILD_CARDS:
        return True
    if current_card["color"] == played_card["color"]:
        return True
    if current_card["value"] == played_card["value"]:
        return True
    return False

def apply_card_effect(played_card, session):
    """
    Modify the session based on the card's effect.
    For example:
      - If it's a Skip, move the turn forward an extra time.
      - If it's Reverse, reverse the order of play.
      - If it's Draw Two or Wild Draw Four, add cards to the next player's hand.
    """
    if played_card["value"] == "Skip":
        session.advance_turn(skip=True)
    elif played_card["value"] == "Reverse":
        session.reverse_play_order()
    elif played_card["value"] == "Draw Two":
        session.next_player_draw(2)
    elif played_card["value"] == "Wild Draw Four":
        session.next_player_draw(4)
    # Wild cards might also involve selecting a new color—handle that as needed.
