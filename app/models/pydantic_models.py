from pydantic import BaseModel

class RoomConnection(BaseModel):
    room_code: str
    player_name: str
    players : list[str] = []
