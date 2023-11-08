from PyQt5.QtWidgets import *

from PyQt5 import QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from webcolors import *

from scipy import signal as sign
import numpy as np


class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Esto detecta color background y se lo pone a la figura del grafico (asi es generico)
        color = self.palette().color(QtGui.QPalette.Background)
        color.red(), color.green(), color.blue()
        hex = rgb_to_hex((color.red(), color.green(), color.blue()))

        self.fig = Figure(facecolor=hex)
        self.fig.savefig("image_filename.png", edgecolor=self.fig.get_edgecolor())

        self.canvas = FigureCanvas(self.fig)



        layout = QVBoxLayout()
        #layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.axes.set_facecolor("#e1ddbf")
        self.setLayout(layout)
        self.canvas.axes.set_position([0.2, 0.2, 0.6, 0.6])
    def plot_timebase(self, signal, sample_rate):

        self.canvas.axes.clear()

        self.canvas.axes.set_xlabel('Time [s]')
        self.canvas.axes.set_ylabel('Amplitude')
        self.canvas.axes.plot(np.arange(0, len(signal) / sample_rate, 1/sample_rate), signal)
        self.canvas.draw()

    def plot_spectrogram(self, signal, sample_rate, window, n_per_seg, overlaping):


        print('dibuje')

        
        self.canvas.axes.clear()

        print('spetcrogramam')

        f, t, Sxx = sign.spectrogram(signal, fs=sample_rate, window=window, nperseg=int(n_per_seg),
                                     noverlap=int(n_per_seg * overlaping / 100))

        self.canvas.axes.pcolormesh(t, f, 10 * np.log10(Sxx))

        self.canvas.axes.set_xlabel('Time [sec]')
        self.canvas.axes.set_ylabel('Frequency [Hz]')
        self.canvas.axes.plot(np.arange(0, len(signal) / sample_rate, 1/sample_rate), signal)
        
        self.canvas.draw()




    def clear_axes(self):
        self.canvas.axes.clear()
        self.canvas.draw()