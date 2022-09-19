from fastapi import WebSocket, WebSocketDisconnect, FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from server.singletons.webSocketConnectionManager import WebSocketConnectionManager
from server.routes import router as logs_router
import logging
import traceback

from server.stream_logs import read_logs_from_files

manager = WebSocketConnectionManager.get_ws_connection()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def catchall_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.log(logging.ERROR, e)
        msg = str(e)
        traceback.print_exc()
        return JSONResponse({'detail': msg, 'loc': 'generic exception handler'}, status_code=500)


app.include_router(logs_router, prefix='/logs', tags=["logs operations"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to lightweight logger backend application"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # token = websocket.headers['Sec-WebSocket-Protocol']
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logs = await read_logs_from_files(data['start_date'], data['end_date'], data['per_page'], data['page_no'])
            await manager.send_personal_message(logs, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
