"""

Funciones y calculos auxiliares


"""


def calculate_overtones_share(timbre):
    """
    Calcula distribucion de volumenes para los sobretonos

    :param timbre:
        objeto timbre
    :return:
        float que representa la particion de volumen total de todos los sobretonos
    """

    overtones_share = sum(x.volume_share for x in timbre.overtones)
    overtones_share = overtones_share or 0
    return overtones_share

