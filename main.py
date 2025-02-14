import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import joblib
import requests
import gzip
import os
import zipfile 

file_path = "./"

def save_data_to_file(data, file_path):
    """
    Сохраняет DataFrame обратно в файл .tsv.
    """
    data.to_csv(file_path)
    print(f"Данные сохранены в файл: {file_path}")


def update_movie_rating(basics, ratings, new_rating, movie_title):
    id = basics.loc[basics['primaryTitle'] == movie_title, 'tconst'].values[1]
    ratings.loc[ratings['tconst'] == id, 'averageRating'] = int(new_rating)
    print(f"Рейтинг фильма '{movie_title}' обновлён до {new_rating}.")
    



def load_and_process_imdb_data(new_rating, movie_title):



    basics = pd.read_csv("title.basics.tsv", dtype=str, sep="\t")
    ratings = pd.read_csv("title.ratings.tsv", dtype=str, sep="\t")

    update_movie_rating(basics,ratings,new_rating, movie_title)
    basics.to_csv('./title.basics.tsv')
    ratings.to_csv('./title.ratings.tsv')

    basics = basics[basics["titleType"] == "movie"]

    basics = basics[["tconst", "primaryTitle", "startYear", "runtimeMinutes", "genres"]]
    ratings = ratings[["tconst", "averageRating", "numVotes"]]
    

    basics = basics.replace("\\N", np.nan).dropna()
    ratings = ratings.replace("\\N", np.nan).dropna()


    basics["startYear"] = basics["startYear"].astype(int)
    basics["runtimeMinutes"] = basics["runtimeMinutes"].astype(int)
    ratings["averageRating"] = ratings["averageRating"].astype(float)
    ratings["numVotes"] = ratings["numVotes"].astype(int)
    
    data = pd.merge(basics, ratings, on="tconst")
    
    genres_list = ['Action', 'Adventure', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Horror',
                   'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    for genre in genres_list:
        data[genre] = data['genres'].apply(lambda x: 1 if genre in x.split(',') else 0)


    
    data = data.drop(columns=["tconst", "primaryTitle", "genres"])

    return data


def create_and_train_model(new_rating, movie_title):

    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=9c4e7486"
    response = requests.get(url)
    data = response.json()
    movie_data = {'film': data['Title']}
    data = load_and_process_imdb_data(new_rating, movie_data["film"])

    X = data.drop(columns=["averageRating"])
    y = data["averageRating"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    joblib.dump(scaler, "scaler.pkl")

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_dim=X_scaled.shape[1]),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])


    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    model.fit(X_scaled, y, epochs=10, batch_size=32)


    model.save("movie_rating_model.keras")
    print("Модель и scaler успешно сохранены.")



def load_trained_model(model_path="movie_rating_model.keras"):
    model = tf.keras.models.load_model(model_path)
    return model


def get_movie_data_from_omdb(api_key, movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["Response"] == "True":
        movie_data = {
            "startYear": int(data["Year"]),
            "runtimeMinutes": int(data["Runtime"].split(" ")[0]),
            "numVotes": int(data["imdbVotes"].replace(",", "")),
            "genres": data["Genre"].split(", ")
        }
        return movie_data
    else:
        print("Ошибка получения данных фильма")
        return None


def preprocess_input_data(movie_data, scaler):
    genres_list = ['Action', 'Adventure', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Horror',
                   'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']


    genres = movie_data["genres"]
    genre_vector = [1 if genre in genres else 0 for genre in genres_list]

    start_year = movie_data["startYear"]
    runtime_minutes = movie_data["runtimeMinutes"]
    num_votes = movie_data["numVotes"]

    movie_features = [start_year, runtime_minutes, num_votes] + genre_vector
 
    movie_features = np.array([movie_features])


    movie_features_scaled = scaler.transform(movie_features)

    return movie_features_scaled



def predict_movie_rating(model, movie_data, scaler):
    input_data = preprocess_input_data(movie_data, scaler)

    prediction = model.predict(input_data)

    return prediction[0][0]


def main():
    api_key = "9c4e7486"

    movie_title = "Fight club"

    create_and_train_model()

    movie_data = get_movie_data_from_omdb(api_key, movie_title)

    if movie_data:
        model = load_trained_model()

        scaler = joblib.load("scaler.pkl")
        predicted_rating = predict_movie_rating(model, movie_data, scaler)
        if predicted_rating >= 10:
            print(f"Предсказанная оценка фильма '{movie_title}': 10/10")
        else:
            print(f"Предсказанная оценка фильма '{movie_title}': {predicted_rating}/10")


if __name__ == "__main__":
    main()