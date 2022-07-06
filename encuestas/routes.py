from collections import UserDict
from fileinput import filename
from re import A
from textwrap import indent
from turtle import title
from flask import render_template, url_for, flash, redirect, request, jsonify
from datetime import datetime

from sqlalchemy import and_
from encuestas import app,db, bcrypt

from encuestas.forms import CrearEncuestaForm, CrearItemForm, CrearPreguntaForm, RegistrationForm, LoginForm, EnviarRespuestaForm, updatePerfil
from encuestas.models import Encuesta, Item, User, Post, Pregunta, Respuesta,ListaDifusion,UserInList,UsuarioInvitado
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from PIL import Image
import os
import numpy as np
import random

@app.route("/")
@app.route("/home")
def home():

    encuestas = Encuesta.query.filter_by(estado = "publicada")

    #Creo un diccionario y por cada encuesta le pregunto a la base de datos
    # cuantas respuestas tiene asociadas, como cada Respuesta esta asociada a una 
    # pregunta, la cantidad de respuestas entregadas por la query la divido
    # entre la cantidad de preguntas de la encuesta y listo.

    enc_title = {}
    enc_categorie = {}
    cant_respuestas = {}    
    for encuesta in encuestas:
        aux = Respuesta.query.filter(Respuesta.id_encuesta == encuesta.id).count()
        aux = int(aux / len(encuesta.preguntas)) 
        cant_respuestas[encuesta.id] = aux
        enc_title[encuesta.id] = encuesta.title
        enc_categorie[encuesta.id] = encuesta.categoria

    return render_template('home.html', encuestas = encuestas, cant_respuestas = cant_respuestas, enc_title = enc_title, enc_cat = enc_categorie)



@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/responder_encuesta/<int:encuesta_id>", methods=['GET', 'POST'])
@login_required
def responder_encuesta(encuesta_id):
    encuesta = Encuesta.query.get_or_404(encuesta_id)
    preguntas = Pregunta.query.filter_by(encuesta_id = encuesta_id)
    
    selected_preguntas_id = []
    for pregunta in preguntas:
        selected_preguntas_id.append(pregunta.id)
        
    items = Item.query.filter(Item.pregunta_id.in_(selected_preguntas_id))
    
    respuesta_form = EnviarRespuestaForm()

    if respuesta_form.validate_on_submit():
        todas_respondidas = True

        for pregunta in preguntas:
            if str(type(request.form.get(f'{pregunta.id}'))) == "<class 'NoneType'>":
                todas_respondidas = False
                flash("¡Aun existen preguntas sin responder!", 'danger')
                break

        if todas_respondidas:
            for pregunta in preguntas:
                item_id_seleccionado = request.form.get(f'{pregunta.id}')
                respuesta = Respuesta(item_id = item_id_seleccionado, pregunta_id = pregunta.id, id_usuario = current_user.username , id_encuesta =encuesta_id)
                db.session.add(respuesta)
            
            #likes    
            if respuesta_form.like.data:
                encuesta.likes += 1
            if respuesta_form.dislike.data:
                encuesta.dislikes += 1
            db.session.commit()
            flash("¡Felicidades! Has respondido la encuesta " + str(encuesta.title), 'success')
            return redirect('/')
            
    return render_template('responder_encuesta.html', 
        title = 'Responder Encuesta',
        encuesta = encuesta,
        preguntas = preguntas,
        items = items,
        respuesta_form = respuesta_form,
    )


@app.route('/update_categoria_test',methods=['POST'])
def update_categoria_test():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    encuesta = Encuesta.query.get_or_404(dataGet['encuesta_id'])
    encuesta.categoria = dataGet['categoria']
    db.session.commit()
    # Respuesta

    reply = {"status":"success","id": encuesta.id, "categoria" : encuesta.categoria}
    return jsonify(reply)
# ELIMINAR 
@app.route("/crear_encuesta", methods=['GET', 'POST'])
@login_required
def crear_encuesta():
    encuesta = Encuesta(title = 'Encuesta sin Título',description = "", user_id = current_user.username)
    db.session.add(encuesta)
    db.session.commit()
    flash(f'Encuesta creada!', 'success ')
    return redirect(url_for('editar_encuesta',encuesta_id = encuesta.id))


@app.route("/encuesta/<int:encuesta_id>", methods=['GET', 'POST'])
def encuesta(encuesta_id):
    encuesta = Encuesta.query.get_or_404(encuesta_id)
    preguntas = Pregunta.query.filter_by(encuesta_id = encuesta_id)

    id_preguntas = []
    for preg in preguntas:
        id_preguntas.append(preg.id)

    items = Item.query.filter(Item.pregunta_id.in_(id_preguntas))

    boton_editar = False
    boton_respuestas = False
    if current_user.is_authenticated:
        print("user is auth")
        encuestas_propias = Encuesta.query.filter_by(user_id = current_user.username)
        for encuestas in encuestas_propias:
            if encuestas.id == encuesta_id:
                boton_respuestas = True
                boton_editar = True
                break

    return render_template('encuesta.html', 
        title= 'Encuesta',
        encuesta = encuesta,
        preguntas = preguntas,
        items = items,
        boton_editar = boton_editar,
        boton_respuestas = boton_respuestas
    )



@app.route("/editar_encuesta/<int:encuesta_id>", methods=['GET', 'POST'])
def editar_encuesta(encuesta_id):
    encuesta = Encuesta.query.get_or_404(encuesta_id)
    preguntas = Pregunta.query.filter_by(encuesta_id = encuesta_id)
    listas = ListaDifusion.query.filter_by(user_id = current_user.id)
    invitados_id = UsuarioInvitado.query.filter_by(id_encuesta = encuesta_id)
    
    nombre_inv  = []
    mail_inv = []
    image_inv = []
    id_inv = []
    

    for i in invitados_id:
        usuario = User.query.filter_by(id = i.id_user).first()
        nombre_inv.append(usuario.name)
        mail_inv.append(usuario.email)
        image_inv.append(usuario.image_file)
        id_inv.append(usuario.id)
    
    print('mail',mail_inv)
    cantidad = np.arange(len(nombre_inv))
    print(cantidad)
    not_vacio = False
    if cantidad !=[]:
        not_vacio = True
    id_preguntas = []
    id_listas = []
    for preg in preguntas:
        id_preguntas.append(preg.id)
    for lista in listas:
        id_listas.append(lista.id)

    # se le hace un join con usuarios pertenecientes a una lista
    # i.e: claudio, rainlaudio@gmail.com, profile.jpg, 5 (pertenezco a la lista 5)
    #      claudio, rainlaudio@gmail.com, profile.jpg, 6 (también a la lista 6)
    #      manuel, rainlaudio@gmail.com, profile.jpg, 5 (pertenezco a la lista 5)
    #      julio, rainlaudio@gmail.com, profile.jpg, 5 (pertenezco a la lista 5)
    usuarios_con_id_lista = db.session.query(UserInList,User).join(User, UserInList.user_id == User.id).filter(UserInList.lista_id.in_(id_listas)).all()

    # DEBUG
    # for lis in usuarios_con_id_lista:
    #         print(lis[0].user_id,lis[0].lista_id,lis[1].name, lis[1].image_file, lis[1].email)

    items = Item.query.filter(Item.pregunta_id.in_(id_preguntas))
    items_preguntas = []
    counter = 0

    for preg in preguntas:
        for item in items:
            if preg.id == item.pregunta_id:
                counter+= 1
        items_preguntas.append(counter)
        counter = 0
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
        bool_items = bool_items,
        listas = listas,
        usuarios_con_id_lista = usuarios_con_id_lista,
        id_inv = id_inv,
        nombre_inv  = nombre_inv,
        mail_inv = mail_inv,
        image_inv = image_inv,
        cantidad=cantidad,
        not_vacio = not_vacio

    )
        
###########################################
# Probando Javascript con flask
@app.route('/crear_lista_difusion',methods=['GET','POST'])
#http://127.0.0.1:5000/crear_lista_difusion
def crear_lista_difusion():

    listas = ListaDifusion.query.all()
    usuarios_en_listas = UserInList.query.all()
    lista = ListaDifusion(title = 'Lista sin título',description =  'agregue una descripción', user_id = current_user.id)
    db.session.add(lista)
    db.session.commit()

  

    # total encuestados que no están en lista
    total_encuestados = User.query.filter(User.tipo == False)
 

    return render_template('editar_lista.html',title = 'Editar lista',total_encuestados = total_encuestados, lista = lista);

@app.route("/editar_lista/<int:lista_id>", methods=['GET', 'POST'])
def editar_lista(lista_id):
    lista = ListaDifusion.query.get_or_404(lista_id)


    # obtención de los usuarios en lista
    ids_encuestados_en_lista = UserInList.query.filter_by(lista_id = lista_id)
    id_users = []
    for enc in ids_encuestados_en_lista:
        id_users.append(enc.user_id)
    
   

    # total encuestados que no están en lista
    total_encuestados = User.query.filter(and_(User.id.not_in(id_users),User.tipo == False))
    # total encuestados en la lista
    encuestados_en_lista = User.query.filter(User.id.in_(id_users))

    return render_template('editar_lista.html', 
        title= 'Editar lista',
        lista = lista,
        total_encuestados = total_encuestados,
        encuestados_en_lista = encuestados_en_lista
    )
#  crud lista
@app.route('/add_user_in_list',methods=['POST'])
def add_user_in_list():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    lista_id = dataGet['lista_id']   
    user_id = dataGet['user_id']

     
    usuario_en_lista = UserInList(lista_id = lista_id, user_id = user_id)
    db.session.add(usuario_en_lista)
    db.session.commit()

    # Respuesta
    reply = {"status":"success","lista: ": usuario_en_lista.lista_id, "usuario: " : usuario_en_lista.user_id}
    return jsonify(reply) 

@app.route('/add_invitado_encuesta',methods=['GET','POST'])
def add_invitado_encuesta():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    encuesta_id = dataGet['encuesta_id']   
    user_id = dataGet['email']
    usuario = User.query.filter_by(email = user_id ).first_or_404()
    exists = db.session.query(UsuarioInvitado.id).filter_by(id_user = usuario.id).first() is not None
    
    if exists:
        print(exists)
    else: 
        usuario_invitado = UsuarioInvitado(id_user = usuario.id, id_encuesta = encuesta_id)
        db.session.add(usuario_invitado)

    #test  = UsuarioInvitado.query.filter_by(email = user_id ).first()
    #if test:
    #    print('existe')
    #else:
    usuario_invitado = UsuarioInvitado(id_user = usuario.id, id_encuesta = encuesta_id)
    db.session.add(usuario_invitado)
    db.session.commit()

 


 
    # Respuesta
    reply = {"status":"success","lista: ": encuesta_id, "usuario: " : usuario.id}
    return  jsonify(reply) 

@app.route('/delete_user_in_list', methods= ['POST'])
def delete_user_in_list():

    # obtener data recibida  
    dataGet = request.get_json(force=True)
    user_id = dataGet['user_id']
    lista_id = dataGet['lista_id']
    
    tupla = UserInList.query.filter_by(user_id = user_id,lista_id = lista_id).first_or_404()
    # Creación de datos 
    db.session.delete(tupla)
    db.session.commit()
    # respuesta
    reply = {"status": "deleted successfully"}
   
    return jsonify(reply)
@app.route('/update_title_list',methods=['POST'])
def update_title_list():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    lista = ListaDifusion.query.get_or_404(dataGet['lista_id'])
    lista.title = dataGet['description']
    db.session.commit()
    # Respuesta
    reply = {"status":"success","id": lista.id, "description" : lista.title}
    return jsonify(reply)

@app.route('/update_description_list',methods=['POST'])
def update_description_list():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    lista = ListaDifusion.query.get_or_404(dataGet['lista_id'])
    lista.description = dataGet['description']
    db.session.commit()
    # Respuesta
    reply = {"status":"success","id": lista.id, "description" : lista.description}
    return jsonify(reply)



# CRUD ENCUESTA
@app.route('/update_pregunta_test',methods=['POST'])
def update_pregunta_test():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    pregunta = Pregunta.query.get_or_404(dataGet['pregunta_id'])
    pregunta.title = dataGet['description']
    db.session.commit()
    # Respuesta
    reply = {"status":"success","id": pregunta.id, "description" : pregunta.title}
    return jsonify(reply)


@app.route('/add_item_test',methods=['POST'])
def add_item_test():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    pregunta_id = dataGet['pregunta_id']   
    print(dataGet['pregunta_id'])

    # creación del ITEM
    item = Item(description = dataGet['description'], pregunta_id = pregunta_id)
    db.session.add(item)
    db.session.commit()

    # Respuesta
    reply = {"status":"success","id": item.id, "description" : item.description}
    return jsonify(reply)
    
@app.route('/add_pregunta_test',methods=['POST'])
def add_pregunta_test():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    encuesta_id = dataGet['encuesta_id']   
    print(dataGet['encuesta_id'])

    # creación del ITEM
    pregunta = Pregunta(title = dataGet['description'], encuesta_id = encuesta_id)
    db.session.add(pregunta)
    db.session.commit()

    # Respuesta
    reply = {"status":"success","id": pregunta.id, "description" : pregunta.title}
    return jsonify(reply)


@app.route('/update_item_test',methods=['POST'])
def update_item_test():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    item = Item.query.get_or_404(dataGet['item_id'])
    item.description = dataGet['description']
    db.session.commit()
    # Respuesta
    reply = {"status":"success","id": item.id, "description" : item.description}
    return jsonify(reply)
@app.route('/delete_pregunta_test', methods=['POST'])
def delete_pregunta():

    # obtener data recibida  
    dataGet = request.get_json(force=True)
    pregunta_id = dataGet['pregunta_id']
    pregunta = Pregunta.query.get_or_404(pregunta_id)
    # Creación de datos 
    print("ahora borro la pregunta")
    id_items = []
    items_of_preg = Item.query.filter_by(pregunta_id = pregunta_id)
    for item in items_of_preg:
        id_items.append(item.id)
    print(id_items)
    db.session.delete(pregunta)
    db.session.commit()
    # respuesta
    reply = {"status": "deleted successfully"}
   
    return jsonify(reply)
 
@app.route('/delete_item_test', methods= ['POST'])
def delete_item():

    # obtener data recibida  
    dataGet = request.get_json(force=True)
    item_id = dataGet['item_id']
    item = Item.query.get_or_404(item_id)
    # Creación de datos 
    db.session.delete(item)
    db.session.commit()
    # respuesta
    reply = {"status": "deleted successfully"}
   
    return jsonify(reply)

@app.route('/update_title_test',methods=['POST'])
def update_title_test():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    encuesta = Encuesta.query.get_or_404(dataGet['encuesta_id'])
    encuesta.title = dataGet['description']
    db.session.commit()
    # Respuesta
    reply = {"status":"success","id": encuesta.id, "description" : encuesta.title}
    return jsonify(reply)

@app.route('/update_description_test',methods=['POST'])
def update_description_test():
    # obtener la data que se ha recibido
    dataGet = request.get_json(force=True)
    encuesta = Encuesta.query.get_or_404(dataGet['encuesta_id'])
    encuesta.description = dataGet['description']
    db.session.commit()
    # Respuesta
    reply = {"status":"success","id": encuesta.id, "description" : encuesta.description}
    return jsonify(reply)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/survey_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    # i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/save_image_test", methods=['GET', 'POST'])
def save_image():
   picture = request.files['static_file']
   id_enc = request.form['static_id']
   print(request.form['static_id'])
   encuesta = Encuesta.query.get_or_404(id_enc)
   if picture:
        picture_file = save_picture(picture)
        encuesta.image_file = picture_file
   print(encuesta.image_file)
   db.session.commit()
   flash('La imagen ha sido subida!', 'success')
   return jsonify({ "jajas": "jajas"})
# FIN experimentación javascript con flask
###########################################

# Eliminar
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
# Eliminar
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
        user = User(username =form.username.data, name =form.name.data, email=form.email.data, password =  hash_pass, tipo=form.tipo.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Creaste tu cuenta, bienvenid@ {form.name.data}!', 'success')
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

def guardarfoto(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    
    prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
        os.remove(prev_picture)

    return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():

    form = updatePerfil()
    respuesta = Respuesta.query.filter_by(id_usuario = current_user.username)



    if form.validate_on_submit():
        if form.picture.data:
            picture_file = guardarfoto(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.visible_inf = form.visible.data

        db.session.commit()
        flash('Tus datos han sido actualizados', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email



    lista_query= []
    encuest = {}
    for i in respuesta:

        datet =  i.date
        encuest[i.date.strftime("%d-%m-%Y %H:%M:%S")] = i.id_encuesta
        encRESP = Encuesta.query.filter_by(id = i.id_encuesta )

        #print(encRESP)}



    keys = list(encuest.keys())


    for i in encuest:
        print(encuest[i])
        lista_query.append(Encuesta.query.filter_by(id = encuest[i] ))
    if len(lista_query) ==0:
        lista_query = 0

    
    
    encPUBLIC = Encuesta.query.filter_by(user_id = current_user.username,estado = "publicada" )
    encCREATE = Encuesta.query.filter_by(user_id = current_user.username,estado = "creada" )
    encCLOSED = Encuesta.query.filter_by(user_id = current_user.username,estado = "cerrada" )

    # listas de difusión del encuestador
    listas = ListaDifusion.query.filter_by(user_id = current_user.id)

    TOTAL=len(encuest)
    TOTALC=0
    
  
    tipo = False 
    perfil_usuario =  'profile_encuestado.html'
   
    if current_user.tipo == '1':
        tipo = True
        perfil_usuario =  'profile_encuestador.html'
        for i in encPUBLIC:
            TOTAL=TOTAL+1
        for i in encCREATE:
            TOTAL=TOTAL+1
        for i in encCLOSED:
            TOTALC=TOTALC+1
        
    image_file = url_for('static', filename= 'profile_pics/' + current_user.image_file)
    
   
    return render_template(perfil_usuario, title='Profile', image_file=image_file , encPUBLIC = encPUBLIC, form = form, encCREATE=encCREATE, encCLOSED=encCLOSED, TOTAL =TOTAL+TOTALC, TOTALC  =  TOTALC, tipo=tipo, lista_query=lista_query, keys = keys,listas = listas)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


#VER RESULTADOS
@app.route("/resultados_encuesta/<int:encuesta_id>", methods=['GET', 'POST'])
@login_required
def resultados_encuesta(encuesta_id):
    
    encuesta = Encuesta.query.get_or_404(encuesta_id)
    preguntas = Pregunta.query.filter_by(encuesta_id = encuesta_id)
    
    map_preg_a_array_cant_resp_item = {}
    map_preg_a_array_percent_resp_item = {}
    map_preg_a_array_str = {}
    id_preguntas = []

    for preg in preguntas:
        id_preguntas.append(preg.id)
        map_preg_a_array_cant_resp_item[preg.id] = []
        map_preg_a_array_percent_resp_item[preg.id] = []
        map_preg_a_array_str[preg.id] = []
    
    items = Item.query.filter(Item.pregunta_id.in_(id_preguntas))

    colores = [
        'rgb(191, 161, 148)',
        'rgb(248, 207, 155)',
        'rgb(232, 80, 90)',
        'rgb(250, 141, 119)',
        'rgb(159, 166, 209)',
        'rgb(253, 234, 204)',
        'rgb(123, 126, 175)',
        'rgb(74, 75, 123)',
        'rgb(240, 185, 197)',
        'rgb(196, 143, 193)',
        'rgb(110, 112, 172)',
        'rgb(159, 166, 209)',
        'rgb(253, 224, 202)',
        'rgb(2, 138, 155)',
        'rgb(253, 197, 150)',
    ]

    item_a_color = {}

    for preg in preguntas:
        index = 0
        for item in items:
            if item.pregunta_id == preg.id:
                map_preg_a_array_cant_resp_item[preg.id].append(len(Respuesta.query.filter_by(item_id = item.id).all()))
                map_preg_a_array_percent_resp_item[preg.id].append(len(Respuesta.query.filter_by(item_id = item.id).all()))
                map_preg_a_array_str[preg.id].append(item.description)
                item_a_color[item.id] = colores[index % len(colores)]
                index += 1

    map_respuestas_y_total = {}

    for item in items:
        temp = Respuesta.query.filter_by(item_id = item.id).all()
        temp_tot = Respuesta.query.filter_by(pregunta_id = item.pregunta_id).all()
        map_respuestas_y_total[item.id] = [len(temp), len(temp_tot)]
    
    for preg in preguntas:
        for i in range(len(map_preg_a_array_percent_resp_item[preg.id])):
            if map_respuestas_y_total[item.id][1] != 0:
                map_preg_a_array_percent_resp_item[preg.id][i] = round(map_preg_a_array_percent_resp_item[preg.id][i] * 100 / map_respuestas_y_total[item.id][1], 1)
            else:
                map_preg_a_array_percent_resp_item[preg.id][i] = 0

    return render_template('resultado_encuesta.html', 
        title= 'Resultados Encuesta',
        encuesta = encuesta,
        preguntas = preguntas,
        items = items,
        map_respuestas_y_total = map_respuestas_y_total,
        map_preg_resp = map_preg_a_array_cant_resp_item,
        map_preg_perc = map_preg_a_array_percent_resp_item,
        map_preg_str = map_preg_a_array_str,
        item_a_color = item_a_color,
        colores = colores,
    )


@app.route("/encuesta/<encuesta_id>/respuesta/<date_time>", methods=['GET'])
@login_required
def respuestas_encuesta(encuesta_id, date_time):
    
    
    encuesta = Encuesta.query.get_or_404(encuesta_id)
    preguntas = Pregunta.query.filter_by(encuesta_id = encuesta_id)

    id_preguntas = []
    for preg in preguntas:
        id_preguntas.append(preg.id)

    items = Item.query.filter(Item.pregunta_id.in_(id_preguntas))


    filtro1 = date_time + ":000000"
    filtro2 = date_time + ":999999"

    date1 = datetime.strptime(filtro1, '%d-%m-%Y %H:%M:%S:%f')
    date2 = datetime.strptime(filtro2, '%d-%m-%Y %H:%M:%S:%f')

    respuestas = Respuesta.query.filter(Respuesta.id_usuario == current_user.username, Respuesta.date >= date1, Respuesta.date <= date2)

    for r in respuestas:
        print("hola " + str(r.id))

    return render_template('respuestas_encuesta.html', 
        title = 'Respuestas Encuesta',
        encuesta = encuesta,
        preguntas = preguntas,
        items = items,
        respuestas = respuestas,
        date_time = date_time
    )