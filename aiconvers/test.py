from aiconvers.claude import Conversation
from aiconvers.claude import SystemAction
eng = Conversation("123456")

while True:
    user_input = input("> ")
    print(eng.handle_user_input(user_input))
    print(eng.system_action)
    if eng.system_action != SystemAction.continue_:
        break

