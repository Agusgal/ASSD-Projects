"""

Genero ondas senoidales basicas


"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, ifft


def generate_wave(frequency, amplitudes, sample_rate):
    """
    :param frequency:
        frecuencia de la onda, define el tono del sonido
    :param amplitudes:
        arreglo de amplitudes para cada instante (sample)
        define el volumen del sonido y su duracion, además con este dato se cuantas muestras tomo
    :param sample_rate:
        número de muestras por segundo (instantes en el tiempo) al que se procesa el sonido
    :return:
        onda sonora representada como un array de numpy n-dimensional
    """

    timepoints = len(amplitudes)
    x = np.arange(timepoints)

    plain_wave = np.sin((2 * np.pi * frequency) * (x / sample_rate))

    wave = amplitudes * plain_wave

    return wave
