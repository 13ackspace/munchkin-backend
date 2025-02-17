
# Define Uno card types and colors
COLORS = ["Red", "Green", "Blue", "Yellow"]
NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
SPECIALS = ["Skip", "Reverse", "Draw Two"]

# Wild cards (no color until played)
WILD_CARDS = ["Wild", "Wild Draw Four"]

def get_standard_deck():
    deck = []
    # Each color: one 0, two of each number 1-9, two of each special card
    for color in COLORS:
        deck.append({"color": color, "value": NUMBERS[0]})
        for number in NUMBERS[1:]:
            deck.extend([{"color": color, "value": number}] * 2)
        for special in SPECIALS:
            deck.extend([{"color": color, "value": special}] * 2)
        deck.extend([{"color": None, "value": wild} for wild in WILD_CARDS])
    return deck

deck = get_standard_deck()
for card in deck :
    print(card)