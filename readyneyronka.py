import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import joblib
import requests
import gzip
import os
from PIL import Image


model_path='./movie_rating_model.keras'
def load_trained_model(model_path):
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


def main(film):
    api_key = "9c4e7486"

    movie_title = film

    movie_data = get_movie_data_from_omdb(api_key, movie_title)

    if movie_data:
        model = load_trained_model(model_path)

        scaler = joblib.load("scaler.pkl")

        predicted_rating = predict_movie_rating(model, movie_data, scaler)
        
        if predicted_rating >= 10:
            return '10'
        else:
            return f"{predicted_rating:.1f}"



if __name__ == "__main__":
    main("Green mile")