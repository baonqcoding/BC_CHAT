import customtkinter as ctk
import tkinter as tk
import threading
from PIL import Image
from gui.gui_voice_call import VoiceClient

class RoomWindow(ctk.CTkFrame):
    def __init__(self, master, client, room):
        super().__init__(master)
        self.client = client
        self.room = room
        self.client.on_message = self.handle_server
        
        self.voice = None

        
        self.icon_send = None
        self.icon_mic = None
        self.icon_hangup = None
        self.img_user = None

        try:
            self.icon_send = ctk.CTkImage(light_image=Image.open("send.png"), dark_image=Image.open("send.png"), size=(20, 20))
            self.icon_mic = ctk.CTkImage(light_image=Image.open("mic.png"), dark_image=Image.open("mic.png"), size=(20, 20))
            self.icon_hangup = ctk.CTkImage(light_image=Image.open("hangup.png"), dark_image=Image.open("hangup.png"), size=(20, 20))
            self.img_user = ctk.CTkImage(light_image=Image.open("user_icon.png"), dark_image=Image.open("user_icon.png"), size=(20, 20))
        except Exception as e:
            print(f"Lưu ý: Không tìm thấy file icon ({e}). Sẽ dùng text thay thế.")

        
        self.header = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color="#2b2b2b")
        self.header.pack(fill="x", side="top")
        ctk.CTkLabel(self.header, text=f"PHÒNG: {room}", font=("Arial", 16, "bold")).pack(pady=10)

        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        self.chat_box = ctk.CTkTextbox(self.body_frame, state="disabled", font=("Consolas", 14))
        self.chat_box.pack(side="left", fill="both", expand=True)

        self.user_list_frame = ctk.CTkFrame(self.body_frame, width=160, corner_radius=10)
        self.user_list_frame.pack(side="right", fill="y", padx=(10, 0))
        
        ctk.CTkLabel(self.user_list_frame, text="Thành viên", font=("Arial", 13, "bold"), text_color="gray").pack(pady=(10, 5))
        
        self.user_scroll = ctk.CTkScrollableFrame(self.user_list_frame, fg_color="transparent")
        self.user_scroll.pack(fill="both", expand=True)

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", side="bottom", padx=10, pady=10)

        self.entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="Nhập tin nhắn...")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda event: self.send_chat())

        self.btn_send = ctk.CTkButton(
            self.bottom_frame, 
            text="Gửi" if not self.icon_send else "", 
            image=self.icon_send,
            width=50, 
            command=self.send_chat
        )
        self.btn_send.pack(side="left", padx=(0, 5))

        self.btn_voice = ctk.CTkButton(
            self.bottom_frame, 
            text="Gọi" if not self.icon_mic else "", 
            image=self.icon_mic,
            width=50, 
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.toggle_voice
        )
        self.btn_voice.pack(side="left")


    def send_chat(self):
        msg = self.entry.get()
        if not msg: return
        self.entry.delete(0, tk.END)

        self.client.send({
            "type": "chat",
            "data": {"room": self.room, "message": msg}
        })

    def handle_server(self, msg):
        msg_type = msg.get("type")
        
        if msg_type == "chat":
            user = msg["data"]["user"]
            message = msg["data"]["message"]
            self.chat_box.configure(state="normal")
            self.chat_box.insert(tk.END, f"[{user}]: {message}\n")
            self.chat_box.configure(state="disabled")
            self.chat_box.see(tk.END)
            
        elif msg_type == "update_users":
            users = msg.get("data", {}).get("users", [])
            self.update_user_list(users)

    def update_user_list(self, users):
        
        for widget in self.user_scroll.winfo_children():
            widget.destroy()

        for user in users:
            item = ctk.CTkFrame(self.user_scroll, fg_color="transparent")
            item.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(
                item, 
                text=f"👤  {user}",
                image=self.img_user,
                compound="left",
                anchor="w",
                font=("Arial", 13)
            )
            lbl.pack(fill="x", padx=5)

    def toggle_voice(self):
    
        if self.voice is None:
            self.voice = VoiceClient(username="User", room=self.room)
            self.voice.start()
            
            self.btn_voice.configure(
                text="📞" if not self.icon_hangup else "",
                image=self.icon_hangup if self.icon_hangup else self.icon_mic,
                fg_color="#c0392b",
                hover_color="#922b21"
            )
            print("[GUI] Voice Call Started")

        else:
            self.voice.stop()
            self.voice = None
            
            self.btn_voice.configure(
                text="🎤" if not self.icon_mic else "",
                image=self.icon_mic,
                fg_color="#2ecc71",
                hover_color="#27ae60"
            )
            print("[GUI] Voice Call Stopped")