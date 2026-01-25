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
        for conn in self.rooms.get(room, []):
            try:
                conn.send(encode_message(data))
            except:
                pass

    def remove_client(self, conn):
        for room in list(self.rooms.keys()):
            self.leave(room, conn)