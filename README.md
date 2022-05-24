# nidaqinterface
Interfacing with NIDAQmx Python For Digital Ouput &amp; Counter

Hello! There are currently two ways to interface  with the counter powered digital output.
Firstly, the user can set bindings between names of devices and port numbers as a python dictionary,

Ex: ``{'aom':0,'count':1,'camera':2,'yeetmobile':3,'gate':4}``

which can then be given to create a new counter class.
Then, the user can give a set of instructions in a list such as:

``['camera+aom',1,'count+yeetmobile',2,'gate',1]``

The device names separated by ``+`` come first followed by the delay in seconds. Then the run function can be called. This helps provide support for iteratively generated sets of instructions.

Additionally, csv files can be provided. For example, see https://docs.google.com/spreadsheets/d/13sZ6qZb4qE-D7gNuWoM_5hjdPfuNFFxXkazGccKCVB8

Downloaded as a csv, this can then be given to the run_from_csv function and executed simply and directly. Users can utilize functionality of excel or google sheets to reduce
the amount of time required to write up those instructions.
