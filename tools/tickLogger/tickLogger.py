#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tick logger with ib_insync
@author: jev
"""

import logging
import utils
utils.configLogging('tickLogger.log')

logFields = ['bidSize','bid','ask','askSize','high','low','close']
import traceback, sys, pdb
 
def tick2str(tick, fields= logFields, sep =','):
    """ convert ibinsync tick to a (loggable) string """
    symbol = str(tick.contract.symbol)
    f = [symbol]+[ str(getattr(tick,field)) for field in fields]
    s = sep.join(f)
    return s


#%%

def onPendingTickers(tickers):
    
    try:
        for t in tickers:
            log.debug(str(t))
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)


#%%


import ib_insync as ibis


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

