import json

def encode_message(data: dict) -> bytes:
    return (json.dumps(data) + "\n").encode("utf-8")


def decode_message(buffer: str):
    """
    Nhận buffer dạng string
    Trả về (list_message, remaining_buffer)
    """
    parts = buffer.split("\n")
    return parts[:-1], parts[-1]
