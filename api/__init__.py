from fastapi import APIRouter

from api.twilioapi.twilioapi import tw_router
from api.conversations.conversations import cnv_router
from api.settings.settings import stng_router

api_router = APIRouter()
api_router.include_router(tw_router, prefix="/twilio")
api_router.include_router(cnv_router, prefix="/conversations")
api_router.include_router(stng_router, prefix="/settings")
