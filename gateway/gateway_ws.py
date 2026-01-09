import asyncio
import websockets
import socket
import json

TCP_HOST = "127.0.0.1"
TCP_PORT = 9000
WS_PORT = 8765

#Hàm xử lý 1 client WebSocket

async def handle_ws(websocket):
    print("[WS] Client connected")

    # Kết nối TCP tới server
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((TCP_HOST, TCP_PORT))

#Nhận dữ liệu từ WebSocket → gửi TCP

    async def ws_to_tcp():
        async for message in websocket:
            tcp_sock.send(message.encode("utf-8"))

#Nhận dữ liệu từ TCP → gửi WebSocket

    async def tcp_to_ws():
        while True:
            data = tcp_sock.recv(1024)
            if not data:
                break
            await websocket.send(data.decode("utf-8"))


#Chạy 2 nhiệm vụ song song
    await asyncio.gather(ws_to_tcp(), tcp_to_ws())

#Dọn dẹp kết nối

    tcp_sock.close()
    print("[WS] Client disconnected")

#Khởi động WebSocket server
async def main():
    async with websockets.serve(handle_ws, "0.0.0.0", WS_PORT):
        print(f"[WS] WebSocket running on port {WS_PORT}")
        await asyncio.Future()  # Chạy mãi mãi
