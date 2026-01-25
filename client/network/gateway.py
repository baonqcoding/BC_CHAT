import socket
import threading
import json

from utils import encode_message

class GatewayClient:
    def __init__(self, host="127.0.0.1", port=9000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.running = True
        self.on_message = None

        self.buffer = ""

        threading.Thread(
            target=self.listen_server,
            daemon=True
        ).start()

    def send(self, data: dict):
        self.sock.sendall(encode_message(data))

    def listen_server(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break

                self.buffer += data.decode("utf-8")

                while "\n" in self.buffer:
                    line, self.buffer = self.buffer.split("\n", 1)
                    if not line.strip():
                        continue

                    msg = json.loads(line)
                    print("[DEBUG][CLIENT] recv =", msg)

                    if self.on_message:
                        self.on_message(msg)

            except Exception as e:
                print("[CLIENT ERROR]", e)
                break
                