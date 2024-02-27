import tkinter as tk
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path)

from GameLogic import Player
from GameLogic import Game

class GameFrame(tk.Frame):
    def __init__(self, master):

        #Potentially have it so Player 1 and Player 2 are passed in from lobby as parameters
        self.player1 = Player.Player("Player 1")
        self.player2 = Player.Player("Player 2")

        self.game = Game.Game(self.player1, self.player2)

        super().__init__(master)
        self.label = tk.Label(self, text="Game Screen", font=("Comic Sans", 18))
        self.backButton = tk.Button(self, text="Back to Lobby")
        self.backButton.pack(pady=10)

        self.guessArea = tk.Label(self, font=("Comic Sans", 18))
        self.guessArea.pack(pady=10)
        def validate_input(char):
            return char.isalpha() and len(char) == 1

        vcmd = master.register(validate_input)
        self.guessEntry = tk.Entry(self, validate="key", validatecommand=(vcmd, "%S"))
        self.guessEntry.pack(pady=10)
        self.livesLabel = tk.Label(self, font=("Comic Sans", 18))
        self.livesLabel.pack(pady=10)
        self.guessButton = tk.Button(self, text="Guess", command=self.guessButtonCommand)
        self.guessButton.pack(pady=10)
        self.establishBoard()
    
    def establishBoard(self):
        self.dashes = self.game.get_guessed()
        self.updateWord()
        self.updateLives()

    def updateWord(self):
        self.dashes = self.game.get_guessed()
        self.guessArea.config(text=self.dashes)

    def updateLives(self):
        self.livesLabel.config(text="Lives: " + str(self.game.get_lives()))

    def guessButtonCommand(self):
        self.game.guess(self.guessEntry.get(), self.game.player1, self.game.player1Turn)
        self.updateWord()
        self.updateLives()
        self.guessEntry.delete(0, 'end')
        if self.determineGameOver():
            self.gameOver(self.getWinner())        

    def gameOver(self,winner):
        self.guessButton.config(state="disabled")
        self.guessEntry.config(state="disabled")
        self.livesLabel.config(text="Game Over, " + winner + " wins!")
        self.backButton.config(text="Return to Lobby", command=self.clearGameAndReturn)
        
    def getWinner(self):
        if self.game.get_lives() == (0,0):
            return "No one"
        elif self.game.player1.get_lives() == 0:
            return self.game.player2.get_name()
        else:
            return self.game.player1.get_name()
        
    def determineGameOver(self):
        if self.game.get_guessed() == list(self.game.get_word()):
            return True
        elif self.game.get_lives() == (0,0):
            return True
        else:
            return False
    def clearGameAndReturn(self):
        self.master.resetGameFrame()
        self.master.showLobbyFrame()

