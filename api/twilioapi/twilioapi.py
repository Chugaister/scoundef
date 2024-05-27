from fastapi import APIRouter
from fastapi import Form
from fastapi import Response
from aiohttp import ClientSession
from aiohttp import BasicAuth

from utils.config import config
from twilio.twiml.voice_response import VoiceResponse

tw_router = APIRouter()
NUMBER_TO_REDIRECT = "+380989602010"


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


@tw_router.get("/voice")
async def incoming():
    response = VoiceResponse()
    response.say("Hello! I am AI helper. Please, say who you are and provide a reason why are you calling mrs. Smith")
    response.gather(input='speech', action=f'{config.PUBLIC_URL}/api/twilio/gather', timeout=5)
    return Response(content=str(response), headers={"Content-Type": "text/xml"})


@tw_router.post("/gather")
async def gather(SpeechResult: str = Form(), CallSid: str = Form()) -> Response:
    print(SpeechResult)
    response = VoiceResponse()
    # feeding speech result to ai model
    ai_speech_response = "Okay, I got you. Provide more details"
    if "ACCEPT" in ai_speech_response:
        response.say("Thank you. You have passed the control. Redirecting to the target user")
        # response.dial(number=NUMBER_TO_REDIRECT)
        response.hangup()
    elif "DECLINE" in ai_speech_response:
        response.say("You have not passed the control. Good bye")
        response.hangup()
    else:
        response.say(ai_speech_response)
        response.gather(input='speech', action=f'{config.PUBLIC_URL}/api/twilio/gather', timeout=5)
    return Response(content=str(response), headers={"Content-Type": "text/xml"})
