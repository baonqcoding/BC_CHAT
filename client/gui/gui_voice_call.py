import socket
import threading
import pyaudio

class VoiceClient:
    def __init__(self, username, room, port=9001):
        self.server_ip = "192.168.1.124"
        self.port = port
        self.username = username
        self.room = room
        
        self.client_socket = None
        self.is_running = False

        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        
        self.p = pyaudio.PyAudio()

    def start(self):
        """Bắt đầu cuộc gọi"""
        if self.is_running:
            return

        self.is_running = True
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        init_msg = f"JOIN:{self.room}:{self.username}"
        self.client_socket.sendto(init_msg.encode(), (self.server_ip, self.port))

        threading.Thread(target=self.send_audio, daemon=True).start()
        threading.Thread(target=self.receive_audio, daemon=True).start()
        print(f"[VOICE] Started for room {self.room}")

    def stop(self):
        """Dừng cuộc gọi"""
        self.is_running = False
        
        if self.client_socket:
            self.client_socket.close()
        
        print("[VOICE] Stopped")

    def send_audio(self):
        """Luồng thu âm từ Mic và gửi đi"""
        try:
            stream = self.p.open(format=self.format, channels=self.channels, 
                                 rate=self.rate, input=True, frames_per_buffer=self.chunk)
            
            while self.is_running:
                try:
                    data = stream.read(self.chunk)
                    if self.is_running:
                        self.client_socket.sendto(data, (self.server_ip, self.port))
                except Exception as e:
        
                    break
            
            stream.stop_stream()
            stream.close()
        except Exception as e:
            print(f"[VOICE ERROR] Send: {e}")

    def receive_audio(self):
        """Luồng nhận dữ liệu và phát ra Loa"""
        try:
            stream = self.p.open(format=self.format, channels=self.channels, 
                                 rate=self.rate, output=True, frames_per_buffer=self.chunk)
            
            while self.is_running:
                try:
                    self.client_socket.settimeout(1.0)
                    data, addr = self.client_socket.recvfrom(4096)
                    stream.write(data)
                except socket.timeout:
                    continue
                except:
                    break
                    
            stream.stop_stream()
            stream.close()
        except Exception as e:
            print(f"[VOICE ERROR] Receive: {e}")