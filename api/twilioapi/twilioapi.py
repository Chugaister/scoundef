from fastapi import APIRouter
from fastapi import Form
from fastapi import Response

from twilio.twiml.voice_response import VoiceResponse

tw_router = APIRouter()
NUMBER_TO_REDIRECT = "+380989602010"
HOSTNAME = "https://e483-193-56-151-249.ngrok-free.app"


@tw_router.get("/voice")
async def incoming():
    response = VoiceResponse()
    response.say("Hello! I am AI helper. Please, say who you are and provide a reason why are you calling mrs. Smith")
    response.dial(number=NUMBER_TO_REDIRECT)
    #response.gather(input='speech', action=f'{HOSTNAME}/api/twilio/gather', timeout=2)
    return Response(content=str(response), headers={"Content-Type": "text/xml"})


@tw_router.post("/gather")
async def gather(SpeechResult: str = Form(), CallSid: str = Form()) -> Response:
    print(SpeechResult)
    response = VoiceResponse()
    # feeding speech result to ai model
    ai_speech_response = "Okay, I got you. Provide more details"
    if "ACCEPT" in ai_speech_response:
        response.say("Thank you. You have passed the control. Redirecting to the target user")
        response.dial(number=NUMBER_TO_REDIRECT)
    elif "DECLINE" in ai_speech_response:
        response.say("You have not passed the control. Good bye")
        response.hangup()
    else:
        response.say(ai_speech_response)
        # response.gather(input='speech', action=f'{HOSTNAME}/api/twilio/gather', timeout=2)
    response.dial(number=NUMBER_TO_REDIRECT)
    return Response(content=str(response), headers={"Content-Type": "text/xml"})
