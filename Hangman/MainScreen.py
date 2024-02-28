import customtkinter as ctk
import tkinter as tk
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Frames.MainFrame import MainFrame
from Frames.LobbyFrame import LobbyFrame
from Frames.GameFrame import GameFrame
from GameLogic import Game
from GameLogic import Player

class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.main_frame = MainFrame(self)
        self.lobby_frame = LobbyFrame(self)
        self.game_frame = GameFrame(self)

        self.main_frame.playButton['command'] = self.showLobbyFrame
        self.lobby_frame.backButton['command'] = self.showMainframe
        self.lobby_frame.joinGameButton['command'] = self.showGameFrame
        self.game_frame.backButton['command'] = self.showLobbyFrame

        self.title("Hangman Game")
        self.geometry("600x400")

        self.showMainframe()

    def showMainframe(self):
        self.main_frame.pack(fill='both', expand=True)
        self.lobby_frame.pack_forget()
        self.game_frame.pack_forget()
        print("Switching to Main Frame")

    def showLobbyFrame(self):
        self.main_frame.pack_forget()
        self.lobby_frame.pack(fill='both', expand=True)
        self.game_frame.pack_forget()
        print("Switching to Lobby Frame")
    
    def showGameFrame(self):
        self.main_frame.pack_forget()
        self.lobby_frame.pack_forget()
        self.game_frame.pack(fill='both', expand=True)
        print("Switching to Game Frame")

    def resetGameFrame(self):
        self.game_frame.pack_forget()
        self.game_frame = GameFrame(self)
        self.game_frame.backButton['command'] = self.showLobbyFrame
        self.game_frame.pack(fill='both', expand=True)
        print("Resetting Game Frame")

if __name__ == "__main__":
    app = MainScreen()
    app.mainloop()