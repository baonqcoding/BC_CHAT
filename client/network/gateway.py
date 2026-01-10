import socket
import threading
import json

class GatewayClient:
    def __init__(self, host="127.0.0.1", port=9000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.running = True
        self.on_message = None  # callback cho GUI

        threading.Thread(
            target=self.listen_server,
            daemon=True
        ).start()

    def send(self, data: dict):
        msg = json.dumps(data).encode()
        self.sock.sendall(msg)

    def listen_server(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                msg = json.loads(data.decode())
                if self.on_message:
                    self.on_message(msg)
            except:
                break

    def close(self):
        self.running = False
        self.sock.close()
