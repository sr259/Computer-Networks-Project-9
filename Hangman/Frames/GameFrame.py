import tkinter as tk
import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from GameLogic import Player
from GameLogic import Game
from Frames import Man

class GameFrame(tk.Frame):
    def __init__(self, master):
        self.gameFinished = False
        self.canvas1 = tk.Canvas(master, width=200, height=200)
        self.canvas2 = tk.Canvas(master, width=200, height=200)
        self.player1Man = Man.Man(self.canvas1, "blue", .6)
        self.player2Man = Man.Man(self.canvas2, "red", .6)

        super().__init__(master)
        self.label = tk.Label(self, text="Game Screen", font=("Comic Sans", 18))
        self.backButton = tk.Button(self, text="Back to Home Screen", command=self.backToHome)
        self.backButton.pack(pady=10)

        self.guessArea = tk.Label(self, font=("Comic Sans", 18))
        self.guessArea.pack(pady=10)

        #Makes sure that the input is a single letter, needs to be changed so the player can guess the
        def validate_input(char):
            return (char.isalpha())
        vcmd = master.register(validate_input)
        self.guessEntry = tk.Entry(self, validate="key", validatecommand=(vcmd, "%S"))
        self.guessEntry.pack(pady=10)
        self.guessEntry.bind("<KeyRelease>", self.validateEntry)

        self.livesLabel = tk.Label(self, text = "Loading...", font=("Comic Sans", 18))
        self.livesLabel.pack(pady=10)

        self.guessButton = tk.Button(self, text="Guess", command=self.guessButtonCommand, state=tk.DISABLED)
        self.guessButton.pack(pady=10)

        self.guessedLetters = tk.Label(self, font=("Comic Sans", 18))
        self.guessedLetters.pack(pady=10)
    
    def backToHome(self):
        if self.master.client.gameLobby[0] == self.master.client.player.name:
            otherName = self.master.client.gameLobby[1]
        else:
            otherName = self.master.client.gameLobby[0]
        self.master.client.send_message(f"QUIT: {self.master.client.player.name}, {otherName}")
        #self.master.client.close_connection()
        self.master.showMainframe()
        self.clearTexts()

    def instantiateMen(self):
        self.canvas1 = tk.Canvas(self.master, width=100, height=200)
        self.canvas2 = tk.Canvas(self.master, width=100, height=200)
        self.canvas1.pack(side=tk.LEFT, padx=10)
        self.canvas2.pack(side=tk.RIGHT, padx=10)
        self.player1Man = Man.Man(self.canvas1, "blue", .6, self.master.client.gameLobby[0])
        self.player2Man = Man.Man(self.canvas2, "red", .6, self.master.client.gameLobby[1])
    
    def hideMen(self):
        self.player1Man.clear()
        self.player2Man.clear()
        self.canvas1.pack_forget()
        self.canvas2.pack_forget()

    def establishBoard(self):
        self.updateWord()
        self.updateLives()
        self.updateGuessedLetters()
        self.guessEntry.delete(0, 'end')
        
    def updateWord(self):
        if self.master.client.guessed == []:
            self.guessArea.config(text= "_ "* len(self.master.client.word))
        else:
            self.dashes = self.master.client.guessed
            self.guessArea.config(text=self.dashes)

    def updateLives(self):
        self.player1Man.draw(6 - self.master.client.lives[0])
        self.player2Man.draw(6 - self.master.client.lives[1])
        self.livesLabel.config(text="Lives: " + str(self.master.client.lives[0]) + ", " + str(self.master.client.lives[1]))

    def guessButtonCommand(self):
        # self.game.guess(self.guessEntry.get())
        self.master.client.send_message("GUESS: " + self.guessEntry.get())
        time.sleep(3)
               
    def gameOver(self,winner):
        self.guessButton.config(state="disabled")
        self.guessEntry.config(state="disabled")
        self.livesLabel.config(text="Game Over, " + winner + " wins!")
        #self.backButton.config(text="Return to Lobby", command=self.master.showMainframe)
        self.guessArea.config(text=self.master.client.word)
        self.gameFinished = True

    def clearTexts(self):
        self.guessArea.config(text="")
        self.livesLabel.config(text="Loading...")
        self.guessedLetters.config(text="")
        self.guessEntry.config(state=tk.NORMAL)
        self.guessEntry.delete(0, 'end')
    
    def clearGameAndReturn(self):
        self.hideMen()
        self.master.resetGameFrame()
        self.master.showLobbyFrame()

    def updateGuessedLetters(self):
        guessed_letters = self.master.client.player.guesses
        returnWord = ""
        for letter in guessed_letters:
            returnWord += letter + " "
        self.guessedLetters.config(text="Guessed Letters: " + returnWord)

    def validateEntry(self, event):
        # Get the input from the entry box
        input_text = self.guessEntry.get()
            # Check if it's the player's turn
        if self.master.client.turn == False:
            self.guessButton.config(state=tk.DISABLED)
            return
        # Check if the input is empty
        if input_text == "":
            self.guessButton.config(state=tk.DISABLED)
            return
        if len(input_text) == 1 or len(input_text) == len(self.master.client.word):
            # Check if all characters in the input are letters
            if input_text.isalpha():
                self.guessButton.config(state=tk.NORMAL)
            else:
                self.guessButton.config(state=tk.DISABLED)
        else:
            self.guessButton.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game_frame = GameFrame(root)
    game_frame.pack()
    game_frame.establishBoard()
    root.mainloop()