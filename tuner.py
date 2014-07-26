"""
tuner.py

Checks a signal against preset values (guitar strings) to determine
flat or sharp.
TODO: Detect if signal is noise (no peaks)
      String selection(detection)

"""
# import sys
import alsaaudio
import numpy as np
# import matplotlib.pyplot as plt

""" TESTSIGNAL """
# t = np.linspace(0, N/float(fs), N)
# tsig = np.sin(150*2*np.pi*t) + np.sin(250*2*np.pi*t)
# y = tsig
# plt.plot(t,y)


class Tuner:

    freqs = {1: 329.63,
             2: 246.94,
             3: 196.00,
             4: 146.83,
             5: 110.00,
             6:  82.41,
             }
    fs = 2000
    N = 512
    tol = 1

    recorder = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
                             alsaaudio.PCM_NORMAL,
                             'default')
    recorder.setchannels(1)
    recorder.setrate(fs)
    recorder.setformat(alsaaudio.PCM_FORMAT_S16_BE)
    recorder.setperiodsize(N)

    def __init__(self, tolerance=0.5):
        self.tol = tolerance
        pass

    def tune(self, string=4):
        fc = self.freqs[string]

        while(True):
            _, datat = self.recorder.read()
            y = [ord(x[0]) + ord(x[1])
                 for x in zip(datat[0::2], datat[1::2])]
            Y = [abs(x) for x in np.fft.rfft(y)]
            i_c = int((fc*self.N)/self.fs + 1)
            f_range = np.linspace(0, self.fs/2,
                                  self.N/2+1)[i_c/2:min(i_c*2, self.N/2)]
            Y_window = [abs(x) for x in Y[i_c/2:min(i_c*2, self.N/2)]]
            root_index = np.argmax(Y_window)
            if Y_window[root_index] > 4 * np.mean(Y_window):
                root = f_range[root_index]
            else:
                print("no input")
                continue

            if root < fc - self.tol:
                print("flat: -{0}Hz".format(fc-root))
            elif root > fc + self.tol:
                print("sharp: +{0}Hz".format(root-fc))
            else:
                print("Ok")


def main():
    tuner = Tuner()
    tuner.tune(4)

if __name__ == "__main__":
    main()

""" Plotting """
# plt.plot(f_range,
#         [abs(x) for x in Y[i_c/2:i_c*2]])
# plt.show()
