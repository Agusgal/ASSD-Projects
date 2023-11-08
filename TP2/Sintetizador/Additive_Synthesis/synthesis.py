"""

Sintetizo un sonido.


"""

from Additive_Synthesis.waves import generate_wave
from Additive_Synthesis.utils2 import calculate_overtones_share


def synthesize(timbre, frequency, volume, duration, sample_rate):
    """
    Sintetizo un fragmento sonoro que se corresponde con una nota.

    :param timbre:
        objeto timbre
    :param frequency:
        frecuencia de fundamental en Hz
    :param volume:
        volumen del fragmento sonoro
    :param duration:
        duracion del fragmento generado en segundos
    :param sample_rate:
        velocidad de muestreo
    :return:
        onda sonora represenatda como un arreglo de numpy
    """

    envelope = timbre.fundamental_envelope_fn(duration, sample_rate)
    overtones_share = calculate_overtones_share(timbre)
    fundamental_share = 1 - overtones_share

    sound = generate_wave(frequency, volume * fundamental_share * envelope, sample_rate)

    for overtone in timbre.overtones:
        envelope = overtone.envelope_fn(duration, sample_rate)
        overtone_sound = generate_wave(
            overtone.frequency_ratio * frequency,
            volume * overtone.volume_share * envelope,
            sample_rate
        )
        sound += overtone_sound
    return sound



