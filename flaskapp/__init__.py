from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskapp.config import Config


#  run python run.py
# CREATE EXTENSIONS OUTSIDE OF FUNCTION BUT INITIALIZE INSIDE FUNCTION WITH THE APPLICATION
db = SQLAlchemy() #represent database structure as classes -> called MODELS
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # telling extension where the login route is located, login is fn name for route
login_manager.login_message_category = 'info' # blue info alert in bootstrap
mail = Mail() #initializes extension



def create_app(config_class=Config):
    app = Flask(__name__)  # special variable in python that's the name of the module
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # REGISTER BLUEPRINTS
    from flaskapp.users.routes import users  # name of users that is instance of Blueprint class
    from flaskapp.main.routes import main
    from flaskapp.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app



