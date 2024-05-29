from websockets import serve
from websockets.exceptions import ConnectionClosed
from utils.config import config
from asyncio import Future
from utils.config import config
from ssl import SSLContext, PROTOCOL_TLS_SERVER

async def handle_stream(websocket, path):
    print("Socket connection established.")
    try:
        async for message in websocket:
            #TODO feed message into stt
            await websocket.send(message)
    except ConnectionClosed:
        print("Socket connection closed.")


async def run_streamHandler():
    ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=config.SSL_CERTFILE_PATH, keyfile=config.SSL_KEYFILE_PATH)
    async with serve(handle_stream, config.HOST, config.SOCKET_PORT, ssl=ssl_context):
        print(f"WS server started")
        await Future() #will never actually complete
