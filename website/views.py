from flask import Blueprint
from flask import Flask, render_template, redirect, url_for, request
from .forms import EditForm

views = Blueprint("routes", __name__)

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/edit", methods=['GET', 'POST'])
def edit():
    edit_form = EditForm()
    # book_to_update = Book.query.get(id)
    # if edit_form.validate_on_submit():
    #     book_to_update.rating = edit_form.new_rating.data
    #     db.session.commit()  
    #     return redirect(url_for('home'))
    return render_template('edit.html', form=edit_form)