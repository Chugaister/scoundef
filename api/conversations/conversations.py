from fastapi import APIRouter
from typing import List
from schemas.conversations import Conversation
from database.db import history

cnv_router = APIRouter()


@cnv_router.get("/")
async def get_all() -> List[Conversation]:
    return history

