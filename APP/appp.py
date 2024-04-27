import pickle
import streamlit as st
import requests
import hashlib
import pandas as pd

def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    return data

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie, movies):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append((movies.iloc[i[0]].title, fetch_poster(movie_id), fetch_movie_details(movie_id)))

    return recommended_movies

st.title('Movie Recommender System')

# User login selectbox
user_login = st.sidebar.selectbox("User Login", ['User1','User2','User3','User4'])

movies_list = pickle.load(open(r"C:\Users\devje\OneDrive\Desktop\MACHINE LEARNING PROJECTS\CONTENT BASED MOVIE RECOMMENDER SYSTEM\python model\movie_list.pkl", 'rb'))
similarity = pickle.load(open(r"C:\Users\devje\OneDrive\Desktop\MACHINE LEARNING PROJECTS\CONTENT BASED MOVIE RECOMMENDER SYSTEM\python model\similarity.pkl",'rb'))

movie_list = movies_list['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie, movies_list)
    for movie_title, poster_path, movie_details in recommended_movies:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(poster_path, caption=movie_title, width=100)
        with col2:
            st.subheader(movie_title)
            st.write("**Release Date:**", movie_details['release_date'])
            st.write("**Genre:**", ', '.join([genre['name'] for genre in movie_details['genres']]))
            st.write("**Plot Summary:**", movie_details['overview'])
            st.write("---")

