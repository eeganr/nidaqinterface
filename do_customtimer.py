from interface.counter import Counter

c = Counter({'camera':2,'aom':0,'count':1,'yeetmobile':3,'gate':4})

data = [2, 1, 2, 1, 2, 1]

instructions = ['camera+aom',1,'count+yeetmobile',2,'gate',1]

#c.run(instructions)

#c.run_from_csv('exampleinstructions.csv')

times = [0.5,0.2,0.3,0.2,0.1]

c.gen_and_collect(times)