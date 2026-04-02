from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PetPostForm(FlaskForm):
    announcement_type = SelectField('Announcement Type', choices=[('Lost', 'Lost'), ('Found', 'Found')], validators=[DataRequired()])
    animal_type = SelectField('Animal Type', choices=[('Cat', 'Cat'), ('Dog', 'Dog'), ('Bird', 'Bird'), ('Other', 'Other')], validators=[DataRequired()])
    breed = StringField('Breed')
    color = StringField('Color')
    district = SelectField('District (Rayon)', choices=[
        ('Absheron', 'Absheron'), ('Baku', 'Baku'), ('Ganja', 'Ganja'), ('Sumqayit', 'Sumqayit'),
        ('Binagadi', 'Binagadi'), ('Khatai', 'Khatai'), ('Khazar', 'Khazar'), ('Garadagh', 'Garadagh'),
        ('Narimanov', 'Narimanov'), ('Nasimi', 'Nasimi'), ('Nizami', 'Nizami'), ('Sabail', 'Sabail'),
        ('Sabunchu', 'Sabunchu'), ('Surakhani', 'Surakhani'), ('Yasamal', 'Yasamal'), ('Pirallahi', 'Pirallahi')
    ], validators=[DataRequired()])
    date_lost_found = DateField('Date Lost/Found', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=500)])
    images = MultipleFileField('Upload Images (up to 5)')
    submit = SubmitField('Post Announcement')

class ContactForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Send Message')
