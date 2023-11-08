import numpy as np 
import scipy as sp

from scipy import signal
# import ks_synth as ks

# Sampling Frecuency
f_s = 44100

# Noise Wavetable
L = f_s/55

wavetable = (2 * np.random.randint(0, 2, L) -1 ).astype(np.float)
