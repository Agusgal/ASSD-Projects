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

def main():
    fa=4800;
    Aa=40;
    fp=6000;
    Ap=2;
    fs=44100;
    #Calculo de nuevo Aa
    delta_a=10**(-(Aa/20));
    delta_b=(10**(Ap/20)-1)/(10**(Ap/20)+1);
    delta= min(delta_a,delta_b);
    Aa=-20*np.log10(delta);
    #Calculo el Alfa/Beta
    if (Aa <= 21):
        Alfa=0;
    elif (Aa > 21) and (Aa <= 50):
        Alfa=0.5842*(Aa-21)**(0.4)+0.07886*(Aa-21)
    elif (Aa > 50):
        Alfa=0.1102*(Aa-8.7)
    #Calculo N
    if (Aa <= 21):
        D=0.9222;
    elif (Aa > 21):
        D=(Aa-7.95)/14.36
    N=np.ceil( ( fs*D/(fp-fa) ) + 1 );
    if (N%2) == 0:  #Me aseguro numero impar
        N=N+1;

    h=HighPassGenerator(fa,fp,fs,N);

    #Ventena de Kaiser
    Wind=np.kaiser(N,Alfa);
    #Calcule el filtro digital
    hf=h*Wind;
    #Respuesta en frecuencia del filtro
    w,H=signal.freqz(hf,1);
    f=(fs*w)/(2*np.pi);
    #Grafico
    plt.figure (1)
    plt.ylabel("Magnitud [dB]")
    plt.xlabel("Frecuencia [Hz]")
    plt.plot(f , 20*np.log10( np.abs(H)) )
    plt.grid(True)
    plt.figure (2)
    plt.ylabel("Angulo [deg]")
    plt.xlabel("Frecuencia [Hz]")
    plt.plot(f, 180/np.pi*np.angle(H))
    plt.grid(True)
    plt.show ()

if __name__ == "__main__":
    main()