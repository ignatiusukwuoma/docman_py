from flask import flash, url_for, redirect, render_template
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm

from .. import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles requests to the /register route
    :return: login or register page
    """
    new_account = True
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        # add user to database
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('You have successful registered.')

        return redirect(url_for('home.dashboard'))

    return render_template('auth/register.html', title='Register', form=form, new_account=new_account)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs user into the application
    :return: dashboard or login page
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        else:
            flash('Invalid email or password')

    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handles request to the logout route
    :return: login page
    """
    logout_user()

    flash('You have signed out')
    return redirect(url_for('auth.login'))

