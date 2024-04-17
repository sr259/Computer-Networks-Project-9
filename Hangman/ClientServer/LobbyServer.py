import socket
import os 
from  _thread import *
import sys
import signal
import functools
import threading
import logging
import time
import os
import sys
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from GameLogic import WordPicker, Player, Game

logging.basicConfig(level=logging.INFO, format = "%(asctime)s: %(message)s", stream=sys.stdout)
class LobbyServer:
    def __init__(self, port = 5550):
        self.PORT = port       
        self.MAX_CLIENTS = 6
        self.HOST = self.get_ip_address()
        self.lobby = []    # List of clients in the lobby
        self.clients = {}  # Dictionary to map client names to their connections
        self.serversocket = None
        self.signal_handler = None
        self.turn = None

    def run(self):    
        # Create a socket object
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        # Bind the socket to the port
        try:
            self.serversocket.bind((self.HOST,self.PORT))
        except socket.error as e:
            logging.error("Error binding the socket to the port, try a different port.")
            sys.exit(1)

        # Listen for a connection
        self.serversocket.listen(self.MAX_CLIENTS)
        logging.info(f"Server listening to {self.HOST}:{self.PORT}...")

        def signal_handler(sig, frame):
            # Signal handler for Ctrl+C
            logging.info("Ctrl+C detected. Shutting down the server...")
            self.serversocket.close()
            sys.exit()
        
        # Register the signal handler for Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)


        try:
            while True:    
                #Accept Client Connection 
                client_socket, client_addr = self.serversocket.accept()
                logging.info(f"Connection established with {client_addr}")  

                time.sleep(1)
                # Start a new thread to handle client communication
                threading.Thread(target = self.handle_client, args = (client_socket,)).start()
        except Exception as e:
            logging.error(f"Error accepting client connection: {e}") 

    def get_ip_address(self):
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except socket.error as e:
            logging.error(f"Error retrieving IP address: {e}")
            return None
    
    def broadcast(self, message, sender=None):
        #Broadcast a message to all clients except the sender.
        if isinstance(message, str):
            encoded_message = message.encode()
        else:
            encoded_message = message
        for client_name, client_socket in self.clients.items():
            if client_socket != sender:
                client_socket.sendall(encoded_message)
        
    def handle_client(self, client_socket):
        #Handle communication with a client.
        try:
            # Receive the client's name
            client_name = client_socket.recv(2048).decode("utf-8")
            logging.info(f"{client_name} joined the lobby.")

            # Add the client to the list of clients and lobby
            self.clients[client_name] = client_socket
            self.lobby.append(client_name)
            # Notify other clients about the new member
            self.sendLobbyUpdate()
            self.broadcast(f"{client_name} joined the lobby.\n")            
            while True:
                try:
                    # logging.info(f"Waiting for message from {client_name}...")
                    message = ''
                    message = str(client_socket.recv(2048).decode("utf-8")).strip()
                    # logging.info(f"{client_name}: {message}")
                    if message == "GET_PLAYERS":
                        # Logic to get the list of players from the lobby           
                        players = self.lobby
                        # Send the list of players back to the client
                        client_socket.sendall(("GET_PLAYERS: " + ", ".join(players)).encode("utf-8"))
                        # logging.info(f"Sent the list of players to {client_name}.")
                    if message.startswith("CONNECT_TO_GAME: "):
                        # Logic to connect two players to a game
                        players = message.split(": ")[1].split(", ")
                        logging.info(f"Connecting {players[0]} and {players[1]} to a game.")
                        # Notify the clients about the game starting
                        player1_socket = self.clients[players[0]]
                        player2_socket = self.clients[players[1]]
                        player1_socket.sendall(f"GAME_STARTED: {players[0]}, {players[1]}".encode("utf-8"))
                        player2_socket.sendall(f"GAME_STARTED: {players[0]}, {players[1]}".encode("utf-8"))
                        #time.sleep(2)
                        self.lobby.remove(players[0])
                        self.lobby.remove(players[1])
                        self.sendLobbyUpdate()
                        self.startGame(players[0], players[1])

                    if message.startswith("QUIT: "):
                        names = message.split(": ")[1].split(", ")
                        logging.info(f"{names[0]} has left the game.")
                        self.closeAndRemoveClient(names[0], self.clients[names[0]])
                        self.clients[names[1]].sendall(f"GAME_OVER: {names[1]}".encode("utf-8"))
                        self.closeAndRemoveClient(names[1], self.clients[names[1]])
                        self.sendLobbyUpdate()
                    
                    if not message:
                        # If no data is received, client has disconnected
                        logging.info(f"Client {client_name} disconnected.")
                        break
                except Exception as e:
                    # Handle exceptions such as client disconnecting abruptly
                    logging.info(f"{client_name} has left the lobby, inside while loop. {e}")
                    #self.serversocket.close()
                    break
        except Exception as e:
            logging.error(f"Error handling client: {e}")
        
        finally:
            if client_name in self.lobby:
                self.closeAndRemoveClient(client_name, client_socket)
                self.broadcast(f"{client_name} has left the lobby.\n")
                self.sendLobbyUpdate()

    def closeAndRemoveClient(self, client_name, client_socket):
            client_socket.close()
            del self.clients[client_name]
            if client_name in self.lobby:
                self.lobby.remove(client_name)
            # Notify other clients about the member leaving

    def sendLobbyUpdate(self):
        # Send the updated list of players to all clients
        players = self.lobby
        for client_name, client_socket in self.clients.items():
            client_socket.sendall(("GET_PLAYERS: " + ", ".join(players)).encode("utf-8"))
            # logging.info(f"Sent the list of players to {client_name}.")

    def startGame(self, name1, name2):
        # Start a game between two players
        picker = WordPicker.WordPicker()
        #word = picker.pick_word()
        word = "banana"
        player1_socket = self.clients[name1]
        player2_socket = self.clients[name2]
        player1 = Player.Player(name1, player1_socket)
        player2 = Player.Player(name2, player2_socket)
        game = Game.Game(player1, player2, word)
        player1_socket.sendall(f"WORD: {word}".encode("utf-8"))
        player2_socket.sendall(f"WORD: {word}".encode("utf-8"))
        time.sleep(3)
        while True:
            try:
                
                player1_socket.sendall(f"LIVES: {player1.get_lives()}, {player2.get_lives()}".encode("utf-8"))
                player2_socket.sendall(f"LIVES: {player1.get_lives()}, {player2.get_lives()}".encode("utf-8"))
                
                player = game.determineTurn()
                socket = player.get_socket()
                message = socket.recv(2048).decode("utf-8")

                if message.startswith("GUESS: "):
                    message = message.split(": ")[1]
                    guessed = game.guess(player, message)
                    isOver = game.determineGameOver()
                    if isOver:
                        winner = game.getWinner()
                        player1_socket.sendall(f"GAME_OVER: {winner.get_name()}".encode("utf-8"))
                        player2_socket.sendall(f"GAME_OVER: {winner.get_name()}".encode("utf-8"))
                        break
                    guessed = "".join(guessed)
                    logging.info(f"{player.get_name()}'s Guess: {message}")
                    time.sleep(3)
                    player1_socket.sendall(f"GUESSED: {guessed}, {message}".encode("utf-8"))
                    player2_socket.sendall(f"GUESSED: {guessed}, {message}".encode("utf-8"))
                if message.startswith("QUIT: "):
                    player1_socket.sendall(f"GAME_OVER: {player.get_name()}".encode("utf-8"))
                    player2_socket.sendall(f"GAME_OVER: {player.get_name()}".encode("utf-8"))
                    self.closeAndRemoveClient(player1.get_name(), player1.get_socket())
                    self.closeAndRemoveClient(player2.get_name(), player2.get_socket())
                    self.sendLobbyUpdate()
                if not message:
                    logging.info(f"{player.get_name()} has left the game.")
                    # Notify the other player about the game over
                    other_player = player2 if player == player1 else player1
                    other_player_socket = other_player.get_socket()
                    other_player_socket.sendall(f"GAME_OVER: {player.get_name()}".encode("utf-8"))
                    break
            except Exception as e:
                logging.error(f"Error in game: {e}")
                break
        #logging.info(f"Game started between {player1.get_name()} and {player2.get_name()}.")




if __name__ == "__main__":
    server = LobbyServer()
    server.run()