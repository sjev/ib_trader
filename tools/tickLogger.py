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

def onPendingTickers(tickers):
    for t in tickers:
        print(t.contract.symbol,t.bidSize, t.bid, t.ask, t.askSize, t.high, t.low, t.close)

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
ib.pendingTickersEvent +=onPendingTickers

# show all loggers
#pprint(logging.Logger.manager.loggerDict)

# subscribe to data
symbols = ['VXX','SPY','XLE']
contracts = [ibis.Stock(symbol,'SMART','USD')  for symbol in symbols]

for contract in contracts:
    ib.reqMktData(contract, '', False, False)


try:
    while True:    
        ib.sleep(0.5)
except KeyboardInterrupt:
    log.info('Exiting')

