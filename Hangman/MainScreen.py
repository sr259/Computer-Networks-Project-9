import tkinter as tk
import os
import sys
import socket
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Frames.MainFrame import MainFrame
from Frames.LobbyFrame import LobbyFrame
from Frames.GameFrame import GameFrame
from Frames.Man import Man
from GameLogic import Game
from GameLogic import Player
from ClientServer import Client
import time
import threading
class MainScreen(tk.Tk):
    def __init__(self, server_ip_address, server_port_num):
        super().__init__()
        self.name = "Player"
        self.players = None
        self.server_ip_address = server_ip_address
        self.server_port_num = server_port_num
        self.main_frame = MainFrame(self)
        self.lobby_frame = LobbyFrame(self)
        self.game_frame = GameFrame(self)
        self.client = Client.Client(Player.Player(self.name),  self.main_frame, self.lobby_frame, self.game_frame, self.server_ip_address, self.server_port_num)

        self.main_frame.joinLobbyButton['command'] = self.showLobbyFrame
        self.lobby_frame.backButton['command'] = self.showMainframe
        self.lobby_frame.joinGameButton['command'] = self.joinGameWithPlayer
        #self.game_frame.backButton['command'] = self.showMainframe

        self.title("Hangman Game")
        self.geometry("600x400")
        
        self.showMainframe()

    def showMainframe(self):
        if self.client.client_socket:
            self.client.close_connection()
        self.client = Client.Client(Player.Player(self.name), self.main_frame, self.lobby_frame, self.game_frame, self.server_ip_address, self.server_port_num )
        self.main_frame.pack(fill='both', expand=True)
        self.lobby_frame.pack_forget()
        self.game_frame.pack_forget()
        self.game_frame.hideMen()


    def showLobbyFrame(self, name= "Player"):
        self.main_frame.label.config(text = "Welcome to Hangman!")
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
    
    def joinGameWithPlayer(self):
        self.client.send_message("CONNECT_TO_GAME: " + self.client.player.name + ", " + self.lobby_frame.playerList.get(tk.ACTIVE))
        self.game_frame.gameFinished = False
        
if __name__ == "__main__":
    yorNo = input("Are you running the server on your local machine? (y/n): ")
    if yorNo == "y":
        try:
            # Create a temporary socket to retrieve the IP address
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.connect(("8.8.8.8", 80))  # Connect to a public DNS server
            server_ip_address = temp_socket.getsockname()[0]  # Get the local IP address
            temp_socket.close()
            port_num = input("Please submit the server port number: ")
        except socket.error as e:
            print(f"Error retrieving server IP address: {e}")
        
    else:
        server_ip_address = input("Please submit the server IP address: ")
        port_num = input("Please submit the server port number: ")
    app = MainScreen(server_ip_address, int(port_num))
    app.mainloop()