from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import ValidationError
from models.pydantic_models import RoomConnection
from services.connection_manager import ConnectionManager
from rooms import rooms, router
import json

#TO DO limit the number of players in a room

manager = ConnectionManager()
STATUS = [{"not ready": False}, {"ready": True}]

@router.websocket("/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    await manager.connect(websocket, room_code)

    join_data = await websocket.receive_text()
    try:
        join_message = json.loads(join_data)
        nickname = join_message.get("nickname")
    except json.JSONDecodeError:
        await websocket.close(code=1003, reason="Invalid join message format")
        return

    if not nickname:
        await websocket.close(code=1008, reason="Nickname required")
        return
    
    if nickname in rooms[room_code]["players"]:
        await websocket.close(code=1008, reason="Nickname already taken")
        return
    
    # Now store the connection with the nickname
    rooms[room_code]["players"].append([{"nickname": nickname, "status": STATUS["not ready"]}])
    print(f"Player '{nickname}' joined room {room_code}")
    
    ready_status = await websocket.receive_text()
    if ready_status not in STATUS:
        await websocket.close(code=1008, reason="Invalid ready status")
        return
    rooms[room_code]["players"]["status"] = ready_status
    
    # Broadcast the player status to all players in the room

    # TO DO - start game when all players are ready
    # TO DO - handle game logic


