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

class Add(Resource):
    def post(self):
        postedData = request.get_json()
        retMap = {
            'Message': 'ok',
            'Status Code': 200
        }
        States.insert_one(postedData)

        return jsonify(retMap)

class Get(Resource):
    def get(self):
        prev_num = States.find({})[0]
        return jsonify(prev_num)



api.add_resource(Add, "/states/add")
api.add_resource(Get, "/states")

if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0')
