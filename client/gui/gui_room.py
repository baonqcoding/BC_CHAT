import tkinter as tk
import threading
from gui.gui_voice_call import VoiceClient   

class RoomWindow(tk.Frame):
    def __init__(self, master, client, room):
        super().__init__(master)
        self.client = client
        self.room = room
        self.client.on_message = self.handle_server

        self.voice = None 

        self.chat_box = tk.Text(self, state="disabled", height=15)
        self.chat_box.pack(fill="both", expand=True)

        self.entry = tk.Entry(self)
        self.entry.pack(fill="x")

        tk.Button(self, text="Send", command=self.send_chat).pack()
        tk.Button(self, text="Voice Call", command=self.start_voice).pack()

    def send_chat(self):
        msg = self.entry.get()
        self.entry.delete(0, tk.END)

        self.client.send({
            "type": "chat",
            "data": {
                "room": self.room,
                "message": msg
            }
        })

    def start_voice(self):
        if self.voice:
            return  

        self.voice = VoiceClient(room=self.room)
        threading.Thread(
            target=self.voice.start,
            daemon=True
        ).start()

        print("[VOICE] Started")

    def handle_server(self, msg):
        if msg.get("type") == "chat":
            user = msg["data"]["user"]
            message = msg["data"]["message"]

            self.chat_box.config(state="normal")
            self.chat_box.insert(tk.END, f"{user}: {message}\n")
            self.chat_box.config(state="disabled")
    def start_voice(self):
        if hasattr(self, "voice") and self.voice:
            print("[VOICE] Already running")
            return

        self.voice = VoiceClient(
            username="user",   
            room=self.room
        )

        threading.Thread(
            target=self.voice.start,
            daemon=True
        ).start()

        print("[VOICE] Started")
