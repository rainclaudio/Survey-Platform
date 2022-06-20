from datetime import datetime
from encuestas import db, login_manager_
from flask_login import UserMixin

@login_manager_.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    tipo = db.Column(db.String(20), nullable=False)
    visible_inf = db.Column(db.String(20), nullable=False, default=True)


    def __repr__(self):
        return f"User('{self.username}', {self.name}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# Modelos útiles para la creación de encuestas

class Encuesta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    description = db.Column(db.String(1000), nullable = False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    preguntas = db.relationship('Pregunta', backref = 'content', lazy = True)
    estado =  db.Column(db.String(100), default = "creada")
class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    encuesta_id = db.Column(db.Integer, db.ForeignKey('encuesta.id'), nullable = False)
    items = db.relationship('Item', backref = 'options', lazy = True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(1000), nullable = False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable = False)

class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable = False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable = False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    id_encuesta = db.Column(db.Integer, db.ForeignKey('encuesta.id'), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

class ListaDifusion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    description = db.Column(db.String(1000), nullable = False)

class UserInList(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    lista_id = db.Column(db.Integer, db.ForeignKey('lista_difusion.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    __table_args__ = (db.UniqueConstraint('lista_id', 'user_id'), )
    # __table_args__ = (db.PrimaryKeyConstrain('lista_id', 'user_id'))