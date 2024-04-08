import socket
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
import queue
from GameLogic import Player
import tkinter as tk

logging.basicConfig(level=logging.INFO, format = "%(asctime)s: %(message)s", stream=sys.stdout)


class Client:
    def __init__(self, player, playerList, server_port=5550):
        self.SERVER_HOST = self.get_server_ip_address()
        self.SERVER_PORT = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player = player
        self.players = []
        self.isConnected = False
        self.event_queue = queue.Queue()
        self.playerList = playerList

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
                message = self.client_socket.recv(2048).decode("utf-8")
                if message.startswith("GET_PLAYERS: "):
                    logging.info("Getting players")
                    self.players = message.split(": ")[1].split(", ")
                    self.updatePlayerList()
                elif message.startswith("GAME_STARTED: "):
                    logging.info("Game started")
                    self.event_queue.put(message)
        except KeyboardInterrupt:
            logging.info("Closing connection...")
            self.client_socket.close()
            self.isConnected = False
        except Exception as e:
            logging.error(f"Error receiving message: {e}")
    
    def send_message(self, message):
        try:
            logging.info("Sending message: " +message)
            self.client_socket.sendall(message.encode("utf-8"))
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            self.client_socket.close()
            self.isConnected = False
    def changeName(self, newName):
        self.player.name = newName
    def wait_for_message(self):
        while self.event_queue.empty():
            pass
        return self.event_queue.get()
    def close_connection(self):
        try:
            logging.info("Closing connection...")
            self.client_socket.close()
            self.isConnected = False
        except Exception as e:
            logging.error(f"Error closing connection: {e}")
            self.isConnected = False

    def updatePlayerList(self):
        self.playerList.delete(0, tk.END)
        for player in self.players:
            self.playerList.insert(tk.END, player)

def main():
    playerList = tk.Listbox()
    player = Player.Player("Player 1")
    client = Client(player, playerList)
    client.connect_to_server()
    client.send_message("GET_PLAYERS")

if __name__ == "__main__":
    main()
