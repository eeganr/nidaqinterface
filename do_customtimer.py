from interface.counter import Counter

c = Counter({'camera':2,'aom':0,'count':1,'yeetmobile':3,'gate':4})

data = [2, 1, 2, 1, 2, 1]

instructions = ['camera+aom',4,'count+yeetmobile',5,'gate',2]

c.run(instructions)