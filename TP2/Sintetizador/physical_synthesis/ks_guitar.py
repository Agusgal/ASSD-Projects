import numpy as np

def karplus_strong(wavetable, n_samples, stretch_factor):
    # stretch_factor = 1    no altera el estiramiento de la nota
    # stretch_factor = inf  genera un tono puro.
    samples = [] 
    # Condiciones Iniciales:
    curr_sample = 0 # Índice para recorrer la tabla de onda
    prev_value = 0  # Valor anterior
    while len(samples) < n_samples: # Recorro hasta que retorno tenga mismo largo
        stretch = np.random.binomial(1, 1-1/stretch_factor)
        if stretch == 0: # Hago el promedio entre la muestra y la anterior
            wavetable[curr_sample] = 0.5 * (wavetable[curr_sample] + prev_value)
        samples.append(wavetable[curr_sample])
        prev_value = samples[-1]    # Tomo el último valor que ingresé a la nueva señal
        curr_sample = (curr_sample+1) % wavetable.size  # Avanzo el índice circularmente
    return np.array(samples)


class GuitarString:
    def __init__(self, pitch, fs, A, T, noise_type, S=1):
        """Initialize Guitar String"""
        self.pitch = pitch                      # Frecuencia de la nota
        self.fs = fs                            # Frecuencia de Sampleo
        self.S = S                              # Stretch Factor
        self.A = A                              # Amplitud
        self.T = T                              # Duración de la nota (samples)
        self.noise_type = noise_type            # Tipo de Ruido Inicial
        self.init_wavetable()
        self.init_samples()
        self.L = None
        
    def init_wavetable(self):
        """Generate new Wavetable for String"""
        self.L = int(np.floor(self.fs / int(self.pitch)-1/2/self.S))
        if self.noise_type == "normal":
            self.wavetable = (self.A * np.random.normal(0, 1, self.L)).astype(np.float)
        if self.noise_type == "uniform":
            self.wavetable = (self.A * np.random.uniform(-1, 1, self.L)).astype(np.float)
        if self.noise_type == "2-level":
            self.wavetable = (self.A * 2 * np.random.randint(0, 2, self.L) - 1).astype(np.float)

    def init_samples(self):
        """Create sound samples for string"""
        self.samples = karplus_strong(self.wavetable, 2*self.T, self.S)
        
    def get_samples(self):
        """Return Sound Samples"""
        return self.samples