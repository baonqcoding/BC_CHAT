from utils import encode_message

class RoomManager:
    def __init__(self):
        self.rooms = {}  

    def join(self, room, conn):
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(conn)

    def leave(self, room, conn):
        if room in self.rooms:
            self.rooms[room].discard(conn)
            if not self.rooms[room]:
                del self.rooms[room]

    def broadcast(self, room, data):
        # Lấy danh sách kết nối, dùng list() để copy tránh lỗi runtime nếu set thay đổi
        for conn in list(self.rooms.get(room, [])):
            try:
                conn.send(encode_message(data))
            except:
                pass
    
    # --- [MỚI] Hàm lấy tất cả kết nối trong 1 phòng ---
    def get_connections(self, room):
        return list(self.rooms.get(room, []))

    # --- [CẬP NHẬT] Hàm xóa user và trả về danh sách phòng bị ảnh hưởng ---
    def remove_client(self, conn):
        affected_rooms = []
        for room in list(self.rooms.keys()):
            if conn in self.rooms[room]:
                self.leave(room, conn)
                affected_rooms.append(room)
        return affected_rooms