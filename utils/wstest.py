import asyncio
import websockets



async def test_websocket():
    uri = "ws://localhost:8080/api/conversations/stream"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, server!")
        while True:
            response = await websocket.recv()
            print(f"Received response: {response}")


asyncio.run(test_websocket())
