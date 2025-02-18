from fastapi import WebSocket
from typing import Dict, List
from models.pydantic_models import RoomConnection

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[tuple[WebSocket, str]]] = {}

    async def connect(self, websocket: WebSocket, room_code: str):
        await websocket.accept()
        if room_code not in self.active_connections:
            self.active_connections[room_code] = []
        self.active_connections[room_code].append(websocket)

    def disconnect(self, websocket: WebSocket, room_code: str):
        self.active_connections[room_code].remove(websocket)
        if not self.active_connections[room_code]:
            del self.active_connections[room_code]

    async def broadcast(self, room_code: str, message: any):
        if room_code in self.active_connections:
            for connection in self.active_connections[room_code]:
                await connection.send_JSON(message)
