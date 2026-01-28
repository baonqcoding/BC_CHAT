import customtkinter as ctk
from gui.gui_room import RoomWindow

class LobbyWindow(ctk.CTkFrame):
    def __init__(self, master, client):
        super().__init__(master)
        self.client = client
        self.client.on_message = self.handle_server
        
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.center_frame, text="THAM GIA PHÒNG CHAT", font=("Arial", 20, "bold")).pack(pady=20, padx=40)

        self.room = ctk.CTkEntry(self.center_frame, placeholder_text="Nhập tên phòng...", width=250)
        self.room.pack(pady=10)

        self.btn_join = ctk.CTkButton(
            self.center_frame, 
            text="Vào Phòng Ngay", 
            command=self.join_room,
            fg_color="green",
            hover_color="darkgreen",
            width=250
        )
        self.btn_join.pack(pady=(10, 30))

    def join_room(self):
        self.client.send({
            "type": "join",
            "data": {
                "room": self.room.get()
            }
        })

    def handle_server(self, msg):
        if msg.get("type") == "join":
            room_name = msg.get("data", {}).get("room")
            if room_name:
                self.destroy()
                room = RoomWindow(self.master, self.client, room_name)
                room.pack(fill="both", expand=True)