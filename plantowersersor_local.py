#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import datetime
import serial
import pymongo


ser = serial.Serial(  # 下面这些参数根据情况修改
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

import json
data = ''
import datetime


def fun(data):
    return data.pop(0) * (2**8) + data.pop(0)


time.sleep(5)

while True:
    if ser.read() == b'B' and ser.read() == b'M':
        data = ser.read(2 * 13 + 2)
        data = list(map(int, data))
        par = ser.read(2)
        out = {}
        out['datalen'] = fun(data)
        out['pm1-0_std'] = fun(data)
        out['pm2-5_std'] = fun(data)
        out['pm10_std'] = fun(data)

        out['pm1-0_atm'] = fun(data)
        out['pm2-5_atm'] = fun(data)
        out['pm10_atm'] = fun(data)

        out['dust0-3'] = fun(data) * 10000
        out['dust0-5'] = fun(data) * 10000
        out['dust1-0'] = fun(data) * 10000
        out['dust2-5'] = fun(data) * 10000
        out['dust5-0'] = fun(data) * 10000
        out['dust10'] = fun(data) * 10000

        '''
        out['dust0-3']=out['dust0-3']-out['dust0-5']

        out['dust0-5']=out['dust0-5']-out['dust1-0']

        out['dust1-0']=out['dust1-0']-out['dust2-5']

        out['dust2-5']=out['dust2-5']-out['dust5-0']

        out['dust5-0']=out['dust5-0']-out['dust10']
        '''

        out['empty'] = fun(data)
        out['time'] = str(datetime.datetime.now()).split('.')[0]
        out['timestamp'] = time.time()
        d = json.dumps(out)
        print(d)
