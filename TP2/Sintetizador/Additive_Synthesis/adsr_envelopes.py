"""

Genero las envolventes ADSR para cada nota


"""

import numpy as np
from math import ceil, floor


def relative_adsr(duration, sample_rate, attack_share=0.228, decay_share=0, sustain_level=0.6, release_share=0.114):
    """
    Crea envolvente con tiempos de ataque, decaimiento y release proporcionales a la duracion

    :param duration:
        duracion del sonido en segundos
    :param sample_rate:
        muestreo
    :param attack_share:
        particion de ataque
    :param decay_share:
        particion de decaimiento
    :param sustain_level:
        volumen en sostenido (1 es peak volume)
    :param release_share:
        particion de release
    :return:
        envolvente en arreglo numpy
    """
    timepoints = ceil(duration * sample_rate)

    if attack_share > 0:
        attack_tmpts = floor(attack_share * timepoints)
        step = 1 / attack_tmpts
        attack = np.arange(0, 1, step)
    else:
        attack = np.array([])

    if decay_share > 0:
        decay_tmpts = floor(decay_share * timepoints)
        step = (1 - sustain_level) / decay_tmpts
        decay = np.arange(1, sustain_level, -step)
    else:
        decay = np.array([])

    if release_share > 0:
        release_tmpts = floor(release_share * timepoints)
        step = sustain_level / release_tmpts
        release = np.arange(sustain_level, 0, -step)
    else:
        release = np.array([])

    sustain_tmpts = (timepoints - len(attack) - len(decay) - len(release))
    sustain = sustain_level * np.ones(sustain_tmpts)

    envelope = np.concatenate((attack, decay, sustain, release))
    return envelope


def absolute_adsr(duration, sample_rate, attack_time=0.3, decay_time=0.2, sustain_level=0.6, release_time=0.49):
    """
    Creo envolvente con tiempos de ataque, decaimiento, y release fijos

    :param duration:
         duracion del sonido en segundos
    :param sample_rate:
        muestras por segundo
    :param attack_time:
        tiempo de ataque máximo en segundos
    :param decay_time:
        tiempo de decaimiento máximo en segundos
    :param sustain_level:
        volumen en la etapa de sostenido del sonido, 1 es el máximo
    :param release_time:
        tiempo de finalizacion máximo
    :return:
        envolvente en un arreglo numpy n-dimensional
    """

    timepoints = ceil(duration * sample_rate)

    max_tmpts_attack = int(round(attack_time * sample_rate))
    max_tmpts_decay = int(round(decay_time * sample_rate))
    max_tmpts_release = int(round(release_time * sample_rate))

    adr_duration_in_tmpts = (max_tmpts_attack + max_tmpts_decay + max_tmpts_release)
    sustain_duration_in_tmpts = timepoints - adr_duration_in_tmpts

    if sustain_duration_in_tmpts < 0:
        envelope = relative_adsr(
            duration,
            sample_rate,
            max_tmpts_attack / adr_duration_in_tmpts,
            max_tmpts_decay / adr_duration_in_tmpts,
            sustain_level,
            max_tmpts_release / adr_duration_in_tmpts
        )
        return envelope

    if max_tmpts_attack > 0:
        step = 1 / max_tmpts_attack
        attack = np.arange(0, 1, step)
    else:
        attack = np.array([])

    if max_tmpts_decay > 0:
        step = (1 - sustain_level) / max_tmpts_decay
        decay = np.arange(1, sustain_level, -step)
    else:
        decay = np.array([])

    if max_tmpts_release > 0:
        step = sustain_level / max_tmpts_release
        release = np.arange(sustain_level, 0, -step)
    else:
        release = np.array([])

    tmpts_with_sustain = (timepoints - len(attack) - len(decay) - len(release))
    sustain = sustain_level * np.ones(tmpts_with_sustain)

    envelope = np.concatenate((attack, decay, sustain, release))

    return envelope

