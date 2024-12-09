from flask import Flask, Blueprint, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from .forms import EditMovie, AddMovie
from utilities import helper_db, helper_api

views = Blueprint('views', __name__)

SAMPLE_POSTER = "https://www.shortlist.com/media/images/2019/05/the-30-coolest-alternative-movie-posters-ever-2-1556670563-K61a-column-width-inline.jpg"

@views.route("/")
@login_required
def home():
    data = helper_db.Get_All(user_id=current_user.id)
    if not data[0] and not data[1]:  # Check if both lists have data
        flash("No movies available. Please try again later.", category="warning")
        return render_template("error.html", user=current_user)

    return render_template("index.html", top_10_movies=data[0], all_movies=data[1], user=current_user)



@views.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    add_form = AddMovie()

    if add_form.validate_on_submit():
        # Extract only the movie ID from the input field
        movie_id = add_form.title.data.split()[-1]  # Assumes the ID is the last part of the input
        data = helper_api.SEARCH_MOVIE(movie_id)  # Send ID to the api call

        if "error" in data:
            flash(data["error"], category="error")
            return render_template('add.html', form=add_form, user=current_user)
        
        # Add movie poster does not exist, it adds a sample poster
        if not data["poster"]:
            data["poster"] = SAMPLE_POSTER

        # Add movie to the database
        data["movie_id"] = movie_id
        status = helper_db.Add(form=add_form, data=data, id_user=current_user.id)
        if status == "SUCCESS":
            flash("Movie added successfully!", category="success")
            return redirect(url_for('views.home'))
        elif status == "MOVIE_ALREADY_EXISTS":
            flash(f"Movie '{data.get('title')}' already exists.", category="error")
        elif status == "TOP_10_FULL":
            flash("Cannot add more movies to the Top 10 list. It is already full.", category="error")
        else:
            flash("Internal Server Error in Adding Movie to the Database", category="error")
    
    return render_template('add.html', form=add_form, user=current_user)



@views.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit(id):
    edit_form = EditMovie()
    movie = helper_db.Get(id=id, table="EDIT", id_user=current_user.id)

    if movie == "UNAUTHORIZED":
        flash(message="Please Login or Signup to Create Movie Collection.", category="error")
        return redirect(url_for('auth.login'))
    elif not movie:
        flash(message="Movie not found.", category="error")
        return redirect(url_for('views.home'))

    if edit_form.validate_on_submit():
        inputs = {
            "review": edit_form.review.data,
            "rank": edit_form.ranking.data
        }

        # Check if at least one input is provided
        if not any(inputs.values()):
            flash(message="You need to provide at least one input.", category="error")
        else:
            for field, value in inputs.items():
                if value:
                    status = helper_db.Edit(movie=movie, column_name=field, data=value, id_user=current_user.id)
                    if not status:
                        flash(message=f"Error updating '{field}' for movie '{movie.title}'.", category="error")
                        return render_template('edit.html', form=edit_form, movie=movie, user=current_user)

            flash(message=f"Movie '{movie.title}' updated successfully.", category="success")
            return redirect(url_for('views.home'))

    return render_template('edit.html', form=edit_form, movie=movie, user=current_user)



@views.route("/delete/<int:id>/<string:table>")
@login_required
def delete(id, table):
    movie = helper_db.Get(id=id, table=table, id_user=current_user.id)

    if not movie:
        flash(message="Movie not found.", category="error")
        return redirect(url_for('views.home'))
    
    status = helper_db.Delete(movie_to_delt=movie, id_user=current_user.id)
    
    if not status:
        flash(message=f"Error deleting the movie '{movie.title}'.", category="error")
    else:
        flash(message=f"Successfully deleted the movie '{movie.title}'.", category="success")

    return redirect(url_for('views.home'))
