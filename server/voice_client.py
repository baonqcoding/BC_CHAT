import socket
import json
import threading
import pyaudio

UDP_HOST = "127.0.0.1"
UDP_PORT = 9001

username = input("Username: ")
room = input("Room: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 0))
audio = pyaudio.PyAudio()


stream_in = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1024
)

stream_out = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    output=True,
    frames_per_buffer=1024
)

def send_voice():
    while True:
        data = stream_in.read(1024, exception_on_overflow=False)
        packet = {
            "user": username,
            "room": room,
            "audio": data.hex()
        }
        sock.sendto(json.dumps(packet).encode(), (UDP_HOST, UDP_PORT))

def receive_voice():
    while True:
        data, _ = sock.recvfrom(65535)
        msg = json.loads(data.decode())

        audio_bytes = bytes.fromhex(msg["audio"])
        stream_out.write(audio_bytes)


t1 = threading.Thread(target=send_voice, daemon=True)
t2 = threading.Thread(target=receive_voice, daemon=True)


t1.start()
t2.start()

print("Voice call started. Press Ctrl+C to stop.")

while True:
    pass