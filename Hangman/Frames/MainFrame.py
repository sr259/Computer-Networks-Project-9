import tkinter as tk
class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="Welcome to Hangman!", font=("Comic Sans", 18))
        self.label.pack(pady=20)

        self.playButton = tk.Button(self, text="Join Lobby")
        self.playButton.pack(pady=10)

        exit_button = tk.Button(self, text="Exit", command=self.quit)
        exit_button.pack(pady=10)