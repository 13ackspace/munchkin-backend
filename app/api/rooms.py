from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from models.pydantic_models import RoomConnection
from services.connection_manager import ConnectionManager
from game.session import GameSession
import secrets, string

router = APIRouter()

rooms = {}  # e.g., {"ABC123": {"players": ["Alice"], "status": "waiting", ...}}
manager = ConnectionManager()
MIN_PLAYERS = 2
MAX_PLAYERS = 6



def generate_room_code(length=6):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))



@router.post("/create-room")
async def create_room(max_number_of_players: int):
    # Validate the max_number_of_players
    if max_number_of_players < MIN_PLAYERS or max_number_of_players > MAX_PLAYERS:
        raise HTTPException(status_code=400, detail=f"Invalid number of players. Must be between {MIN_PLAYERS} and {MAX_PLAYERS}")
    # Generate a unique room code
    code = generate_room_code()
    while code in rooms:
        code = generate_room_code()
    # Initialize the room state (e.g., waiting for players)
    rooms[code] = {
        "players": [],
        "status": "waiting",
        "ready_counter": 0,
        "max_number_of_players": max_number_of_players
        # Other room-specific data can go here
    }
    return {"room_code": code, "message": "Room created successfully"}



"""@router.post("/join-room")
async def join_room(join_request: RoomConnection):
    player_name = join_request.player_name
    room_code = join_request.room_code.upper()

    if room_code not in rooms:
       raise HTTPException(status_code=404, detail="Room not found")

    room = rooms[room_code]

    if player_name in room["players"]:
       raise HTTPException(status_code=400, detail="Player name already taken in this room")

    room["players"].append(player_name)

    return {"message": f"Player {player_name} joined room {room_code}", "room_code": room_code, "players": room["players"]}
"""
    
