from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
selected_db = client.twitter_workers_db
worker_states = selected_db.worker_states


class Add(Resource):
    def post(self):
        try:
            postedData = request.get_json()
            worker_states.insert_one(postedData)
            returnMap = {
                'success': True
            }
            return jsonify(returnMap)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)


class Get(Resource):
    def get(self):
        try:
            res = worker_states.find({})
            for x in res:
                del x['_id']

            returnMap = {
                'success': True,
                'data': res
            }

            return jsonify(returnMap)
        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)


api.add_resource(Add, "/states/add")
api.add_resource(Get, "/states/all")

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
