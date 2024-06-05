from enum import Enum
from anthropic import Anthropic
from utils.config import config
from database.db import history
from random import randint


class SystemAction(str, Enum):
    accept = "-ACCEPT-"
    decline = "-DECLINE-"
    continue_ = "-CONTINUE-"


class Conversation:

    client = Anthropic(
        api_key=config.ANTHROPIC_API_KEY,
    )

    def __init__(self, system_prompt: str, start_message: str, call_sid: str, from_: str, to_: str):
        self.history_dict = {
            "call_sid": call_sid,
            "from_": from_,
            "to_": to_,
            "status": "active",
            "threat": None,
            "messages": [
              {
                "from_": "assistant",
                "content": start_message
              }
            ]
        }
        history.append(self.history_dict)
        self.system_prompt = system_prompt
        self.start_message = start_message
        self.call_sid = call_sid
        self.from_ = from_
        self.to_ = to_
        self.messages = []
        self.system_action: SystemAction = SystemAction.continue_

    def _get_response(
            self,
            user_input: str
    ) -> str:
        new_user_message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_input
                }
            ]
        }
        self.messages.append(new_user_message)
        new_assistant_message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0,
            system=self.system_prompt,
            messages=self.messages
        )
        current_response = "".join(block.text for block in new_assistant_message.content)
        self.messages.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": current_response
                }
            ]
        })
        return current_response

    @staticmethod
    def define_system_action(current_response: str) -> SystemAction:
        if SystemAction.accept.name.swapcase() in current_response:
            return SystemAction.accept
        elif SystemAction.decline.name.swapcase() in current_response:
            return SystemAction.decline
        else:
            return SystemAction.continue_

    @staticmethod
    def _sanitize_response(current_response: str) -> str:
        current_response = current_response.replace(SystemAction.accept.name.swapcase(), "")
        current_response = current_response.replace(SystemAction.decline.name.swapcase(), "")
        current_response = current_response.strip()
        return current_response

    def handle_user_input(self, user_input: str) -> str:
        print("User:\n", user_input, "\n")
        self.history_dict["messages"].append({
            "from_": "user",
            "content": user_input
        })
        current_response = self._get_response(user_input)
        self.system_action = self.define_system_action(current_response)
        sanitised_response = self._sanitize_response(current_response)
        print("AI secretary:\n", current_response, "\n")
        self.history_dict["messages"].append({
            "from_": "assistant",
            "content": sanitised_response
        })
        return sanitised_response

    def finish(self):
        self.history_dict["status"] = "finished"
        self.history_dict["threat"] = randint(4, 7)
