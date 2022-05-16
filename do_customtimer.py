from interface.counter import counter_do

data = [2, 1, 2, 1, 2, 1]

samps = len(data)

delays = [0.1, 0.2, 0.3, 0.2, 0.1, 0.2]

counter_do(data, delays)
