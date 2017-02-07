#!/usr/bin/env python3
import json
import pymongo
import datetime
import os

from logger import Logger

conn = pymongo.MongoClient("127.0.0.1",27017)
db = conn.aqir #连接库

l = Logger('mkts.log')
trace = l.trace
ll = l.getlog()


def main():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           str(datetime.datetime.now()) + '.json'), 'w') as ojson:
        while db.log.count() > 100000:
            ll.debug('db count[{0}]'.format(db.log.count()))
            ids = []
            for log in db.log.find().limit(1000):
                idx = log['_id']
                ids.append(idx)
                log['_id'] = str(idx)
                ojson.write(json.dumps(log))
                ojson.write('\n')

            for idx in ids:
                db.log.delete_one({"_id": idx})

if __name__ == '__main__':
    main()
