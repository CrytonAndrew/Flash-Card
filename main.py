
import tkinter as t
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
words_to_learn = {}
current_card = {}

try:
    data = pandas.read_csv("./data/word_to_learn.csv")
except FileNotFoundError:
    old_data = pandas.read_csv("./data/french_words.csv")
    words_to_learn = old_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")  # Stores each row as a nested dictionary


def generate_next_card():
    global current_card, delay
    screen.after_cancel(id=delay)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=f"{current_card['French']}", fill="black")
    canvas.itemconfig(style, image=image)
    delay = screen.after(3000, func=show_answer)


def show_answer():
    canvas.itemconfig(style, image=back_image)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=f"{current_card['English']}", fill="white")


def is_known():
    words_to_learn.remove(current_card)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_next_card()


screen = t.Tk()
screen.title("Flash Cards")
screen.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

delay = screen.after(ms=3000, func=show_answer)

image = t.PhotoImage(file="./images/card_front.png")
back_image = t.PhotoImage(file="./images/card_back.png")
text1 = t.Label(text="hello", font=("Arial", 25, "bold"))
canvas = t.Canvas(screen, height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
style = canvas.create_image(400, 263, image=image)
language = canvas.create_text(380, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(380, 260, text="", font=("Arial", 50, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

x_image = t.PhotoImage(file="./images/wrong.png")
wrong = t.Button(image=x_image, highlightthickness=0, command=generate_next_card)
wrong.config(pady=0)
wrong.grid(row=1, column=0)

r_image = t.PhotoImage(file="./images/right.png")
right = t.Button(image=r_image, highlightthickness=0, command=is_known)
right.config(pady=0)
right.grid(row=1, column=1)

generate_next_card()

screen.mainloop()
