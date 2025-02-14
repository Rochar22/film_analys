from readyneyronka import main
from pathlib import Path
from PIL import ImageTk, Image
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import requests
from io import BytesIO
from main import create_and_train_model
import pandas as pd
import gzip
import shutil
import os
import time

def delete_text(text_id):
    canvas.delete(text_id)

def swap_rating(new_rating, Title, text):
    url = f"http://www.omdbapi.com/?t={Title}&apikey=9c4e7486"
    response = requests.get(url)
    data = response.json()
    try:
        movie_data = {
        "filmname": data["Title"],
        }
    except:
        canvas.itemconfig(text, text=f'Фильма {Title} не существует', fill='#FF2400')
        return 0
    create_and_train_model(new_rating, movie_data["filmname"])
    canvas.itemconfig(text, text=f'Оценка {movie_data["filmname"]} изменена на {new_rating}', fill='#00ff2a')


    



def validate_digit_input(new_value): 
    if new_value == "": 
        return True 
    elif (new_value.isdigit() or (new_value[0].isdigit() and new_value[1] == '.' and new_value[2:].isdigit)) and float(new_value)<=10 and len(new_value)<=4:
        return True
    else: 
        return False

def relative_to_assets(path: str, assets_path) -> Path:
    return assets_path / Path(path)

def checking_film(button_rait,button_check,movie_title,*args):
    flag = True
    for i in args:
        if str(i).isdigit():
            canvas.delete(i)
        else:
            i.grid()
            i.destroy()
    film(button_rait, button_check, movie_title)

def film(button_rait,button_check, movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=9c4e7486"
    response = requests.get(url)
    data = response.json()

    basics = pd.read_csv("title.basics.tsv", sep="\t")
    ratings = pd.read_csv("title.ratings.tsv", sep="\t")


    movie_data = {"startYear": data["Released"],
            "runtimeMinutes": data["Runtime"],
            "genres": data["Genre"],
            'poster': data['Poster'],
            'filmname': data['Title'],
            "imdbRating": data["imdbRating"]}
    
    id = basics.loc[basics['primaryTitle'] == movie_data["filmname"], 'tconst'].values[1]
    user_rating = ratings.loc[ratings['tconst'] == id, 'averageRating'].values[0]
    print(id,user_rating)

    predict_rating = main(movie_title)

    im = requests.get(movie_data["poster"])

    posterim = Image.open(BytesIO(im.content)).resize((212,294))
    image_image_2 = ImageTk.PhotoImage(
        posterim, [100,100])
    poster = canvas.create_image(
        307.0,
        222.0,
        image=image_image_2
    )

    nickname = canvas.create_text(
        55.0,
        24.0,
        anchor="nw",
        text="Nickname\n\n\n",
        fill="#FFFFFF",
        font=("Inter", 12 * -1)
    )

    film_name = canvas.create_text(
        209.0,
        16.0,
        anchor="nw",
        text=movie_data["filmname"],
        fill="#FFFFFF",
        font=("Jaldi Regular", 48 * -1)
    )

    video = canvas.create_rectangle(
        424.0,
        76.0,
        931.0,
        369.0,
        fill="#288B1B",
        outline="")

    imdb_rating = canvas.create_text(
        720.0,
        15.0,
        anchor="nw",
        text="IMDb RATING",
        fill="#B1ABAB",
        font=("Jaldi Regular", 14 * -1)
    )

    ai_rating = canvas.create_text(
        827.0,
        15.0,
        anchor="nw",
        text="AI RATING",
        fill="#B1ABAB",
        font=("Jaldi Regular", 14 * -1)
    )

    num_rate_imdb = canvas.create_text(
        715.0,
        31.0,
        anchor="nw",
        text=movie_data["imdbRating"],
        fill="#FFFFFF",
        font=("Inter", 32 * -1)
    )

    num_rate_ai = canvas.create_text(
        824.0,
        32.0,
        anchor="nw",
        text=predict_rating,
        fill="#FFFFFF",
        font=("Inter", 32 * -1)
    )

    of_ten = canvas.create_text(
        766.0,
        31.0,
        anchor="nw",
        text="/10",
        fill="#B1ACAC",
        font=("Inter", 20 * -1)
    )

    of_ten2 = canvas.create_text(
        875.0,
        32.0,
        anchor="nw",
        text="/10",
        fill="#B1ACAC",
        font=("Inter", 20 * -1)
    )

    runtime = canvas.create_text(
        209.0,
        373.0,
        anchor="nw",
        text="Runtime",
        fill="#FFFFFF",
        font=("Jaldi Regular", 24 * -1)
    )

    realesed = canvas.create_text(
        209.0,
        407.0,
        anchor="nw",
        text="Released ",
        fill="#FFFFFF",
        font=("Jaldi Regular", 24 * -1)
    )

    genre = canvas.create_text(
        209.0,
        438.0,
        anchor="nw",
        text="Genre",
        fill="#FFFFFF",
        font=("Jaldi Regular", 24 * -1)
    )

    value_of_runtime = canvas.create_text(
        303.0,
        374.0,
        anchor="nw",
        text=movie_data["runtimeMinutes"],
        fill="#6391E7",
        font=("Jaldi Regular", 24 * -1)
    )

    value_of_realesed = canvas.create_text(
        315.0,
        407.0,
        anchor="nw",
        text=movie_data['startYear'],
        fill="#6391E7",
        font=("Inter", 24 * -1)
    )

    value_of_genre = canvas.create_text(
        283.0,
        440.0,
        anchor="nw",
        text=movie_data['genres'],
        fill="#6391E7",
        font=("Inter", 24 * -1)
    )

    user_txt_rating = canvas.create_text(
        615.0,
        15.0,
        anchor="nw",
        text="YOUR RATING",
        fill="#B1ABAB",
        font=("Jaldi Regular", 14 * -1)
    )
    num_rate_user = canvas.create_text(
        610.0,
        31.0,
        anchor="nw",
        text=user_rating,
        fill="#FFFFFF",
        font=("Inter", 32 * -1)
    )
    of_ten3 = canvas.create_text(
        661.0,
        31.0,
        anchor="nw",
        text="/10",
        fill="#B1ACAC",
        font=("Inter", 20 * -1)
    )





    button_rait.config(command=lambda:add_rating(button_rait,button_check,ai_rating,imdb_rating,num_rate_ai,num_rate_imdb,film_name,poster,realesed,genre,runtime,value_of_genre,value_of_realesed,value_of_runtime,video,of_ten,of_ten2, nickname, of_ten3, user_txt_rating, num_rate_user))
    window.mainloop()


    

def add_rating(add_rating_button,checker_button,*args):
    add_rating_button.config(state='disabled')

    for i in args:
        if str(i).isdigit():
            canvas.delete(i)
        else:
            i.grid()
            i.destroy()

        nickname = canvas.create_text(
        55.0,
        24.0,
        anchor="nw",
        text="Nickname\n\n\n",
        fill="#FFFFFF",
        font=("Inter", 12 * -1)
    )

    new_rating_entry_image = PhotoImage(
    file=relative_to_assets("entry_1.png", ASSETS_PATH1))
    entry_bg_1 = canvas.create_image(
        650.0,
        253,
        image=new_rating_entry_image,
    )

    film = canvas.create_text(
        196.0,
        175.0,
        anchor="nw",
        text="Film:",
        fill="#FFFFFF",
        font=("Inter", 36 * -1)
    )

    new_rating = canvas.create_text(
        509.0,
        175.0,
        anchor="nw",
        text="New Rating:",
        fill="#FFFFFF",
        font=("Inter", 36 * -1)
    )

    validate_digit_command = window.register(validate_digit_input)
    new_rating_entry = Entry(
        bd=0,
        bg="#383232",
        fg="#ffffff",
        highlightthickness=0,
        font=("Inter", 45 * -1),
        validate='key',
        validatecommand=(validate_digit_command, '%P')
    )

    new_rating_entry.place(
        x=519.0,
        y=220.0,
        width=262.0,
        height=65.0
    )

    congratulations = canvas.create_text(
    200.0,
    300.0,
    anchor="nw",
    text=".",
    fill="#00ff2a",
    font=("Inter", 32 * -1),
)
    film_image = PhotoImage(
        file=relative_to_assets("entry_2.png", ASSETS_PATH1))
    entry_bg_2 = canvas.create_image(
        340.0,
        253.0,
        image=film_image
    )

    film_entry = Entry(
        bd=0,
        bg="#383232",
        fg="#ffffff",
        highlightthickness=0,
        font=("Inter", 45 * -1),
    )

    film_entry.place(
        x=211,
        y=220,
        width=262.0,
        height=65.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png", ASSETS_PATH1))
    button_add = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: swap_rating(new_rating_entry.get(), film_entry.get(), congratulations),
        relief="flat"
    )
    button_add.place(
        x=800.0,
        y=223.0,
        width=60,
        height=60
    )
    checker_button.config(state='normal', command=lambda: checker_film(film=film,new_rating=new_rating,film_entry=film_entry,new_rating_entry=new_rating_entry,button_add=button_add, congratulations=congratulations,new_rating_entry_image=entry_bg_1,film_entry_image=entry_bg_2))
    window.mainloop()


def checker_film(film=None, new_rating=None, film_entry=None, new_rating_entry=None, button_add=None,new_rating_entry_image=None, film_entry_image=None, congratulations=None ):
    canvas.delete(film)
    canvas.delete(new_rating)
    canvas.delete(new_rating_entry_image)
    canvas.delete(film_entry_image)
    canvas.delete(congratulations)
    try:
        film_entry.grid()
        film_entry.destroy()
        new_rating_entry.grid()
        new_rating_entry.destroy()
        button_add.grid()
        button_add.destroy()
    except:
        pass

    if not os.path.exists("title.basics.tsv"):
        os.system("curl -o ./title.basics.tsv.gz https://datasets.imdbws.com/title.basics.tsv.gz")
        with gzip.open('title.basics.tsv.gz', 'rb') as f_in:
            with open('title.basics.tsv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    if not os.path.exists("title.ratings.tsv"):
        os.system("curl -o ./title.ratings.tsv.gz https://datasets.imdbws.com/title.ratings.tsv.gz")
        with gzip.open('title.ratings.tsv.gz', 'rb') as f_in:
            with open('title.ratings.tsv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)





    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png", ASSETS_PATH))
    image_1 = canvas.create_image(
        34.0,
        31.0,
        image=image_image_1
    )

    nickname = canvas.create_text(
        55.0,
        24.0,
        anchor="nw",
        text="Nickname\n\n\n",
        fill="#FFFFFF",
        font=("Inter", 12 * -1)
    )

    entry_image = PhotoImage(
        file=relative_to_assets("entry_1.png", ASSETS_PATH))
    film_for_checking_image = canvas.create_image(
        483.0,
        253.0,
        image=entry_image
    )
    film_for_checking = Entry(
        bd=0,
        bg="#383232",
        fg="#ffffff",
        highlightthickness=0,
        font=('Inter', 36 * -1)
    )
    film_for_checking.place(
        x=211.0,
        y=220.0,
        width=544.0,
        height=65.0
    )

    checker_text = canvas.create_text(
        196,
        175,
        anchor="nw",
        text="Check your film:",
        fill="#FFFFFF",
        font=("Inter", 36 * -1)
    )

    button_loupe_image = ImageTk.PhotoImage(Image.open("./assets/frame0/image.png"))
    button_loupe = Button(
        image=button_loupe_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: checking_film(add_rating_button,checker_button,film_for_checking.get(),button_loupe, film_for_checking, film_for_checking_image, checker_text, nickname),
        relief="flat"
    )
    button_loupe.place(
        x=773.0,
        y=218.0,
        width=70.0,
        height=69.0
    )

    checker_button_image = PhotoImage(
        file=relative_to_assets("button_2.png",ASSETS_PATH))
    checker_button = Button(
        image=checker_button_image,
        borderwidth=0,
        state='disabled',
        highlightthickness=0,
        command=lambda: checker_film(),
        relief="flat"
    )
    checker_button.place(
        x=10.0,
        y=84.0,
        width=136.0,
        height=60.0
    )

    add_rating_button_image = PhotoImage(
        file=relative_to_assets("button_3.png", ASSETS_PATH))
    add_rating_button = Button(
        image=add_rating_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: add_rating(add_rating_button,checker_button,checker_text,film_for_checking_image,film_for_checking,button_loupe, nickname),
        relief="flat"
    )
    add_rating_button.place(
        x=10.0,
        y=172.0,
        width=136.0,
        height=60.49079895019531
    )
    window.mainloop()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")
ASSETS_PATH1 = OUTPUT_PATH / Path(r"./assets/frame1")
ASSETS_PATH2 = OUTPUT_PATH / Path(r"./assets/frame2")

window = Tk()

window.geometry("950x506")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 506,
    width = 950,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    177.0,
    506.0,
    fill="#282424",
    outline="")

canvas.create_rectangle(
    177.0,
    0.0,
    950.0,
    506.0,
    fill="#282424",
    outline="")

canvas.create_rectangle(
    176.0,
    -1.0,
    177.00000000000006,
    506.0009765625,
    fill="#000000",
    outline="")

window.resizable(False, False)
checker_film()
window.mainloop()
