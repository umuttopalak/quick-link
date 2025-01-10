from flask import Flask, request, session
from flask_babel import Babel, _
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
babel = Babel()

def get_locale():
    # Önce session'da kayıtlı dili kontrol et
    if 'lang' in session:
        return session['lang']
    # Yoksa tarayıcının tercih ettiği dili kullan
    return request.accept_languages.best_match(['en', 'tr'])

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = _('Please log in to access this page.')

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth import auth
    from app.routes import main

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app 