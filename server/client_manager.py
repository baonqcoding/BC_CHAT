class ClientManager:
    def __init__(self):
        self.clients = {}

    def add(self, conn, username):
        self.clients[conn] = username

    def remove(self, conn):
        return self.clients.pop(conn, None)

    def get_username(self, conn):
        return self.clients.get(conn)

    def is_online(self, username):
        return username in self.clients.values()