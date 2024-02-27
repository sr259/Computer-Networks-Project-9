import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path)
from GameLogic import Player
from GameLogic import WordPicker

class Game:
    def __init__(self, player1, player2):
        wordpicker = WordPicker.WordPicker()
        self.word = "BANANA" #wordpicker.pick_word()
        self.guessed = ["_"] * len(self.word)
        self.player1 = player1
        self.player2 = player2
        self.player1Turn = True

    def guess(self, letter, player, turn):
        #Letter is the guess, Player is the player object, and turn is a boolean ( true for player 1, false for player 2)
        if turn:
            player = self.player1
        else:
            player = self.player2

        #Player gets to keep guessing if other player has no lives left
        if player.get_lives() == 0:
            self.switch_turn()
            return self.guessed
        letter = letter.lower()
        if player.guess(letter):
            if letter in self.word:
                indices = [i for i, l in enumerate(self.word) if l == letter]
                for index in indices:
                    self.guessed[index] = letter
            else:
                player.lose_life()
        self.switch_turn()
        return self.guessed

    def switch_turn(self):
        self.player1Turn = not self.player1Turn
    
    def get_guessed(self):
        return self.guessed

    def get_word(self):
        return self.word

    def get_lives(self):
        return self.player1.get_lives(), self.player2.get_lives()

    def get_name(self):
        return self.player1.get_name(), self.player2.get_name()

    def get_guesses(self):
        return self.player1.get_guesses(), self.player2.get_guesses()