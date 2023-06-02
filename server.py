import asyncio

import websockets

from chat.chat_utils import send_message

PORT = 8766
start_server = websockets.serve(send_message, "localhost", PORT)
print(f"Server started at port {PORT}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
