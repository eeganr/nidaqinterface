# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 16:00:23 2022

@author: User
"""

from interface.counter import *

data = [1,2,1,2,1,2,1,2,1,2,1]

samps=len(data)

delays=[0.2,0.5,0.1,0.7,0.1,0.2,0.2,0.3,0.1,0.4]

lows,highs = uniform_to_lowhigh(delays)

data=np.array(data,dtype=np.uint8)

counter_do(data,lows,highs)
