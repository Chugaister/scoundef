from fastapi import APIRouter
from fastapi import Form
from fastapi import Response
from aiohttp import ClientSession
from aiohttp import BasicAuth
from typing import Optional
from json import dumps
from asyncio import sleep
from asyncio import create_task

from aiconvers.factory import ConversationFactory
from aiconvers.claude import SystemAction
from aiconvers.claude import Conversation
from utils.config import config
from utils.wsmanager import manager
from utils.twcustom import CustomVoiceResponse
from database.db import data


tw_router = APIRouter(tags=["Twilio API"])


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
    response = CustomVoiceResponse()
    global conv_engine
    if From in data["trusted_group"]:
        text = "Redirecting to recipient. Please wait a moment"
        response.say(text)
        create_task(stream_ai_response(text))
        response.dial(data["recipient"])
        return Response(content=str(response), headers={"Content-Type": "text/xml"})
    if From == "anonymous" or From == "Anonymous":
        conv_engine = ConversationFactory.hidden(CallSid, From, To)
        action = f'{config.PUBLIC_URL}/api/twilio/gather_hidden'
    else:
        conv_engine = ConversationFactory.unknown(CallSid, From, To)
        action = f"{config.PUBLIC_URL}/api/twilio/gather_unknown"
    response.say(conv_engine.start_message)
    create_task(stream_ai_response(conv_engine.start_message))
    response.gather(
        action=action,
        partial_result_callback=f'{config.PUBLIC_URL}/api/twilio/partial_result',
        action_on_empty_result=f'{config.PUBLIC_URL}/api/twilio/no_input'
    )
    response.redirect(f"{config.PUBLIC_URL}/api/twilio/no_input")
    return Response(content=str(response), headers={"Content-Type": "text/xml"})


@tw_router.post("/gather_hidden")
async def gather_hidden(SpeechResult: str = Form(default=None), CallSid: str = Form()) -> Response:
    response = CustomVoiceResponse()
    current_response = await conv_engine.handle_user_input(SpeechResult)
    response.say(current_response)
    create_task(stream_ai_response(current_response))
    if conv_engine.system_action == SystemAction.accept:
        response.dial(number=data["recipient"])
    elif conv_engine.system_action == SystemAction.decline:
        response.dial(number=data["caretaker"])
    elif conv_engine.system_action == SystemAction.continue_:
        response.gather(
            action=f'{config.PUBLIC_URL}/api/twilio/gather_hidden',
            partial_result_callback=f'{config.PUBLIC_URL}/api/twilio/partial_result',
            action_on_empty_result=f'{config.PUBLIC_URL}/api/twilio/no_input'
        )
    return Response(content=str(response), headers={"Content-Type": "text/xml"})


@tw_router.post("/gather_unknown")
async def gather_unknown(SpeechResult: str = Form(default=None), CallSid: str = Form()) -> Response:
    response = CustomVoiceResponse()
    current_response = await conv_engine.handle_user_input(SpeechResult)
    response.say(current_response)
    create_task(stream_ai_response(current_response))
    if conv_engine.system_action == SystemAction.accept:
        response.dial(number=data["caretaker"])
        conv_engine.finish()
    elif conv_engine.system_action == SystemAction.decline:
        response.hangup()
        conv_engine.finish()
    elif conv_engine.system_action == SystemAction.continue_:
        response.gather(
            action=f'{config.PUBLIC_URL}/api/twilio/gather_unknown',
            partial_result_callback=f'{config.PUBLIC_URL}/api/twilio/partial_result',
            action_on_empty_result=f'{config.PUBLIC_URL}/api/twilio/no_input'
        )
    return Response(content=str(response), headers={"Content-Type": "text/xml"})


@tw_router.post("/no_input")
async def no_input() -> Response:
    response = CustomVoiceResponse()
    text = "I am sorry but I did not heard you. Good bye"
    response.say(text)
    create_task(stream_ai_response(text))
    response.hangup()
    conv_engine.finish()
    return Response(content=str(response), headers={"Content-Type": "text/xml"})


@tw_router.post("/partial_result")
async def get_partial_result(
        UnstableSpeechResult: Optional[str] = Form(default=None)
):
    partial_speech = {
        "from_": "user",
        "content": UnstableSpeechResult
    }
    if not UnstableSpeechResult:
        partial_speech = {
            "from_": "system",
            "content": "NEXTMESSAGE"
        }
    await manager.broadcast(dumps(partial_speech))


async def stream_ai_response(ai_response):
    UnstableSpeechResultList = []
    for word in ai_response.split():
        await sleep(0.5)
        UnstableSpeechResultList.append(word)
        partial_speech = {
            "from_": "assistant",
            "content": " ".join(UnstableSpeechResultList)
        }
        await manager.broadcast(dumps(partial_speech))

    await manager.broadcast(dumps({
        "from_": "system",
        "content": "NEXTMESSAGE"
    }))

