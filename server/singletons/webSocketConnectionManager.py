from typing import List
from fastapi import WebSocket


class WebSocketConnectionManager:
    __instance__ = None

    def __init__(self):
        if WebSocketConnectionManager.__instance__ is None:
            WebSocketConnectionManager.__instance__ = self
            self.active_connections: List[WebSocket] = []

        else:
            raise Exception("only one instance of connection manager can be created")

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    def get_ws_connection() -> 'WebSocketConnectionManager':
        """ Static method to fetch the current instance.
       """
        if not WebSocketConnectionManager.__instance__:
            WebSocketConnectionManager()
        return WebSocketConnectionManager.__instance__
