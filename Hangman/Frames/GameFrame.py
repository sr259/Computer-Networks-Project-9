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

        self.guessedLetters = tk.Label(self, font=("Comic Sans", 12))
        self.guessedLetters.pack(pady=10)
        self.turnText = tk.Label(self, text=f"It is your turn!", font=("Comic Sans", 12))
        self.turnText.pack(pady=10)
    
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
        p1Lives = self.master.client.lives.get(self.master.client.gameLobby[0])
        p2Lives = self.master.client.lives.get(self.master.client.gameLobby[1])

        self.player1Man.draw(6 - p1Lives)
        self.player2Man.draw(6 - p2Lives)
        self.livesLabel.config(text="Lives: " + str(p1Lives) + ", " + str(p2Lives))

    def guessButtonCommand(self):
        # self.game.guess(self.guessEntry.get())
        self.master.client.send_message('GUESS: ' + self.guessEntry.get())
        time.sleep(1)
        self.master.client.send_message("GUESS: " + self.guessEntry.get())
        time.sleep(3)
        self.guessButton.config(state=tk.DISABLED)
               
    def gameOver(self,winner):
        self.guessButton.config(state="disabled")
        self.guessEntry.config(state="disabled")
        self.livesLabel.config(text="Game Over, " + winner + " wins!")
        #self.backButton.config(text="Return to Lobby", command=self.master.showMainframe)
        self.guessArea.config(text=self.master.client.word)

        self.turnText.config(text=f"Thanks for playing!")
        self.gameFinished = True


    def clearTexts(self):
        self.guessArea.config(text="")
        self.livesLabel.config(text="Loading...")
        self.guessedLetters.config(text="")
        self.guessEntry.config(state=tk.NORMAL)
        self.guessEntry.delete(0, 'end')
        self.turnText.config(text="")
    
    def clearGameAndReturn(self):
        self.hideMen()
        self.master.resetGameFrame()
        self.master.showLobbyFrame()

    def updateTurnText(self):

        lives = self.master.client.lives
        name = self.master.client.player.get_name()
        otherName = self.master.client.gameLobby[0] if self.master.client.gameLobby[1] == name else self.master.client.gameLobby[1]
        if self.master.client.turn == True and lives.get(name) > 0 or self.master.client.turn == False and lives.get(otherName) == 0:
            self.turnText.config(text=f"It is your turn, {name}!")
        elif self.master.client.turn == True and lives.get(name) == 0 or self.master.client.turn == False and lives.get(name) == 0:
            self.turnText.config(text=f"You have no more lives {name},\nwait for the other player to finsih guessing.")
        elif self.master.client.turn == False and lives.get(otherName) > 0:
            self.turnText.config(text=f"Wait until it is your turn, {name}...")


    def updateGuessedLetters(self):
        guessed_letters = self.master.client.player.guesses
        returnWord = ""
        for letter in guessed_letters:
            returnWord += letter + " "
        self.guessedLetters.config(text="Guessed Letters:\n" + returnWord)

    def validateEntry(self, event):
        # Get the input from the entry box
        input_text = self.guessEntry.get()
            # Check if it's the player's turn
        if self.master.client.turn == False or self.master.client.lives.get(self.master.client.player.get_name()) == 0:
            self.guessButton.config(state=tk.DISABLED)
            return
        # Check if the input is empty
        if input_text == "" or input_text in self.master.client.player.guesses:
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
