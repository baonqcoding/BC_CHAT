import socket
import threading
import json
from utils import encode_message, decode_messages
from client_manager import ClientManager
from room_manager import RoomManager

HOST = "0.0.0.0"
PORT = 9000

client_manager = ClientManager()
room_manager = RoomManager()

with open("users_db.json", "r") as f:
    USERS = json.load(f)




def handle_client(conn, addr):
    print(f"[+] Client connected: {addr}")
    buffer = ""

    try:
        while True:
            raw = conn.recv(1024)
            if not raw:
                break

            buffer += raw.decode("utf-8")
            messages, buffer = decode_messages(buffer)

            for line in messages:
                msg = json.loads(line)
                print("[DEBUG][SERVER] msg =", msg)

                msg_type = msg.get("type")
                data = msg.get("data", {})

                
                if msg_type == "login":
                    user = data.get("username")
                    password = data.get("password")

                    if USERS.get(user) == password:
                        client_manager.add(conn, user)
                        conn.sendall(encode_message({
                            "type": "login",
                            "data": {"status": "ok"}
                        }))
                    else:
                        conn.sendall(encode_message({
                            "type": "login",
                            "data": {"status": "fail"}
                        }))


                elif msg_type == "join":
                    room = data.get("room")
                    room_manager.join(room, conn)

                    conn.sendall(encode_message({
                        "type": "join",
                        "data": {"room": room}
                    }))


                elif msg_type == "chat":
                    room = data.get("room")
                    message = data.get("message")
                    user = client_manager.get_username(conn)

                    room_manager.broadcast(room, {
                        "type": "chat",
                        "data": {
                            "user": user,
                            "message": message
                        }
                    })

    finally:
        client_manager.remove(conn)
        room_manager.remove_client(conn)
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
