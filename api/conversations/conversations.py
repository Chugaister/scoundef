from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from typing import List
from schemas.conversations import Conversation
from database.db import history
from utils.wsmanager import manager

cnv_router = APIRouter(tags=["Conversations"])


@cnv_router.get("/")
async def get_all() -> List[Conversation]:
    return history[::-1]


@cnv_router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep the connection open
    except WebSocketDisconnect:
        manager.disconnect(websocket)
