import os
from flask import (render_template, url_for, flash, redirect, request, Blueprint, abort)
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import db, bcrypt
from flaskapp.models import User
from flaskapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, UpdateAccountFormProfile)
from flask import current_app

users = Blueprint('users', __name__)

# VARIABLES
#####################################################

UPLOAD_FOLDER = "profile-pictures"
BUCKET = "datafied-public"


# ROUTES
#####################################################

@users.route('/users/register', methods=['GET', 'POST']) #POST submits register form
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8') # utf-8 makes it a string
        user = User(first_name=form.first_name.data.capitalize(),
                    last_name=form.last_name.data.capitalize(),
                    username=form.username.data.lower().replace(" ", ""),
                    email=form.email.data.lower(),
                    password=hashed_password)
        db.session.add(user)# add user to database
        db.session.commit() #save database
        login_user(user)
        flash(f'Your account has been created! '
              f'You are now logged in.', 'success') #"success" = bootstrap class name
        return redirect(url_for('main.explore')) #redirect to name of function
    return render_template('register.html', title='Register', form=form)



@users.route('/users/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.explore'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): #check that password entered matches
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #redirect to intended page
            return redirect(next_page) if next_page else redirect(url_for('main.home')) #redirect
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)



@users.route('/users/logout')
def logout():
    logout_user()
    return redirect(url_for('main.explore'))



@users.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def settings():
    # posts = db.session.query(Post).filter(Post.user_id == current_user.id).subquery()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data.lower().replace(" ", "")
        current_user.email = form.email.data.lower()
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your account has been updated!', 'success') # success = bootstrap category
        return redirect(url_for('users.profile', username=current_user.username)) #lookip POST GET redirect pattern
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('settings.html', title='Account',
                           image_file=image_file, form=form)


@users.route('/<string:username>', methods=['GET', 'POST'])
def profile(username):
    form = UpdateAccountFormProfile()
    page = request.args.get('page', 1, type=int) #not sure what this does. vid9
    user = User.query.filter_by(username=username).first_or_404() #first user or 404 error
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    if current_user == user:
        if form.validate_on_submit():
            current_user.bio = form.bio.data
            db.session.commit()
            flash('Your account has been updated!', 'success') # success = bootstrap category
            return redirect(url_for('users.profile', username=current_user.username)) #lookip POST GET redirect pattern
        elif request.method == "GET":
            form.bio.data = current_user.bio
    return render_template('profile.html', user=user, image_file=image_file, form=form)



@users.route('/settings/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user and not current_user.is_admin:
        abort(403)
    # DELETE NOTEBOOK FROM S3
    db.session.delete(user)
    db.session.commit()
    flash('Your account has successfully been deleted.', 'success')
    return redirect(url_for('main.home'))



@users.route('/users/reset_password', methods=['GET', 'POST']) #vid10
def reset_request():
    if current_user.is_authenticated: #make sure user is logged out to reset password
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST']) #vid10
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # utf-8 makes it a string
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in.', 'success') #"success" = bootstrap class name
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
