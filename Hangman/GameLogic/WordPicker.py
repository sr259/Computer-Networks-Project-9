import random


class WordPicker:
    def __init__(self):
        file_path = "Hangman/GameLogic/WordBank.txt"
        with open(file_path, 'r') as file:
            # Read the content and split into words
            content = file.read()
            words = content.split()
        self.word_list = words

    def pick_word(self):
        return random.choice(self.word_list)