"""
Leo archivos midi y los interpreto

"""

import mido
import numpy as np

from Additive_Synthesis.instrument_utils import find_nearest

from Player.utils import midi_to_freq, find_note_off, synthesize
import pyaudio


class Player:
    def __init__(self, sample_rate):
        self.mid = None
        self.sample_rate = sample_rate
        self.tracks = []

    def load_file(self, path):
        self.mid = mido.MidiFile(path, clip=True)
        self.tracks = []

    def create_tracks(self):
        tempo = 0
        for msg in self.mid.tracks[0]:
            if msg.dict()['type'] == 'set_tempo':
                tempo = msg.dict()['tempo']

        for k in range(1, len(self.mid.tracks)):
            new_track = MyTrack(self.sample_rate, self.mid.length, k, tempo)
            new_track.parse_track(self.mid.tracks[k])
            self.tracks.append(new_track)

    def synthesize_track(self, iden, form, instrument, noise='normal'):
        for track in self.tracks:
            if track.iden == iden:
                track.create_timebase()
                track.create_sounds()
                track.set_instrument(instrument)
                nota = 1
                for note in track.notes:

                    length = note.get_len_seconds(self.mid.ticks_per_beat, track.tempo)
                    pitch = note.pitch

                    #if form == 'additive' and pitch > 750:
                    #    pitch = convert_4oct(freq2midi(pitch))
                    #    print(pitch)
                    #    #pitch = midi_to_freq(pitch)

                    #print(pitch)

                    # busco que indice es el mas cercano al tiempo inicial de mi nota
                    initial_time = note.get_initial_time_seconds(self.mid.ticks_per_beat, track.tempo)
                    begin_index = find_nearest(track.timebase, initial_time)

                    # sintetizo nota
                    sample = synthesize(self.sample_rate, pitch, length, form, instrument, noise)
                    print('nota creada:  %s' % nota)
                    nota += 1

                    # Ahora debo sumar en el arreglo y, desde index hasta el final de mi nota
                    synth_note_index = 0
                    for idx in range(begin_index, begin_index + len(sample)):
                        try:
                            track.sounds[idx] += sample[synth_note_index]
                            synth_note_index += 1
                        except IndexError:
                            track.sounds = np.append(track.sounds, 0)
                            track.sounds[idx] += sample[synth_note_index]
                            synth_note_index += 1

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate

    #todo que reproduzca varios tracks al mismo tiempo (sumo todo lmao)
    def play_track(self, iden):
        sounds = self.tracks[iden - 1].sounds
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.sample_rate,
                        frames_per_buffer=1024,
                        output=True,
                        output_device_index=1
                        )

        stream.write(sounds.astype(np.float32).tostring())
        stream.close()
        print('finished')

    def play_multiple_tracks(self, iden_list):
        sounds = self.make_song(iden_list)

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.sample_rate,
                        frames_per_buffer=1024,
                        output=True,
                        output_device_index=1
                        )

        stream.write(sounds.astype(np.float32).tostring())
        stream.close()

    def make_song(self, iden_list):
        max_length = 0

        for track in self.tracks:
            if len(track.sounds) > max_length:
                max_length = len(track.sounds)

        sounds = np.zeros(max_length)

        for element in iden_list:
            copy = np.copy(self.tracks[element - 1].sounds)
            diff = max_length - len(copy)

            ceros = np.zeros(diff)
            sumar = np.append(copy, ceros)

            sounds += sumar

        return sounds

    def play_single_note(self, pitch, length, form, instrument, noise='normal'):

        sample = synthesize(self.sample_rate, pitch, length, form, instrument, noise)

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.sample_rate,
                        frames_per_buffer=1024,
                        output=True,
                        output_device_index=1
                        )

        stream.write(sample.astype(np.float32).tostring())
        stream.close()


class MyTrack:
    def __init__(self, sample_rate, length, iden, tempo):
        self.notes = []
        self.sample_rate = sample_rate
        self.length = length
        self.timebase = None
        self.sounds = None
        self.tempo = tempo
        self.iden = iden
        self.reproductor = None
        self.instrument = None

    def parse_track(self, track):
        current_time_in_ticks = 0
        msg_num = 0

        for msg in track:
            if msg.is_meta == 0:
                current_time_in_ticks += msg.time
                if msg.type == 'note_on':
                    amp = msg.velocity
                    t_f = current_time_in_ticks + find_note_off(msg.note, track[msg_num:len(track) + 1])
                    pitch = midi_to_freq(msg.note)

                    #if pitch > 1000:
                    #    var = freq2midi(pitch)
                    #    var2 = convert_4oct(var)
                    #    pitch = midi_to_freq(var2)

                    new_note = Mynote(self.sample_rate, pitch, current_time_in_ticks, t_f, amp)
                    self.notes.append(new_note)
                    # msg_num += 1
            msg_num += 1

    def create_timebase(self):
        self.timebase = np.arange(0, self.length, 1 / self.sample_rate)

    def create_sounds(self):
        self.sounds = np.zeros(len(self.timebase))

    def set_tempo(self, tempo):
        self.tempo = tempo

    def set_instrument(self, instrument):
        self.instrument = instrument

    def set_reproductor(self, number):
        self.reproductor = number


class Mynote:
    def __init__(self, fs, pitch, t_i, t_f, amp):
        """Initialize Note Object"""
        self.fs = fs
        self.pitch = pitch
        self.t_i = t_i
        self.t_f = t_f
        self.amp = amp
        self.sound = None

    def get_len(self):
        return self.t_f - self.t_i

    def get_len_seconds(self, ticks_per_beat, tempo):
        return mido.tick2second(self.get_len(), ticks_per_beat, tempo)

    def get_initial_time_seconds(self, ticks_per_beat, tempo):
        return mido.tick2second(self.t_i, ticks_per_beat, tempo)

    def add_sound(self, sound): #Sound should be the array of sample values in time
        """Attaches the sound for this note as an array of samples"""
        self.sound = sound

    def get_sample(self, time):
        """Returns the sample at a given time. If it isn't the time for the note to play it will return an empty value"""

        if time < self.t_i or time > self.t_f:
            sample = 0
        else:
            sample = self.sound[time-self.t_i]

        return sample






#### Prueba de funcionamiento

#player = Player(11025)
#player.load_file('/Users/agustin/Documents/GitHub/TP2/Sintetizador/Midis/Lalaland.mid')
#player.create_tracks()
#print('creadas')

#player.synthesize_track(2, 'physical', 'guitar')
#print('sintetizada 1')

#player.synthesize_track(1, 'physical', 'guitar')
#print('sintetizada 2')

#player.play_multiple_tracks([1, 2])


###### Pruebas de Victor ########
"""
fs = 44100
freqs = [98, 123, 147, 196, 294, 392, 392, 294, 196, 147, 123, 98]

unit_delay = fs//3

# Son los tiempos iniciales de cada nota
delays = [unit_delay * _ for _ in range(len(freqs))]

notes=[]
for freq, delay in zip(freqs, delays):
    new_note = Mynote(fs, freq, delay, delay+2*fs, 1) # 2*fs hace que cada una dure 2 seg
    notes.append(new_note)

for note in notes:
    # Sintetizo nota
    guitarnote = GuitarString(note.pitch, note.fs, note.A, note.get_len(), '2-level')
    note.add_sound(guitarnote.get_samples()) # Le asocio a cada objeto nota su respectivo sonido

# Combino los sonidos   
# Básicamente, recorre cada objeto MyNota, se fija si a un tiempo 't' le corresponde tocar (devuelve 0 o x(t)) y suma todo lo que encuentre para el momento 't'. Así continúa con toda la secuencia.
# Este nuevo arreglo deberías poder insertarlo al pyaudio. Es sólo el y(n) final con todas las notas juntas.
guitar_sound = np.array([sum(note.get_sample(t) for note in notes) for t in range(fs*6)])

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                frames_per_buffer=1024,
                output=True,
                output_device_index=1
                )


stream.write(guitar_sound.astype(np.float32).tostring())
stream.close()

"""