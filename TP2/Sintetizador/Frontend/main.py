from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QFrame, QMessageBox

from Frontend.MainWindow import Ui_MainWindow
from Frontend.MplWidget import MplWidget

import numpy as np
import pyaudio

from effects.flanger import flange2, chorus

from nptowav.numpy_to_wav import write_timeline_to_wav

from Player.Working_Classes import Player

import sys


#####  This code makes exceptions appear when sometimes pyqt wraps them in some random error  #####
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = my_exception_hook

####################################################################################################


class MainWindow(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        #Este es el reporductor, aca tengo todos los tracks, el archivo midi y lo necesario para sintetizar
        self.player = Player(11025)
        self.note_player = Player(11025)


        ###   Callbacks   ###

        self.ui.Reproducir_track1.clicked.connect(lambda: self.play_track(1))
        self.ui.Reproducir_track2.clicked.connect(lambda: self.play_track(2))
        self.ui.Reproducir_track3.clicked.connect(lambda: self.play_track(3))
        self.ui.Reproducir_track4.clicked.connect(lambda: self.play_track(4))
        self.ui.Reproducir_track5.clicked.connect(lambda: self.play_track(5))
        self.ui.Reproducir_track6.clicked.connect(lambda: self.play_track(6))
        self.ui.Reproducir_track7.clicked.connect(lambda: self.play_track(7))
        self.ui.Reproducir_track8.clicked.connect(lambda: self.play_track(8))
        self.ui.Reproducir_track9.clicked.connect(lambda: self.play_track(9))
        self.ui.Reproducir_track10.clicked.connect(lambda: self.play_track(10))
        self.ui.Reproducir_track11.clicked.connect(lambda: self.play_track(11))
        self.ui.Reproducir_track12.clicked.connect(lambda: self.play_track(12))
        self.ui.Reproducir_track13.clicked.connect(lambda: self.play_track(13))
        self.ui.Reproducir_track14.clicked.connect(lambda: self.play_track(14))
        self.ui.Reproducir_track15.clicked.connect(lambda: self.play_track(15))
        self.ui.Reproducir_track16.clicked.connect(lambda: self.play_track(16))

        self.ui.Eliminar_track1.clicked.connect(lambda: self.remove_track(1))
        self.ui.Eliminar_track2.clicked.connect(lambda: self.remove_track(2))
        self.ui.Eliminar_track3.clicked.connect(lambda: self.remove_track(3))
        self.ui.Eliminar_track4.clicked.connect(lambda: self.remove_track(4))
        self.ui.Eliminar_track5.clicked.connect(lambda: self.remove_track(5))
        self.ui.Eliminar_track6.clicked.connect(lambda: self.remove_track(6))
        self.ui.Eliminar_track7.clicked.connect(lambda: self.remove_track(7))
        self.ui.Eliminar_track8.clicked.connect(lambda: self.remove_track(8))
        self.ui.Eliminar_track9.clicked.connect(lambda: self.remove_track(9))
        self.ui.Eliminar_track10.clicked.connect(lambda: self.remove_track(10))
        self.ui.Eliminar_track11.clicked.connect(lambda: self.remove_track(11))
        self.ui.Eliminar_track12.clicked.connect(lambda: self.remove_track(12))
        self.ui.Eliminar_track13.clicked.connect(lambda: self.remove_track(13))
        self.ui.Eliminar_track14.clicked.connect(lambda: self.remove_track(14))
        self.ui.Eliminar_track15.clicked.connect(lambda: self.remove_track(15))
        self.ui.Eliminar_track16.clicked.connect(lambda: self.remove_track(16))

        self.ui.efecto_reproducir.clicked.connect(self.play_effects)

        self.ui.Reproducir_todo.clicked.connect(self.play_song)

        self.ui.reproduce_single_note.clicked.connect(self.play_single_note)
        self.ui.synth_selector_single_note.currentIndexChanged.connect(self.change_single_note_synth)

        self.ui.cargar_archivo.clicked.connect(self.load_mid)
        self.ui.synthesis_selector.currentIndexChanged.connect(self.change_synth)
        self.ui.add_track.clicked.connect(self.add_track)

        self.ui.guardar_archivo.clicked.connect(self.save_file)

        self.ui.espectrograma_track.clicked.connect(self.plot_spectrogram)
        ###   Callbacks   ###

    # Carga el archivo midi a player
    def load_mid(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Midi Files (*.mid)", options=options)
        if fileName:
            self.player.load_file(fileName)
            self.player.create_tracks()
            print(self.player.tracks)
            # en este punto tengo EN PLAYER todos los tracks del midi que abri con el boton, y cada track con su
            # respectiva nota, etc...

            self.ui.track_number.setText('Hay %s tracks en su archivo MIDI' % len(self.player.tracks))

            self.ui.track_selector.clear()
            for track in self.player.tracks:
                self.ui.track_selector.addItem('Track %s' % track.iden)

    def save_file(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(path)

        ids = []
        for track in self.player.tracks:
            if track.reproductor:
                ids.append(track.iden)

        output_song = self.player.make_song(ids)
        print(ids)

        name = self.ui.save_name.text()
        name += '.wav'

        final_path = path + '/' + name

        print(final_path)
        write_timeline_to_wav(final_path, output_song, self.player.sample_rate)

    def change_synth(self):
        current_text = self.ui.synthesis_selector.currentText()
        if current_text == 'Sintesis aditiva':
            self.ui.instrument_selector.clear()
            self.ui.instrument_selector.addItems(['flute', 'piano', 'violin', 'trumpet'])
        elif current_text == 'Sintesis fisica':
            self.ui.instrument_selector.clear()
            self.ui.instrument_selector.addItems(['guitar', 'drums'])
        elif current_text == 'Sintesis basada en muestras':
            pass

    def change_single_note_synth(self):
        current_text = self.ui.synth_selector_single_note.currentText()
        if current_text == 'Sintesis aditiva':
            self.ui.instrument_selector_single_note.clear()
            self.ui.instrument_selector_single_note.addItems(['flute', 'piano', 'violin', 'trumpet'])
        elif current_text == 'Sintesis física':
            self.ui.instrument_selector_single_note.clear()
            self.ui.instrument_selector_single_note.addItems(['guitar', 'drums'])
        elif current_text == 'Sintesis basada en muestras':
            pass

    def add_track(self):
        reproductor  = -1
        for ui in self.ui.scrollAreaWidgetContents.children():
            reproductor += 1
            if isinstance(ui, QFrame) and not ui.isEnabled():
                # Agrego track al primer reproductor desactivado que encuentro
                ui.setEnabled(True)

                lista = self.ui.track_selector.currentText().split()
                ind = int(lista[1])

                self.ui.track_selector.removeItem(self.ui.track_selector.currentIndex())

                current_instrument = self.ui.instrument_selector.currentText()
                current_form = self.ui.synthesis_selector.currentText()

                # todo agregar sintesis basada en muestras
                if current_form == 'Sintesis aditiva':
                    current_form = 'additive'
                elif current_form == 'Sintesis fisica':
                    current_form = 'physical'
                elif current_form == 'Sintesis basada en muestras':
                    current_form = 'samplesynth'

                self.player.tracks[ind - 1].set_reproductor(reproductor)

                self.player.synthesize_track(ind, current_form, current_instrument)
                print('sintetizo')
                self.plot_timelines(reproductor, ind)
                ui.repaint()
                break


    def remove_track(self, iden):

        for ui in self.ui.scrollAreaWidgetContents.children():
            if isinstance(ui, QFrame):
                if ui.objectName() == 'trackui' + str(iden):
                    ui.setEnabled(False)
                    ui.repaint()
                    eval('self.ui.tracktimeline' + str(iden) + '.clear_axes()')

        for track in self.player.tracks:
            if track.reproductor == iden:
                track.set_reproductor(None)
                track.set_instrument(None)
                track.sounds = None

                print('eliminado 1')
                self.ui.track_selector.addItem('Track ' + str(track.iden))
                self.ui.track_selector.repaint()


    # plays desired track
    def play_track(self, iden):
        self.player.play_track(iden)

    # plays all the tracks at the same time
    def play_song(self):
        iden_list = []
        for i in range(1, 17):
            if eval('self.ui.track' + str(i) + '_checkbox.isChecked()'):
                iden_list.append(i)

        self.player.play_multiple_tracks(iden_list)

    def play_single_note(self):
        notes = {'Do': 261, 'Re': 293, 'Mi': 329, 'Fa': 349, 'Sol': 392, 'La': 440, 'Si': 493}

        pitch = notes[self.ui.single_note_selector.currentText()]

        length = self.ui.duration_lineedit.text()

        try:

            if int(length) < 5:

                length = int(length)
                current_form = self.ui.synth_selector_single_note.currentText()
                if current_form == 'Sintesis aditiva':
                    current_form = 'additive'
                elif current_form == 'Sintesis física':
                    current_form = 'physical'
                elif current_form == 'Sintesis por muestras':
                    current_form = 'samplesynth'

                instrument = self.ui.instrument_selector_single_note.currentText()
                self.note_player.play_single_note(pitch, length, current_form, instrument)
            else:
                self.show_pop_up('Porque querrías escuchar la misma nota por tanto tiempo?')

        except (ValueError, TypeError):
            self.show_pop_up('Ingrese una duracion  válida para la nota')


    def play_effects(self):
        form = self.ui.select_effect.currentText()
        speed = float(self.ui.speed_lineedit.text())
        depth = float(self.ui.depth_lineedit.text())
        if self.ui.inversion.isChecked():
            inv = True
        else:
            inv = False

        ids = []
        for track in self.player.tracks:
            if track.reproductor:
                ids.append(track.iden)

        output_song = self.player.make_song(ids)

        if form == 'Flanger':
            out = flange2(output_song, speed, depth, inv, self.player.sample_rate)
        elif form == 'Chorus':
            out = chorus(output_song, speed, depth, inv, self.player.sample_rate)

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.player.sample_rate,
                        frames_per_buffer=1024,
                        output=True,
                        output_device_index=1
                        )

        stream.write(out.astype(np.float32).tostring())
        stream.close()



    # plots track timelines
    def plot_timelines(self, reproductor, index):

        eval('self.ui.tracktimeline' + str(reproductor) + '.plot_timebase(self.player.tracks[' + str(index - 1) + '].sounds, self.player.sample_rate)')
        pass

    # Pots spectrogram
    def plot_spectrogram(self):
        iden_list = []
        for i in range(1, 17):
            if eval('self.ui.track' + str(i) + '_checkbox.isChecked()'):
                iden_list.append(i)

        if not len(iden_list):
            self.show_pop_up('Debe Seleccionar al menos un track para realizar el espectrograma')

        output_song = self.player.make_song(iden_list)

        window = self.ui.ventana_espectrograma.currentText()
        n_per_seg = int(self.ui.window_size.text())
        overlaping = int(self.ui.overlaping.text())

        self.ui.espectrograma.plot_spectrogram(output_song, self.player.sample_rate, window, n_per_seg, overlaping)
        self.ui.espectrograma.repaint()

    def reset_tracks(self):
        for ui in self.ui.scrollAreaWidgetContents.children():
            ui.setEnabled(False)

        for track in self.player.tracks:
            track.set_reproductor = None
            track.set_instrument = None

    def show_pop_up(self, error):
        msg = QMessageBox()
        msg.setWindowTitle('Mistakes were made')
        msg.setText(error)
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec_()


# Controlador de ventanas, conecta señales que le dicen a las distintas ventanas cuando abrirse y cerrarse
class Controller:

    def __init__(self):
        pass

    def show_main(self):
        self.window = MainWindow()
        self.window.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()