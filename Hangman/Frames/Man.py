import tkinter as tk

class Man:
    def __init__(self, canvas, color = "black",scale = 1, name = "Player"):
        self.canvas = canvas
        self.rod = self.canvas.create_line(10*scale, 5*scale, 10*scale, 300*scale, fill=color, width=4)
        self.rope = self.canvas.create_line(100*scale, 5*scale, 100*scale, 20*scale, fill=color, width=4)
        self.top = self.canvas.create_line(10*scale, 5*scale, 100*scale, 5*scale, fill=color, width=4)
        self.gallows = [self.rod, self.rope, self.top]
        self.name = name


        self.head = self.canvas.create_oval(70*scale, 20*scale, 130*scale, 80*scale, outline=color, width=4,state = "hidden")
        self.body = self.canvas.create_line(100*scale, 80*scale, 100*scale, 200*scale, fill=color, width=4,state = "hidden")
        self.left_arm = self.canvas.create_line(100*scale, 100*scale, 70*scale, 140*scale, fill=color, width=4,state = "hidden")
        self.right_arm = self.canvas.create_line(100*scale, 100*scale, 130*scale, 140*scale, fill=color, width=4,state = "hidden")
        self.left_leg = self.canvas.create_line(100*scale, 200*scale, 70*scale, 240*scale, fill=color, width=4,state = "hidden")
        self.right_leg = self.canvas.create_line(100*scale, 200*scale, 130*scale, 240*scale, fill=color, width=4,state = "hidden")
        self.body_parts = [self.head, self.body, self.left_arm, self.right_arm, self.left_leg, self.right_leg]
        self.name_label = self.canvas.create_text(100*scale, 320*scale, text=self.name, fill=color, font=("Arial", 12), state = "normal")
    def draw(self, lives):
        for i in range(len(self.gallows)):
            self.canvas.itemconfig(self.gallows[i], state="normal")
        for i in range(lives):
            self.canvas.itemconfig(self.body_parts[i], state="normal")
    def clear(self):
        for part in self.body_parts:
            self.canvas.delete(part)
        for part in self.gallows:
            self.canvas.delete(part)   
        self.canvas.delete(self.name_label)         

if __name__ == "__main__":
    canvas = canvas = tk.Canvas()
    man = Man(canvas, "red",.5)
    for i in range(7):
        man.draw(i)
        canvas.pack()
        wait = input("Press enter to continue")
    man.clear()
    tk.mainloop()
