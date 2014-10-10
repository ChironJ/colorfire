#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging.config
import os

configfile = os.path.dirname(os.path.dirname(__file__))+'/conf/logging.conf'

logging.config.fileConfig(configfile)
log = logging.getLogger('server')

