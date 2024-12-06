import requests
from .logger import logger
from website import API_KEY

BASE_URL = "https://api.themoviedb.org/3"

def SEARCH_MOVIE(movie_name):
    search_url = f"{BASE_URL}/search/movie"
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
