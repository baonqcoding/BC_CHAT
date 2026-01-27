import socket

def start_udp_server():
    HOST = "0.0.0.0"
    PORT = 9001
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    
    print(f"[UDP] Voice server running on port {PORT}")
    
    client_rooms = {} 
    
    while True:
        try:
            data, addr = sock.recvfrom(4096)
    
            is_command = False
            try:
                if len(data) < 200:
                    decoded = data.decode('utf-8')
                    
                    if decoded.startswith("JOIN:"):
                        parts = decoded.split(":")
                        if len(parts) >= 2:
                            room = parts[1]
                            username = parts[2] if len(parts) > 2 else "Unknown"
                            
                            client_rooms[addr] = room
                            print(f"[UDP] {username} ({addr}) đã vào phòng Voice '{room}'")
                            is_command = True
            except UnicodeDecodeError:
            
                pass
            except Exception:
                pass

            
            if not is_command:
                sender_room = client_rooms.get(addr)
                
                if sender_room:
                
                    for client_addr, room in list(client_rooms.items()):
                
                        if room == sender_room and client_addr != addr:
                            sock.sendto(data, client_addr)

        except Exception as e:
            print(f"[UDP ERROR] {e}")

if __name__ == "__main__":
    start_udp_server()