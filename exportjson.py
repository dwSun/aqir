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
    count = 0
    dbs = db.log.count()
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           str(datetime.datetime.now()) + '.json'), 'w') as ojson:

        for log in db.log.find({},{'_id':0, 'time':0, 'datalen':0}):
            ojson.write(json.dumps(log))
            ojson.write('\n')
            count = count + 1
           
            if count % 100 == 0:
                ll.debug('db count[{0}] exported[{1}]'.format(dbs, count))
             
        ll.debug('db count[{0}] exported[{1}]'.format(dbs, count))

if __name__ == '__main__':
    main()
