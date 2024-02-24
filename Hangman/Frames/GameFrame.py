import tkinter as tk

class GameFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="Game Screen", font=("Comic Sans", 18))
        self.backButton = tk.Button(self, text="Back to Lobby")
        self.backButton.pack(pady=10)