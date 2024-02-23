import socket
from  _thread import *
import sys

server = "10.176.2.216"
port = 5555

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
try:
    serversocket.bind((server, port))
except socket.error as e:
    str(e)

# Listen for a connection
serversocket.listen(2)
print("Waiting for a connection, Server Started")

# Function to send and receive messages
def threaded_client(connection):
    connection.send(str.encode("Connected"))
    reply = ""
    while True:
        data = connection.recv(2048)
        reply = "Server Says: " + data.decode("utf-8")
        if not data:
            break
        connection.sendall(str.encode(reply))
    print("Connection Closed")
    connection.close()

while True:
    # Accept connection from client
    client, address = serversocket.accept()
    print("Connected to: ", address)
    # Start a new thread
    start_new_thread(threaded_client, (client, ))


