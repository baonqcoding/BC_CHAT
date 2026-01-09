from websocket import create_connection
import json
import threading

ws = create_connection("ws://localhost:8765")

def listen():
    while True:
        try:
            msg = ws.recv()
            print("<<", msg)
        except:
            break

threading.Thread(target=listen, daemon=True).start()

# LOGIN
ws.send(json.dumps({
    "type": "login",
    "username": input("Username: "),
    "password": "123"
}))

# JOIN
ws.send(json.dumps({
    "type": "join",
    "room": "python"
}))

# CHAT LOOP
while True:
    text = input("> ")
    ws.send(json.dumps({
        "type": "chat",
        "room": "python",
        "message": text
    }))
