from turtle import title
from flask import render_template, url_for, flash, redirect
from datetime import datetime
from encuestas import app,db
from encuestas.forms import CrearEncuestaForm, CrearItemForm, CrearPreguntaForm, RegistrationForm, LoginForm
from encuestas.models import Encuesta, Item, User, Post, Pregunta


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
    if encuesta_form.validate_on_submit():
            encuesta = Encuesta(title = encuesta_form.title.data, user_id = 'claudio' )
            db.session.add(encuesta)
            db.session.commit()
            flash(f'Encuesta {encuesta_form.title.data} creada! {encuesta.id}', 'success ')
            return redirect( url_for('editar_encuesta', encuesta_id=encuesta.id))
    return render_template('crear_encuesta.html', title= 'Crear Encuesta',encuesta_form = encuesta_form)

@app.route("/editar_encuesta/<int:encuesta_id>", methods=['GET', 'POST'])
def editar_encuesta(encuesta_id):
    encuesta = Encuesta.query.get_or_404(encuesta_id)
    preguntas = Pregunta.query.filter_by(encuesta_id = encuesta_id)
    print('numero de la encuesta: ' + str(encuesta_id) )
    id_preguntas = []
    for preg in preguntas:
        id_preguntas.append(preg.id)
    print(id_preguntas)
    items = Item.query.filter(Item.pregunta_id.in_(id_preguntas))
    for item in items:
        print(item.description)
    encuesta_form = CrearEncuestaForm()
    pregunta_form = CrearPreguntaForm()
    return render_template('editar_encuesta.html', 
        title= 'Editar Encuesta',
        encuesta = encuesta,
        preguntas = preguntas,
        items = items,
        encuesta_form = encuesta_form,
        pregunta_form = pregunta_form,
    )
        
@app.route("/editar_encuesta/<int:encuesta_id>/añadir_pregunta", methods=['GET', 'POST'])
def add_pregunta(encuesta_id):
    pregunta_form = CrearPreguntaForm()
    if pregunta_form.validate_on_submit():
        pregunta = Pregunta(title = pregunta_form.title.data, encuesta_id = encuesta_id)
        db.session.add(pregunta)
        db.session.commit()
        flash(f'Pregunta {pregunta_form.title.data} añadida! {encuesta_id}', 'success')
        return redirect( url_for('editar_encuesta', encuesta_id=encuesta_id))
    return render_template(
        'añadir_pregunta.html', 
        title= 'Añadir Encuesta',
        pregunta_form = pregunta_form
    )

@app.route("/editar_encuesta/<int:encuesta_id>/añadir_pregunta/<int:pregunta_id>", methods=['GET', 'POST'])
def add_item(encuesta_id,pregunta_id):
    item_form = CrearItemForm()
    pregunta = Pregunta.query.get_or_404(pregunta_id)
    if item_form.validate_on_submit():
        item = Item(description = item_form.description.data, pregunta_id = pregunta_id)
        db.session.add(item)
        db.session.commit()
        flash(f'Item {item_form.description.data} añadida! {pregunta_id}', 'success')
        return redirect( url_for('editar_encuesta', encuesta_id=encuesta_id))
    return render_template(
        'añadir_item.html', 
        title= 'Añadir Item',
        pregunta = pregunta,
        item_form = item_form
    )

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


@app.route("/post/<int:encuesta_id>/delete", methods=['POST'])
def delete_encuesta(encuesta_id):
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))