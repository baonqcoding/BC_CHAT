import customtkinter as ctk
from network.gateway import GatewayClient
from gui.gui_login import LoginWindow

def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk() 
    root.title("Chat Client")
    root.geometry("400x600")

    client = GatewayClient(host="192.168.1.124", port=9000)

    app = LoginWindow(root, client)
    app.pack(fill="both", expand=True)

    try:
        root.mainloop()
    finally:
        client.close()

if __name__ == "__main__":
    main()