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

def Add(form, data, id_user):
    try:
        # Check if the movie_id already exists for the user in either table
        movie_in_top_10 = Top_10_Movies.query.filter_by(user_id=id_user, movie_id=data.get("movie_id")).first()
        movie_in_all = All_Movies.query.filter_by(user_id=id_user, movie_id=data.get("movie_id")).first()
        if movie_in_top_10 or movie_in_all:
            logger.warning(f"Movie with ID {data.get('movie_id')} already exists for user {id_user}.")
            return "MOVIE_ALREADY_EXISTS"
        
        if form.ranking.data:
            # Check if the Top_10_Movies table already has 10 entries
            top_10_count = Top_10_Movies.query.filter_by(user_id=id_user).count()
            # print(f'\n \n {top_10_count} \n \n')    #   For Debug
            if top_10_count >= 10:
                logger.warning("Top_10_Movies table already has 10 entries. Cannot add more.")
                return "TOP_10_FULL"

            # Get the movies belonging to the user
            user_movies = Top_10_Movies.query.filter_by(user_id=id_user).all()
            # print(f'\n \n {user_movies} \n \n')  #   For Debug

            # Adjust rankings if necessary
            existing_movie = next(
                (movie for movie in user_movies if movie.rank == form.ranking.data), None
            )
            # print(f'\n \n {existing_movie} \n \n')  #   For Debug

            if existing_movie:
                # Get movies with rank >= the new rank, belonging to the same user
                movies_to_shift = sorted(
                    [movie for movie in user_movies if movie.rank >= form.ranking.data],
                    key=lambda x: x.rank,
                    reverse=True,
                )
                # print(f'\n \n {movies_to_shift} \n \n')   #   For Debug

                # Temporarily increase ranks
                for movie in movies_to_shift:
                    movie.rank += 10

                db.session.flush()  # Temporary flush the database to highlight changes

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
                user_id=id_user
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
                user_id=id_user
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



def Get(id, id_user, table=Top_10_Movies):
    try:
        if id_user:
            movie = table.query.filter_by(id=id, user_id=id_user).first()  # Fetch movie with user_id filter, to ensure movie belongs to a user
        else:
            return "UNAUTHORIZED"
        
        if movie:
            logger.info(f"Successfully fetched Movie with id={id} from {table.__tablename__} for user ID {id_user}.")
        else:
            logger.warning(f"No Movie found with id={id} in {table.__tablename__} for user ID {id_user}.")
            return None
        
        return movie
    
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while fetching Movie with id={id} from {table.__tablename__} for user ID {id_user}: {db_error}")
        return None
    except Exception as error:
        logger.error(f"Unexpected error while fetching Movie with id={id} from {table.__tablename__} for user ID {id_user}: {error}")
        return None
    


def Edit(movie, column_name, data, id_user):
    try:
        # Check if the movie belongs to the current user
        if movie.user_id != id_user:
            logger.error(f"User ID {id_user} does not own Movie ID {movie.id}. Edit denied.")
            return False

        # Validate if the column exists on the movie object
        if not hasattr(movie, column_name):
            logger.error(f"Invalid column name '{column_name}' for Movie ID {movie.id}")
            return False

        if column_name == "rank":
            # print(f'\n \n {movie} | rank: {movie.rank} \n \n')  #   For Debug
            # Check if the rank is already in use by another movie
            conflicting_movie = Top_10_Movies.query.filter_by(user_id=id_user, rank=data).first()
            # print(f'\n \n {conflicting_movie} | rank: {conflicting_movie.rank} \n \n')  #   For Debug
            if conflicting_movie and conflicting_movie.id != movie.id:
                # Temporarily set conflicting movie's rank to a placeholder
                placeholder_rank = -1  # Ensure this value doesn't conflict
                conflicting_movie.rank = placeholder_rank

                db.session.flush()  # Flush the placeholder update to the database
                # print(f'\n \n {conflicting_movie} | temp new rank: {conflicting_movie.rank} \n \n')  #   For Debug

                conflicting_movie_new_rank = movie.rank
                movie.rank = data   # Update the current movie's rank

                db.session.flush() 
                # print(f'\n \n {conflicting_movie} | temp new rank: {conflicting_movie.rank} \n \n')  #   For Debug

                conflicting_movie.rank = conflicting_movie_new_rank # Restore the conflicting movie's rank

            else:
                movie.rank = data
        else:
            # Update the review or other fields
            setattr(movie, column_name, data)

        db.session.commit()
        # print(f'\n \n {conflicting_movie} | temp new rank: {conflicting_movie.rank} \n \n')  #   For Debug

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



def Delete(movie_to_delt, id_user):
    try:
        # Check if the movie belongs to the current user
        if movie_to_delt.user_id != id_user:
            logger.error(f"User ID {id_user} does not own Movie ID {movie.id}. Edit denied.")
            return False
        
        # Adjust rankings if the movie is in Top_10_Movies
        if isinstance(movie_to_delt, Top_10_Movies):
            movies_to_shift = Top_10_Movies.query.filter(
                                Top_10_Movies.rank > movie_to_delt.rank,
                                Top_10_Movies.user_id == id_user
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