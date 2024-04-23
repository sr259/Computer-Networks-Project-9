import socket
import threading
import sys
import os
import time
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
import queue
from GameLogic import Player
import tkinter as tk

logging.basicConfig(level=logging.INFO, format = "%(asctime)s: %(message)s", stream=sys.stdout)


class Client:
    def __init__(self, player, main , lobby, game, server_ip, server_port):
        self.SERVER_HOST = server_ip
        self.SERVER_PORT = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player = player
        self.players = []
        self.gameLobby = []
        self.isConnected = False
        self.isInGame = False
        self.mainFrame = main
        self.lobbyFrame = lobby
        self.gameFrame = game
        self.word = ""
        self.guessed = []
        self.turn = False
        self.lives = {}
        self.peer_socket = None
        self.peer_port = None
        self.peer_host = None
        self.peer_name = None
        

    def get_server_ip_address(self):
        try:
            # Create a temporary socket to retrieve the IP address
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.connect(("8.8.8.8", 80))  # Connect to a public DNS server
            server_ip_address = temp_socket.getsockname()[0]  # Get the local IP address
            temp_socket.close()
            return server_ip_address
        except socket.error as e:
            logging.error(f"Error retrieving server IP address: {e}")
            return None
    
    def connect_to_server(self):
        try:
            # Connect to the server
            self.client_socket.connect((self.SERVER_HOST, self.SERVER_PORT))
            logging.info("Connected to the server.")
            self.isConnected = True
            # Send the client's name to the server
            
            self.client_socket.sendall(self.player.name.encode())
            threading.Thread(target=self.receive_message).start()
        except KeyboardInterrupt:
            # Close the client socket and exit
            logging.info("Closing connection (KeyboardInterrupt)...")
            self.client_socket.close()
        except Exception as e:
            logging.error(f"Error occurred during connection: {e}")
            self.client_socket.close()
            self.isConnected = False

    def receive_message(self):
        try:
            while self.isConnected:
                logging.info("Waiting for message...")
                message = self.client_socket.recv(2048).decode("utf-8")
                if message.startswith("NAME: "):
                    self.player.name = message.split(": ")[1]
                    logging.info(f"Name was taken, added digits for uniqueness: {self.player.get_name()}")
                    self.lobbyFrame.establishWelcomeText(self.player.get_name())


                elif message.startswith("GET_PLAYERS: "):
                    logging.info("Getting players")
                    self.players = message.split(": ")[1].split(", ")
                    self.updatePlayerList()
               
                elif message.startswith("GAME_STARTED: "):
                    logging.info("Game started")
                    self.gameLobby = message.split(": ")[1].split(", ")
                    logging.info(f"Players in game: {self.gameLobby}")
                    logging.info("My name: " + self.player.get_name())
                    self.gameFrame.clearTexts()
                    self.lobbyFrame.master.showGameFrame()
                    #self.event_queue.put(message)
                    self.gameFrame.gameFinished = False
                    self.isInGame = True
                    if self.player.get_name() == self.gameLobby[0]:
                        self.turn = False
                    else:
                        self.turn = True
                
                elif message.startswith("WORD: "):
                    self.word = message.split(": ")[1]
                    self.gameFrame.updateWord()
                
                elif message.startswith("GUESSED: "):
                    stringForm = message.split(": ")[1].split(", ")
                    self.guessed = list(stringForm[0].lower())
                    if len(stringForm[1]) == 1:
                        self.addToGuesses(stringForm[1])
                    self.gameFrame.establishBoard()
                    logging.info(f"Guessed: {self.guessed}")
                    self.gameFrame.updateTurnText()
                
                elif message.startswith("LIVES: "):
                    asString = message.split(": ")[1].split(", ")
                    self.lives = {self.gameLobby[0]: int(asString[0]), self.gameLobby[1]: int(asString[1])}
                    self.turn = self.determineTurn()
                    logging.info("Is it my turn? : " + str(self.turn))
                    logging.info(f"Lives: {self.lives}")
                    self.gameFrame.updateLives()
                    self.gameFrame.updateTurnText()

                elif message.startswith("GAME_OVER: "):
                    winner = message.split(": ")[1]
                    logging.info(f"Game over. Winner: {winner}")
                    self.guessed = []
                    self.turn = False
                    self.lives.clear()
                    self.isInGame = False
                    if self.gameFrame.gameFinished == False:
                        self.gameFrame.gameOver(winner)
                    word = ""
        except KeyboardInterrupt:
            logging.info("Closing connection...")
            self.client_socket.close()
            self.isConnected = False
        except socket.error as e:
            if e.errno == 10053 or e.errno == 10054:
                logging.error("Connection to the server was lost.")
                self.client_socket.close()
                self.isConnected = False
            if e.errno == 10038:
                logging.error("Socket was closed, cannot connect to server")
                self.isConnected = False
            else:
                logging.error(f"Error receiving message: {e}")
    
    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode("utf-8"))
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            self.client_socket.close()
            self.isConnected = False
    
    def changeName(self, newName):
        self.player.name = newName
    
    def close_connection(self):
        try:
            self.client_socket.close()
            self.isConnected = False
        except Exception as e:
            logging.error(f"Error closing connection: {e}")
            self.isConnected = False

    def updatePlayerList(self):
        self.lobbyFrame.playerList.delete(0, tk.END)
        for player in self.players:
            self.lobbyFrame.playerList.insert(tk.END, player)

    def addToGuesses(self, word):
        for i in word:
            if i not in self.player.guesses and i != "_":
                self.player.guesses.append(i)
    
    def determineTurn(self):
        self.turn = not self.turn
        otherName = self.gameLobby[0] if self.gameLobby[1] == self.player.get_name() else self.gameLobby[1]
        if self.turn == False:
            if self.lives.get(otherName) == 0:
                return True
            return False
        elif self.turn == True:
            if self.lives.get(self.player.get_name()) == 0:
                return False
            return True

def main():
    playerList = tk.Listbox()
    player = Player.Player("Player 1")
    client = Client(player, playerList)
    client.connect_to_server()
    client.send_message("GET_PLAYERS")

if __name__ == "__main__":
    main()
