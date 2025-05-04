from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_babel import _
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.firebase_config import (verify_firebase_token,
                                 verify_google_oauth_token)
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
            password_hash=generate_password_hash(password, method='scrypt'),
            auth_provider='local'
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

        if not user or not check_password_hash(user.password_hash or '', password):
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


@auth.route('/auth/google', methods=['POST'])
def google_auth():
    """Handle Google Sign In Authentication"""
    data = request.get_json()
    
    if not data or 'idToken' not in data:
        return jsonify({'error': 'No ID token provided'}), 400
    
    
    # Verify the token
    firebase_data = verify_firebase_token(data['idToken'])
    
    if not firebase_data:
        return jsonify({'error': 'Invalid token'}), 401
    
    
    # Parse user info from token
    user_info = {
        'uid': firebase_data['uid'],
        'email': firebase_data['email'],
        'name': firebase_data.get('name', ''),
        'picture': firebase_data.get('picture', '')
    }
    
    # Find or create user
    user = User.find_or_create_by_firebase(user_info)
    
    # Log the user in
    login_user(user, remember=True)
    
    return jsonify({
        'success': True,
        'message': _('Successfully logged in with Google!'),
        'redirect': url_for('main.home')
    })


@auth.route('/auth/check')
def auth_check():
    """Check if the user is authenticated"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email,
                'auth_provider': current_user.auth_provider
            }
        })
    return jsonify({'authenticated': False})
