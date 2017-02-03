#!/usr/bin/env python3
import requests
import json
from bson.objectid import ObjectId
import time
from multiprocessing.dummy import Pool
import pymongo

from logger import Logger

conn = pymongo.MongoClient("127.0.0.1",27017)
db = conn.aqir #连接库

l = Logger('backup.log', log_f=True)
trace = l.trace
ll = l.getlog()

limit = 100
api = 'http://192.168.1.199:5001/api/record/{0}/'

apiLimit = api.format('?limit={0}'.format(limit))


def retrieve(idx):
    try:
        r = requests.get(api.format(idx), timeout=60)
        ret = r.json()
        log = ret['payload']['data']
        idx = log['_id']

        log['_id'] = ObjectId(idx)

        db.log.save(log)
        r = requests.delete(api.format(idx), timeout=60)
    except requests.exceptions.ConnectionError as ex:
        ll.error('failed with[{0}]'.format(ex))


def main():
    while True:
        r = requests.get(apiLimit, timeout=60)
        ret = r.json()
        log = ret['payload']['data']
        count = ret['payload']['count']
        if count < 1000:
            ll.debug('remote count[{0}], stop retrieve'.format(count))
            break
        pool = Pool()
        pool.map(retrieve, log)
        pool.close()
        pool.join()

        lcount = db.log.count()
        ll.debug('remote count[{0}] local count[{1}]'.format(count, lcount))


if __name__ == '__main__':
    main()
