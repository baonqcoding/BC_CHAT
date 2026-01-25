import socket
import json
import threading
import pyaudio

UDP_HOST = "127.0.0.1"   # IP UDP server
UDP_PORT = 9001

class VoiceClient:
    def __init__(self, username="user", room="default"):
        self.username = username
        self.room = room
        self.running = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 0))

        self.audio = pyaudio.PyAudio()

        self.stream_in = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )

        self.stream_out = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            output=True,
            frames_per_buffer=1024
        )

    def start(self):
        print("[VOICE] Voice started")
        threading.Thread(target=self.send_voice, daemon=True).start()
        threading.Thread(target=self.receive_voice, daemon=True).start()

        while self.running:
            pass

    def send_voice(self):
        while self.running:
            data = self.stream_in.read(1024, exception_on_overflow=False)
            packet = {
                "user": self.username,
                "room": self.room,
                "audio": data.hex()
            }
            self.sock.sendto(
                json.dumps(packet).encode(),
                (UDP_HOST, UDP_PORT)
            )

    def receive_voice(self):
        while self.running:
            data, _ = self.sock.recvfrom(65535)
            msg = json.loads(data.decode())
            audio_bytes = bytes.fromhex(msg["audio"])
            self.stream_out.write(audio_bytes)

    def stop(self):
        self.running = False
        self.stream_in.close()
        self.stream_out.close()
        self.audio.terminate()
        self.sock.close()
