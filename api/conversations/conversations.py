from fastapi import APIRouter
from typing import List
from schemas.conversations import Conversation
from database.db import history
from utils.exceptions import NotFoundException

cnv_router = APIRouter(tags=["Conversations"])


@cnv_router.get("/")
async def get_all() -> List[Conversation]:
    return history[::-1]


# @cnv_router.get("/live")
# async def get_live() -> Conversation:
#     if len(history) == 0 or history[-1]["status"] != "active":
#         raise NotFoundException("There are no active conversations")
#     return history[-1]
