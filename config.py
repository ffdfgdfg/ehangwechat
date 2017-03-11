# -*- coding: utf-8 -*-

import os
import json
import tornado.web

#tornado settings

settings = {
            'session_timeout': 3600,
            'port': 8888,
            'debug' : True,
            'UpdatePeriod': 5*3600,
            }


#wechat
wechatsettings = {
'checksignature': True,
'token': 'wobuzhidao',
'appid': 'wx0c1e2161428c94a0',
'appsecret': '9c3954920e8d104d96e2363195349ae6',
'encrypt_mode': 'normal',
'encoding_aes_key': '0LxqZIxuXvS10HhFFgEzFAtZMx7UxYfSwriExG29EkE',
}


#database
databasesettings = {
'type': 'mongodb',
'drivername': 'pymongo',
'port': 27017,
'host': 'localhost',
'dbname': 'wechat',
}

