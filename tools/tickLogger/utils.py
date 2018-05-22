# -*- coding: utf-8 -*-
"""
utilities for tick logger

@author: Jev Kuznetsov
"""

import logging
import os
import time
import datetime as dt


def configLogging(logFile, fileLevel= logging.INFO, consoleLevel = logging.INFO):
    """ configure logging to console and file """

    fmt_file = "%(asctime)s  %(levelname)s [%(name)s-%(funcName)s] - %(message)s"
    fmt_console ="%(asctime)s  %(levelname)s [%(name)s] - %(message)s"
    
    
    # configure other modules
    logging.getLogger('ib_insync').setLevel(logging.ERROR)
    logging.getLogger('ibapi').setLevel(logging.ERROR)
    
    
    # file logging
    logging.basicConfig(level=fileLevel,
                    filename = logFile,
                    filemode = 'w',
                    format=fmt_file,
                    datefmt="%H:%M:%S")
                   
                       
    log = logging.getLogger()
    
    
    # add filter for ibapi, cluttering root logger
    # not needed with a forked version of ibapi
    #f  = RootLogFilter(logging.ERROR)
    #log.addFilter(f)
    
   
    console = logging.StreamHandler()
    console.setLevel(consoleLevel)
    formatter = logging.Formatter(fmt_console,datefmt="%H:%M:%S")
    console.setFormatter(formatter)
    log.addHandler(console)
  
    



#class RootLogFilter:
#
#    def __init__(self, ibapiLevel=logging.ERROR):
#        self.ibapiLevel = ibapiLevel
#
#    def filter(self, record):
#        # if it's logged on the root logger assume it's from ibapi
#        if record.name == 'root' and record.levelno < self.ibapiLevel:
#            return False
#        else:
#            return True
        
class RotatingFile():
    """ data file rotated each day """
    
    def __init__(self,path):
        
        self._path = path
        
        
        # open file
        self._newFile()
        
    def _day_changed(self):
        return self._day != time.localtime().tm_mday 

    def _newFile(self):
        """ create filename """
        fileName = 'tickLog_%s.csv' % dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        fileName = os.path.join(self._path, fileName)
        print('Logging ticks to ' , fileName)
        self._file = open(fileName,'w')       
        
        self._day = time.localtime().tm_mday
        
    def write(self, *args):
        
        if self._day_changed():
            self._file.close()
            self._newFile()
        
        return getattr(self._file,'write')(*args)
    
    def close(self):
        self._file.close()
        
    def flush(self):
        self._file.flush()
        
    def __del__(self):
        self._file.close()
