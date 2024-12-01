from flask import Blueprint
from flask import Flask, render_template, redirect, url_for, request
from .forms import EditMovie, AddMovie

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/add", methods=['GET', 'POST'])
def add():
    add_form = AddMovie()
    # book_to_update = Book.query.get(id)
    if add_form.validate_on_submit():
    #     book_to_update.rating = edit_form.new_rating.data
    #     db.session.commit()  
        return redirect(url_for('views.home'))
    return render_template('add.html', form=add_form)

@views.route("/edit", methods=['GET', 'POST'])
def edit():
    edit_form = EditMovie()
    # book_to_update = Book.query.get(id)
    if edit_form.validate_on_submit():
    #     book_to_update.rating = edit_form.new_rating.data
    #     db.session.commit()  
        return redirect(url_for('views.home'))
    return render_template('edit.html', form=edit_form)