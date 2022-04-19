from turtle import title
from flask import render_template, url_for, flash, redirect
from datetime import datetime
from encuestas import app,db
from encuestas.forms import CrearEncuestaForm, CrearPreguntaForm, RegistrationForm, LoginForm
from encuestas.models import Encuesta, User, Post


posts = [
    {
        'author': 'Claudio Rain',
        'title': 'Entrevista 1',
        'content': 'Aquí va una pequeña descripción',
        'date_posted': 'April 20, 2022'
    },
    {
        'author': 'Claudio Rain',
        'title': 'Entrevista 2',
        'content': 'Aquí va una pequeña descripción',
        'date_posted': 'April 21, 2022'
    }
]


@app.route("/")
@app.route("/home")
def home():
    encuestas = Encuesta.query.all()
    return render_template('home.html', posts=posts, encuestas = encuestas)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/crear_encuesta", methods=['GET', 'POST'])
def crear_encuesta():
    encuesta_form = CrearEncuestaForm()
    counter = 1
    if encuesta_form.validate_on_submit():
            encuesta = Encuesta(title = encuesta_form.title.data, user_id = 'claudio' )
            db.session.add(encuesta)
            preguntas_form = []
            db.session.commit()
            flash(f'Encuesta {encuesta_form.title.data} creada! {encuesta.id} y el counter es {counter}', 'success ')
            counter = counter + 1
    return render_template('crear_encuesta.html', title= 'Crear Encuesta',encuesta_form = encuesta_form)




@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)