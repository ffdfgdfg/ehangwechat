# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpserver
from tornado.options import define, options

from config import *
from utils import ActiveOperate
from handles import *

web_handlers = [
        (r'/', WechatMain.wechat),
        ]

define("port", default=settings['port'], help="run on the given port", type=int)

if __name__ == '__main__':
    app = tornado.web.Application(web_handlers, **settings)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    if wechatsettings['checksignature'] is True:
        #不掉用接口进行检测
        pass
    else:
        op = ActiveOperate.OperateSystem()
        Like_Cron = op.AutoChekingMaterialProcess()
        tornado.ioloop.PeriodicCallback(Like_Cron, settings['UpdatePeriod']).start()
    tornado.ioloop.IOLoop.instance().start()
