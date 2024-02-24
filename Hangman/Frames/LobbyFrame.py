import tkinter as tk

class LobbyFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="Game Screen", font=("Comic Sans", 18))
        self.backButton = tk.Button(self, text="Back to Home Screen")
        self.backButton.pack(pady=10)
        
        self.joinGameButton = tk.Button(self, text="Join Game")
        self.joinGameButton.pack(pady=10)