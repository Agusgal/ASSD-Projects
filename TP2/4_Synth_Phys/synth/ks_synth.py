import numpy as np
import scipy as sp
from scipy import signal

import matplotlib as plt

def wave(shape, amp, phase, freq, t):
    # Returns the correspoding wavetable
    wavetable = np.zeros_like(t)
    
    if shape == "sine":
        wavetable = amp * np.sin(2 * np.pi * freq * t + phase)
    elif shape == "sine sine":
        wavetable = amp * np.sin(np.sin(2 * np.pi * freq * t + phase))
    elif shape == "sqaure":
        wavetable = amp * signal.square(2 * np.pi * freq * t + phase)
    elif shape == "down_ramp":
        wavetable = amp * signal.sawtooth(2 * np.pi * freq * t + phase, 0)
    
    return wavetable

def make_wavetable(n_samples, amps, phases, freqs):
    #Generate Wavetable: el track contiene la información
    # MIDI: Amplitud, Fase, Frecuencia
    t = np.linspace(0, 1, num=n_samples)
    wavetable = np.zeros_like(t)
    for amp, phase, freq in zip(amps,phases,freqs):
        wavetable += wave("sine",amp,phase,freq, t)
    return wavetable

def karplus_strong(wavetable, n_samples, stretch_factor):
    # stretch_factor = 1    no altera el estiramiento de la nota
    # stretch_factor = inf  genera un tono puro.
    samples = [] 
    # Condiciones Iniciales:
    curr_sample = 0 # Índice para recorrer la tabla de onda
    prev_value = 0  # Valor anterior
    while len(samples) < n_samples: # Recorro hasta que retorno tenga mismo largo
        stretch = np.random.binomial(1, 1-1/stretch_factor)
        if stretch == 0: # Hago el promedio entre la muestra y la anterior
            wavetable[curr_sample] = 0.5 * (wavetable[curr_sample] + prev_value)
        samples.append(wavetable[curr_sample])
        prev_value = samples[-1]    # Tomo el último valor que ingresé a la nueva señal
        curr_sample = (curr_sample+1) % wavetable.size  # Avanzo el índice circularmente
    return np.array(samples)

def karplus_strong_drum(wavetable, n_samples, stretch_factor, probability):
    samples = [] 
    # Condiciones Iniciales:
    curr_sample = 0 # Índice para recorrer la tabla de onda
    prev_value = 0  # Valor anterior
    while len(samples) < n_samples: # Recorro hasta que retorno tenga mismo largo
        stretch = np.random.binomial(1, 1/stretch_factor)
        drum_sign = np.random.binomial(1,probability)
        
        if stretch == 1: # Decido si estiro con prob 1/S
            wavetable[curr_sample] = 0.5 * (wavetable[curr_sample] + prev_value)
        if drum_sign == 0: # Decido si invierto el signo con prob b
            wavetable[curr_sample] = -wavetable[curr_sample]
        
        samples.append(wavetable[curr_sample])
        prev_value = samples[-1]    # Tomo el último valor que ingresé a la nueva señal
        curr_sample = (curr_sample+1) % wavetable.size  # Avanzo el índice circularmente
    return np.array(samples)