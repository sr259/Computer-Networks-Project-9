import socket
import threading
import sys
import os
import socket
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Player:
    def __init__(self, name, socket = None):
        self.name = name
        self.lives = 6
        self.guesses = []
        self.socket = socket

    def guess(self, letter):
        if len(letter) == 1:
            if letter not in self.guesses:
                self.guesses.append(letter)
                return True
            else:
                return False

    def get_socket(self):
        return self.socket
    
    def get_lives(self):
        return self.lives

    def lose_life(self):
        self.lives -= 1

    def get_name(self):
        return self.name

    def get_guesses(self):
        return self.guesses

    def connect(self):
        pass