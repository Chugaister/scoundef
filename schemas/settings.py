from pydantic import BaseModel


class PhoneNumber(BaseModel):
    phone_number: str

