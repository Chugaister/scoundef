from json import load
from utils.config import config

data = {}


with open(config.DATA_FILE_PATH, "r", encoding="utf-8") as file:
    data = load(file)


history = [
    {
        "call_sid": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "from_": "+380000000000",
        "to_": "+10000000000",
        "threat": 4,
        "status": "finished",
        "messages": [
          {
            "from_": "assistant",
            "content": "Hello! I am AI secretary. Please, say who you are and provide a reason why are you calling this number. Note, that this call is being recorded"
          },
          {
            "from_": "user",
            "content": "Hello. I'm the the Dr. Jackson from New York Central Hospital. We have done your CT scans and we want to make an appointment. We have free slot on Friday at 3 p.m."
          },
          {
            "from_": "assistant",
            "content": "I'm sorry, but I don't have any information about CT scans or appointments at New York Central Hospital. Could you please provide more details about the patient you're trying to reach? I need to verify this information before proceeding."
          },
          {
            "from_": "user",
            "content": "I want to contact with Mrs. Anna Barker. It is very urgent call. Her health is under the risk."
          },
          {
            "from_": "assistant",
            "content": "I apologize, but I cannot provide any personal information about Mrs. Anna Smith or connect you with her directly. If this is a genuine urgent medical matter, please contact her or her family through official channels. I hope you understand.\n\n--"
          }
        ]
    },
    {
        "call_sid": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "from_": "+380000000000",
        "to_": "+10000000000",
        "threat": 4,
        "status": "finished",
        "messages": [
          {
            "from_": "assistant",
            "content": "Hello! I am AI secretary. Please, say who you are and provide a reason why are you calling this number. Note, that this call is being recorded"
          },
          {
            "from_": "user",
            "content": "Hello. I'm the the Dr. Jackson from New York Central Hospital. We have done your CT scans and we want to make an appointment. We have free slot on Friday at 3 p.m."
          },
          {
            "from_": "assistant",
            "content": "I'm sorry, but I don't have any information about CT scans or appointments at New York Central Hospital. Could you please provide more details about the patient you're trying to reach? I need to verify this information before proceeding."
          },
          {
            "from_": "user",
            "content": "I want to contact with Mrs. Anna Barker. It is very urgent call. Her health is under the risk."
          },
          {
            "from_": "assistant",
            "content": "I apologize, but I cannot provide any personal information about Mrs. Anna Smith or connect you with her directly. If this is a genuine urgent medical matter, please contact her or her family through official channels. I hope you understand.\n\n--"
          }
        ]
    },
    {
        "call_sid": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "from_": "+380000000000",
        "to_": "+10000000000",
        "threat": 4,
        "status": "finished",
        "messages": [
          {
            "from_": "assistant",
            "content": "Hello! I am AI secretary. Please, say who you are and provide a reason why are you calling this number. Note, that this call is being recorded"
          },
          {
            "from_": "user",
            "content": "Hello. I'm the the Dr. Jackson from New York Central Hospital. We have done your CT scans and we want to make an appointment. We have free slot on Friday at 3 p.m."
          },
          {
            "from_": "assistant",
            "content": "I'm sorry, but I don't have any information about CT scans or appointments at New York Central Hospital. Could you please provide more details about the patient you're trying to reach? I need to verify this information before proceeding."
          },
          {
            "from_": "user",
            "content": "I want to contact with Mrs. Anna Barker. It is very urgent call. Her health is under the risk."
          },
          {
            "from_": "assistant",
            "content": "I apologize, but I cannot provide any personal information about Mrs. Anna Smith or connect you with her directly. If this is a genuine urgent medical matter, please contact her or her family through official channels. I hope you understand.\n\n--"
          }
        ]
    },
]

