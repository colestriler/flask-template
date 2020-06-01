from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskapp import db, bcrypt
from flaskapp.models import User

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
#@main.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

