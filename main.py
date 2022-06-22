from tkinter import *
import pandas
import random
import json

BACKGROUND_COLOR = "#B1DDC6"
rand_nr = 0
from_lang = "French"
to_lang = "English"


# -------------------FUNCTIONS---------------------
def new_card():
    global rand_nr
    canvas.itemconfig(canvas_image, image=card_green)
    rand_nr = f"{random.randint(0, len(to_lang))}"
    canvas.itemconfig(language, text=f"{from_lang}")
    canvas.itemconfig(word, text=f"{ready_data[from_lang][rand_nr]}")
    window.after(3000, flip_card)


def flip_card():
    global rand_nr
    canvas.itemconfig(canvas_image, image=card_white)
    canvas.itemconfig(language, text=f"{to_lang}")
    canvas.itemconfig(word, text=f"{ready_data[to_lang][rand_nr]}")


def to_learn():
    new_data = {
        f"{rand_nr}": {
            from_lang: ready_data[from_lang][rand_nr],
            to_lang: ready_data[to_lang][rand_nr]
        }
    }

    try:
        with open("to_learn.json", "r") as file:
            read_data = json.load(file)
    except FileNotFoundError:
        with open("to_learn.json", "w") as file:
            json.dump(new_data, file, indent=4)
    else:
        if new_data not in read_data.items():
            read_data.update(new_data)
            with open("to_learn.json", "w") as file:
                json.dump(read_data, file, indent=4)
    finally:
        new_card()


def know():
    new_data = {
        f"{rand_nr}": {
            from_lang: ready_data[from_lang][rand_nr],
            to_lang: ready_data[to_lang][rand_nr]
        }
    }

    try:
        with open("know.json", "r") as file:
            read_data = json.load(file)
    except FileNotFoundError:
        with open("know.json", "w") as file:
            json.dump(new_data, file, indent=4)
    else:
        if new_data not in read_data.items():
            read_data.update(new_data)
            with open("know.json", "w") as file:
                json.dump(read_data, file, indent=4)
    finally:
        new_card()


# -------------------UI-------------------------------

window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=100, pady=50)

card_green = PhotoImage(file="images/card_back.png")
card_white = PhotoImage(file="images/card_front.png")

canvas = Canvas(width=800,
                height=526,
                highlightthickness=0,
                bg=BACKGROUND_COLOR)
canvas_image = canvas.create_image(400, 263, image=card_green)
language = canvas.create_text(400, 170,
                              text="txt",
                              font=("Arial", 22, "italic"),
                              fill="#25252a")
word = canvas.create_text(400, 250,
                          text="word",
                          font=("Arial", 60, "normal"),
                          fill="#25252a")
canvas.grid(column=0, row=0)

yes_img = PhotoImage(file="images/right.png")
no_img = PhotoImage(file="images/wrong.png")
yes_btn = Button(image=yes_img,
                 highlightthickness=0,
                 highlightbackground=BACKGROUND_COLOR,
                 command=know).grid(column=0,
                                    row=1,
                                    sticky="e",
                                    padx=140)

no_btn = Button(image=no_img,
                highlightthickness=0,
                highlightbackground=BACKGROUND_COLOR,
                command=to_learn).grid(column=0,
                                       row=1,
                                       sticky="w",
                                       padx=140)

try:
    try:
        with open("data/words.json", "r") as data_file:
            ready_data = json.load(data_file)
    except FileNotFoundError:
        data = pandas.read_csv("data/french_words.csv")
        new_d = data.to_dict()
        with open("data/words.json", "w") as data_file:
            json.dump(new_d, data_file, indent=4)
        with open("data/words.json", "r") as data_file:
            ready_data = json.load(data_file)
    finally:
        new_card()
except FileNotFoundError:
    canvas.itemconfig(language, text=f"Language")
    canvas.itemconfig(word, text=f"word")

window.mainloop()
