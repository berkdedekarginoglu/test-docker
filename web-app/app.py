import datetime

from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)



client = MongoClient("mongodb://db:27017")
selected_db = client.twitter_workers_db

worker_states = selected_db.worker_states
worker_states.drop()
worker_states = selected_db.worker_states

agent_stats = selected_db.agent_stats
agent_stats.drop()
agent_stats = selected_db.agent_stats

agent_scans = selected_db.agent_scans
agent_scans.drop()
agent_scans = selected_db.agent_scans

@app.route("/bandits/live")
def live_bandits():
    return render_template("bandits.html")

@app.route("/agents/live")
def live_agents():
    return render_template("agents.html")

@app.route("/")
def index():
    return render_template("bandits.html")


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
            res = worker_states.find({},{'_id':0})
            return jsonify(list(res))
        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class Update(Resource):
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

#agents

class GetAgentScans(Resource):
    def get(self):
        try:
            res = agent_scans.find({},{'_id':0})
            return jsonify(list(res))
        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class GetAgentStats(Resource):
    def get(self):
        try:
            res = agent_stats.find({},{'_id':0})
            return jsonify(list(res))
        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class UpdateAgentScan(Resource):
    def post(self):
        try:
            postedData = request.get_json()
            agent_scans.update_one({"country_code":postedData['country_code'],
                                      "gsm_code":postedData['gsm_code'],
                                      "current_step":postedData['current_step']},{"$set":postedData}, upsert=True)

            agent_stats.update_one({"agent":postedData["agent"]},{"$set": {
                "agent":postedData["agent"],
                "last_info":str(datetime.datetime.now()),
                "current_country":postedData["country_code"],
                "current_gsm":postedData["gsm_code"],
                "current_step":postedData["current_step"],
                "proxy_host":postedData["proxy_host"],
                "proxy_port":postedData["proxy_port"]
            }}, upsert=True)
            retunMap = {
                'success': True
            }
            return jsonify(retunMap)
        except Exception as e:
            retunMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(retunMap)


api.add_resource(Update, "/bandits")
api.add_resource(UpdateAgentScan, "/agents/scans")

api.add_resource(Get, "/bandits")
api.add_resource(GetAgentScans, "/agents/scans")
api.add_resource(GetAgentStats, "/agents/stats")

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
