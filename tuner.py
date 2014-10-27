"""
tuner.py

Checks a signal against preset values (guitar strings) to determine
flat or sharp.
"""
# TODO: harmonic product spectrum,
#       hamming window, autocorrelation, class indeling
#       Threads voor input


# import sys
import alsaaudio
import numpy as np
# import matplotlib.pyplot as plt

""" TESTSIGNAL """
# t = np.linspace(0, N/float(fs), N)
# tsig = np.sin(150*2*np.pi*t) + np.sin(250*2*np.pi*t)
# y = tsig
# plt.plot(t,y)


freqs = {1: 329.63,
         2: 246.94,
         3: 196.00,
         4: 146.83,
         5: 110.00,
         6:  82.41,
         }
fs = 2000  # Sampling frequency
N = 512    # Chunk size
tol = 0.5  # Tolerance

recorder = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
                         alsaaudio.PCM_NORMAL,
                         'default')
recorder.setchannels(1)
recorder.setrate(fs)
recorder.setformat(alsaaudio.PCM_FORMAT_S16_BE)
recorder.setperiodsize(N)


def setup(**kwargs):
    pass


def tune(string, **kwargs):
    method = "fft"
    if "method" in kwargs:
        method = kwargs[method]
    if method == "fft":
        tune_fft(string)


def tune_fft(string):
    fc = freqs[string]

    while(True):
        y = get_data()
        Y_mag = [abs(x) for x in np.fft.rfft(y)]
        i_c = int((fc*N)/fs + 1)  # array index of desired frequency
        f_range = np.linspace(0, fs/2,
                              N/2+1)[i_c/2:min(i_c*2, N/2)]
        Y_window = Y_mag[i_c/2:min(i_c*2, N/2)]
        root_index = np.argmax(Y_window)
        # TODO: HPS TOEPASSEN
        if Y_window[root_index] > 4 * np.mean(Y_window):
            root = f_range[root_index]
            compare(root, fc)
        else:
            print("no input")


def tune_autocorr(string):
    pass


def get_data():
    _, y_raw = recorder.read()
    return [ord(x[0]) + ord(x[1]) for x in zip(y_raw[0::2], y_raw[1::2])]


def compare(inpitch, desired):
    if inpitch < desired - tol:
        print("flat: -{0}Hz".format(desired-inpitch))
    elif inpitch > desired + tol:
        print("sharp: +{0}Hz".format(inpitch-desired))
    else:
        print("Ok")


def main():
    setup()
    tune(4)

if __name__ == "__main__":
    main()

""" Plotting """
# plt.plot(f_range,
#         [abs(x) for x in Y[i_c/2:i_c*2]])
# plt.show()
