import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType
import nidaqmx.stream_writers
from nidaqmx.errors import DaqError

def counter_do(data, delays, initial_delay=0.001, ctr=0,port=0,line='0:7', rate=1000000):
    
    # prechecks to ensure lengths are okay
    if len(data) != len(delays):
        raise Exception('data length does not match lengths provided!')
    
    # modifying delays
    
    data=np.array(data,dtype=np.uint8)
    
    low, high = uniform_to_lowhigh(delays)
    low = [initial_delay] + low
    low = low[:-1]

    testlow=np.array(low)
    testhigh=np.array(high)
    
    # creating tasks for counter and output channels
    counter=nidaqmx.Task()
    counter.co_channels.add_co_pulse_chan_time("Dev1/ctr"+str(ctr))
    
    output = nidaqmx.Task()
    output.do_channels.add_do_chan("Dev1/port"+str(port)+"/line"+str(line))
    
    # setting up timing for counter and DO channels
    counter.timing.cfg_implicit_timing(
        samps_per_chan=len(low),
        sample_mode=AcquisitionType.FINITE
    )
    
    output.timing.cfg_samp_clk_timing(
        rate = rate,
        source = 'Ctr0InternalOutput',
        sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
        samps_per_chan=len(low)
    )

    # output generation attempt
    try:
        sw=nidaqmx.stream_writers.CounterWriter(counter.out_stream)
        sw.write_many_sample_pulse_time(testhigh,testlow)
        
        streamwriter = nidaqmx.stream_writers.DigitalSingleChannelWriter(output.out_stream)
        streamwriter.write_many_sample_port_byte(data)
        
        counter.start()
        output.start()
          
        output.wait_until_done(timeout=sum(low)+sum(high))
        counter.wait_until_done(timeout=sum(low)+sum(high))
        
        output.stop()
        output.close()
        
        counter.stop()
        counter.close()
        
    except DaqError as e:
        raise RuntimeError(f'An error occured while running: {e}')
        output.stop()
        output.close()
        
        counter.stop()
        counter.close()
        
def uniform_to_lowhigh(arr):
    lows=[]
    highs=[]
    for val in arr:
        lows.append(val/2)
        highs.append(val/2)
    return lows, highs

def delay_to_lowhigh(delay, samps):
    vals=[delay/2]*samps
    return vals, vals
