import socket
import threading 

SERVER_PORT = 5555         

def get_server_ip_address():
    try:
        # Create a temporary socket to retrieve the IP address
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))  # Connect to a public DNS server
        server_ip_address = temp_socket.getsockname()[0]  # Get the local IP address
        temp_socket.close()
        return server_ip_address
    except socket.error as e:
        print(f"Error retrieving server IP address: {e}")
        return None
    
def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(2048).decode()
            if not message:  # If message is empty, client socket is closed/ Attempting to fix Winerror on client quit
                break
            if "left the lobby." in message or "joined the lobby." in message:
                print(message)  # Print leave notification
            else:
                print(message)  # Print other messages
    except KeyboardInterrupt:
        print("Closing connection...")
        client_socket.close()
    except Exception as e:
        print(f"Error receiving message: {e}")

def main():
    # Retrieve the server's IP address
    SERVER_HOST = get_server_ip_address()
    if not SERVER_HOST:
        print("Failed to retrieve server IP address. Exiting...")
        return    

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((SERVER_HOST,SERVER_PORT))
        
        # Get the client's name
        client_name = input("Enter your name: ")
        
        # Send the client's name to the server
        client_socket.sendall(client_name.encode())
        
        # Start a separate thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()
        
        # Start sending messages
        while True:
            message = input("You: ")
            if message.lower() == "quit":  # Check if the client wants to quit
                print("You left the lobby.")
                client_socket.sendall(message.encode())
                client_socket.close()  # Close the client socket
                break  # Exit the loop            
            client_socket.sendall(message.encode())
    except KeyboardInterrupt:
        # Close the client socket and exit
        client_socket.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        client_socket.close()

if __name__ == "__main__":
    main()
