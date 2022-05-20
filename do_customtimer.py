from interface.counter import Counter

c = Counter({'h':2})

data = [2, 1, 2, 1, 2, 1]

samps = len(data)

delays = [0.1, 0.2, 0.3, 0.2, 0.1, 0.2]

c.counter_do(data, delays)