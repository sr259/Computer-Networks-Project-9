import tkinter as tk
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from GameLogic import Player
from GameLogic import Game
from Frames import Man

class GameFrame(tk.Frame):
    def __init__(self, master):
        self.canvas1 = tk.Canvas(master, width=200, height=200)
        self.canvas2 = tk.Canvas(master, width=200, height=200)
        self.player1Man = Man.Man(self.canvas1, "blue", .6)
        self.player2Man = Man.Man(self.canvas2, "red", .6)
        #Potentially have it so Player 1 and Player 2 are passed in from lobby as parameters
        self.player1 = Player.Player("Player 1")
        self.player2 = Player.Player("Player 2")
        self.playerMaxLives = self.player1.get_lives()
        self.game = Game.Game(self.player1, self.player2)

        super().__init__(master)
        self.label = tk.Label(self, text="Game Screen", font=("Comic Sans", 18))
        self.backButton = tk.Button(self, text="Back to Lobby")
        self.backButton.pack(pady=10)

        self.guessArea = tk.Label(self, font=("Comic Sans", 18))
        self.guessArea.pack(pady=10)

        #Makes sure that the input is a single letter, needs to be changed so the player can guess the
        def validate_input(char):
            return (char.isalpha())
        vcmd = master.register(validate_input)
        self.guessEntry = tk.Entry(self, validate="key", validatecommand=(vcmd, "%S"))
        self.guessEntry.pack(pady=10)

        self.livesLabel = tk.Label(self, font=("Comic Sans", 18))
        self.livesLabel.pack(pady=10)

        self.guessButton = tk.Button(self, text="Guess", command=self.guessButtonCommand)
        self.guessButton.pack(pady=10)

        self.guessedLetters = tk.Label(self, font=("Comic Sans", 18))
        self.guessedLetters.pack(pady=10)
    
    def instantiateMen(self):
        self.canvas1 = tk.Canvas(self.master, width=100, height=150)
        self.canvas2 = tk.Canvas(self.master, width=100, height=150)
        self.canvas1.pack(side=tk.LEFT, padx=10)
        self.canvas2.pack(side=tk.RIGHT, padx=10)
        self.player1Man = Man.Man(self.canvas1, "blue", .6)
        self.player2Man = Man.Man(self.canvas2, "red", .6)
    
    def hideMen(self):
        self.player1Man.clear()
        self.player2Man.clear()
        self.canvas1.pack_forget()
        self.canvas2.pack_forget()

    def establishBoard(self):
        self.dashes = self.game.get_guessed()
        self.updateWord()
        self.updateLives()
        
    def updateWord(self):
        self.dashes = self.game.get_guessed()
        self.guessArea.config(text=self.dashes)

    def updateLives(self):
        self.player1Man.draw(self.playerMaxLives - self.game.get_lives()[0])
        self.player2Man.draw(self.playerMaxLives - self.game.get_lives()[1])
        self.livesLabel.config(text="Lives: " + str(self.game.get_lives()))

    def guessButtonCommand(self):
        self.game.guess(self.guessEntry.get(), self.game.player1Turn)
        self.updateWord()
        self.updateLives()
        self.updateGuessedLetters()
        self.guessEntry.delete(0, 'end')
        if self.determineGameOver():
            self.gameOver(self.getWinner())        

    def gameOver(self,winner):
        self.guessButton.config(state="disabled")
        self.guessEntry.config(state="disabled")
        self.livesLabel.config(text="Game Over, " + winner + " wins!")
        self.backButton.config(text="Return to Lobby", command=self.clearGameAndReturn)
        self.guessArea.config(text=self.game.get_word())
        
    def getWinner(self):
        if self.game.get_guessed() == list(self.game.get_word()):
            if self.game.player1Turn:
                return self.game.player2.get_name()
            else:
                return self.game.player1.get_name()
        elif self.game.get_lives() == (0,0):
            return "No one"
        elif self.game.player1.get_lives() == 0:
            return self.game.player2.get_name()
        else:
            return self.game.player1.get_name()
        
    def determineGameOver(self):
        if self.game.get_guessed() == list(self.game.get_word()):
            return True
        elif self.game.get_lives() == (0,0) or self.game.player1.get_lives() < 0 or self.game.player2.get_lives() < 0:
            return True
        else:
            return False
    
    def clearGameAndReturn(self):
        self.hideMen()
        self.master.resetGameFrame()
        self.master.showLobbyFrame()

    def updateGuessedLetters(self):
        guessed_letters = ""
        for i in range(0,2):
            for letter in self.game.get_guesses()[i]:
                guessed_letters += letter + " "
        self.guessedLetters.config(text="Guessed Letters: " + guessed_letters)