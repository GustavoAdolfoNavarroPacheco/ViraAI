from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Map chat_id (as string) to list of active WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: str):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)
        print(f"[WebSocket] Client connected to chat {chat_id}. Active: {len(self.active_connections[chat_id])}")

    def disconnect(self, websocket: WebSocket, chat_id: str):
        if chat_id in self.active_connections:
            if websocket in self.active_connections[chat_id]:
                self.active_connections[chat_id].remove(websocket)
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]
        print(f"[WebSocket] Client disconnected from chat {chat_id}.")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast_to_chat(self, message: dict, chat_id: str):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    # Connection might be closed, we will clean it up on disconnect,
                    # but let's log the error here
                    print(f"[WebSocket] Error broadcasting to connection in chat {chat_id}: {e}")

manager = ConnectionManager()
