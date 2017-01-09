#!/usr/bin/env python3
import pymongo
from pymongo import DeleteOne

conn_bak = pymongo.MongoClient("127.0.0.1", 27017)
db_bak = conn_bak.aqir

conn = pymongo.MongoClient("192.168.1.199", 27017)
db = conn.aqir


while db.log.count() > 1000:
    print(db.log.count())
    origs = list(db.log.find().sort('_id').limit(100))
    rqs = []
    for log in origs:
        db_bak.log.save(log)
        db.log.delete_one({'_id': log['_id']})

print('done')
print(db.log.count())
