#!/usr/bin/env python3

import json
from bson.objectid import ObjectId
import os
import pymongo
from multiprocessing.dummy import Pool

from logger import Logger

conn = pymongo.MongoClient("127.0.0.1",27017)
db = conn.aqir #连接库

l = Logger(__name__ + '.log')
trace = l.trace
log = l.getlog()


def handle_json(f):
    log.debug('handle [{0}]'.format(f))
    with open(f) as jsons:
        for rec in jsons:
            weather = json.loads(rec)
            weather['_id'] = ObjectId(weather['_id'])

            db.log.save(weather)
            #log.debug('saved [{0}]'.format(weather['_id']))

    log.debug('log count [{0}]'.format(db.log.count()))
    log.debug('remove [{0}]'.format(f))
    os.remove(f)


def main():
    jsons = []
    
    for r, d, fs in os.walk('./jsons'):
        for f in fs:
            f = os.path.join(r, f)
            if f.endswith('.json'):
                jsons.append(f)
#                handle_json(f)
            else:
                log.debug('skip [{0}]'.format(f))

    p=Pool(16)
    p.map(handle_json, jsons)
    p.close()
    p.join()
    
if __name__ == '__main__':
    main()
