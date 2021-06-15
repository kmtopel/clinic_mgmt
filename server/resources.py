from flask_restful import Resource, abort
from flask_restful.utils import http_status_message
from .models import Patient
from api import auth, db
from flask import request

def abort_if_not_found(pt_id):
    tbl = Patient.query.with_entities(Patient.id)
    tbl = [value for value, in tbl]
    if pt_id not in tbl:
        abort(404, message="{} not found.".format(pt_id)) 

class Patients(Resource):
    decorators = [auth.login_required]
    def get(self, pt_id=None):
        if pt_id is None:
            pts = [pt.to_json() for pt in Patient.query.all()]
            return pts
        else:
            pt = Patient.query.filter_by(id=pt_id).first()
            abort_if_not_found(pt_id)
            return pt.to_json()

    def post(self):
        try:
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            dob = request.form.get('dob')
            new_pt = Patient(fname=fname, lname=lname, dob=dob, active=True)
            db.session.add(new_pt)
            db.session.commit()
            return http_status_message(201)
        except:
            return http_status_message(400)

    def put():
        pass

    def delete():
        pass