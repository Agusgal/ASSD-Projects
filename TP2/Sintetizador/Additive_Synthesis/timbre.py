"""

Genero el timbre (composicion en frecuencia) del instrumento virtual


"""


class Overtone:
    def __init__(self, frequency_ratio, volume_share, envelope_fn):
        """
        Sobretono en particular

        :param frequency_ratio:
            proporción entre la frecuencia del sobretono y la frecuencia de su fundamental. (2, 3, 4,...)
        :param volume_share:
            volumen del sobretono con respecto al volumen total.
            en otras palabras, el volumen máximo de éste sobretono dividido entre la suma de los volumenes
            maximos de todos los sobretonos y la fundamental
        :param envelope_fn:
            funcion que mapea la duracion en segundos y el sample rate a la envolvente
        """

        self.frequency_ratio = frequency_ratio
        self.volume_share = volume_share
        self.envelope_fn = envelope_fn


class Timbre:
    def __init__(self, fundamental_envelope_fn, overtones):
        """
        Timbre de un sonido en particular
        :param fundamental_envelope_fn:
            funcion que mapea duracion en segundos y sample rate a la envolvente de la fundamental
        :param overtones:
            lista con todos los sobretonos
        """

        self.fundamental_envelope_fn = fundamental_envelope_fn
        self.overtones = overtones

