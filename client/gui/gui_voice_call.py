import socket
import json
import threading
import pyaudio

class VoiceClient:
    def __init__(self, username, room,
                 host="127.0.0.1", port=9001):
        self.username = username
        self.room = room
        self.host = host
        self.port = port

        self.running = False

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
        self.running = True
        self.t_send = threading.Thread(target=self.send_voice, daemon=True)
        self.t_recv = threading.Thread(target=self.receive_voice, daemon=True)
        self.t_send.start()
        self.t_recv.start()

    def stop(self):
        self.running = False
        self.stream_in.stop_stream()
        self.stream_out.stop_stream()
        self.stream_in.close()
        self.stream_out.close()
        self.audio.terminate()
        self.sock.close()

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
                (self.host, self.port)
            )

    def receive_voice(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(65535)
                msg = json.loads(data.decode())
                audio_bytes = bytes.fromhex(msg["audio"])
                self.stream_out.write(audio_bytes)
            except:
                pass

    def join_voice(self):
        self.voice = VoiceClient(
            username=self.username,
            room=self.current_room
        )
        self.voice.start()
        self.btn_voice.config(text="🔇 Leave Voice")

    def leave_voice(self):
        if self.voice:
            self.voice.stop()
            self.voice = None
        self.btn_voice.config(text="🎤 Join Voice")