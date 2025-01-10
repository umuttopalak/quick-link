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
    password_hash = db.Column(db.String(512))
    urls = db.relationship('URL', backref='author', lazy=True)


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

    def __repr__(self):
        return f'<URL {self.short_id}>' 