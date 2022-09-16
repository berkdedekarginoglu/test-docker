from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)


### WEB ####

### MONGO ####
class MongoDB:
    def __init__(self, db_name, column_name):
        self.client = MongoClient('mongodb://db:27017')
        self.client.drop_database(db_name)
        self.selected_db = self.client[db_name]
        self.selected_column = self.selected_db[column_name]

    def get(self, query, limit=10, skip=0, deleteAfterFind=False):
        try:
            if deleteAfterFind:
                m = [x['_id'] for x in self.selected_column.find({}, {'_id': 1}, limit=limit)]
                self.selected_column.delete_many({'_id': {'$in': list(m)}})
                return jsonify({
                    'success': True,
                    'data': list(m)
                })
            else:
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

    def insertMany(self, data):
        try:
            self.selected_column.insert_many(data,ordered=False)
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

    def updateMany(self, query, data):
        try:
            self.selected_column.update_many(query, {'$set': data}, upsert=True)
            return jsonify({
                'success': True
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })


### Bandit-API ###


class AddAccountsToLocked(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_locked')

    def post(self):
        try:

            postedData = request.get_json()
            for x in list(postedData):
                result = self.mongo.updateOne({'phone_number':x['phone_number']},x)
            return jsonify(result.json)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class GetAccountsFromLocked(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_locked')

    def post(self):
        try:
            postedData = request.get_json()
            result = self.mongo.get({},limit=int(postedData['count']),deleteAfterFind=False)

            return jsonify(result.json)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class AddAccountsToNotRegistred(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_not_registred')

    def post(self):
        try:

            postedData = request.get_json()

            result = self.mongo.insertMany(postedData)
            return jsonify(result.json)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class GetAccountsFromNotRegistred(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_not_registred')

    def post(self):
        try:
            postedData = request.get_json()
            result = self.mongo.get({},limit=int(postedData['count']),deleteAfterFind=False)

            return jsonify(result.json)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class AddAccountsToSuccess(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_success')

    def post(self):
        try:

            postedData = request.get_json()

            result = self.mongo.insertMany(postedData)
            return jsonify(result.json)

            return jsonify({
                'success': False,
                'error':result.json
            })

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class GetAccountsFromSuccess(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_success')

    def post(self):
        try:
            postedData = request.get_json()
            result = self.mongo.get({},limit=int(postedData['count']),deleteAfterFind=False)

            return jsonify(result.json)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class AddAccountsToWrongPassword(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_wrong_password')

    def post(self):
        try:

            postedData = request.get_json()

            result = self.mongo.insertMany(postedData)
            return jsonify(result.json)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class GetAccountsFromWrongPassword(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_wrong_password')

    def post(self):
        try:
            postedData = request.get_json()
            result = self.mongo.get({},limit=int(postedData['count']),deleteAfterFind=False)

            return jsonify(result.json)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class AddAccountsToExceptions(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_exceptions')

    def post(self):
        try:

            postedData = request.get_json()

            result = self.mongo.insertMany(postedData)
            return jsonify(result.json)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)

class GetAccountsFromExceptions(Resource):
    def __init__(self):
        self.mongo = MongoDB('banditos', 'accounts_exceptions')

    def post(self):
        try:
            postedData = request.get_json()
            result = self.mongo.get({},limit=int(postedData['count']),deleteAfterFind=False)

            return jsonify(result.json)

        except Exception as e:
            returnMap = {
                'success': False,
                'error': str(e)
            }
            return jsonify(returnMap)


api.add_resource(AddAccountsToLocked, '/api/accounts/locked/add')
api.add_resource(GetAccountsFromLocked, '/api/accounts/locked/get')
api.add_resource(AddAccountsToNotRegistred, '/api/accounts/notregistred/add')
api.add_resource(GetAccountsFromNotRegistred, '/api/accounts/notregistred/get')
api.add_resource(AddAccountsToSuccess, '/api/accounts/success/add')
api.add_resource(GetAccountsFromSuccess, '/api/accounts/success/get')
api.add_resource(AddAccountsToWrongPassword, '/api/accounts/wrongpasswords/add')
api.add_resource(GetAccountsFromWrongPassword, '/api/accounts/wrongpasswords/get')
api.add_resource(AddAccountsToExceptions, '/api/accounts/exceptions/add')
api.add_resource(GetAccountsFromExceptions, '/api/accounts/exceptions/get')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
