import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, ifft
from scipy.io import wavfile

from Additive_Synthesis.instrument_utils import find_nearest, shift2, extend, smooth
from Additive_Synthesis.waves import generate_wave
from nptowav.numpy_to_wav import write_timeline_to_wav

violin_sample_rate, violin_data = wavfile.read('/Users/agustin/Documents/GitHub/TP2/Sintetizador/Additive_Synthesis/Wavs/violin-C4.wav')
flute_sample_rate, flute_data = wavfile.read('/Users/agustin/Documents/GitHub/TP2/Sintetizador/Additive_Synthesis/Wavs/flute-G4.wav')
trumpet_sample_rate, trumpet_data = wavfile.read('/Users/agustin/Documents/GitHub/TP2/Sintetizador/Additive_Synthesis/Wavs/trumpet-C4.wav')
piano_sample_rate, piano_data = wavfile.read('/Users/agustin/Documents/GitHub/TP2/Sintetizador/Additive_Synthesis/Wavs/piano-C4.wav')



class Instrument:
    def __init__(self, instrumnet):
        self.instrument = instrumnet
        self.adsr = None

        if self.instrument == 'violin':
            self.sample_rate = violin_sample_rate
            self.data = violin_data
            self.harmonics_n = 5
            self.fundamental_frequency = 261
            self.cutoff = 80
            self.fundamental_amp = 1.662e7
            self.partial_amps = [5.45651e6, 3.02029e6, 2.30182e6, 2.29503e6, 1.6187e6, 612246, 1.14481e6, 1.27999e6,
                              141558, 104204, 331075, 789459, 291382]

        elif self.instrument == 'flute':
            self.sample_rate = flute_sample_rate
            self.data = flute_data
            self.harmonics_n = 5
            self.fundamental_frequency = 392
            self.cutoff = 40
            self.fundamental_amp = 2.74479e7
            self.partial_amps = [9.26164e6, 2.37813e6, 2.09471e6, 962194, 512023]

        elif self.instrument == 'piano':
            self.sample_rate = piano_sample_rate
            self.data = piano_data
            self.harmonics_n = 5
            self.fundamental_frequency = 261
            self.cutoff = 40
            self.fundamental_amp = 5.3073e6
            self.partial_amps = [3.74364e6, 470247, 594022, 53413, 574684, 156378, 223971, 194611, 92896, 90520, 70542]

        elif self.instrument == 'trumpet':
            self.sample_rate = trumpet_sample_rate
            self.data = trumpet_data
            self.harmonics_n = 5
            self.fundamental_frequency = 261
            self.cutoff = 30
            self.fundamental_amp = 2.165e6
            self.partial_amps = [3.06691e6, 5.30304e6, 6.9947e6, 2.63067e6, 5.72642e6, 2.88338e6, 1.78508e5, 1.41131e6, 1.18833e6, 1.56109e6, 869455, 60259, 279227, 159287, 154722, 109846, 108000]

        else:
            pass

    def get_sound(self, frequency, duration):
        """
        Genera el sonido en base a la frecuencia de la nota y la duracion deseada
        :param frequency:
            frecuencia de la nota
        :param duration:
            duracion de la nota
        :return:
            sonido como arreglo de numpy
        """

        samples = self.data.shape[0]

        time = np.arange(0, samples / self.sample_rate, 1 / self.sample_rate)

        datafft = fft(self.data)


        freqs = fftfreq(samples, 1 / self.sample_rate)


        pos_freqs = freqs[:int(len(freqs) / 2)]



        index_pos_fundamental = find_nearest(pos_freqs, self.fundamental_frequency)
        index_pos_target = find_nearest(pos_freqs, frequency)
        # Si el indice es el ultimo significa que la frecuencia es muy alta, entonces debo alargar mis arreglos de frecuencia


        diff = index_pos_target - index_pos_fundamental

        mask = np.copy(datafft)
        empty = []


        self.calculate_partial_shares()

        for var in range(1, self.harmonics_n + 1):
            mask2 = np.copy(mask)
            for cont in range(len(freqs)):
                if (freqs[cont] < -(self.fundamental_frequency * var) - self.cutoff) \
                        or (
                        -(self.fundamental_frequency * var) + self.cutoff < freqs[cont] < (self.fundamental_frequency * var) - self.cutoff) \
                        or (freqs[cont] > (self.fundamental_frequency * var) + self.cutoff):
                    mask2[cont] = 0

            pos_mask2 = mask2[:int(len(freqs) / 2)]
            neg_mask2 = mask2[int(len(freqs) / 2): len(freqs)]

            pos_mask2_shifted = shift2(pos_mask2, diff * var)
            neg_mask2_shifted = shift2(neg_mask2, - (diff * var))

            shifted_mask2 = np.concatenate((pos_mask2_shifted, neg_mask2_shifted))

            empty.append(shifted_mask2)

        output = sum(empty)

        adsr = ifft(output)
        self.adsr = adsr

        maxi = np.amax(adsr)
        normalized = adsr / maxi

        ##hasta aca standard para cualquier instrumento


        #caso violin, piano y flauta (funca buenardo con un solo suavizado) trompeta no tanto
        copy = normalized.copy()

        copy[copy < 0] = 0

        suave = smooth(copy.real)

        max_smooth = np.amax(suave)
        suave = suave / max_smooth

        fundamental = generate_wave(frequency, suave, self.sample_rate)

        for v in range(2, self.harmonics_n + 1):
            sobretono = generate_wave(frequency * v, suave, self.sample_rate)
            fundamental += self.partial_amps[v - 2] * sobretono

        fundamental *= suave

        out = extend(fundamental, time, duration, self.sample_rate, self.instrument)

        return out

    def calculate_partial_shares(self):
        for k in range(len(self.partial_amps)):
            self.partial_amps[k] = self.partial_amps[k] / self.fundamental_amp

    def fft_data(self):
        plt.plot(fftfreq(self.data.shape[0], 1 / self.sample_rate), abs(fft(self.data)))
        plt.show()

    def plot_adsr(self):
        time = np.arange(0, self.data.shape[0] / self.sample_rate, 1/self.sample_rate)
        plt.plot(time, self.adsr)
        plt.show()

    def suavizado(self, data):

        #copia = np.copy(data)

        #for k in range(100):
        #    copia = smooth(copia)

        #plt.plot(np.arange(0, len(copia) / self.sample_rate, 1 / self.sample_rate), copia)
        #plt.show()
        pass


#instrumneto = Instrument('violin')
#instrumneto.fft_data()

#print(instrumneto.instrument)
#c4 = instrumneto.get_sound(261, 3)
#instrumneto.plot_adsr()

#path = '/Users/agustin/Desktop/c4.wav'

#write_timeline_to_wav(path, c4, instrumneto.sample_rate)

#path = '/Users/agustin/Desktop/e4.wav'

#write_timeline_to_wav(path, e4, instrumneto.sample_rate)

#path = '/Users/agustin/Desktop/g4.wav'

#write_timeline_to_wav(path, g4, instrumneto.sample_rate)

#acorde = c4 + e4 + g4

#path = '/Users/agustin/Desktop/acorde.wav'

#write_timeline_to_wav(path, acorde, instrumneto.sample_rate)


"""
import pyaudio
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=instrumneto.sample_rate,
                frames_per_buffer=1024,
                output=True,
                output_device_index=1
                )


stream.write(c4.astype(np.float32).tostring())
stream.close()

"""