from sqlalchemy.exc import SQLAlchemyError
from website import db
from website.models import Top_10_Movies, All_Movies
from .logger import logger

def Add(form):
    try:
        if form.ranking.data:
            movie = Top_10_Movies(
                title=form.title.data, year=2000, description="sample description", rating=7.8, 
                rank=form.ranking.data, review=form.review.data, img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
            )
        else:
            movie = All_Movies(
                title=form.title.data, year=2000, rating=7.8, review=form.review.data, 
                img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
            )

        db.session.add(movie)
        db.session.flush()  # Ensures the data is valid before committing
        db.session.commit()

        logger.info(f"Successfully added Movie: {form.title.data} (Rank: {form.ranking.data if form.ranking.data else 'N/A'}) to the Database")
        return True

    except SQLAlchemyError as db_error:
        # Handle SQLAlchemy-related errors (e.g., database connectivity, integrity constraints)
        logger.error(f"Database error while adding Movie '{form.title.data}': {db_error}")
        db.session.rollback()  # Rollback in case of an error
    except AttributeError as attr_err:
        # Handle case where the movie object doesn't have the expected attributes
        logger.error(f"AttributeError while adding Movie ('{form.title.data}'): {attr_err}")
        db.session.rollback()
    except Exception as error:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error while adding Movie '{form.title.data}': {error}")
        db.session.rollback()

    return False


def Get_All():
    try:
        top_10_movies = Top_10_Movies.query.limit(10).all()  # Limit to 10 if needed
        all_movies = All_Movies.query.all()  # Fetch all movies

        logger.info(f"Fetched {len(top_10_movies)} top 10 movies and {len(all_movies)} all movies from the database.")
        return (top_10_movies, all_movies)
    
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while fetching movies: {db_error}")
        return ([], [])  # Return empty lists to prevent breaking the route
    except Exception as error:
        logger.error(f"Unexpected error while fetching movies: {error}")
        return ([], [])  # Return empty lists in case of an error



def Get(id, table=Top_10_Movies):
    try:
        movie = table.query.get(id)
        
        if movie:
            logger.info(f"Successfully fetched Movie with id={id} from {table.__tablename__}.")
        else:
            logger.warning(f"No Movie found with id={id} in {table.__tablename__}.")
        return movie
    
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while fetching Movie with id={id} from {table.__tablename__}: {db_error}")
        return None
    except Exception as error:
        logger.error(f"Unexpected error while fetching Movie with id={id} from {table.__tablename__}: {error}")
        return None
    


def Edit(movie, column_name, data):
    try:
        # Validate if the column exists on the movie object
        if not hasattr(movie, column_name):
            logger.error(f"Invalid column name '{column_name}' for Movie ID {movie.id}")
            return False

        # Dynamically update the column
        setattr(movie, column_name, data)

        db.session.flush()
        db.session.commit()

        logger.info(f"Successfully updated Movie ID {movie.id}: Set [{column_name}] to '{data}'")
        return True
    
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while editing Movie ID {movie.id} ('{movie.title}'): {db_error}")
        db.session.rollback()
    except AttributeError as attr_err:
        logger.error(f"AttributeError while editing Movie ID {movie.id}: {attr_err}")
        db.session.rollback()
    except Exception as error:
        logger.error(f"Failed to edit Movie ID {movie.id} --> ERROR: {error}")
        db.session.rollback()

    return False



def Delete(movie):
    try:
        db.session.delete(movie)
        db.session.flush()
        db.session.commit()

        logger.info(f"Successfully deleted Movie ID {movie.id}: {movie.title}")
        return True
    
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while deleting Movie ID {movie.id} ('{movie.title}'): {db_error}")
        db.session.rollback
    except AttributeError as attr_err:
        logger.error(f"AttributeError while deleting Movie ID {movie.id} ('{movie.title}'): {attr_err}")
        db.session.rollback()
    except Exception as error:
        logger.error(f"Unexpected error while deleting Movie ID {movie.id} ('{movie.title}'): {error}")
        db.session.rollback()

    return False

