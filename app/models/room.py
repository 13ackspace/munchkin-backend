
class Room:
    def __init__(self, max_players: int):
        self.status = "waiting"
        self.ready_counter = 0
        self.max_players = max_players
        self.players = {}  # Using a dict for players

    def add_player(self, nickname: str):
        if nickname in self.players:
            raise ValueError("Nickname already taken")
        self.players[nickname] = {"ready_status": False}
    
    def update_ready_status(self, nickname: str, status: bool):
        if nickname not in self.players:
            raise ValueError("Player not found")
        self.players[nickname]["ready_status"] = status
        # Update ready_counter if needed, etc.
