import sys

from cryptography.hazmat.primitives import serialization

from encryption.encryption_utils import generate_keys


def save_private_key(filename, private_key):
    # Serialize private key to PEM format
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Save the private key to a file
    with open(filename, 'w') as file:
        file.write(pem.decode('utf-8'))

def save_public_key(filename, public_key):
    # Serialize public key to PEM format
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Save the public key to a file
    with open(filename, 'w') as file:
        file.write(pem.decode('utf-8'))

username = sys.argv[1]

# Generate RSA keys
private_key, public_key = generate_keys()

# Save the public key to a text file
save_public_key(f'{username}_public_key.pem', public_key)

# Save the private key to a text file
save_private_key(f'{username}_private_key.pem', private_key)
