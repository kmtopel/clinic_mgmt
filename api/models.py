from api import db, bcrypt, login_manager, app
from flask_login import UserMixin
import jwt
from datetime import datetime as dt, timedelta

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(255))
    lname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    admin = db.Column(db.Boolean())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = bcrypt.generate_password_hash(self.password) 

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': dt.utcnow() + timedelta(days=0, seconds=5),
                'iat': dt.utcnow(),
                'sub': user_id
            }
            
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "fname": self.fname,
            "lname": self.lname,
            "email": self.email,
            "password": self.password,
            "active": bool(self.active),
            "date_created": self.date_created,
            "admin": bool(self.admin)
        }
        
        return tbl_dict

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "fname": self.fname,
            "lname": self.lname,
            "dob": self.dob,
            "active": bool(self.active),
            "date_created": dt.strftime(self.date_created, "%m/%d/%Y %H:%m")
        }
        
        return tbl_dict

db.create_all()

# user = User(fname="kevin",lname="topel",email="kmtopel@gmail.com",password="testing",active=True,admin=True)
# db.session.add(user)
# db.session.commit()

# user = User.query.first()
# print(user.password.decode('utf-8'))

# user = User(id=1,password='testing')
# token = user.encode_auth_token(user.id)
# print('\n')
# print(token)
# print('\n')