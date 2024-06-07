from pydantic import BaseModel
from pydantic import Field


class EntityCreated(BaseModel):
    detail: str = Field(default="Entity created successfully")
