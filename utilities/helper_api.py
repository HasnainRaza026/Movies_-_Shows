import requests
from .logger import logger
from website import API_KEY

BASE_URL = "https://api.themoviedb.org/3"

def SEARCH_MOVIE(movie_id):
    search_url = f"{BASE_URL}/movie/{movie_id}"  # Use the movie endpoint with the ID
    params = {"api_key": API_KEY}

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        # The response is the movie details, no `results` key
        movie_data = response.json()
        
        return {
            "title": movie_data.get("title", "Unknown Title"),
            "rating": movie_data.get("vote_average", "N/A"),
            "poster": f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}" 
                      if movie_data.get("poster_path") else None,
            "description": movie_data.get("overview", "No description available."),
            "year": movie_data.get("release_date", "N/A").split("-")[0] if movie_data.get("release_date") else "N/A"
        }

    except requests.exceptions.HTTPError as http_error:
        if response.status_code == 404:
            logger.warning(f"No movie found for id: {movie_id}")
            return {"error": "Movie not found"}
        else:
            logger.error(f"HTTP error occurred for movie with id: {movie_id}, error: {http_error}")
            return {"error": "Failed to fetch movie details. Please try again later."}
    except requests.exceptions.RequestException as req_error:
        logger.error(f"API request failed for movie with id: {movie_id}, error: {req_error}")
        return {"error": "Failed to connect to the movie database API. Please try again later."}
    except Exception as error:
        logger.error(f"Unexpected error for movie with id: {movie_id}, error: {error}")
        return {"error": "An unexpected error occurred. Please try again later."}



def SUGGEST_MOVIES_OR_SHOWS(content_type, query):
    try:
        # Construct search URL based on content type
        if content_type not in ["movie", "tv"]:
            raise ValueError(f"Invalid content_type: {content_type}. Allowed values are 'movie' or 'tv'.")

        search_url = f"{BASE_URL}/search/{content_type}?api_key={API_KEY}&query={query}"

        response = requests.get(search_url)
        response.raise_for_status()

        data = response.json()
        results = []
        for item in data.get("results", []):
            result = {
                "title": item.get("title") or item.get("name", "Unknown Title"),
                "year": item.get("release_date") or item.get("first_air_date", "N/A")[:4],
                "poster": f"https://image.tmdb.org/t/p/w200{item.get('poster_path')}" if item.get("poster_path") else None,
                "movie_id": item.get("id")
            }
            results.append(result)

        logger.debug(f"Successfully fetched suggestions for keyword '{query}': {results}")
        return results

    except ValueError as val_error:
        logger.error(f"ValueError: {val_error}")
        return {"error": str(val_error)}

    except requests.exceptions.RequestException as req_error:
        logger.error(f"API request failed for suggestions | query: '{query}' | error: {req_error}")
        return {"error": "Failed to connect to the movie database API. Please try again later."}

    except Exception as error:
        logger.error(f"Unexpected error in suggestions API | query: '{query}' | error: {error}")
        return {"error": "An unexpected error occurred. Please try again later."}
    