"""A Flash Card game to help study words"""

from random import choice
from os.path import exists
from tkinter import Tk, Canvas, Button, PhotoImage
from pandas import DataFrame, read_csv

BACKGROUND_COLOR = "#B1DDC6"
FRENCH = ("Ariel", 40, "italic")
ENGLISH = ("Ariel", 60, "bold")

class Flashy:
    """A Flash Card game to help study words"""

    def __init__(self):
        self.root = Tk()
        self.root.title("Flashy")
        self.root.resizable(False, False)
        self.root.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

        self.canvas = Canvas(bg=BACKGROUND_COLOR, width=800, height=526, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.bg_image = PhotoImage(file=r"images\card_front.png")
        self.bg_image_back = PhotoImage(file=r"images\card_back.png")
        self.correct_image = PhotoImage(file=r"images\right.png")
        self.wrong_image = PhotoImage(file=r"images\wrong.png")
        self.background = self.canvas.create_image(400, 263, image=self.bg_image)
        self.card_title = self.canvas.create_text(400, 150, text="", font=FRENCH)
        self.card_word = self.canvas.create_text(400, 263, text="", font=ENGLISH)

        correct = Button(image=self.correct_image, highlightthickness=0, bd=0, activebackground=BACKGROUND_COLOR, command=self.is_known)
        correct.grid(row=1, column=1)
        wrong = Button(image=self.wrong_image, highlightthickness=0, bd=0, activebackground=BACKGROUND_COLOR, command=self.next_card)
        wrong.grid(row=1, column=0)

        if exists("data/words_to_learn.csv"):
            self.data = read_csv('data/words_to_learn.csv').to_dict(orient="records")
        else:
            self.data = read_csv('data/french_words.csv').to_dict(orient="records")

        self.flip_timer = self.root.after(3000, self.flip_card)
        self.next_card()

        self.root.mainloop()


    def next_card(self):
        """Generates a random word"""
        self.root.after_cancel(self.flip_timer)
        self.chosen_word = choice(self.data)
        self.canvas.itemconfig(self.background, image=self.bg_image)
        self.canvas.itemconfig(self.card_title, text='French', fill='black')
        self.canvas.itemconfig(self.card_word, text=self.chosen_word['French'], fill='black')
        self.flip_timer = self.root.after(3000, self.flip_card)


    def flip_card(self):
        """Flips the card"""
        self.canvas.itemconfig(self.background, image=self.bg_image_back)
        self.canvas.itemconfig(self.card_title, text='English', fill='white')
        self.canvas.itemconfig(self.card_word, text=self.chosen_word['English'], fill='white')


    def is_known(self):
        """Removes the current word from the card stack and generates a new card"""
        self.data.remove(self.chosen_word)
        new_data = DataFrame(self.data)
        new_data.to_csv("data/words_to_learn.csv", index=False)
        self.next_card()


if __name__ == "__main__":
    test = Flashy()
