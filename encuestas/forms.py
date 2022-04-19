from operator import length_hint
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CrearItem(FlaskForm):
    description = StringField('Descripcion', validators=[DataRequired(), Length(min=1,max=100)])

class CrearPreguntaForm(FlaskForm):
    title = StringField('Titulo', validators = [DataRequired(),Length(min=2,max=100)])


class CrearEncuestaForm(FlaskForm):
    title = StringField('Titulo', validators = [DataRequired(), Length(min=2, max = 100)])
    submit = SubmitField('Guardar')
