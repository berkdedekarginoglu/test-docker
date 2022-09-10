from flask import Flask, request
from flask_restful import Resource, Api

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client["TwitterWorkers"]
TwitterWorkers = db["States"]

TwitterWorkers.insert_one({
    "worker_id": "185.203.67.209"
})

class States(Resource):
    def post(self):
        data = request.get_json()
        TwitterWorkers.update_one({"worker_id":"185.203.67.209"},data)
        return {"success":True}

    def get(self):
        state = TwitterWorkers.find({"worker_id":"185.203.67.209"})
        return state


class Student(Resource):
    def get(self,name):
        return {'student': name}




api.add_resource(Student, '/student/<string:name>')
api.add_resource(States,'/states/add')
api.add_resource(States,'/states')

if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0')
