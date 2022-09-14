import datetime
from calendar import calendar
from unittest import result
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)


### WEB ####
@app.route('/')
def index():
    return render_template('bandits-scan-statistics.html')


### MONGO ####
class MongoDB:
    def __init__(self, db_name, column_name):
        self.client = MongoClient('mongodb://db:27017')
        self.selected_db = self.client[db_name]
        self.selected_column = self.selected_db[column_name]

    def get(self, query):
        try:
            res = self.selected_column.find(query, {'_id': 0})

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
        self.mongo = MongoDB('twitter_banditos', 'bandits_scan_statistics')

    def post(self):  # Add New Statistic
        try:
            postedData = request.get_json()

            isExist = self.mongo.get({'bandit':postedData['bandit']})

            if len(isExist.json['data']) > 0:
                return jsonify({
                    'success':False,
                    'error':'Bandit exist'
                })

            postedData['created_at'] = datetime.datetime.timestamp(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
            res = self.mongo.get({})
            return jsonify({'success':True,'data':res.json['data']})

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
                    'success':False,
                    'error':'User does not exist'
                })

            postedData['updated_at'] = datetime.datetime.timestamp(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
        self.mongo = MongoDB('twitter_banditos', 'bandits_scan_statistics')

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

api.add_resource(BanditsStatistics, '/api/bandits/statistics')
api.add_resource(BanditsStatisticsFilter, '/api/bandits/statistics/filter')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
