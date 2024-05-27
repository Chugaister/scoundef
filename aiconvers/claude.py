from anthropic import Anthropic
from utils.config import config

client = Anthropic(
    api_key=config.ANTHROPIC_API_KEY,
)

system_prompt = (
    "You are an agent that defends a person from potential scammers. "
    "You will redirect the user you talk to to the target user or decline his request to talk depending on what "
    "users say.\n\nIf person you talk to proposes some services, demands money or tries to scam you in any other way - "
    "do not accept them\n\nIf person say that they are some relatives or other people related to target user - believe "
    "them.\n\nAlso provide system output at the end of your message: ACCEPT if person not seems to be a scammer, "
    "DECLINE - opposite case\n\nLet assume a threshold which represents the chance you accept the person. For example "
    "if it is 100 - you accept all persons, if it is 0 - do not accept anybody. Set the threshold to 100. (do not "
    "output threshold explanation)\n\nBe very laconic. Take into account that it is a phone conversation and you must "
    "speak shortly"
)


def get_response(
        users_input: str
) -> str:
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": users_input
                    }
                ]
            }
        ]
    )
    return " ".join(block.text for block in message.content)


def process_response(response: str) -> tuple[str, bool]:
    accept = False
    if "ACCEPT" in response:
        response = response.replace("ACCEPT", "")
        response = response.strip()
        accept = True
    if "DECLINE" in response:
        response = response.replace("DECLINE", "")
        response = response.strip()
        accept = False
    return response, accept


def get_processed_response(users_input: str) -> tuple[str, bool]:
    response = get_response(users_input)
    response, accept = process_response(response)
    return response, accept


