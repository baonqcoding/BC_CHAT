import socket
import json

UDP_HOST = "0.0.0.0"
UDP_PORT = 9001  


rooms = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_HOST, UDP_PORT))

print(f"[UDP] Voice server running on port {UDP_PORT}")


while True:
    try:
        data, addr = sock.recvfrom(65535)
        msg = json.loads(data.decode())
        user = msg["user"]
        room = msg["room"]
        audio = msg["audio"]


        
        if room not in rooms:
            rooms[room] = set()
        rooms[room].add(addr)

        
        for client_addr in rooms[room]:
            if client_addr != addr:
                sock.sendto(data, client_addr)

    except Exception as e:
        print(f"UDP [ERROR] {e}")
