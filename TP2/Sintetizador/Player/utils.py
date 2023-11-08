"""
Utilidades de MidiReader

"""
from physical_synthesis.ks_guitar import GuitarString
from physical_synthesis.ks_drum import DrumString
from Additive_Synthesis.Instruments import Instrument
from Sintesis_muestras.Sample_synth import Samplesynth
from audiolazy.lazy_midi import freq2midi, midi2freq


def midi_to_freq(midi_note):
    midiA4 = 69
    f = 2**((midi_note-midiA4)/12) * 440
    return round(f, 2)


def find_note_off(note, track):
    current_time_in_ticks = 0
    for msg in track:
        if msg.is_meta == 0:
            current_time_in_ticks += msg.time
            if msg.type == 'note_off' and msg.note == note:
                break
    return current_time_in_ticks


#Covierte a la 5ta octava,
def convert_5oct(real_note):
    if round(real_note) in range(84, 96):
        return real_note - 12
    elif round(real_note) in range(96, 108):
        return real_note - 24
    elif round(real_note) in range(108, 120):
        return real_note - 36
    elif round(real_note) in range(120, 128):
        return real_note - 48
    else:
        return real_note


def synthesize(sample_rate, frequency, length, form, instrument, noise):
    if form == 'additive':
        if frequency > 1000:
            midi = freq2midi(frequency)
            convertida = convert_5oct(midi)
            frequency = midi_to_freq(convertida)

        instrumento = Instrument(instrument)
        return instrumento.get_sound(frequency, length)
    elif form == 'physical':
        if instrument == 'guitar':
            guitarnote = GuitarString(frequency, sample_rate, 1, length * sample_rate, noise)
            return guitarnote.get_samples()
        elif instrument == 'drums':
            drumnote = DrumString(frequency, sample_rate, 1, length * sample_rate)
            return drumnote.get_samples()

    elif form == 'samplesynth':
        samplesynth = Samplesynth(instrument)
        return samplesynth.get_sound(frequency, length)
