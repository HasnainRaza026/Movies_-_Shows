import requests
from flask_socketio import emit

from . import socketio, API_KEY

@socketio.on('search_query')
def handle_search(query):
    # print(f"Received query: {query}") # Debug

    # TMDb API endpoint
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        results = [
            {
                "title": movie["title"],
                "year": movie.get("release_date", "N/A")[:4],
                "poster": f"https://image.tmdb.org/t/p/w200{movie['poster_path']}" if movie.get("poster_path") else None
            }
            for movie in data.get("results", [])
        ]
        # print(f"Emitting results: {results}")  # Debug
    else:
        print(f"Error fetching data from TMDb: {response.status_code}")
        results = []

    emit('search_results', results)
