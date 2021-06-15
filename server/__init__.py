from flask import Flask
import os
from flask_login.utils import _secret_key
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth

app=Flask(__name__)
secret_key = os.urandom(25)
jwt_secret_key = os.urandom(50)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = secret_key
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


db = SQLAlchemy(app)
migrate = Migrate(app,db)
api = Api(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
auth = HTTPBasicAuth()

from .models import User
from .views import *
from .resources import *

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(email=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user

@app.route("/")
@auth.login_required
def index():
    user = auth.current_user()
    return "Hello {} {}".format(user.fname, user.lname)

api.add_resource(Patients,'/patients','/patients/','/patients/<int:pt_id>')