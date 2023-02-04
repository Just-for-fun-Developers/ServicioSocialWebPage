# models.py
from ServicioSocialPaginaWeb import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(64), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('NewsPost', backref='author', lazy=True)
    events = db.relationship('NewsEvent', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"


class NewsPost(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime , nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}"

class NewsEvent(db.Model):
    users = db.relationship(User)
    
    id = id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime , nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    time = db.Column(db.String(60), nullable=False)
    place = db.Column(db.Text, nullable=False)

    def __init__(self, title, time, place, user_id):
        self.title = title
        self.time = time
        self.place = place
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"Event ID: {self.id} -- Date: {self.date} --- {self.title}"
