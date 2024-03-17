import socket
import os 
from  _thread import *
import sys
import signal


PORT = 5555         
MAX_CLIENTS = 5

def signal_handler(sig, frame):
    # Signal handler for Ctrl+C
    print("Ctrl+C detected. Shutting down the server...")
    serversocket.close()
    sys.exit()

def get_ip_address():
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except socket.error as e:
            print(f"Error retrieving IP address: {e}")
            return None
       
HOST = get_ip_address()
clients = {}  # Dictionary to map client names to their connections
lobby = []    # List of clients in the lobby

def broadcast(message, sender=None):
    #Broadcast a message to all clients except the sender.
    if isinstance(message, str):
        encoded_message = message.encode()
    else:
        encoded_message = message
    for client_name, client_socket in clients.items():
        if client_socket != sender:
            client_socket.sendall(encoded_message)

def handle_client(client_socket, client_name):
    #Handle communication with a client.
    while True:
        try:
            message = client_socket.recv(2048)
            if message:
                # Broadcast the message to all clients
                print(f"{client_name}: {message.decode()}")

                broadcast(f"{client_name}: {message.decode()}", client_socket)
            else:
                # If no data is received, client has disconnected
                print(f"Client {client_name} disconnected.")
                break
        except:
            # Handle exceptions such as client disconnecting abruptly
            print(f"{client_name} has left the lobby.")
            break
        
    # Remove the client from the list of clients and lobby
    del clients[client_name]
    lobby.remove(client_name)
    broadcast(f"{client_name} has left the lobby.".encode())

    # Close the connection
    client_socket.close()

def main():
    
    # Create a socket object
    global serversocket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    # Bind the socket to the port
    try:
        serversocket.bind((HOST,PORT))
    except socket.error as e:
        sys.exit(1)

    # Listen for a connection
    serversocket.listen(MAX_CLIENTS)
    print(f"Server listening to {HOST}:{PORT}...")
    
    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)


    try:
        while True:    
            #Accept Client Connection 
            client_socket, client_addr = serversocket.accept()
            print(f"Connection established with {client_addr}")  

            # Receive the client's name
            client_name = client_socket.recv(2048).decode("utf-8")
            print(f"{client_name} joined the lobby.")

            # Add the client to the list of clients and lobby
            clients[client_name] = client_socket
            lobby.append(client_name)
        
            # Notify other clients about the new member
            broadcast(f"{client_name} joined the lobby.")
        
             # Start a new thread to handle client communication
            start_new_thread(handle_client, (client_socket, client_name))
    except Exception as e:
        print(f"Error accepting client connection: {e}")   

if __name__ == "__main__":
    main()