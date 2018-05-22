#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tick logger with ib_insync
@author: jev
"""

import logging
import utils
utils.configLogging('tickLogger.log')
import ib_insync as ibis
import yaml
import time
import os

logFields = ['bidSize','bid','ask','askSize','last','lastSize']
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
            print(tick2str(t))
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)


#%%

def getParser():
    """ create command line parser """ 
    import argparse
    parser = argparse.ArgumentParser(description='Log ticks for a set of stocks')
    parser.add_argument("--settings",help = 'ini file containing settings', default='settings.yml')
    parser.add_argument("--debug",help = 'log debug level info', action='store_true')
    return parser


#%% 
class TickLogger(object):
    ''' class for handling incoming ticks and saving them to file 
        will create a subdirectory 'tickLogs' if needed and start logging
        to a file with current timestamp in its name.
        All timestamps in the file are in seconds relative to start of logging
 
    '''
    def __init__(self,dataDir ):
        ''' init class '''
        # save starting time of logging. All times will be in seconds relative
        # to this moment
        self._startTime = time.time() 
 
        # create data directory if it does not exist
        if not os.path.exists(dataDir): os.mkdir(dataDir)     
 
        # open data file for writing
        self.dataFile = utils.RotatingFile(dataDir)      
 
    
    def tickHandler(self, tickers):
        
        for tick in tickers:
            log.debug(str(tick))
            self._writeData(tick2str(tick))
    
    
    def _writeData(self,s):
        ''' write data to log file while adding a timestamp '''
        timestamp = '%.3f' % (time.time()-self._startTime) # 1 ms resolution
        dataLine = timestamp+','+s+ '\n'
        self.dataFile.write(dataLine)
 
    def flush(self):
        ''' commits data to file'''
        log.info('committing to file')
        self.dataFile.flush()
        
 
    def close(self):
        '''close file in a neat manner '''
        log.info('Closing data file')
        self.dataFile.close()




#%% main script

if __name__=="__main__":
    log = logging.getLogger('main')    
    parser = getParser()
    args = parser.parse_args()
    log.debug(args)
    if args.debug:
       log.setLevel(logging.DEBUG)
    settings = yaml.load(open(args.settings,'r'))
    
    tickLogger = TickLogger(settings['dataRoot'])
    
    ib = ibis.IB()
    log.info('Connecting to IB')
    
    ib.connect('127.0.0.1', 4002, clientId=10)
    ib.pendingTickersEvent += tickLogger.tickHandler
    
    
    # subscribe to data
    
    contracts = [ibis.Contract(**sub)  for sub in settings['subscriptions']]
    
    for contract in contracts:
        log.info('Subscribing to '+str(contract))
        ib.reqMktData(contract, '', False, False)
    
    
    try:
        while True:    
            ib.sleep(10)
            tickLogger.flush()
    except KeyboardInterrupt:
        log.info('Exiting')
    
