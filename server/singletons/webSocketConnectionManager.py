from collections import OrderedDict
from typing import List
from fastapi import WebSocket


class ManageLogs:
    def __init__(self, websocket=None, page_number=0):
        self.websocket_dict = {
            'websocket': websocket,
            'page_number': page_number
        }

    def __getitem__(self, key):
        return self.websocket_dict[key]

    def __setitem__(self, key, value):
        self.websocket_dict[key] = value


class WebSocketConnectionManager:
    __instance__ = None

    def __init__(self):
        if WebSocketConnectionManager.__instance__ is None:
            WebSocketConnectionManager.__instance__ = self
            self.active_connections: List[ManageLogs] = []

        else:
            raise Exception("only one instance of connection manager can be created")

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        _conn_dict = ManageLogs()
        _conn_dict.websocket_dict['websocket'] = websocket
        _conn_dict.websocket_dict['page_number'] = 0
        self.active_connections.append(_conn_dict)

        print(_conn_dict.websocket_dict, '#############')

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection['websocket'] == websocket:
                self.active_connections.remove(connection)
                break

    async def send_personal_message(self, message: str, conn):
        await conn['websocket'].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection['websocket'].send_text(message)

    @staticmethod
    def get_ws_connection() -> 'WebSocketConnectionManager':
        """ Static method to fetch the current instance.
       """
        if not WebSocketConnectionManager.__instance__:
            WebSocketConnectionManager()
        return WebSocketConnectionManager.__instance__
