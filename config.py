import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///urls.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TIMEZONE = 'Europe/Istanbul' 
    
    LANGUAGES = ['en', 'tr']
    BABEL_DEFAULT_LOCALE = 'en'

    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_DIR = './flask_session' 