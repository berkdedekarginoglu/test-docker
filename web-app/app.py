import json

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.TwitterWorkers

States = db["States"]

States.insert_one({
    "worker_id": "185.203.67.209"
})

class States(Resource):
    def post(self):
        data = request.get_json()
        States.update_one({"worker_id":"185.203.67.209"},{"$set":data})
        return {"success":True}

    def get(self):
        state = States.find({})
        return jsonify(state)


class Student(Resource):
    def get(self,name):
        return {'student': name}



routes = ['/states/add','/states']

api.add_resource(Student, '/student/<string:name>')
api.add_resource(States,*routes)

if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0')
