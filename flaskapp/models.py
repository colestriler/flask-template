
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskapp import db, login_manager
from flask_login import UserMixin


# From Documentation
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sex = db.Column(db.String(6), nullable=True, default='N/A')
    dob = db.Column(db.DateTime(), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable=False, default = 'default.jpg')
    is_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text, default=' ')
    num_posts = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800): # 30 mins
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod # doesn't take self parameter as an argument
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self): #how our object is printed when we print it out
        return f"User('{self.date_joined}', '{self.username}', '{self.first_name}', '{self.email}', '{self.image_file}')"
