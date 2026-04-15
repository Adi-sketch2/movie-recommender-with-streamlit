import streamlit as st
import pickle
import difflib
import requests
import os
from dotenv import load_dotenv
import gdown

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.movie-card {
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    background-color: #1c1f26;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Find movies similar to your favorites</h4>", unsafe_allow_html=True)

load_dotenv()
api_key = os.getenv("OMDB_API_KEY")

if not os.path.exists("models"):
    os.makedirs("models")

MOVIES_URL = "https://drive.google.com/uc?id=1PXVAz5R4jFvCGqPgurN0DZEWtNBwpaFh"
SIMILARITY_URL = "https://drive.google.com/uc?id=1R3BqI3HKtm-y-9ZfqTAzktTNmESBX_FP"

if (not os.path.exists("models/movies.pkl") or 
    not os.path.exists("models/similarity.pkl")):

    with st.spinner("Downloading model, please wait..."):
        if not os.path.exists("models/movies.pkl"):
            gdown.download(MOVIES_URL, "models/movies.pkl", quiet=False)

        if not os.path.exists("models/similarity.pkl"):
            gdown.download(SIMILARITY_URL, "models/similarity.pkl", quiet=False)

new_df = pickle.load(open('models/movies.pkl','rb'))
similarity = pickle.load(open('models/similarity.pkl','rb'))

def fetch_poster(movie_title):
    clean_title = movie_title.split("(")[0]
    url = f"http://www.omdbapi.com/?t={clean_title}&apikey={api_key}"
    data = requests.get(url).json()

    poster = "https://via.placeholder.com/300x450.png?text=No+Image"
    rating = "N/A"

    if data.get('Response') == 'True':
        if data.get('Poster') != "N/A":
            poster = data.get('Poster')
        if data.get('imdbRating') != "N/A":
            rating = data.get('imdbRating')

    return poster, rating

def recommend(movie):
    movie_lower = movie.lower()
    matches = new_df[new_df['title'].str.lower().str.contains(movie_lower)]

    if not matches.empty:
        movie = matches.iloc[0].title
    else:
        movie_list = new_df['title'].tolist()
        match = difflib.get_close_matches(movie, movie_list, n=1)

        if not match:
            return [], [], []

        movie = match[0]

    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         key=lambda x: x[1],
                         reverse=True)[1:8]

    names = []
    posters = []
    ratings = []

    for i in movies_list:
        title = new_df.iloc[i[0]].title
        poster, rating = fetch_poster(title)

        names.append(title)
        posters.append(poster)
        ratings.append(rating)

    return names, posters, ratings

movie_name = st.text_input("Enter a movie name")

if st.button("Recommend"):
    if movie_name:
        with st.spinner("Loading..."):
            names, posters, ratings = recommend(movie_name)

        st.markdown("## Top Recommendations")
        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns(4)

        for i in range(len(names)):
            with cols[i % 4]:
                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                st.image(posters[i])
                st.markdown(f"<h5>{names[i]}</h5>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:gold;'>⭐ {ratings[i]}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a movie name")