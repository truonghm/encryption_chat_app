import asyncio
import json

import websockets

from encryption.encryption_utils import decrypt_message, encrypt_message

connected = {}

async def register(websocket):
    username = await websocket.recv()
    connected[username] = websocket


async def unregister(websocket):
    for user, ws in connected.items():
        if ws == websocket:
            del connected[user]
            break


async def send_message(websocket, path):
    # This is where we'll get the remote address (IP and port)
    remote_address = websocket.remote_address

    username = await websocket.recv()
    connected[username] = websocket

    print(f"A client has connected from {remote_address} with username {username}")

    try:
        async for message in websocket:
            data = json.loads(message)
            receiver_username = data[0]
            encrypted_message = data[1]
            hash_value = data[2]
            if receiver_username in connected:
                receiver_ws = connected[receiver_username]
                await receiver_ws.send(json.dumps([receiver_username, encrypted_message, hash_value]))
    finally:
        await unregister(websocket)
