from fastapi import APIRouter

from api.twilioapi.twilioapi import tw_router

api_router = APIRouter()
api_router.include_router(tw_router, prefix="/twilio")