from turtle import title
from flask import render_template, url_for, flash, redirect, request
from datetime import datetime
from encuestas import app,db, bcrypt
from encuestas.forms import CrearEncuestaForm, CrearItemForm, CrearPreguntaForm, RegistrationForm, LoginForm
from encuestas.models import Encuesta, Item, User, Post, Pregunta
from flask_login import login_user, current_user,logout_user, login_required

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
    items_preguntas = []
    counter = 0
    for item in items:
        print(item.description)

    for preg in preguntas:
        for item in items:
            if preg.id == item.pregunta_id:
                counter+= 1
        items_preguntas.append(counter)
        counter = 0

    print(items_preguntas)

    total_pregs = len(id_preguntas)
    bool_items = 1

    if len(items_preguntas) == 0:
        bool_items = 0

    for n in items_preguntas:
        if n <= 1:
            bool_items = 0


    encuesta_form = CrearEncuestaForm()
    pregunta_form = CrearPreguntaForm()
    return render_template('editar_encuesta.html', 
        title= 'Editar Encuesta',
        encuesta = encuesta,
        preguntas = preguntas,
        items = items,
        encuesta_form = encuesta_form,
        pregunta_form = pregunta_form,
        total_pregs = total_pregs,
        bool_items = bool_items
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username =form.username.data, email=form.email.data, password =  hash_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Creaste tu cuenta, bienvenid@ {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('No puedes entrar, vuelve a checkear la contraseña o usuario.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/post/<int:encuesta_id>/cerrar", methods=['POST'])
def cerrar_encuesta(encuesta_id):
    encuesta = Encuesta.query.get_or_404(encuesta_id)
    encuesta.estado = "cerrada"
    db.session.commit()
    flash('Your post #' + str(encuesta_id) + ' has been closed!', 'success')
    return redirect(url_for('home'))


@app.route("/post/<int:encuesta_id>/<int:total_pregs>/<int:bool_items>/publicar", methods=['POST'])
def publicar_encuesta(encuesta_id,total_pregs,bool_items):
    if total_pregs == 0:
        flash('Para publicar encuesta se necesita minimo una pregunta', 'danger')
        return redirect( url_for('editar_encuesta', encuesta_id=encuesta_id))
    if bool_items == 0:
        flash('Para publicar encuesta se necesita minimo dos items por pregunta', 'danger')
        return redirect( url_for('editar_encuesta', encuesta_id=encuesta_id))
    else:
        encuesta = Encuesta.query.get_or_404(encuesta_id)
        encuesta.estado = "publicada"
        db.session.commit()
        flash('Your post #' + str(encuesta_id) + ' has been posted!', 'success')
        return redirect(url_for('home'))

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', title='Profile')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

