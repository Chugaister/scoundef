from fastapi import APIRouter, Form, Response
from aiohttp import ClientSession, BasicAuth
from utils.config import config
from twilio.twiml.voice_response import VoiceResponse, Gather

tw_router = APIRouter()
NUMBER_TO_REDIRECT = "+380989602010"

async def set_webhook() -> None:
    url = f"https://api.twilio.com/2010-04-01/Accounts/{config.ACCOUNT_SID}/IncomingPhoneNumbers/{config.PHONE_NUMBER_SID}.json"
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
    gather = Gather(input='speech', action=f'{config.PUBLIC_URL}/api/twilio/gather', timeout=5)
    gather.say("Hello! I am AI helper. Please, say who you are and provide a reason why you are calling Mrs. Smith.")
    response.append(gather)
    response.redirect(f'{config.PUBLIC_URL}/api/twilio/voice')
    return Response(content=str(response), media_type="application/xml")

@tw_router.post("/gather")
async def gather(SpeechResult: str = Form(), CallSid: str = Form()) -> Response:
    print("Speech Result:", SpeechResult)
    response = VoiceResponse()
    # feeding speech result to AI model
    ai_speech_response = "Okay, I got you. Provide more details."
    if SpeechResult:
        # If speech was recognized, process the input
        if "ACCEPT" in ai_speech_response:
            response.say("Thank you. You have passed the control. Redirecting to the target user.")
            response.dial(NUMBER_TO_REDIRECT)
        elif "DECLINE" in ai_speech_response:
            response.say("You have not passed the control. Goodbye.")
            response.hangup()
        else:
            response.say(ai_speech_response)
            gather = Gather(input='speech', action=f'{config.PUBLIC_URL}/api/twilio/gather', timeout=5)
            response.append(gather)
    else:
        # If no speech was recognized, prompt the user to try again
        response.say("I'm sorry, I didn't catch that. Please try again.")
        gather = Gather(input='speech', action=f'{config.PUBLIC_URL}/api/twilio/gather', timeout=5)
        response.append(gather)
    return Response(content=str(response), media_type="application/xml")


