from fastapi import APIRouter
from typing import List
from schemas.settings import PhoneNumber
from schemas.common import EntityCreated

from database.db import data

stng_router = APIRouter(tags=["Settings"])


@stng_router.post("/allowed_list")
async def add_number_to_whitelist(
    phone_number_request: PhoneNumber
) -> EntityCreated:
    data["allowed_list"].append(phone_number_request.phone_number)
    return EntityCreated()


@stng_router.get("/allowed_list")
async def get_allowed_list_numbers(

) -> List[PhoneNumber]:
    return [PhoneNumber(phone_number=phone_number) for phone_number in data["allowed_list"]]


@stng_router.post("/trusted_group")
async def add_number_to_trusted_group(
    phone_number_request: PhoneNumber
) -> EntityCreated:
    data["trusted_group"].append(phone_number_request.phone_number)
    return EntityCreated()


@stng_router.get("/trusted_group")
async def get_trusted_group_numbers(

) -> List[PhoneNumber]:
    return [PhoneNumber(phone_number=phone_number) for phone_number in data["trusted_group"]]


@stng_router.get("/public")
async def get_public_number() -> PhoneNumber:
    return PhoneNumber(phone_number=data["public_number"])


@stng_router.get("/caretaker")
async def get_public_number() -> PhoneNumber:
    return PhoneNumber(phone_number=data["caretaker"])


@stng_router.get("/recipient")
async def get_public_number() -> PhoneNumber:
    return PhoneNumber(phone_number=data["recipient"])
