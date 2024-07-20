import streamlit as st
import os
import pickle
import requests

# Get the current working directory
base_path = os.path.dirname(__file__)

# Construct the absolute path to your pickle files
file_path = os.path.join(base_path, 'movies_list.pkl')
file_path1 = os.path.join(base_path, 'similarity.pkl')

# Load the pickle files
try:
    with open(file_path, 'rb') as file:
        movies_data = pickle.load(file)
        movies_list = movies_data['title'].values
    with open(file_path1, 'rb') as file:
        similarity = pickle.load(file)
except FileNotFoundError:
    st.error(f"File '{file_path}' not found.")
    st.stop()
except Exception as e:
    st.error(f"Error loading pickle file: {e}")
    st.stop()

st.header("Movie Recommender System")
selectValue = st.selectbox("Select movie from dropdown", movies_list)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=33c924339c54a6880c6484fcabed9490"
    data = requests.get(url).json()
    if 'poster_path' in data and data['poster_path']:
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    else:
        # Return a placeholder image URL or None if no poster is available
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

def recommend(movie):
    index = movies_data[movies_data['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distances[1:6]:
        movie_id = movies_data.iloc[i[0]].id
        recommend_movie.append(movies_data.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

if st.button("Show Recommendation"):
    movie_name, movie_poster = recommend(selectValue)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(movie_name[idx])
            st.image(movie_poster[idx])
