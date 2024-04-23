# Hangman: A Multiplayer Word Guessing Game

This project implements a multiplayer word guessing game where players can connect to a server, join a lobby, and start games with other connected players.

## Features

- Server-client architecture using Python sockets for communication.
- Lobby system for managing connected players.
- Word guessing game with player interaction.

## Installation

1. Clone the repository to your local machine
2. Navigate to the ClientServer folder and run. (Only one person should have the server up, anyone else can join the server based on its IP and port number)
```python
python LobbyServer.py
```
4. After this, go back to the Hangman folder and run
```python
python Mainscreen.py
```
6. It will ask you in the terminal if you are running the Server on your local machine, if you are running the server on your machine, you can type "y" and hit enter, if not, you will need to get the ip of the person who is running the server. You can get the IP your server is listening too from the first output from the server.
```
2024-04-22 16:23:42,806: Server listening to 10.178.3.136:5553...

```
In this case, 10.178.3.136 is the IP, and 5553 is the port number.

7. Enter the port number. It defaults to 5553.

8. A tkinter window should pop up and allow you to join the lobby after entering the name. To play someone else, click on their name when it pops up and join their lobby. Hope you have fun!