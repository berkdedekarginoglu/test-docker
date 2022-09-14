import datetime

from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)



client = MongoClient("mongodb://db:27017")
selected_db = client.twitter_workers_db

worker_states = selected_db.bandits_statistics
worker_states.drop()
worker_states = selected_db.bandits_statistics


@app.route("/")
def index():
    return render_template("bandits.html")


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
            res = worker_states.find({},{'_id':0})
            return jsonify(list(res))
        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class UpdateBanditScan(Resource):
    def post(self):
        try:
            postedData = request.get_json()
            worker_states.update_one({"worker_ip":postedData['worker_ip']},{"$set":postedData}, upsert=True)
            retunMap = {
                'success': True
            }
            return jsonify(retunMap)
        except Exception as e:
            retunMap = {
                'success': False,
                'error': str(e)
            }

api.add_resource(UpdateBanditScan, "/bandits")
api.add_resource(Get, "/bandits")


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
