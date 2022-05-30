from operator import length_hint
from wsgiref.validate import validator
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from encuestas.models import User
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Nombre',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    tipo = BooleanField('Tipo usuario', default=False)
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso, por favor escoga otro.')
    def validate_email(self,email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('Este email ya está en uso, por favor escoga otro.')

class updatePerfil(FlaskForm):
    name = StringField('Nombre',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Actualiza tu información')
    picture = FileField('Actualiza foto de perfil', validators=[FileAllowed(['jpg','png'])])
    visible = BooleanField('Sí, quiero mi información visible en el perfil', default=True)
    def validate_name(self,name):
        if name.data!= current_user.name:
            user = User.query.filter_by(name= name.data).first()
            if user:
                raise ValidationError('Este nombre de usuario ya está en uso, por favor escoga otro.')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError('Este email ya está en uso, por favor escoga otro.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuerda mi usuario')
    submit = SubmitField('Login')


class CrearItemForm(FlaskForm):
    description = StringField('Descripcion', validators=[DataRequired(), Length(min=1,max=100)])
    submit = SubmitField('Añadir Item')


class CrearPreguntaForm(FlaskForm):
    title = StringField('Titulo', validators = [DataRequired(),Length(min=2,max=100)])
    submit = SubmitField('Añadir Pregunta')


class CrearEncuestaForm(FlaskForm):
    title = StringField('Titulo', validators = [DataRequired(), Length(min=2, max = 100)])
    submit = SubmitField('Guardar Título')

class EnviarRespuestaForm(FlaskForm):
    submit = SubmitField('Enviar Respuesta')
