from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import Login, Signup
from utilities import helper_db


auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = Signup()

    if signup_form.validate_on_submit():
        # Extract form data
        user_data = {
            "name": signup_form.name.data,
            "email": signup_form.email.data,
            "password": generate_password_hash(signup_form.password.data, method='pbkdf2:sha256'),
        }
        # Add user to database
        status, new_user = helper_db.Add_User(data=user_data)

        if status == "SUCCESS" and new_user:
            login_user(new_user, remember=True)
            flash("Account Created Successfully!", category="success")
            return redirect(url_for('views.home'))
        elif status == "EXISTS":
            flash("User with the given email already exists.", category="error")
        else:
            flash("Internal Server Error while creating account.", category="error")

    return render_template("signup.html", form=signup_form, user=current_user)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = Login()

    if login_form.validate_on_submit():
        # Extract form data
        email = login_form.email.data
        password = login_form.password.data

        user = helper_db.Get_User(email=email)

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid credentials. Please check your password and try again.', category='error')
        else:
            flash('No account found with this email. Please register first.', category='error')

    return render_template("login.html", form=login_form, user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
