import numpy as np

from Sintesis_muestras.samplesynth_utils import shift_pitch
from Additive_Synthesis.instrument_utils import extend
from Additive_Synthesis.instrument_utils import smooth

from scipy.io import wavfile
violin_sample_rate, violin_data = wavfile.read('/Users/agustin/Documents/GitHub/TP2/Sintetizador/Additive_Synthesis/Wavs/violin-C4.wav')
flute_sample_rate, flute_data = wavfile.read('/Users/agustin/Documents/GitHub/TP2/Sintetizador/Additive_Synthesis/Wavs/flute-G4.wav')
trumpet_sample_rate, trumpet_data = wavfile.read('/Users/agustin/Documents/GitHub/TP2/Sintetizador/Additive_Synthesis/Wavs/trumpet-C4.wav')
piano_sample_rate, piano_data = wavfile.read('/Users/agustin/Documents/GitHub/TP2/Sintetizador/Additive_Synthesis/Wavs/piano-C4.wav')


class Samplesynth:
    def __init__(self, instrument):
        self.instrument = instrument

        if self.instrument == 'violin':
            self.sample_rate = violin_sample_rate
            self.data = violin_data
            self.fundamental_frequency = 261

        elif self.instrument == 'flute':
            self.sample_rate = flute_sample_rate
            self.data = flute_data
            self.fundamental_frequency = 392

        elif self.instrument == 'piano':
            self.sample_rate = piano_sample_rate
            self.data = piano_data
            self.fundamental_frequency = 261

        elif self.instrument == 'trumpet':
            self.sample_rate = trumpet_sample_rate
            self.data = trumpet_data
            self.fundamental_frequency = 261

    def get_sound(self, frequency, duration):
        N = len(self.data)



        # Pitch shift amount as a ratio
        f_ratio = frequency / self.fundamental_frequency

        new_signal = shift_pitch(self.data, self.sample_rate, f_ratio)

        time = np.arange(0, len(new_signal) / self.sample_rate, 1 / self.sample_rate)
        out = extend(new_signal, time, duration, self.sample_rate, self.instrument)

        #for k in range(10):
        #    out = smooth(out)

        return out * 0.1


"""
instrumneto = Samplesynth('piano')


c4 = instrumneto.get_sound(261, 1)



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