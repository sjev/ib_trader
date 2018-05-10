# -*- coding: utf-8 -*-
"""
utilities for tick logger

@author: Jev Kuznetsov
"""

import logging


def configLogging(logFile, fileLevel= logging.DEBUG, consoleLevel = logging.INFO):
    """ configure logging to console and file """
    
    fmt = "%(asctime)s  %(levelname)s [%(name)s-%(funcName)s] - %(message)s"
    
    # file logging
    logging.basicConfig(level=fileLevel,
                    filename = logFile,
                    filemode = 'w',
                    format=fmt,
                    datefmt="%H:%M:%S")
                   
     
                  
                       
    log = logging.getLogger()
    
    
    # add filter for ibapi, cluttering root logger
    # not needed with a forked version of ibapi
    #f  = RootLogFilter(logging.ERROR)
    #log.addFilter(f)
    
    
    console = logging.StreamHandler()
    console.setLevel(consoleLevel)
    formatter = logging.Formatter(fmt,datefmt="%H:%M:%S")
    console.setFormatter(formatter)
    log.addHandler(console)
  
    

class RootLogFilter:

    def __init__(self, ibapiLevel=logging.ERROR):
        self.ibapiLevel = ibapiLevel

    def filter(self, record):
        # if it's logged on the root logger assume it's from ibapi
        if record.name == 'root' and record.levelno < self.ibapiLevel:
            return False
        else:
            return True