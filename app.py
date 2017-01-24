#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make things as simple as possible, but not simpler.
from gevent import monkey; monkey.patch_all()
from flask import Flask, render_template, request, json

from gevent import queue
from gevent.pywsgi import WSGIServer
import pymongo
from functools import reduce

app = Flask(__name__)
app.debug = True

conn = pymongo.MongoClient("127.0.0.1",27017)
db = conn.aqir #连接库

datas ={'msg':'None'}


@app.route('/')
def choose_name():
    return render_template('main.html')

@app.route('/new')
def new():
    return render_template('main2.html')

@app.route("/put", methods=["POST"])
def put():
    message = request.json['message']
    datas['msg']=message
    return ''

@app.route("/poll", methods=["POST"])
def poll():
    x=list(db.log.find({},{'_id':0}).sort('_id', pymongo.DESCENDING).limit(1))[0]
    return json.dumps(x)

def add(d1,d2):
    d={}
    for key in d1:
        if 'time' not in key:
            d[key] = d1[key]+ d2[key]
    return d

@app.route("/poll30s", methods=["POST"])
def poll30s():
    return getDat(30)

@app.route("/poll10m", methods=["POST"])
def poll10m():
    return getDat(600)

def getDat(time):
    d=list(db.log.find({},{'_id':0}).sort('_id', pymongo.DESCENDING).limit(time))
    x=reduce(add,d)
    for key in x:
        if 'time' not in key:
            x[key] = int(x[key]/len(d))
    x['time'] = d[-1]['time'] +' ~ '+ d[0]['time']

    return json.dumps(x)

@app.route("/period", methods=["GET"])
def periodG():
    d=list(db.log.find({},{'_id':0}).sort('_id', pymongo.DESCENDING).limit(100))
    d.reverse()

    return json.dumps(d)

@app.route("/period", methods=["POST"])
def periodP():
    x=list(db.log.find({},{'_id':0}).sort('_id', pymongo.DESCENDING).limit(1))[0]
    return json.dumps(x)

if __name__ == "__main__":
    http = WSGIServer(('0.0.0.0', 5001), app)
    http.serve_forever()
