import datetime
import uuid
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)


### WEB ####
@app.route('/')
def index():
    return render_template('bandits.html')


### MONGO ####
class MongoDB:
    def __init__(self, db_name, column_name):
        self.client = MongoClient('mongodb://db:27017')
        self.selected_db = self.client[db_name]
        self.selected_column = self.selected_db[column_name]

    def get(self, query, limit=10, skip=0):
        try:
            res = self.selected_column.find(query, {'_id': 0}).limit(limit).skip(skip)

            return jsonify({
                'success': True,
                'data': list(res)
            })

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
        return jsonify(returnMap)

    def insertOne(self, data):
        try:
            self.selected_column.insert_one(data)
            return jsonify({
                'success': True
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

    def updateOne(self, query, data):
        try:
            self.selected_column.update_one(query, {'$set': data}, upsert=True)
            return jsonify({
                'success': True
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })


### Bandit-API ###


class BanditsStatistics(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'bandits_scan_statistics')

    def post(self):  # Add New Statistic
        try:
            postedData = request.get_json()

            isExist = self.mongo.get({'bandit': postedData['bandit']})

            if len(isExist.json['data']) > 0:
                return jsonify({
                    'success': False,
                    'error': 'Bandit exist'
                })

            postedData['created_at'] = datetime.datetime.timestamp(datetime.datetime.now())

            result = self.mongo.insertOne(postedData)

            if result.json['success']:
                return jsonify({
                    'success': True
                })

            return jsonify({
                'success': False,
                'error': result.json['error']
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

    def get(self):  # Get All Statistics
        try:
            args = request.args

            limit = int(args['limit'])
            skip = int(args['skip'])

            res = self.mongo.get({}, limit=limit, skip=skip)
            return jsonify({'success': True, 'data': res.json['data']})

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

    def put(self):  # Update Statistic
        try:

            postedData = request.get_json()

            isExist = self.mongo.get({'bandit': postedData['bandit']})

            if len(isExist.json['data']) < 1:
                return jsonify({
                    'success': False,
                    'error': 'User does not exist'
                })

            postedData['updated_at'] = datetime.datetime.timestamp(datetime.datetime.now())

            result = self.mongo.updateOne({'bandit': postedData['bandit']}, postedData)

            if result.json['success']:
                return jsonify({
                    'success': True
                })

            return jsonify({
                'success': False,
                'error': result.json['error']
            })

        except Exception as e:

            return jsonify({
                'success': False,
                'error': str(e)
            })


class BanditsStatisticsFilter(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'bandits_scan_statistics')

    def post(self):  # Get Bandit Filter
        try:
            postedData = request.get_json()
            result = self.mongo.get(postedData)

            if result.json['success']:
                return jsonify({
                    'data': result.json['data'],
                    'success': True
                })

            return jsonify({
                'success': False,
                'error': result.json['error']
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })


class JobPoolCheckService(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'job_pool')

    def post(self):  # Get All Statistics
        try:
            postedData = request.get_json()

            res_con = self.mongo.get({'is_taken': True, 'signed_to': postedData["bandit"], 'is_completed': None},1)

            if len(res_con.json['data']) > 0:
                res_con.json['success'] = True
                return jsonify(res_con.json)

            res = self.mongo.get({'is_taken': False}, 1)

            if len(res.json['data']) < 1:
                return jsonify({
                    'success': False,
                    'error': 'Job not exist'
                })

            job_signed_result = self.mongo.updateOne({"job_id": res.json['data'][0]["job_id"]}, {
                "signed_to": postedData["bandit"],
                "signed_date": datetime.datetime.timestamp(datetime.datetime.now()),
                "is_taken": True
            })

            if job_signed_result.json["success"]:
                return jsonify({'success': True, 'data': res.json['data']})

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

    def get(self):  # Get All Statistics
        try:
            args = request.args

            limit = int(args['limit'])
            skip = int(args['skip'])

            res = self.mongo.get({}, limit=limit, skip=skip)
            return jsonify({'success': True, 'data': res.json['data']})

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)


class JobPoolCompleteService(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'job_pool')

    def post(self):  # Get All Statistics
        try:
            postedData = request.get_json()
            res = self.mongo.get({'job_id': postedData['job_id']}, 1)

            if len(res.json['data']) < 1:
                return jsonify({
                    'success': False,
                    'error': 'Job not exist'
                })

            job_signed_result = self.mongo.updateOne({"job_id": postedData['job_id']}, {
                "is_completed": True,
                "completed_date": datetime.datetime.timestamp(datetime.datetime.now()),
                "success": postedData['success']
            })

            if job_signed_result.json["success"]:
                return jsonify({'success': True, 'data': res.json['data']})

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)


class JobPoolCreateService(Resource):

    def __init__(self):
        self.mongo = MongoDB('banditos', 'job_pool')

    def post(self):  # Add New Job
        try:
            postedData = request.get_json()
            postedData['job_id'] = str(uuid.uuid4())
            postedData['is_taken'] = False
            postedData['created_date'] = datetime.datetime.timestamp(datetime.datetime.now())

            result = self.mongo.insertOne(postedData)

            if result.json['success']:
                return jsonify({
                    'success': True
                })

            return jsonify({
                'success': False,
                'error': result.json['error']
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })


api.add_resource(BanditsStatistics, '/api/bandits/statistics')
api.add_resource(BanditsStatisticsFilter, '/api/bandits/statistics/filter')
api.add_resource(JobPoolCheckService, '/api/jobs/check')
api.add_resource(JobPoolCompleteService, '/api/jobs/complete')
api.add_resource(JobPoolCreateService, '/api/jobs')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
