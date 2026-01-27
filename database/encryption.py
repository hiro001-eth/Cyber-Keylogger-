# database/encryption.py

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

BLOCK_SIZE = 16


def _pad_bytes(data: bytes) -> bytes:

    padding_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)

    return data + bytes([padding_len]) * padding_len


def _unpad_bytes(data: bytes) -> bytes:

    if not data:

        return data

    padding_len = data[-1]

    if padding_len < 1 or padding_len > BLOCK_SIZE:

        raise ValueError("Invalid padding")

    return data[:-padding_len]


def get_key(password: str) -> bytes:

    return hashlib.sha256(password.encode("utf-8")).digest()


def encrypt(raw: str, password: str) -> str:

    if raw is None:

        raw = ""

    raw_bytes = raw.encode("utf-8")

    padded = _pad_bytes(raw_bytes)

    iv = get_random_bytes(BLOCK_SIZE)

    cipher = AES.new(get_key(password), AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(padded)

    return base64.b64encode(iv + ciphertext).decode("utf-8")


def decrypt(enc: str, password: str) -> str:

    if enc is None or enc == "":

        return ""

    enc_bytes = base64.b64decode(enc)

    iv = enc_bytes[:BLOCK_SIZE]

    cipher = AES.new(get_key(password), AES.MODE_CBC, iv)

    padded_plain = cipher.decrypt(enc_bytes[BLOCK_SIZE:])

    plain_bytes = _unpad_bytes(padded_plain)

    return plain_bytes.decode("utf-8")
