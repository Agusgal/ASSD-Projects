from scipy import signal as sign
import numpy as np
import matplotlib.pyplot as plt


def Spectrograma(signal, Fs, windows, n_per_seg, overlaping):
  #Realizo un control de que se utilisen solo las ventanas permitidas si es string

  """
  if (isinstance(windows,str)):
    if windows != "boxcar":
      if windows != "triang":
        if windows != "blackman":
          if windows != "hamming":
            if windows != "hann":
              if windows != "bartlett":
                if windows != "flattop":
                  if windows != "parzen":
                    if windows != "bohman":
                      if windows != "blackmanharris":
                        if windows != "nuttall":
                          if windows != "barthann":
                            windows = "triang"
                            print("No eligio predeterminada")
  """
  f, t, Sxx = sign.spectrogram(signal, fs=Fs, window=windows, nperseg=int(n_per_seg), noverlap=int(n_per_seg * overlaping / 100))

  plt.pcolormesh(t, f, 10*np.log10(Sxx))
  plt.ylabel('Frequency [Hz]')
  plt.xlabel('Time [sec]')
  plt.show()

def main():
  fs = 10000
  t = np.linspace(0, 1, 1*fs)
  x = sign.chirp(t, f0=1000, f1=1, t1=1, method='linear')
  plt.plot(t, x)
  plt.show()
#   f, t, Sxx = sign.spectrogram(x,fs=fs,window="hann",noverlap=1000, nperseg=2000)
#   plt.ylim(0,2000)
#   plt.pcolormesh(t, f, Sxx)
#   plt.ylabel('Frequency [Hz]')
#   plt.xlabel('Time [sec]')
#   plt.show()
  Spectrograma(x, fs, "hann", 2*500, 50)
  # Con n_per_seg=500 busque una resolución de 500/fs segundos en el tiempo

if __name__ == "__main__":
     main()