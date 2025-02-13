from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic_models import JoinRoomRequest
from connection_manager import ConnectionManager

router = APIRouter()

rooms = {}  # e.g., {"ABC123": {"players": ["Alice"], "status": "waiting", ...}}
manager = ConnectionManager()

@router.post("/join-room")
async def join_room(join_request: JoinRoomRequest):
    room_code = join_request.room_code.upper()
    player_name = join_request.player_name

    if room_code not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")

    room = rooms[room_code]

    if player_name in room["players"]:
        raise HTTPException(status_code=400, detail="Player name already taken in this room")

    room["players"].append(player_name)

    await manager.broadcast(room_code, {"type": "player_joined", "player": player_name, "code": room_code})
    return {"message": f"Player {player_name} joined room {room_code}", "room_code": room_code, "players": room["players"]}
 
@router.websocket("/ws/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    await manager.connect(websocket, room_code)
    
