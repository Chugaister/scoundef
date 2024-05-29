from fastapi import APIRouter
from fastapi import Form
from fastapi import Response
from aiohttp import ClientSession
from aiohttp import BasicAuth

from aiconvers.claude import get_processed_response
from utils.config import config
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream

tw_router = APIRouter()
NUMBER_TO_REDIRECT = "+380989602010" #TODO bro...


async def set_webhook() -> None:
    url = "https://api.twilio.com/2010-04-01/Accounts/{}/IncomingPhoneNumbers/{}.json".format(
        config.ACCOUNT_SID,
        config.PHONE_NUMBER_SID
    )
    data = {
        'VoiceUrl': f'{config.PUBLIC_URL}/api/twilio/voice'
        }
    async with ClientSession() as session:
        async with session.post(url, data=data, auth=BasicAuth(config.ACCOUNT_SID, config.AUTH_TOKEN)) as response:
            response_data = await response.json()
            if response.status >= 300:
                raise Exception(f"Failed to set webhook. {response_data}")


@tw_router.post("/voice")
async def incoming():
    response = VoiceResponse()
    response.say(
        "Hello! I am AI secretary. Please, say who you are and provide a reason why are you calling this number"
    )
    connect = Connect()
    stream = Stream(url=f'wss://{config.PUBLIC_IP}:{config.SOCKET_PORT}')
    connect.append(stream)
    response.append(connect)

    return Response(content=str(response), headers={"Content-Type": "text/xml"})

