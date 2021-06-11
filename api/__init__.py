from flask import Flask
from flask.views import MethodView

app=Flask(__name__)

class PatientAPI(MethodView):

    def get(self, pt_id):
        if pt_id is None:
            # return a list of users
            pass
        else:
            # expose a single user
            pass

    def post(self):
        # create a new user
        pass

    def delete(self, pt_id):
        # delete a single user
        pass

    def put(self, pt_id):
        # update a single user
        pass

@app.route('/')
def home():
    return "Hey there!"