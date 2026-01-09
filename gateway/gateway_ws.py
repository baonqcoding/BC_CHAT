import asyncio
import websockets
import socket
import threading

TCP_HOST = "127.0.0.1"
TCP_PORT = 9000
WS_PORT = 8765


async def handle_ws(websocket):
    print("[WS] Client connected")

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((TCP_HOST, TCP_PORT))
    print("[WS] Connected to TCP server")

    loop = asyncio.get_event_loop()

    # WS -> TCP
    async def ws_to_tcp():
        async for message in websocket:
            tcp_sock.send(message.encode("utf-8"))

    # TCP -> WS (RUN IN THREAD)
    def tcp_to_ws():
        try:
            while True:
                data = tcp_sock.recv(1024)
                if not data:
                    break
                asyncio.run_coroutine_threadsafe(
                    websocket.send(data.decode("utf-8")),
                    loop
                )
        except:
            pass

    threading.Thread(target=tcp_to_ws, daemon=True).start()
    await ws_to_tcp()

    tcp_sock.close()
    print("[WS] Client disconnected")


async def main():
    async with websockets.serve(handle_ws, "0.0.0.0", WS_PORT):
        print(f"[WS] WebSocket running on port {WS_PORT}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
