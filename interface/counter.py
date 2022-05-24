import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType
import nidaqmx.stream_writers
from nidaqmx.errors import DaqError

class Counter:
    def __init__(self, bindings):
        # bindings should be a dictionary like {'Camera':2, 'AOM':3}
        self.bindings = bindings
    
    def run(self, command, port=0):
        '''
            Runs the digital output given a command.
            Command in format ['Camera+AOM','0.3','Counter+Camera','0.2'] 
        '''
        if len(command) % 2 != 0:
            raise Exception('Something is wrong! You should provide a time delta for each state.')
        states = []
        times = []
        for i in range(len(command)):
            if i % 2 == 0:
                states.append(command[i])
            else:
                times.append(command[i])

        # translating states
        states_translated = []
        for state in states:
            nested = state.split('+')
            try:
                port_strings = [self.bindings[n] for n in nested]
            except:
                raise Exception('missing binding or inaccurate input!')
            binary = [0, 0, 0, 0, 0, 0, 0, 0]
            for i in port_strings:
                binary[7 - i] = 1 
            integer = int("".join(str(i) for i in binary),2)
            states_translated.append(integer)
        
        # Running program
        self.counter_do(states_translated, times, port=port)

    def run_from_csv(self, name, port=0):
        '''
            Runs a digital output program from a csv file given as input. See readme or example csv.
        '''
        # Importing csv as pandas dataframe.
        try:
            import pandas as pd
            df = pd.read_csv(name, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8], skiprows=[1])
        except:
            raise Exception('file unreachable!')
           
        # Parsing and translating states and times
        hold_times = list(map(float,[i[0] for i in df.iloc[:, [8]].to_numpy().tolist()]))
        states = []
        for row in df.itertuples():
            binary = [0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(len(row)):
                if row[i]!='':
                    binary[7 - i] = 1
            integer = int("".join(str(i) for i in binary),2)
            states.append(integer)
            
        # Running program
        self.counter_do(states, hold_times, port=port)
        
    def counter_do(self, data, delays, ctr=0, port=0, line='0:7', rate=1000000, initial_delay=0.001):
        '''
            Primarily a helper function internal to the class, helps run the counter and digital out, but can also be called from outside the class if needed.
        '''
        # prechecks to ensure lengths are okay
        if len(data) != len(delays):
            raise Exception('data length does not match lengths provided!')
        
        # turning data into numpy array
        data = np.array(data, dtype=np.uint8)

        # modifying delay format
        
        low, high = self.uniform_to_lowhigh(delays)
        low = [initial_delay] + low
        high[-1] += low[-1]
        low = low[:-1]

        testlow = np.array(low)
        testhigh = np.array(high)
        
        # creating tasks for counter and output channels
        counter = nidaqmx.Task()
        counter.co_channels.add_co_pulse_chan_time("Dev1/ctr"+str(ctr))
        
        output = nidaqmx.Task()
        output.do_channels.add_do_chan("Dev1/port"+str(port)+"/line"+str(line))
        
        # setting up timing for counter and DO channels
        counter.timing.cfg_implicit_timing(
            samps_per_chan=len(low),
            sample_mode=AcquisitionType.FINITE
        )
        
        output.timing.cfg_samp_clk_timing(
            rate=rate,
            source='Ctr0InternalOutput',
            sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
            samps_per_chan=len(low)
        )

        # output generation attempt
        try:
            sw = nidaqmx.stream_writers.CounterWriter(counter.out_stream)
            sw.write_many_sample_pulse_time(testhigh, testlow)
            
            streamwriter = nidaqmx.stream_writers.DigitalSingleChannelWriter(output.out_stream)
            streamwriter.write_many_sample_port_byte(data)

            counter.start()
            output.start()

            output.wait_until_done(timeout=(sum(low)+sum(high)+initial_delay)*2)
            counter.wait_until_done(timeout=(sum(low)+sum(high)+initial_delay)*2)

            output.stop()
            output.close()

            counter.stop()
            counter.close()

        except DaqError as e:
            raise RuntimeError(f'An error occured while running: {e}')

    def uniform_to_lowhigh(self, arr):
        lows = []
        highs = []
        for val in arr:
            lows.append(val/2)
            highs.append(val/2)
        return lows, highs


    def delay_to_lowhigh(self, delay, samps):
        vals = [delay/2]*samps
        return vals, vals
