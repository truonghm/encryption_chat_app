import argparse
import asyncio
import json
import sys

import aioconsole
import aiomonitor
import websockets
from cryptography.hazmat.primitives import serialization

from encryption.encryption_utils import decrypt_message, encrypt_message, hash_message

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-e",
    "--encrypt",
    type=bool,
    default=True,
    help="Enable asymmetric encryption",
    action=argparse.BooleanOptionalAction
)

parser.add_argument(
    "-p",
    "--server-port",
    type=int,
    default=8766,
    help="Port of server",
)


args = parser.parse_args()

URI = f"ws://localhost:{args.server_port}"


def load_private_key(username):
    with open(f'{username}_private_key.pem', 'r') as file:
        pem = file.read().encode('utf-8')

    return serialization.load_pem_private_key(
        pem,
        password=None,
    )

def load_public_key(path_to_public_key):
    # Load the public key from a file
    with open(path_to_public_key, 'r') as file:
        pem = file.read().encode('utf-8')

    return serialization.load_pem_public_key(pem)

async def receive_messages(websocket, private_key, other_username):
    while True:
        try:
            data = await websocket.recv()
            if data:
                data = json.loads(data)
                chat_with, encrypted_message, received_hash_value = data[0], data[1].encode('utf-8'), data[2]

                if args.encrypt:
                    message = decrypt_message(encrypted_message, private_key)
                else:
                    message = encrypted_message

                hash_value = hash_message(message.decode('utf-8'))

                print('\r\x1b[K', end='')

                if hash_value != received_hash_value:
                    print('Warning: Message integrity compromised!')
                else:
                    print(f"{other_username}: {message.decode('utf-8')}")
                print(f'{chat_with}: ', end='', flush=True)

        except websockets.exceptions.ConnectionClosed:
            break


async def send_messages(websocket, receiver_public_key, chat_with, username):
    while True:
        message = await aioconsole.ainput(f"{username}: ")
        if message.lower() == 'quit':
            break
        if args.encrypt:
            encrypted_message = encrypt_message(message.encode('utf-8'), receiver_public_key).decode('utf-8')
        else:
            encrypted_message = message
        hash_value = hash_message(message)

        data = [chat_with, encrypted_message, hash_value]
        await websocket.send(json.dumps(data))

async def chat():
    username = input("Enter your username: ")

    private_key = load_private_key(username)

    chat_with = input("Enter username of the person you want to chat with: ")

    while True:
        try:
            path_to_public_key = input("Enter the path to the public key of the person you want to chat with: ").strip()
            if path_to_public_key == "":
                path_to_public_key = f"{chat_with}_public_key.pem"

            receiver_public_key = load_public_key(path_to_public_key)
            break
        except FileNotFoundError:
            print("File not found, please enter a valid path.")
        except (ValueError, TypeError):
            print("Invalid file content, please make sure the file contains a valid public key.")

    async with websockets.connect(URI) as websocket:
        await websocket.send(username)

        send_task = asyncio.create_task(send_messages(websocket, receiver_public_key, chat_with, username))
        receive_task = asyncio.create_task(receive_messages(websocket, private_key, chat_with))

        with aiomonitor.start_monitor(asyncio.get_running_loop()):
            await asyncio.gather(send_task, receive_task)



asyncio.run(chat())
