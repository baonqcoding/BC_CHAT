import tkinter as tk
from network.gateway import GatewayClient
from gui.gui_login import LoginWindow
from gui.gui_voice_call import VoiceClient
def main():
    root = tk.Tk()
    root.title("Chat Client")

    client = GatewayClient()

    app = LoginWindow(root, client)
    app.pack(fill="both", expand=True)

    root.mainloop()
    client.close()

if __name__ == "__main__":
    main()
