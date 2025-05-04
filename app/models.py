import random
import string
from datetime import datetime, timedelta

from flask_login import UserMixin

from app import db


def get_istanbul_time():
    return datetime.utcnow() + timedelta(hours=3)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=True)
    auth_provider = db.Column(db.String(20), default='local')  # 'local', 'google', 'firebase'
    profile_picture = db.Column(db.String(512), nullable=True)
    urls = db.relationship('URL', backref='author', lazy=True)
    
    @classmethod
    def find_or_create_by_firebase(cls, firebase_data):
        """Find existing user or create a new one based on Firebase data"""
        user = cls.query.filter_by(firebase_uid=firebase_data.get('uid')).first()
        
        if not user:
            # Look for existing user with same email
            user = cls.query.filter_by(email=firebase_data.get('email')).first()
            if user:
                # Update existing user with Firebase UID
                user.firebase_uid = firebase_data.get('uid')
                user.auth_provider = 'google'
                if not user.profile_picture and firebase_data.get('picture'):
                    user.profile_picture = firebase_data.get('picture')
            else:
                # Create new user
                user = cls(
                    username=firebase_data.get('name') or firebase_data.get('email').split('@')[0],
                    email=firebase_data.get('email'),
                    firebase_uid=firebase_data.get('uid'),
                    auth_provider='google',
                    profile_picture=firebase_data.get('picture')
                )
                db.session.add(user)
                
        db.session.commit()
        return user


def generate_short_id():
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(chars, k=6))
        if not URL.query.filter_by(short_id=short_id).first():
            return short_id


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_id = db.Column(db.String(6), unique=True, default=generate_short_id)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=get_istanbul_time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def __repr__(self):
        return f'<URL {self.short_id}>' 