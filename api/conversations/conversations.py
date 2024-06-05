from fastapi import APIRouter
from typing import List
from typing import Union
from schemas.conversations import Conversation
from schemas.exceptions import HTTPError
from database.db import history
from utils.exceptions import NotFoundException

cnv_router = APIRouter()


@cnv_router.get("/")
async def get_all() -> List[Conversation]:
    return history


@cnv_router.get("/last")
async def get_last() -> Union[Conversation, HTTPError]:
    if len(history) == 0:
        raise NotFoundException("Last conversation not found")
    return history[-1]

