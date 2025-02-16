from pydantic import BaseModel

class RoomConnection(BaseModel):
    room_code: str
    player_name: str
    players: list[str] = []

class GameStatus(BaseModel):
    room_code: str
    players: list[str]
    current_player: int 
    current_card: dict [str, any]
    hand: list[dict[str, any]] 