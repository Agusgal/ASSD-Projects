import numpy as np


def gen_delay(data, delay):
    out = data.copy()
    for i in range(len(data)):
        index = int(i - delay)
        if index >= 0 and index < len(data):
            out[i] = data[index]
    return out

def flange(data, lfofreq, depth, phase_inv, M0=1, A=1):
    """ lfofreq: Flanger Speed (samples/sec)
        depth = Degree of Flanging Effect range=[0;1]"""
    out = data.copy()
    for i in range(len(data)):
        delay = M0*(1 + A*np.sin(2*np.pi*lfofreq*i))
        index = int(i - delay)
        if phase_inv == True:
            delay *= -1
        if index >= 0 and index < len(data):
            out[i] = data[i] + depth * data[index]
    return out

def flange2(data, speed, depth, inv, fs, min_delay = 1, max_delay = 10):
    """ Data: Input Signal
        Speed %: f_LFO [0.1,10] Hz => Speed [0,100]
        depth: g [0,1]
        inv: invertion mode
        min_delay = 01 ms
        max_delay = 10 ms
        """
    speed = (1-0.1)*speed/100 + 0.1
    out = data.copy()

    Mo = 20/1000 * fs
    Mw = (30-20)/1000 * fs
    if min_delay >= 20 and min_delay < max_delay: Mo = min_delay/1000 * fs
    if max_delay <= 30 and max_delay > min_delay: Mw = (max_delay-min_delay)/1000 * fs
    
    if inv: depth *= -1
    for i in range(len(data)):
        M = Mo + Mw/2 * (1 + np.sin(2*np.pi* speed/fs * i))
        index = int(i-M)
        if index >= 0 and index<len(data):
            out[i] = data[i] + depth * data[index]

    return out

def chorus(data, speed, depth, inv, fs, min_delay = 20, max_delay = 30):
    """ Data: Input Signal
        Speed %: f_LFO [0.1,3] Hz => Speed [0,100]
        depth: g [0,1]
        inv: invertion mode on/off
        min_delay = 20 ms
        max_delay = 30 ms
        """
    speed = (3-0.1)*speed/100 + 0.1
    out = data.copy()

    Mo = 20/1000 * fs
    Mw = (30-20)/1000 * fs
    if min_delay >= 20 and min_delay < max_delay: Mo = min_delay/1000 * fs
    if max_delay <= 30 and max_delay > min_delay: Mw = (max_delay-min_delay)/1000 * fs
    
    if inv: depth *= -1
    for i in range(len(data)):
        M = Mo + Mw/2 * (1 + np.sin(2*np.pi* speed/fs * i))
        index = int(i-M)
        if index >= 0 and index<len(data):
            out[i] = data[i] + depth * data[index]

    return out