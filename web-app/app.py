from flask import Flask
from flask_restful import Resource, Api

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")

db = client.aNewDB
Workers = db["Workers"]

Workers.insert({
    "num_of_workers": 0
})

class Visit(Resource):
    def get(self):
        prev_num = Workers.find({})[0]['num_of_users']
        new_num = prev_num + 1
        Workers.update({},{"$set":{"num_of_workers":new_num}})
        return str("Hello Wordker " + str(new_num))

class Student(Resource):
    def get(self,name):
        return {'student': name}




api.add_resource(Student, '/student/<string:name>')
api.add_resource(Visit,'/hello')


if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0')
