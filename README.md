# Tegere AI assistant prototype

## Set up the project

* create python virtual environment
`python -m venv venv`

* activate it
`venv\Scripts\activate`

* install dependencies
`pip install -r requirements.txt`

* fill in .env file (including ngrok auth token)

* make file database/data.json and fill it as in data.json.example

* run the project `python main.py --local`

## WebSocket docs
Connect to `ws://{hostname}:{port}/api/conversations/stream`
or `wss://{hostname}:{port}/api/conversations/stream` (try both)

This websocket streams real time speech as from AI as from user including partial speech results.
It does not listen any messages from client.

Examples of messages to receive on FE side

From assistant

```json
{"from_": "assistant", "content": "Hello, I am AI secretary..."}
```

From user

```json
{"from_": "user", "content": "I am Dr. Jackson from NY Central..."}
```

System message that indicates that current message is completed and FE should expect new message
```json
{"from_": "system", "content": "NEXTMESSAGE"}
```