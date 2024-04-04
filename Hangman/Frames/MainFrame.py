import tkinter as tk

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="Welcome to Hangman!", font=("Comic Sans", 18))
        self.label.pack(pady=20)

        self.nameInput = tk.Entry(self)
        self.nameInput.insert(0, "Enter name here")  # Set default text
        self.nameInput.pack(pady=10)

        self.joinLobbyButton = tk.Button(self, text="Join Lobby", state=tk.DISABLED)  # Disable initially
        self.joinLobbyButton.pack(pady=10)

        exit_button = tk.Button(self, text="Exit", command=self.quit)
        exit_button.pack(pady=10)

        # Bind an event handler to the nameInput widget
        self.nameInput.bind("<KeyRelease>", self.check_name_entry)

    def check_name_entry(self, event):
        # Check if the nameInput entry is empty
        if self.nameInput.get().strip() == "":
            self.joinLobbyButton.config(state=tk.DISABLED)  # Disable playButton
        else:
            self.joinLobbyButton.config(state=tk.NORMAL)   # Enable playButton
        
        self.master.name = self.nameInput.get().strip()
