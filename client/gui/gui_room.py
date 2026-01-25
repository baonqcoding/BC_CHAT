import tkinter as tk
from gui.gui_voice_call import VoiceClient


class RoomWindow(tk.Frame):
    def __init__(self, master, client, room):
        super().__init__(master)
        self.client = client
        self.room = room
        self.client.on_message = self.handle_server

        # ===== CHAT AREA =====
        self.chat = tk.Text(self, state="disabled")
        self.chat.pack(fill="both", expand=True)

        self.msg = tk.Entry(self)
        self.msg.pack(fill="x")

        tk.Button(self, text="Send", command=self.send_msg).pack()

        # ===== VOICE =====
        self.voice = None
        self.btn_voice = tk.Button(
            self,
            text="🎤 Join Voice",
            command=self.toggle_voice
        )
        self.btn_voice.pack(pady=5)

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
            self.chat.insert(
                "end",
                f'{msg["user"]}: {msg["message"]}\n'
            )
            self.chat.config(state="disabled")

    # ===== VOICE FUNCTIONS =====
    def toggle_voice(self):
        if self.voice:
            self.leave_voice()
        else:
            self.join_voice()

    def join_voice(self):
        self.voice = VoiceClient(
            username=self.client.username,
            room=self.room
        )
        self.voice.start()
        self.btn_voice.config(text="🔇 Leave Voice")

    def leave_voice(self):
        if self.voice:
            self.voice.stop()
            self.voice = None
        self.btn_voice.config(text="🎤 Join Voice")
