from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskapp.models import User


genders = (('f', 'F'), ('m', 'M'))

class RegistrationForm(FlaskForm):
    # want to use validators
    first_name = username = StringField('First Name:',
                                        validators=[DataRequired()])
    last_name = StringField('Last Name:',
                            validators=[DataRequired()])
    username = StringField('Create Username:',
                    validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password:',
                             validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password:',
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up for Datafied')


    def validate_username(self, username):
        # getting first value back from database, none if no user exists
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. "
                                  "Please choose a different one.")

    def validate_email(self, email):
        # getting first value back from database, none if no user exists
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("That email is taken. "
                                  "Please choose a different one.")


class LoginForm(FlaskForm):
    # username = StringField('Username',
    #                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountFormProfile(FlaskForm):
    # want to use validators
    picture = FileField('Upload a profile picture:',
                        validators=[FileAllowed(['jpg', 'png'])], id='HELLO')
    bio = TextAreaField('Add a bio:', validators=[DataRequired()])
    submit = SubmitField('Update profile')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("That email is taken. "
                                      "Please choose a different one.")


class UpdateAccountForm(FlaskForm):
    # want to use validators
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Upload a profile picture:',
                        validators=[FileAllowed(['jpg', 'png'])], id='HELLO')
    bio = TextAreaField('Add a bio:', validators=[DataRequired()])
    submit = SubmitField('Update account settings')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(
                username=username.data).first()
            if user:
                raise ValidationError("That username is taken. "
                                      "Please choose a different one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("That email is taken. "
                                      "Please choose a different one.")


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. "
                                  "You must register first.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
