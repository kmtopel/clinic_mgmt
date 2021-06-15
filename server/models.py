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
    notes = db.relationship('PtNotes', backref='user')    

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
    contact = db.relationship('PtContact', backref='patient')
    meds = db.relationship('PtMedList', backref='patient')
    disp = db.relationship('PtMedDisp', backref='patient')
    notes = db.relationship('PtNotes', backref='patient')

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

class PtContact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pt_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    type = db.Column(db.String(75),nullable=False)
    info = db.Column(db.String(255),nullable=False)
    desc = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "pt_id": int(self.pt_id),
            "type": self.type,
            "info": self.info,
            "desc": self.desc, 
            "date_created": dt.strftime(self.date_created, "%m/%d/%Y %H:%m")
        }
        return tbl_dict

class PtAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pt_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    zip = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "pt_id": int(self.pt_id),
            "street": self.type,
            "city": self.info,
            "zip": self.desc, 
            "date_created": dt.strftime(self.date_created, "%m/%d/%Y %H:%m")
        }
        return tbl_dict

class PtDx(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pt_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    dx = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "pt_id": int(self.pt_id),
            "dx": self.dx,
            "date_created": self.date_created
        }
        return tbl_dict

class PtMedList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pt_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    med_id = db.Column(db.Integer, db.ForeignKey('drug.id'), nullable=False)
    med = db.Column(db.String(255), nullable=False)
    dose = db.Column(db.String(255), nullable=False)
    sig = db.Column(db.String(255), nullable=False)
    pap_status = db.Column(db.String(255))
    pap_notes = db.relationship('PtPAPNotes', backref='pt_med_list')
    active = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "pt_id": int(self.pt_id),
            "med": self.med,
            "dose": self.dose,
            "sig": self.sig,
            "active": self.active,
            "date_created": self.date_created
        }
        return tbl_dict

class PtMedDisp(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pt_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    strength_id = db.Column(db.Integer, db.ForeignKey('strength.id'), nullable=False)
    drug_id = db.Column(db.Integer, db.ForeignKey('drug.id'), nullable=False)
    date_disp = db.Column(db.DateTime)
    sig = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "pt_id": int(self.pt_id),
            "strength_id": int(self.strength_id),
            "drug_id": int(self.drug_id),
            "date_disp": self.date_disp,
            "med": self.med,
            "dose": self.dose,
            "sig": self.sig,
            "active": self.active,
            "date_created": self.date_created
        }
        return tbl_dict

class PtNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pt_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    
    type = db.Column(db.String(255), nullable=False)
    note = db.Column(db.String(4294000000), nullable=False)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    comments = db.relationship('PtComments', backref='pt_notes')    

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "pt_id": int(self.pt_id),
            "user_id": int(self.user_id),
            "type": self.date_disp,
            "note": self.note,
            "date_created": self.date_created
        }
        return tbl_dict

class PtComments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey('pt_notes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.String(4294000000), nullable=False)
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "note_id": int(self.note_id),
            "comment_id": int(self.comment_id),
            "pt_id": int(self.pt_id),
            "comment": self.note,
            "date_created": self.date_created
        }
        return tbl_dict
 
class PtPAPNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    med_id = db.Column(db.Integer, db.ForeignKey('drug.id'))
    medlist_id = db.Column(db.Integer, db.ForeignKey('pt_med_list.id'))
    type = db.Column(db.String(255), nullable=False)
    note = db.Column(db.String(4294000000), nullable=False)
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "med_id": int(self.med_id),
            "medlist_id": int(self.medlist_id),
            "type": self.type,
            "note": self.type,
            "date_created": self.type
        }
        return tbl_dict

class Drug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    pap = db.Column(db.Boolean())
    manufacturer = db.Column(db.String(80), default="None")
    disp = db.relationship('PtMedDisp', backref='drug')
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def to_json(self):
        tbl_dict = {
        "id": int(self.id),
        "name": self.name,
        "pap":  self.pap,
        "manufacturer": self.manufacturer,
        "date_created": self.date_created
        }
        return tbl_dict

class Strength(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    disp = db.relationship('PtMedDisp', backref='strength', lazy=True)

    def to_json(self):
        tbl_dict = {
            "id": int(self.id),
            "strength": self.strength,
            "date_created": self.date_created
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