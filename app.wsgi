#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
#for webfaction
#sys.path.insert(0,'/home/ghack/webapps/game/lib/python2.7')
from bottle import Bottle, default_app, run, debug 
from colorfire.app import colorfire

rootapp = Bottle()
debug(True)
rootapp.mount('/colorfire/', colorfire.mainapp) 

#for webfaction
#application = default_app()
if __name__ == '__main__':
    run(host="localhost", port=8888, app=rootapp, reloader=True)
