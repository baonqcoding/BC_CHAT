import tkinter as tk
from gui.gui_lobby import LobbyWindow

class LoginWindow(tk.Frame):
    def __init__(self, master, client):
        super().__init__(master)
        self.client = client
        self.client.on_message = self.handle_server

        tk.Label(self, text="Username").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        self.status = tk.Label(self, text="")
        self.status.pack()

        tk.Button(self, text="Login", command=self.login).pack()

    def login(self):
        self.client.send({
            "type": "login",
            "data": {
                "username": self.username.get(),
                "password": self.password.get()
            }
        })

    def handle_server(self, msg):
        if msg.get("type") == "login":
            status = msg.get("data", {}).get("status")

            if status == "ok":
                self.destroy()
                lobby = LobbyWindow(self.master, self.client)
                lobby.pack(fill="both", expand=True)
            else:
                self.status.config(text="Login failed")

