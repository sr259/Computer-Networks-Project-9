import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from GameLogic import Player
from GameLogic import WordPicker

class Game:
    def __init__(self, player1, player2, word):
        self.word = word
        self.guessed = ["_"] * len(self.word)
        self.player1 = player1
        self.player2 = player2
        self.player1Turn = True

    #input is the guess, Player is the player object, and turn is a boolean ( true for player 1, false for player 2)
    def guess(self, player, input):

        input = input.lower()
        
        # If the input is the word, the player wins
        if len(input) == len(self.word):
            if input == self.word:
                self.guessed = list(self.word)
                return self.guessed
            else:
                # If the player guesses the wrong word
                if player.get_lives() == 1:
                    player.lose_life()
                    self.switch_turn()
                    return self.guessed
                player.lose_life()
                player.lose_life()
                self.switch_turn()
                return self.guessed
            
        if input not in self.get_guesses()[0] and input not in self.get_guesses()[1]:
            if player.guess(input):
                if input in self.word:
                    indices = [i for i, l in enumerate(self.word) if l == input]
                    for index in indices:
                        self.guessed[index] = input
                else:
                    player.lose_life()
            if list(self.word) == self.guessed:
                return self.guessed
            self.switch_turn()
            return self.guessed

    def determineGameOver(self):
        if self.get_guessed() == list(self.word):
            return True
        elif self.get_lives() == [0,0] or self.get_lives()[0] < 0 or self.get_lives()[1] < 0:
            return True
        else:
            return False
    def determineTurn(self):
        if self.player1Turn:
            if self.player1.lives == 0:
                self.switch_turn()
                return self.player2
            return self.player1
        elif not self.player1Turn:
            if self.player2.lives == 0:
                self.switch_turn()
                return self.player1
            return self.player2
        
    def getWinner(self):
        lives = self.get_lives()
        if self.guessed == list(self.word):
            if self.player1Turn:
                return self.player1
            else:
                return self.player2
        elif lives == [0,0]:
            return "No one"
        elif lives[0] == 0:
            return self.player2
        else:
            return self.player1

    def switch_turn(self):
        self.player1Turn = not self.player1Turn
    
    def get_guessed(self):
        return self.guessed

    def get_word(self):
        return self.word

    def get_lives(self):
        return [self.player1.get_lives(), self.player2.get_lives()]

    def get_name(self):
        return [self.player1.get_name(), self.player2.get_name()]

    def get_guesses(self):
        return [self.player1.get_guesses(), self.player2.get_guesses()]