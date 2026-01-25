import socket
import json
import time

UDP_HOST = "127.0.0.1"
UDP_PORT = 9001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

username = input("Username: ")
room = input("Room: ")

print("Sending fake voice packets...")

while True:
    msg = {
        "user": username,
        "room": room,
        "audio": "FAKE_AUDIO_DATA"
    }

    sock.sendto(json.dumps(msg).encode(), (UDP_HOST, UDP_PORT))
    time.sleep(1)
