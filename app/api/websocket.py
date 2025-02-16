from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import ValidationError
from models.pydantic_models import RoomConnection
from services.connection_manager import ConnectionManager
from rooms import rooms, router

manager = ConnectionManager()

@router.websocket("/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, player_name: str):
    await manager.connect(websocket, room_code)
    try:
        RoomConnection.model.validate_json = await websocket.receive_JSON()
    except ValidationError as e:
        await websocket.send_json({"error": e.errors()})
        return