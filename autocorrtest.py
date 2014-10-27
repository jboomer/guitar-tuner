import numpy as np
import random
# from numpy.fft import rfft, irfft
import matplotlib.pyplot as plt
import time

N = 500
fs = 10000.0

freqs = {1: 329.63,
         2: 246.94,
         3: 196.00,
         4: 146.83,
         5: 110.00,
         6:  82.41,
         }


def downsample(arr, length, N):
    """Downsample array @arr of length @length @N times """
    out = np.zeros(length)
    out[:(length/N + ((length % N) > 0) * 1)] = arr[::N]
    return out


def filter1(signal):
    pass

# TESTSIGNAL
fund = freqs[6]
t = np.linspace(0, (N-1)/fs, N)
y = sum([np.sin(fund*2*np.pi*t),                     # Fundamental tone
         np.sin(2*fund*2*np.pi*t),                   # Harmonic 1
         1.3 * np.sin(4*fund*2*np.pi*t),             # Harmonic 2
         np.sin(8*fund*2*np.pi*t),                   # Harmonic 3
        [(random.random()-0.5) * 0.5 for ts in t]])  # White noise

# TODO: Hier een highpass/band filter overheen
tic = time.time()
r = np.correlate(y, y, mode='full')
r0 = r[r.size/2:]
# freqs = rfft(y)
# r0 = irfft(freqs * np.conj(freqs))

# NOTE: HPS HSS maakt resultaat slechter (hogere frequenties meer power)

r1 = downsample(r0, N, 2)
toc = time.time()
r2 = downsample(r0, N, 3)
r3 = downsample(r0, N, 4)
r4 = downsample(r0, N, 5)
r_total = r0 + r1 + r2 + r3 + r4
root = fs/(5 + np.argmax(r0[5:]))  # Take the second peak
print("Elapsed time: {0} seconds".format(toc-tic))

print("Fundamental freq: {:+f}Hz".format(root))
plt.subplot(511)
y_plt = plt.plot(t, y)
plt.title("signal")
plt.subplot(512)
r0_plt = plt.plot(t, r0)
plt.subplot(513)
r1_plt = plt.plot(t, r0 + r1)
plt.subplot(514)
r2_plt = plt.plot(t, r0 + r1 + r2)
plt.subplot(515)
r_plt = plt.plot(t, r_total)
plt.title("autocorrelation")
plt.show()
