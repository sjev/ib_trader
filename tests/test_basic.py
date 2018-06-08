#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
basic tests.
run with `pytest`

@author: jev
"""


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ib_trader


print('Running basic tests')
print(dir(ib_trader))

def test_state():
    
    state = ib_trader.State()
    
    
    