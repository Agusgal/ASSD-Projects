import numpy as np
import math


def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx - 1
    else:
        return idx


def shift2(arr, num):
    arr = np.roll(arr, num)
    if num < 0:
        np.put(arr, range(len(arr)+num, len(arr)), 0)
    elif num > 0:
        np.put(arr, range(num), 0)
    return arr


def extend(sound, time, sustain_duration, sample_rate, instrument):
    sustain_timepoints = math.ceil(sustain_duration * sample_rate)

    if instrument == 'violin' or instrument == 'flute' or instrument == 'trumpet':


        attack_index = find_nearest(time, 0.7)
        chopped_attack = sound[:attack_index]


        release_index = find_nearest(time, 2.75)
        chopped_release = sound[release_index:]

        #Genero el sustain a partir del sustain original

        chopped_sustain = sound[attack_index: release_index - 1]
        chopped_sustain_timepoints = len(chopped_sustain)

        chopped_sustain_duration = chopped_sustain_timepoints / sample_rate


        if sustain_duration > chopped_sustain_duration:
            diff = sustain_timepoints - chopped_sustain_timepoints

            chunk = chopped_sustain[:diff + 1]

            chopped_sustain = np.concatenate((chopped_sustain, chunk))

        elif sustain_duration < chopped_sustain_duration:
            cutoff = math.ceil(sustain_duration * sample_rate)

            chopped_sustain = chopped_sustain[:cutoff]
            #print(len(chopped_sustain))

        total = np.concatenate((chopped_attack, chopped_sustain, chopped_release))
    elif instrument == 'piano':
        attack_and_decay_index = find_nearest(time, 0.4)
        chopped_attack_and_decay = sound[:attack_and_decay_index]

        release_index = find_nearest(time, 2.35)
        chopped_release = sound[release_index:]

        chopped_sustain = sound[attack_and_decay_index: release_index - 1]
        chopped_sustain_timepoints = len(chopped_sustain)

        chopped_sustain_duration = chopped_sustain_timepoints / sample_rate

        if sustain_duration > chopped_sustain_duration:
            diff = sustain_timepoints - chopped_sustain_timepoints

            chunk = 0.03 * chopped_sustain[-(diff + 1):]

            chopped_sustain = np.concatenate((chopped_sustain, chunk))

        elif sustain_duration < chopped_sustain_duration:
            cutoff = math.ceil(sustain_duration * sample_rate)

            chopped_sustain = chopped_sustain[:cutoff]

        total = np.concatenate((chopped_attack_and_decay, chopped_sustain, chopped_release))



    return total


def smooth(x, window_len=11, window='bartlett'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y
