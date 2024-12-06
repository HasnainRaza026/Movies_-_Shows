import requests
from .logger import logger
from website import API_KEY

base_url = "https://api.themoviedb.org/3"

def SEARCH_MOVIE(movie_name):
    search_url = f"{base_url}/search/movie"
    params = {"api_key": API_KEY, "query": movie_name}

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        results = response.json().get("results", [])
        
        if not results:
            logger.warning(f"No results found for movie: {movie_name}")
            return {"error": "No results found"}
        
        # Process the first result
        first_result = results[0]
        return {
            "title": first_result.get("title", "Unknown Title"),
            "rating": first_result.get("vote_average", "N/A"),
            "poster": f"https://image.tmdb.org/t/p/w500{first_result.get('poster_path')}" 
                      if first_result.get("poster_path") else None,
            "description": first_result.get("overview", "No description available."),
            "year": first_result.get("release_date", "N/A").split("-")[0] if first_result.get("release_date") else "N/A"
        }

    except requests.exceptions.RequestException as req_error:
        logger.error(f"API request failed for movie: {movie_name}, error: {req_error}")
        return {"error": "Failed to connect to the movie database API. Please try again later."}
    except KeyError as key_error:
        logger.error(f"Unexpected data structure from API for movie: {movie_name}, error: {key_error}")
        return {"error": "Unexpected API response. Please try again later."}
