from sqlalchemy.exc import SQLAlchemyError
from website import db
from website.models import Top_10_Movies, All_Movies, User
from .logger import logger

from sqlalchemy.exc import SQLAlchemyError


#################################### USERS HELPER FUNCTIONS ##############################################

def Add_User(data):
    try:
        # Check if user already exists
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            logger.warning(f"User with the email '{data['email']}' already exists.")
            return "EXISTS", None

        # Create a new user
        new_user = User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
        )

        # Add to the database
        db.session.add(new_user)
        db.session.commit()

        logger.info(f"Successfully added user: {data['name']} ({data['email']})")
        return "SUCCESS", new_user

    except SQLAlchemyError as db_error:
        logger.error(f"Database error while adding user '{data['name']}' ({data['email']}): {db_error}")
        db.session.rollback()

    except Exception as error:
        logger.error(f"Unexpected error while adding user '{data['name']}' ({data['email']}): {error}")
        db.session.rollback()

    return "ERROR", None



def Get_User(email):
    try:
        user = User.query.filter_by(email=email).first()

        if user:
            logger.info("Successfully fetched user.")
        else:
            logger.warning("No user found with the provided email.")
        return user
    
    except SQLAlchemyError as db_error:
        logger.error("Database error while fetching user. Error: %s", db_error)
        return None
    except Exception as error:
        logger.error("Unexpected error while fetching user. Error: %s", error)
        return None




#################################### MOVIES HELPER FUNCTIONS ##############################################

def Add(form, data, user_id):
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
                # Temporarily shift ranks to avoid UNIQUE constraint violations
                movies_to_shift = Top_10_Movies.query.filter(
                    Top_10_Movies.rank >= form.ranking.data
                ).order_by(Top_10_Movies.rank.desc()).all()

                # Temporarily increase ranks
                for movie in movies_to_shift:
                    movie.rank += 10

                db.session.flush()  # Apply temporary shifts

                # Adjust ranks to the correct positions
                for movie in movies_to_shift:
                    movie.rank -= 9

            # Create a new movie with the specified rank
            movie = Top_10_Movies(
                title=data.get("title"),
                year=data.get("year"),
                description=data.get("description"),
                rating=data.get("rating"),
                rank=form.ranking.data,
                review=form.review.data,
                img_url=data.get("poster"),
                movie_id=data.get("movie_id"),
                user_id=user_id
            )
        else:
            # Adding to All_Movies table
            movie = All_Movies(
                title=data.get("title"),
                year=data.get("year"),
                rating=data.get("rating"),
                review=form.review.data,
                img_url=data.get("poster"),
                movie_id=data.get("movie_id"),
                user_id=user_id
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



def Get_All(user_id):
    try:
        top_10_movies = Top_10_Movies.query.filter_by(user_id=user_id).order_by(Top_10_Movies.rank).all() # Query Top_10_Movies and order by rank
        all_movies = All_Movies.query.filter_by(user_id=user_id).all() 

        logger.info(f"Fetched {len(top_10_movies)} top 10 movies and {len(all_movies)} all movies for user ID {user_id}.")
        return (top_10_movies, all_movies)
    
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while fetching movies for user ID {user_id}: {db_error}")
        return ([], [])  # Return empty lists to prevent breaking the route
    except Exception as error:
        logger.error(f"Unexpected error while fetching movies for user ID {user_id}: {error}")
        return ([], [])  # Return empty lists in case of an error



def Get(id, user_id, table=Top_10_Movies):
    try:
        if user_id:
            movie = table.query.filter_by(id=id, user_id=user_id).first()  # Fetch movie with user_id filter, to ensure movie belongs to a user
        else:
            return "UNAUTHORIZED"
        
        if movie:
            logger.info(f"Successfully fetched Movie with id={id} from {table.__tablename__} for user ID {user_id}.")
        else:
            logger.warning(f"No Movie found with id={id} in {table.__tablename__} for user ID {user_id}.")
            return None
        
        return movie
    
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while fetching Movie with id={id} from {table.__tablename__} for user ID {user_id}: {db_error}")
        return None
    except Exception as error:
        logger.error(f"Unexpected error while fetching Movie with id={id} from {table.__tablename__} for user ID {user_id}: {error}")
        return None

    


def Edit(movie, column_name, data, user_id):
    try:
        # Check if the movie belongs to the current user
        if movie.user_id != user_id:
            logger.error(f"User ID {user_id} does not own Movie ID {movie.id}. Edit denied.")
            return False
        
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



def Delete(movie_to_delt, user_id):
    try:
        # Check if the movie belongs to the current user
        if movie.user_id != user_id:
            logger.error(f"User ID {user_id} does not own Movie ID {movie.id}. Edit denied.")
            return False
        
        # Adjust rankings if the movie is in Top_10_Movies
        if isinstance(movie_to_delt, Top_10_Movies):
            movies_to_shift = Top_10_Movies.query.filter(
                Top_10_Movies.rank > movie_to_delt.rank
            ).order_by(Top_10_Movies.rank.asc()).all()

            for movie in movies_to_shift:
                movie.rank += 10

            db.session.delete(movie_to_delt)

            db.session.flush() 

            for movie in movies_to_shift:
                movie.rank -= 11

        db.session.flush()
        db.session.commit()

        logger.info(f"Successfully deleted Movie ID {movie_to_delt.id}: {movie_to_delt.title}")
        return True

    except SQLAlchemyError as db_error:
        logger.error(f"Database error while deleting Movie ID {movie_to_delt.id} ('{movie_to_delt.title}'): {db_error}")
        db.session.rollback()
    except AttributeError as attr_err:
        logger.error(f"AttributeError while deleting Movie ID {movie_to_delt.id} ('{movie_to_delt.title}'): {attr_err}")
        db.session.rollback()
    except Exception as error:
        logger.error(f"Unexpected error while deleting Movie ID {movie_to_delt.id} ('{movie_to_delt.title}'): {error}")
        db.session.rollback()

    return False