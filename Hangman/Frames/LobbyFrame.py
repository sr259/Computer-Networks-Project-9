import tkinter as tk
from  _thread import *
import sys
import signal
import os

class LobbyFrame(tk.Frame):
    def __init__(self, master,):
        super().__init__(master)
        self.label = tk.Label(self, text="Game Screen", font=("Comic Sans", 18))
        self.backButton = tk.Button(self, text="Back to Home Screen")
        self.backButton.pack(pady=10)
        
        self.joinGameButton = tk.Button(self, text="Join Game", state = tk.DISABLED)
        self.joinGameButton.pack(pady=10)

        self.playerList = tk.Listbox(self, width=50)
        self.playerList.pack(pady=10)
        self.playerList.bind("<<ListboxSelect>>", self.on_player_select)

    def addPlayer(self, player):
        self.master.players.append(player)
        self.playerList.insert(tk.END, player.get_name())

    def on_player_select(self, event=None):
        selected_index = self.playerList.curselection()
        if selected_index: 
            selected_player = self.playerList.get(selected_index[0])  # Get the selected player
            if selected_player != self.master.client.player.get_name():
                # Check if selected player is not the client's own name
                self.joinGameButton.config(state=tk.NORMAL)
            else:
                self.joinGameButton.config(state=tk.DISABLED)
        else:
            self.joinGameButton.config(state=tk.DISABLED)
    
    
    