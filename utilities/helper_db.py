from sqlalchemy.exc import SQLAlchemyError
from website import db
from website.models import Top_10_Movies, All_Movies
from .logger import logger

from sqlalchemy.exc import SQLAlchemyError

def Add(form, data):
    try:
        if form.ranking.data:
            # Check if the Top_10_Movies table already has 10 entries
            top_10_count = Top_10_Movies.query.count()
            if top_10_count >= 10:
                logger.warning("Top_10_Movies table already has 10 entries. Cannot add more.")
                return "TOP_10_FULL"

            # Adjust rankings if necessary
            existing_movie = Top_10_Movies.query.filter_by(rank=form.ranking.data).first()
            if existing_movie:
                # Temporarily shift ranks to avoid conflicts
                movies_to_shift = Top_10_Movies.query.filter(
                    Top_10_Movies.rank >= form.ranking.data
                ).order_by(Top_10_Movies.rank.desc()).all()

                # Temporarily increase ranks
                for movie in movies_to_shift:
                    movie.rank += 10  # Temporarily shift ranks

                db.session.flush()  # Apply temporary shifts

                # Adjust ranks to the correct positions
                for movie in movies_to_shift:
                    movie.rank -= 9  # Shift back to the correct rank

            # Create a new movie with the specified rank
            movie = Top_10_Movies(
                title=data.get("title"),
                year=data.get("year"),
                description=data.get("description"),
                rating=data.get("rating"),
                rank=form.ranking.data,
                review=form.review.data,
                img_url=data.get("poster")
            )
        else:
            # Adding to All_Movies table
            movie = All_Movies(
                title=data.get("title"),
                year=data.get("year"),
                rating=data.get("rating"),
                review=form.review.data,
                img_url=data.get("poster")
            )

        db.session.add(movie)
        db.session.flush()  # Ensures data validity before committing
        db.session.commit()

        logger.info(f"Successfully added Movie: {data.get('title')} (Rank: {form.ranking.data if form.ranking.data else 'N/A'}) to the Database")
        return "SUCCESS"

    except SQLAlchemyError as db_error:
        logger.error(f"Database error while adding Movie '{data.get('title')}': {db_error}")
        db.session.rollback()
    except AttributeError as attr_err:
        logger.error(f"AttributeError while adding Movie '{data.get('title')}': {attr_err}")
        db.session.rollback()
    except Exception as error:
        logger.error(f"Unexpected error while adding Movie '{data.get('title')}': {error}")
        db.session.rollback()

    return "ERROR"





def Get_All():
    try:
        top_10_movies = Top_10_Movies.query.order_by(Top_10_Movies.rank).all() # Query Top_10_Movies and order by rank
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

