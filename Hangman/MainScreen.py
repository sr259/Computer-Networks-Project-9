import customtkinter as ctk
import tkinter as tk
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Frames.MainFrame import MainFrame
from Frames.LobbyFrame import LobbyFrame
from Frames.GameFrame import GameFrame
from Frames.Man import Man
from GameLogic import Game
from GameLogic import Player
from ClientServer import Client
import time

class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.name = "Player"
        self.players = None
        self.client = Client.Client(Player.Player(self.name))
        self.main_frame = MainFrame(self)
        self.lobby_frame = LobbyFrame(self)
        self.game_frame = GameFrame(self)

        self.main_frame.joinLobbyButton['command'] = self.showLobbyFrame
        self.lobby_frame.backButton['command'] = self.showMainframe
        self.lobby_frame.joinGameButton['command'] = self.showGameFrame
        self.game_frame.backButton['command'] = self.showLobbyFrame

        self.title("Hangman Game")
        self.geometry("600x400")

        self.showMainframe()

    def showMainframe(self):
        if self.client.client_socket:
            self.client.close_connection()
        self.client = Client.Client(Player.Player(self.name))
        self.main_frame.pack(fill='both', expand=True)
        self.lobby_frame.pack_forget()
        self.game_frame.pack_forget()

    def showLobbyFrame(self, name= "Player"):
        self.main_frame.pack_forget()
        self.instantiateClient()
        self.lobby_frame.pack(fill='both', expand=True)
        self.game_frame.pack_forget()
        self.game_frame.hideMen()
    
    def showGameFrame(self):
        self.game_frame.instantiateMen()
        self.main_frame.pack_forget()
        self.lobby_frame.pack_forget()
        self.game_frame.pack(fill='both', expand=True)

    def resetGameFrame(self):
        self.game_frame.pack_forget()
        self.game_frame = GameFrame(self)
        self.game_frame.backButton['command'] = self.showLobbyFrame
        self.game_frame.pack(fill='both', expand=True)

    def instantiateClient(self):
        self.client.changeName(self.name)
        self.client.connect_to_server()
        time.sleep(4)
        self.client.send_message("GET_PLAYERS")
        while self.client.event_queue.empty():
            pass
        self.players = self.client.event_queue.get()

if __name__ == "__main__":
    app = MainScreen()
    app.mainloop()