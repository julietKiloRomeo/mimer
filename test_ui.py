
import sys
from PyQt4 import QtCore, QtGui, uic

from mimer_lib import mimer
from scipy.io import wavfile
import numpy as np


class ImageDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, )

        # Set up the user interface from Designer.
        self.ui = uic.loadUi("test_interface.ui")
        self.mimer = mimer(1)

        self.T_win = 3
        self.noise = 0

        self.testfile    = ['sound/seinfeld_percentage.wav',
                        'sound/seinfeld_doubledip.wav',
                        'sound/south_park_ask_mr_hat.wav',
                        'sound/batman_ordinary.wav']

        self.ui.episode_select.addItems(self.testfile)
        f = QtGui.QFont('Courier New')
        self.ui.text_output.setFont(f)

        self.loadsound( 0)

        self.ui.show()
        # Make some local modifications.
   
        # Connect up the buttons.
        self.connect(self.ui.play_button, QtCore.SIGNAL("clicked()"),
                     self.process )
                     
        self.ui.episode_select.currentIndexChanged.connect(self.loadsound)
        self.ui.noise_slider.valueChanged.connect(self.adjust_noise)
                      
    def process(self):
        self.ui.text_output.setText('')
        dT = 0.2
        for T in range(8):
            idx         = (T+dT)*1.0*self.mimer.fs
            bite        = self.data[idx:idx + self.T_win*self.mimer.fs]
            bite        += np.random.normal(0,1,bite.shape)*self.noise
            out         = self.mimer.process(bite)
            sc          = [-elm[3] for elm in out]
            ordr        = np.argsort(sc)
            s = "%2.1fs:%20s  %10s     %4s\n" % (T+dT, 'Name', 'Match', 'Time')
            for idx in ordr:
                o = out[idx]
                s += "%25s  %10.0f     %4.1fs\n" % (o[0], o[3] , o[2])
            self.ui.text_output.append(s)
            
            
    def adjust_noise(self, N):
        self.noise = N
                              
    def loadsound(self, idx):
        fname = self.testfile[idx]                        
        fs, data        = wavfile.read(fname)
        self.mimer.fs   = fs
        self.data       = data

                      
                      
                      

app = QtGui.QApplication(sys.argv)
window = ImageDialog()
sys.exit(app.exec_())