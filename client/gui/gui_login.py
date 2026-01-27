import customtkinter as ctk
from gui.gui_lobby import LobbyWindow

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, client):
        super().__init__(master)
        self.client = client
        self.client.on_message = self.handle_server
        
        self.configure(fg_color="transparent") 

        self.card = ctk.CTkFrame(self, corner_radius=15)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        self.label_title = ctk.CTkLabel(self.card, text="ĐĂNG NHẬP", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=(20, 20), padx=40)

        self.username = ctk.CTkEntry(self.card, placeholder_text="Tên đăng nhập", width=220)
        self.username.pack(pady=10, padx=20)

        self.password = ctk.CTkEntry(self.card, placeholder_text="Mật khẩu", show="*", width=220)
        self.password.pack(pady=10, padx=20)

        self.status = ctk.CTkLabel(self.card, text="", text_color="red")
        self.status.pack(pady=5)

        self.btn_login = ctk.CTkButton(
            self.card, 
            text="Đăng nhập", 
            command=self.login, 
            width=220, 
            height=40,
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        self.btn_login.pack(pady=(10, 30), padx=20)

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
                self.status.configure(text="Sai tài khoản hoặc mật khẩu!")