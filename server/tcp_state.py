import socket
import threading
import json
HOST = "0.0.0.0"
PORT = 9000

clients = {}
rooms = {}

with open("users_db.json", "r") as f:
    USERS = json.load(f)

def handle_client(conn, addr):


#------------------------CONNECTED-----------------------
    print(f"[+] Client connected: {addr}")
    username = None

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            msg = json.loads(data.decode())
            msg_type = msg["type"]


#------------------------LOGIN-----------------------
            if msg_type == "login":
                user = msg["username"]
                password = msg["password"]

                if USERS.get(user) == password:
                    clients[conn] = user
                    username = user
                    conn.send(json.dump({
                        "type": "login",
                        "status": "ok"
                    }).encode())
                else:
                    conn.send(json.dumps({
                        "type": "login",
                        "status": "fail"
                    }).encode())



#------------------------JOIN-----------------------                    
            elif msg_type == "join":
                room = msg["room"]

                if room not in rooms:
                    rooms[room] - []

                rooms[room].append(conn)

                conn.send(json.dumps({
                    "type": "join",
                    "room": room
                }).encode())


#------------------------CHAT-----------------------

            elif msg_type == "chat":
                room = msg["room"]
                text = msg["message"]

                for c in rooms.get(room, []):
                    c.send(json.dumps({
                        "type": "chat",
                        "user": username,
                        "message": text
                    }).encode())

        except:
            break



#------------------------DISCONNECTED-----------------------

    print(f"[-] Client disconnected: {username}")

    for room in rooms.values():
        if conn in room:
            room.remove(conn)


    clients.pop(conn, None)
    conn.close()

#------------------------START_SERVER-----------------------
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


