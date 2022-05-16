from interface.counter import *

data = [2,1,2,1,2,1]

samps=len(data)

#Must add extra delay to the start as that is considered the start before any data generation.
delays=[0.1, 0.2, 0.3, 0.2, 0.1, 0.2]

counter_do(data, delays)
