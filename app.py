from fastapi import FastAPI
from api import api_router
from api.twilioapi.twilioapi import set_webhook
from sys import argv
from utils.ngrok_tunnel import create_tunnel
from utils.config import config


app = FastAPI()
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def on_startup() -> None:
    if len(argv) > 1 and argv[1] == "--local":
        config.PUBLIC_URL = create_tunnel(config.PORT)
    await set_webhook()
