import tkinter as tk
from gui.gui_room import RoomWindow

class LobbyWindow(tk.Frame):
    def __init__(self, master, client):
        super().__init__(master)
        self.client = client
        self.client.on_message = self.handle_server

        tk.Label(self, text="Room name").pack()
        self.room = tk.Entry(self)
        self.room.pack()

        tk.Button(self, text="Join Room", command=self.join_room).pack()

    def join_room(self):
        self.client.send({
            "type": "join",
            "room": self.room.get()
        })

    def handle_server(self, msg):
        if msg["type"] == "join":
            self.destroy()
            room = RoomWindow(self.master, self.client, msg["room"])
            room.pack(fill="both", expand=True)
