import random
import os
class WordPicker:
    def __init__(self):
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, "WordBank.txt")
        
        with open(file_path, 'r') as file:
            # Read the content and split into words
            content = file.read()
            words = content.split()
        self.word_list = words

    def pick_word(self):
        return random.choice(self.word_list)