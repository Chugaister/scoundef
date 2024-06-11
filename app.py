from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api import api_router
from api.twilioapi.twilioapi import set_webhook
from sys import argv
from utils.ngrok_tunnel import create_tunnel
from utils.config import config
from utils.exceptions import CustomException


app = FastAPI()
app.include_router(api_router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


@app.on_event("startup")
async def on_startup() -> None:
    if len(argv) > 1 and argv[1] == "--local":
        config.PUBLIC_URL = create_tunnel(config.PORT)
    await set_webhook()
