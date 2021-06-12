from flask_restful import Resource, abort
from .models import Patient

def abort_if_not_found(pt_id):
    tbl = Patient.query.with_entities(Patient.id)
    tbl = [value for value, in tbl]
    if pt_id not in tbl:
        abort(404, message="{} not found.".format(pt_id)) 

class Patients(Resource):
    def get(self, pt_id=None):
        if pt_id is None:
            pts = [pt.to_json() for pt in Patient.query.all()]
            return pts
        else:
            pt = Patient.query.filter_by(id=pt_id).first()
            abort_if_not_found(pt_id)
            return pt.to_json()

    def post():
        pass

    def put():
        pass

    def delete():
        pass