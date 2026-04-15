import pickle
import difflib
import requests
import os
from dotenv import load_dotenv
import gdown

load_dotenv()
api_key = os.getenv("OMDB_API_KEY")

if not os.path.exists("models"):
    os.makedirs("models")

MOVIES_URL = "https://drive.google.com/uc?id=1PXVAz5R4jFvCGqPgurN0DZEWtNBwpaFh"
SIMILARITY_URL = "https://drive.google.com/uc?id=1R3BqI3HKtm-y-9ZfqTAzktTNmESBX_FP"

if not os.path.exists("models/movies.pkl"):
    print("Downloading movies data...")
    gdown.download(MOVIES_URL, "models/movies.pkl", quiet=False)

if not os.path.exists("models/similarity.pkl"):
    print("Downloading similarity model...")
    gdown.download(SIMILARITY_URL, "models/similarity.pkl", quiet=False)

new_df = pickle.load(open('models/movies.pkl','rb'))
similarity = pickle.load(open('models/similarity.pkl','rb'))


def fetch_poster(movie_title):
    clean_title = movie_title.split("(")[0]
    url = f"http://www.omdbapi.com/?t={clean_title}&apikey={api_key}"
    data = requests.get(url).json()

    poster = "No Image"
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
            print("Movie not found")
            return

        movie = match[0]

    print(f"\nShowing results for: {movie}")
    print("-" * 40)

    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         key=lambda x: x[1],
                         reverse=True)[1:6]

    print("\nTop Recommendations:\n")

    for i in movies_list:
        title = new_df.iloc[i[0]].title
        poster, rating = fetch_poster(title)

        print(f"Movie: {title}")
        print(f"Rating: ⭐ {rating}")
        print(f"Poster: {poster}")
        print("-" * 40)


if __name__ == "__main__":
    movie_name = input("Enter movie name: ")
    recommend(movie_name)