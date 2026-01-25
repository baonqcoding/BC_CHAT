import json

def encode_message(data: dict) -> bytes:
    return (json.dumps(data) + "\n").encode("utf-8")

def decode_messages(buffer: str):
    parts = buffer.split("\n")
    return parts[:-1], parts[-1]
