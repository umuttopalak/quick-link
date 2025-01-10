from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User, db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash(_('Email address already registered'))
            return redirect(url_for('auth.register'))

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password, method='scrypt')
        )

        db.session.add(new_user)
        db.session.commit()

        flash(_('Registration successful! Please login.'))
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash(_('Please check your login details'))
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        flash(_('Successfully logged in!'))
        return redirect(url_for('main.home'))

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('Successfully logged out!'))
    return redirect(url_for('main.home'))
