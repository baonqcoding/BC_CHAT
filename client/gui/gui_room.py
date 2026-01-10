import tkinter as tk

class RoomWindow(tk.Frame):
    def __init__(self, master, client, room):
        super().__init__(master)
        self.client = client
        self.room = room
        self.client.on_message = self.handle_server

        self.chat = tk.Text(self, state="disabled")
        self.chat.pack(fill="both", expand=True)

        self.msg = tk.Entry(self)
        self.msg.pack(fill="x")

        tk.Button(self, text="Send", command=self.send_msg).pack()

    def send_msg(self):
        text = self.msg.get()
        self.msg.delete(0, tk.END)

        self.client.send({
            "type": "chat",
            "room": self.room,
            "message": text
        })

    def handle_server(self, msg):
        if msg["type"] == "chat":
            self.chat.config(state="normal")
            self.chat.insert("end", f'{msg["user"]}: {msg["message"]}\n')
            self.chat.config(state="disabled")
