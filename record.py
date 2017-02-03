#!/usr/bin/env python3
from flask import Blueprint
from flask import request
from flask.ext.restful import Api, Resource
from bson.objectid import ObjectId
import pymongo

conn = pymongo.MongoClient("127.0.0.1", 27017)
db = conn.aqir #连接库

app = Blueprint("record", __name__)

api = Api()

@app.record_once
def on_load(state):
    api.init_app(app)


class Record(Resource):
    def get(self, idx=None):
        if idx:
            rc = db.log.find_one({"_id": ObjectId(idx)})
            rc['_id'] = str(rc['_id'])
        else:
            limit = 100
            if request.args.get('limit'):
                limit = int(request.args.get('limit').strip('/'))
            rcs = db.log.find({}, {"_id": 1}).limit(limit)
            rc = []
            for r in rcs:
                rc.append(str(r['_id']))

        return {'code': 0,
                'msg': '',
                'payload': {
                    'data': rc,
                    'count': db.log.count()}
                }

    def delete(self, idx=None):
        db.log.delete_one({"_id": ObjectId(idx)})
        return {'code': 0,
                'msg': '',
                'payload': {}
                }


api.add_resource(Record,
                 '/record/',
                 '/record/<string:idx>/',
                 endpoint='record')
