from flask import Blueprint, flash
from flask import Flask, render_template, redirect, url_for, request
from .forms import EditMovie, AddMovie
from utilities import helper_db

views = Blueprint('views', __name__)



@views.route("/")
def home():
    data = helper_db.Get_All()
    if not data or not data[0] or not data[1]:  # Check if both lists have data
        flash("No movies available. Please try again later.", category="warning")
        return render_template("error.html")

    return render_template("index.html", top_10_movies=data[0], all_movies=data[1])




@views.route("/add", methods=['GET', 'POST'])
def add():
    add_form = AddMovie()

    if add_form.validate_on_submit():
        status = helper_db.Add(add_form)

        if status:
            flash(message="Movie added successfully!", category="success")
            return redirect(url_for('views.home'))
        else:
            flash(message="Internal Server Error in Adding Movie to the Database", category="error")

    return render_template('add.html', form=add_form)




@views.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    edit_form = EditMovie()
    movie = helper_db.Get(id)

    if not movie:
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
                    status = helper_db.Edit(movie, field, value)
                    if not status:
                        flash(message=f"Error updating '{field}' for movie '{movie.title}'.", category="error")
                        return render_template('edit.html', form=edit_form, movie=movie)

            flash(message=f"Movie '{movie.title}' updated successfully.", category="success")
            return redirect(url_for('views.home'))

    return render_template('edit.html', form=edit_form, movie=movie)



@views.route("/delete/<int:id>")
def delete(id):
    movie = helper_db.Get(id)

    if not movie:
        flash(message="Movie not found.", category="error")
        return redirect(url_for('views.home'))
    
    status = helper_db.Delete(movie)
    
    if not status:
        flash(message=f"Error deleting the movie '{movie.title}'.", category="error")
    else:
        flash(message=f"Successfully deleted the movie '{movie.title}'.", category="success")

    return redirect(url_for('views.home'))
