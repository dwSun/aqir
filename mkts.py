#!/usr/bin/env python3
import time
import pymongo

from logger import Logger

conn = pymongo.MongoClient("127.0.0.1",27017)
db = conn.aqir #连接库

l = Logger('mkts.log')
trace = l.trace
ll = l.getlog()

def main():
    for log in db.log.find():
        if 'timestamp' not in log:
            log['timestamp'] = time.mktime(time.strptime(log['time'], '%Y-%m-%d %H:%M:%S'))
            ll.debug('[{0}] => [{1}]'.format(log['time'], log['timestamp']))
            db.log.save(log)

if __name__ == '__main__':
    main()
