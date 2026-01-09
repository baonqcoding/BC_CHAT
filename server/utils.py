import json


def encode_message(data: dict) -> bytes:
    """
    Chuyển dict -> JSON bytes để gửi qua socket
    """
    return json.dumps(data).encode("utf-8")


def decode_message(data: bytes) -> dict:
    """
    Chuyển JSON bytes -> dict để xử lý
    """
    return json.loads(data.decode("utf-8"))

