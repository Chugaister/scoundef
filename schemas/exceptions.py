from pydantic import BaseModel


class HTTPError(BaseModel):
    status_code: int
    detail: str