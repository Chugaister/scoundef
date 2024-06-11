from pydantic import BaseModel
from pydantic import Field
from typing import List
from typing import Optional
from enum import Enum
from datetime import datetime


class MessageFrom(str, Enum):
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    from_: MessageFrom
    content: str


class ConversationStatus(str, Enum):
    active = "active"
    finished = "finished"


class Group(str, Enum):
    trusted_group = "trusted_group"
    allowed_list = "allowed_list"
    hidden = "hidden"
    unknown = "unknown"


class Conversation(BaseModel):
    call_sid: str
    from_: str
    to_: str
    group: Group
    timestamp: datetime
    threat: Optional[int]
    status: ConversationStatus
    messages: List[Message]
