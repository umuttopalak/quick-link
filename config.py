import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///urls.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Timezone ayarı
    TIMEZONE = 'Europe/Istanbul' 
    
    # Dil ayarları
    LANGUAGES = ['en', 'tr']
    BABEL_DEFAULT_LOCALE = 'en' 