from fastapi import APIRouter
from fastapi import Form
from fastapi import Response
from aiohttp import ClientSession
from aiohttp import BasicAuth

from aiconvers.factory import ConversationFactory
from aiconvers.claude import SystemAction
from aiconvers.claude import Conversation
from utils.config import config
from twilio.twiml.voice_response import VoiceResponse
from database.db import data


tw_router = APIRouter()


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


conv_engine: Conversation | None = None


@tw_router.post("/voice")
async def voice(
        From: str = Form(),
        To: str = Form(),
        CallSid: str = Form()
):
    response = VoiceResponse()
    if From in data["trusted_group"]:
        response.say("Redirecting to recipient. Please wait a moment")
        response.dial(data["recipient"])
        return Response(content=str(response), headers={"Content-Type": "text/xml"})
    if From == "hidden":
        pass
        # conv_engine = ConversationFactory.hidden(CallSid)
        # response.say(conv_engine.start_message)
        # response.gather(input='speech', action=f'{config.PUBLIC_URL}/api/twilio/gather_hidden', timeout=2)
        # return Response(content=str(response), headers={"Content-Type": "text/xml"})
    else:
        global conv_engine
        conv_engine = ConversationFactory.unknown(CallSid, From, To)
        response.say(conv_engine.start_message)
        response.gather(input='speech', action=f'{config.PUBLIC_URL}/api/twilio/gather_unknown', timeout=2)
        return Response(content=str(response), headers={"Content-Type": "text/xml"})


@tw_router.post("/gather_hidden")
async def gather_hidden(SpeechResult: str = Form(), CallSid: str = Form()) -> Response:
    response = VoiceResponse()
    current_response = conv_engine.handle_user_input(SpeechResult)
    response.say(current_response)
    if conv_engine.system_action == SystemAction.accept:
        response.dial(number=data["caretaker"])
    elif conv_engine.system_action == SystemAction.decline:
        response.dial(number=data["caretaker"])
    elif conv_engine.system_action == SystemAction.accept:
        response.gather(input='speech', action=f'{config.PUBLIC_URL}/api/twilio/gather', timeout=2)
    return Response(content=str(response), headers={"Content-Type": "text/xml"})


@tw_router.post("/gather_unknown")
async def gather_unknown(SpeechResult: str = Form(), CallSid: str = Form()) -> Response:
    response = VoiceResponse()
    current_response = conv_engine.handle_user_input(SpeechResult)
    response.say(current_response)
    if conv_engine.system_action == SystemAction.accept:
        response.dial(number=data["recipient"])
        conv_engine.finish()
    elif conv_engine.system_action == SystemAction.decline:
        response.dial(number=data["recipient"])
        conv_engine.finish()
    elif conv_engine.system_action == SystemAction.continue_:
        response.gather(input='speech', action=f'{config.PUBLIC_URL}/api/twilio/gather_unknown', timeout=2)
    return Response(content=str(response), headers={"Content-Type": "text/xml"})
