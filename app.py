#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make things as simple as possible, but not simpler.
from gevent import monkey; monkey.patch_all()
from flask import Flask, render_template, request, json
from flask_compress import Compress

from gevent.pywsgi import WSGIServer
import pymongo

app = Flask(__name__)
compressor = Compress(app)

conn = pymongo.MongoClient("127.0.0.1", 27017)
db = conn.aqir  # 连接库


@app.route('/')
def choose_name():
    return render_template('main.html')


@app.route("/last", methods=["GET"])
def last():
    d = list(db.log.find({}, {'_id': 0}).sort('_id', pymongo.DESCENDING).limit(1000))
    d.reverse()

    return json.dumps(d)


@app.route("/period", methods=["GET"])
def periodP():
    x = list(db.log.find({}, {'_id': 0}).sort('_id', pymongo.DESCENDING).limit(1))[0]
    return json.dumps(x)


if __name__ == "__main__":
    http = WSGIServer(('0.0.0.0', 5001), app)
    http.serve_forever()
