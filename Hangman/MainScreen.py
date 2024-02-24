import customtkinter as ctk
import tkinter as tk
from Frames.MainFrame import MainFrame
from Frames.LobbyFrame import LobbyFrame
from Frames.GameFrame import GameFrame

class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.main_frame = MainFrame(self)
        self.lobby_frame = LobbyFrame(self)
        self.game_frame = GameFrame(self)

        self.main_frame.playButton['command'] = self.show_LobbyFrame
        self.lobby_frame.backButton['command'] = self.show_Mainframe
        self.lobby_frame.joinGameButton['command'] = self.show_GameFrame
        self.game_frame.backButton['command'] = self.show_LobbyFrame

        self.title("Hangman Game")
        self.geometry("600x400")

        self.show_Mainframe()

    def show_Mainframe(self):
        self.main_frame.pack(fill='both', expand=True)
        self.lobby_frame.pack_forget()
        self.game_frame.pack_forget()
        print("Switching to Main Frame")

    def show_LobbyFrame(self):
        self.main_frame.pack_forget()
        self.lobby_frame.pack(fill='both', expand=True)
        self.game_frame.pack_forget()
        print("Switching to Lobby Frame")
    
    def show_GameFrame(self):
        self.main_frame.pack_forget()
        self.lobby_frame.pack_forget()
        self.game_frame.pack(fill='both', expand=True)
        print("Switching to Game Frame")

if __name__ == "__main__":
    app = MainScreen()
    app.mainloop()