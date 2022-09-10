from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import bson.json_util as json_util

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.TwitterWorkers
States = db["States"]
States.insert_one({
    "worker_id": "185.203.67.209"
})


def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301 #Missing parameter
        else:
            return 200
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"])==0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "add")

        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return json_util.dumps(retJson)

        States.update({"worker_id":"185.203.67.209"},{"$set":{"num_of_users":postedData}})
        retMap = {
            'success':True
        }

        return json_util.dumps(retMap)

class Get(Resource):
    def get(self):
        res = States.find_one({"worker_id":"185.203.67.209"})
        return json_util.dumps(res)



api.add_resource(Add, "/add")
api.add_resource(Get, "/get")

if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0')
