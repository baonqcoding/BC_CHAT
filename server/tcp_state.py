import socket
import threading
import json
from utils import encode_message, decode_message

HOST = "0.0.0.0"
PORT = 9000   # 🔥 PHẢI TRÙNG VỚI gateway

clients = {}   # conn -> username
rooms = {}     # room -> list[conn]

with open("users_db.json", "r") as f:
    USERS = json.load(f)


def handle_client(conn, addr):
    print(f"[+] Client connected: {addr}")
    username = None

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = decode_message(data)
            msg_type = msg.get("type")

            # ---------- LOGIN ----------
            if msg_type == "login":
                user = msg["username"]
                password = msg["password"]

                if USERS.get(user) == password:
                    username = user
                    clients[conn] = user
                    conn.send(encode_message({
                        "type": "login",
                        "status": "ok"
                    }))
                else:
                    conn.send(encode_message({
                        "type": "login",
                        "status": "fail"
                    }))

            # ---------- JOIN ROOM ----------
            elif msg_type == "join":
                room = msg["room"]

                if room not in rooms:
                    rooms[room] = []

                if conn not in rooms[room]:
                    rooms[room].append(conn)

                conn.send(encode_message({
                    "type": "join",
                    "room": room
                }))

            # ---------- CHAT ----------
            elif msg_type == "chat":
                room = msg["room"]
                text = msg["message"]

                for c in rooms.get(room, []):
                    c.send(encode_message({
                        "type": "chat",
                        "user": username,
                        "message": text
                    }))

    except Exception as e:
        print("[ERROR]", e)

    finally:
        print(f"[-] Client disconnected: {username}")

        for room in rooms.values():
            if conn in room:
                room.remove(conn)

        clients.pop(conn, None)
        conn.close()


def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER] TCP running on port {PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()


if __name__ == "__main__":
    start_tcp_server()
