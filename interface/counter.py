# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 16:24:55 2022

@author: User
"""

import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType
import nidaqmx.stream_writers
from nidaqmx.errors import DaqError

def counter_do(data, wait, high,ctr=0,port=0,line='0:7'):
    
    #Running prechecks.
    
    
    #Turning low (wait) and high times into numpy arrays.
    testwait=np.array(wait)
    testhigh=np.array(high)
    
    counter=nidaqmx.Task()
    counter.co_channels.add_co_pulse_chan_time("Dev1/ctr"+str(ctr))
    
    output = nidaqmx.Task()
    output.do_channels.add_do_chan("Dev1/port"+str(port)+"/line"+str(line))
    
    counter.timing.cfg_implicit_timing(
        samps_per_chan=len(wait),
        sample_mode=AcquisitionType.FINITE
    )
    
    do_samples=len(wait)
    
    output.timing.cfg_samp_clk_timing(
        rate = 100000,
        source = 'Ctr0InternalOutput',
        sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
        samps_per_chan=do_samples
    )

    try:

        sw=nidaqmx.stream_writers.CounterWriter(counter.out_stream)
        sw.write_many_sample_pulse_time(testhigh,testwait)
        
        streamwriter = nidaqmx.stream_writers.DigitalSingleChannelWriter(output.out_stream)
        streamwriter.write_many_sample_port_byte(data)
        
        
        counter.start()
        output.start()
        
        
        output.wait_until_done(timeout=sum(wait)+sum(high))
        counter.wait_until_done(timeout=sum(wait)+sum(high))
        
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

