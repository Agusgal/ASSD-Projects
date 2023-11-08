#Imports
import numpy as np
from scipy import signal
import matplotlib .pylab as plt

#Funcion que crea el h(n) para pasa altos
def HighPassGenerator(fa,fp,fs,N):
    h=[];
    fc=(fa+fp)/2;
    fad=fa/fs;
    fpd=fp/fs;
    n=np.linspace(0,N-1,int(N));
    for i in range(len(n)):
        if (n[i]- ((N-1)/2) ) != 0 :
            h.append( -1 / ( (n[i]-((N-1)/2))*np.pi) * np.sin( (n[i]-((N-1)/2))*2*np.pi*fc/fs) );
        else:
            h.append(1-(2*fc/fs));
    return h;

#Respuesta en frecuencia del filtro ideal
def IdealHighPass(f,fa,fp,Aa,Ap):
    Hi=[];
    fc=(fa+fp)/2;
    for i in range(len(f)):
        if ( f[i] <= fa):
            Hi.append(-Aa);
        elif (f[i] >= fp):
            Hi.append(-Ap);
        else:
            Hi.append(-Aa + ( (Aa-Ap)/(fp-fa) )*(f[i]-fa) )
    return Hi

def main():
    fa=1000;
    Aa=40;
    fp=2000;
    Ap=2;
    fs=44100;
    #Elegi un N impar y en N=131 cumple con lo pedido
    N=131;
    h=HighPassGenerator(fa,fp,fs,N);
    #Ventena de hamming
    Wind=np.hamming(N);
    #Calcule el filtro digital
    hf=h*Wind;
    #Respuesta en frecuencia del filtro
    w,H=signal.freqz(hf,1);
    f=(fs*w)/(2*np.pi);
    Hi=IdealHighPass(f,fa,fp,Aa,Ap);
    #Grafico
    plt.figure (1)
    plt.ylabel("Magnitud [dB]")
    plt.xlabel("Frecuencia [Hz]")
    plt.plot(f , 20*np.log10( np.abs(H)) )
    #plt.plot(f, Hi)
    #plt.legend(['Estimado','Ideal'],loc='upper center',shadow=True,ncol=2)
    plt.grid(True)
    plt.figure (2)
    plt.ylabel("Angulo [deg]")
    plt.xlabel("Frecuencia [Hz]")
    plt.plot(f, 180/np.pi*np.angle(H))
    plt.grid(True)
    plt.show ()

if __name__ == "__main__":
    main()