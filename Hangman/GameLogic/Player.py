class Player:
    def __init__(self, name):
        self.name = name
        self.lives = 2
        self.guesses = []

    def guess(self, letter):
        if letter not in self.guesses:
            self.guesses.append(letter)
            return True
        else:
            return False

    def get_lives(self):
        return self.lives

    def lose_life(self):
        self.lives -= 1

    def get_name(self):
        return self.name

    def get_guesses(self):
        return self.guesses