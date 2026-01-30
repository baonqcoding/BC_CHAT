# BC_CHAT – Chat & Voice Call Application (Python)

BC_CHAT là một ứng dụng chat và voice call đơn giản, ứng dụng được lên ý tưởng dựa theo app Discord, được xây dựng bằng Python theo mô hình Client – Server.  
Dự án sử dụng **TCP cho chat text** và **UDP cho voice call realtime**, kết hợp giao diện **Tkinter GUI**.
+Tính năng chính

- Đăng nhập người dùng (TCP)
- Chat text theo phòng (TCP)
- Tham gia phòng chat
- Voice call ,(UDP)
+Kiến trúc hệ thống

- **TCP Server**
  - Xử lý đăng nhập
  - Quản lý phòng chat
  - Gửi/nhận tin nhắn text
- **UDP Server**
  - Truyền âm thanh
  - Broadcast audio theo room
- **Client**
  - GUI: Login → Lobby → Room
  - TCP: Chat text
  - UDP: Voice call
TCP được sử dụng để đảm bảo độ tin cậy cho dữ liệu text,  
UDP được sử dụng cho voice call để giảm độ trễ.
+Công nghệ sử dụng
- Python 3.x
- Socket (TCP / UDP)
- Threading
- Tkinter (GUI)
- PyAudio (Voice call)
+Hướng dẫn chạy chương trình

+Cài đặt thư viện cần thiết
```bash
pip install pyaudio

2 Chạy TCP Server
cd server
python tcp_state.py

3️ Chạy UDP Voice Server
cd server
python udp_server.py

4 Chạy GateWay
cd gateway
python gateway_ws.py

5 Chạy Client
cd client
python meeting_gui_client.py

