from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from app.models.pydantic_models import RoomConnection
from app.services.connection_manager import ConnectionManager
import secrets, string

router = APIRouter()

rooms = {}  # e.g., {"ABC123": {"players": ["Alice"], "status": "waiting", ...}}
manager = ConnectionManager()



def generate_room_code(length=6):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))



@router.post("/create-room")
async def create_room():
    # Generate a unique room code
    code = generate_room_code()
    while code in rooms:
        code = generate_room_code()
    # Initialize the room state (e.g., waiting for players)
    rooms[code] = {
        "players": [],
        "status": "waiting",
        # Other room-specific data can go here
    }
    return {"room_code": code, "message": "Room created successfully"}



@router.post("/join-room")
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
 


@router.websocket("/{room_code}/{player_name}")
async def websocket_endpoint(websocket: WebSocket, player_name: str, room_code: str):
    await manager.connect(websocket, room_code)
    try:
        await manager.broadcast(room_code, {"player": player_name, "code": room_code, "players": rooms[room_code]["players"]})
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
            manager.disconnect(websocket, room_code)
    
