import tkinter as tk
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Courier"
timer = None

# ---------------------------- DATA CLEANING ------------------------------- #
words_dict = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
    df = pandas.DataFrame(data)
    words_dict = df.to_dict(orient='records')
else:
    df = pandas.DataFrame(data)
    words_dict = df.to_dict(orient='records')


# ---------------------------- BUTTONS MECHANISMS ------------------------------- #
current_card = {}
known_cards = []


def new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_dict)
    canvas.itemconfig(card_title, text="French", fill='black')
    canvas.itemconfig(card_text, text=current_card['French'], fill='black')
    canvas.itemconfig(card_bg, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill='white')
    canvas.itemconfig(card_text, text=current_card['English'], fill='white')
    canvas.itemconfig(card_bg, image=card_back_bg)


def know_word():
    global known_cards
    known_cards.append(current_card)
    words_learned = pandas.DataFrame(known_cards)
    words_learned.to_csv('./data/words_learned.csv', index=False)
    words_dict.remove(current_card)
    words_to_learn = pandas.DataFrame(words_dict)
    words_to_learn.to_csv('./data/words_to_learn.csv', index=False)
    new_card()




# ---------------------------- UI SETUP ------------------------------- #


window = tk.Tk()
window.title('Dany Flash Cards')
window.minsize(width=1000, height=700)
window.config(padx=80, pady=20, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = tk.PhotoImage(file="./images/card_front.png")
card_bg = canvas.create_image(400, 263, image=card_front_img)
card_back_bg = tk.PhotoImage(file="./images/card_back.png")
card_title = canvas.create_text(400, 150, text="French", fill='black', font=(FONT_NAME, 35))
card_text = canvas.create_text(400, 250, text="Trouve", fill='black', font=(FONT_NAME, 35, 'bold'))
canvas.grid(row=1, column=1, columnspan=3)

wrong_img = tk.PhotoImage(file=".\images\wrong.png")
wrong_button = tk.Button(image=wrong_img, highlightthickness=0, command=new_card)
wrong_button.grid(row=3, column=1)

right_img = tk.PhotoImage(file=".\images\\right.png")
right_button = tk.Button(image=right_img, highlightthickness=0, command=know_word)
right_button.grid(row=3, column=3)

# ---------------------------- ALGORITH ------------------------------- #


new_card()

window.mainloop()
