from flask_socketio import emit
from utilities import helper_api, logger
from utilities.logger import logger
from . import socketio

@socketio.on('search_query')
def handle_search(query):
    logger.debug(f"Received query for suggestions: {query}")

    data = helper_api.SUGGEST_MOVIES_OR_SHOWS(content_type="movie", query=query)
    if "error" in data:
        logger.error(f"Error in fetching suggestions: {data['error']}")
        results = []
    else:
        results = data

    logger.debug(f"Sending search results for query '{query}': {results if results else 'No results found'}")
    emit('search_results', results)

