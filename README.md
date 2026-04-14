
# Movie Recommender System

A content-based movie recommendation system built using Machine Learning and deployed with a Streamlit web interface.

## Overview

This project recommends movies similar to a given input using features such as genres, keywords, cast, and overview. It uses text vectorization and cosine similarity to find similar movies and displays results with posters.

## Features

* Content-based recommendation
* Fuzzy search support
* Streamlit web interface
* Movie posters using OMDb API
* Clean grid layout UI

## Tech Stack

* Python
* Pandas
* Scikit-learn
* Streamlit
* Requests
* python-dotenv

## Project Structure

```
movieset/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env
│
├── data/
│   ├── movies.csv
│   ├── credits.csv
│   ├── cleaned_movies.csv
│
├── models/   (auto-downloaded at runtime)
│
├── notebooks/
│   ├── movie.ipynb
│   ├── model.ipynb
```

## Models (Important)

The model files are not stored in this repository due to large file size limits on GitHub.

Instead, they are downloaded automatically at runtime from Google Drive.

* `movies.pkl` → processed dataset
* `similarity.pkl` → cosine similarity matrix

These files are required for the recommendation system to work.

## How it Works

1. User enters a movie name
2. System finds closest match using fuzzy search
3. Features are compared using cosine similarity
4. Top similar movies are returned
5. Posters are fetched using OMDb API

## Setup Instructions

1. Clone the repository

```
git clone https://github.com/your-username/movie-recommender-system.git
cd movie-recommender-system
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Add your API key

Create a `.env` file and add:

```
OMDB_API_KEY=your_api_key_here
```

4. Run the app

```
streamlit run app.py
```

## Notes

* Model files are downloaded automatically when the app runs
* No need to manually add `.pkl` files
* Make sure you have internet connection on first run

## Future Improvements

* Add more datasets (Bollywood + Hollywood)
* Improve recommendation accuracy
* Add filters (genre, rating)
* Deploy with faster model loading

## Author

Adi
