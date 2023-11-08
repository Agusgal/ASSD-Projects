"""
Cconvierte un array con datos de numpy en un archivo WAV.

"""

import scipy.io.wavfile


def write_timeline_to_wav(output_path, data, sample_rate):
    """
    convierte numpy ----> WAV

    :param output_path:
        path al archivo resultante
    :param data:
        sonido en formato arreglo de numpy
    :param sample_rate:
        muestreo
    :return:
        None
    """

    scipy.io.wavfile.write(output_path, sample_rate, data.T)
