from datetime import datetime
from encuestas import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Encuesta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_posted = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    preguntas = db.relationship('Pregunta', backref = 'content', lazy = True)

class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    encuesta_id = db.Column(db.Integer, db.ForeignKey('encuesta.id'), nullable = False)
    items = db.relationship('Item', backref = 'options', lazy = True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(1000), nullable = False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable = False)
    