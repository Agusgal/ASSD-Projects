import matplotlib.pyplot as plt
from scipy import signal as sign
import numpy as np
from numpy.fft import rfft, rfftfreq, ifft

#Sen signal generator
def EntradaSin(Vmax,t,f):
  x=[]
  for i in range(len(t)):
    x.append( Vmax*np.sin(2*np.pi*f*t[i]) )
  return x

#Donde X es la entrada,t los puntos en el tiempo y Yn la salida
def SigmaDelta(X,t):
    Xd=[];
    Xp=[];
    Yn=[];
    for i in range(len(X)):
        if(i == 0):
            #Sumatoria
            Xd.append(X[i]);
            #Integracion
            Xp.append(Xd[i]);
            #Cuantizador Y D/A
        else:
            #Sumatoria
            Xd.append(X[i]-Yn[i-1]);
            #Integracion
            Xp.append(Xd[i]+Xp[i-1]);
        #Cuantizador Y D/A
        if(Xp[i] < 0):
            Yn.append(-1);
        else:
            Yn.append(+1);
    return Yn

def main():
    #Variables
    f=500;
    L=64;
    fs=f*5*L;
    T=1/f;
    t=np.arange(0,1*T+1/fs,1/fs)
    X=EntradaSin(0.8,t,f)
    #Test
    Yn=SigmaDelta(X,t)
    Yd=sign.decimate(Yn,16,ftype="fir")
    td=np.arange(0,1*T+16/fs,16/fs)
    plt.plot(t,Yn)
    plt.plot(t,X)
    plt.step(td,Yd)
    plt.legend(['Cuantizador','Entrada','Decimador'],loc='upper center',shadow=True,ncol=3)
    plt.title('ADC Sigma delta simulación')
    plt.ylabel("Tensión [V]")
    plt.xlabel("Tiempo [Seg]")
    plt.xlim([0,1*T])
    plt.ylim([-1.05,1.3])
    plt.grid(True)
    plt.show()
    #Noise shaping
    freqYn = rfftfreq(len(t), d = t[-1]/len(t))
    fftYn = rfft(Yn)
    fftYn1 = 2*np.abs(fftYn/len(t))
    plt.plot(freqYn,10*np.log10(fftYn1/(10**(-3))))
    plt.title('Noise shaping')
    plt.ylabel("Potencia [dBm]")
    plt.xlabel("Frecuencia [Hz]")
    plt.xlim([0,80000])
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()