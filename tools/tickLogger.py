#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tick logger with ib_insync
@author: jev
"""

import logging
import utils
from pprint import pprint

utils.configLogging('tickLogger.log')
#%%

import os
os.environ['IBAPI_LOGLEVEL'] = str(logging.INFO)

import ib_insync as ibis


#for handler in logger.handlers:
#    handler.setLevel(level)

log = logging.getLogger('main')
ib = ibis.IB()
log.info('Starting')
log.debug('debug message')

ib.connect('127.0.0.1', 4002, clientId=10)

# show all loggers
#pprint(logging.Logger.manager.loggerDict)