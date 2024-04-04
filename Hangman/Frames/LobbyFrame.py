import tkinter as tk
from  _thread import *
import sys
import signal
import os

class LobbyFrame(tk.Frame):
    def __init__(self, master,):
        super().__init__(master)
        self.client = self.master.client
        self.label = tk.Label(self, text="Game Screen", font=("Comic Sans", 18))
        self.backButton = tk.Button(self, text="Back to Home Screen")
        self.backButton.pack(pady=10)
        
        self.joinGameButton = tk.Button(self, text="Join Game")
        self.joinGameButton.pack(pady=10)

        self.playerList = tk.Listbox(self)
        self.playerList.pack(pady=10)
        self.refreshLobbyButton = tk.Button(self, text="Refresh Lobby", command=self.updateLobbyList)
        self.refreshLobbyButton.pack(pady=10)



    def addPlayer(self, player):
        self.master.players.append(player)
        self.playerList.insert(tk.END, player.get_name())
    
    def updateLobbyList(self):
        self.playerList.delete(0, tk.END)
        for player in self.master.players:
            self.playerList.insert(tk.END, player)