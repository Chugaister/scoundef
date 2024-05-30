from pydantic import BaseModel
from typing import List
from typing import Optional
from enum import Enum


class MessageFrom(str, Enum):
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    from_: MessageFrom
    content: str


class ConversationStatus(str, Enum):
    active = "active"
    finished = "finished"


class Conversation(BaseModel):
    call_sid: str
    from_: str
    to_: str
    threat: Optional[int]
    status: ConversationStatus
    messages: List[Message]
